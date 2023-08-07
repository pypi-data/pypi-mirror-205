# 2023.4.29 cp from wps7000.py  as a MQ consumer later 
import json, time, traceback, fire,sys, redis, hashlib ,socket,platform,os,requests,re, difflib, spacy # 3.4.1 needed
redis.r	= redis.Redis(host=os.getenv('rhost', "172.17.0.1" if 'linux' in sys.platform else 'hw160.jukuu.com' ), port=int( os.getenv('rport', 6626 ) ), decode_responses=True) # local cache only , no gec included
dskhost	= os.getenv('dskhost', "gpu120.wrask.com:7095") #gpu120.wrask.com:7095
gechost = os.getenv('gechost', 'gpu120.wrask.com:7626') # HTTP api, on top of redis6626, xadd-blpop 
getdoc	= lambda snt, ttl=37200:  ( res := redis.r.get(snt), doc:= spacy.nlp(snt) if res is None else spacy.tokens.Doc(spacy.nlp.vocab).from_json(json.loads(res) ),  redis.r.setex(f"snt:{snt}", ttl, json.dumps(doc.to_json()) ) if res is None else None ) [1]
getdocs	= lambda snts, ttl=37200: [ ( doc:=spacy.nlp(snt), redis.r.setex(f"snt:{snt}", ttl, json.dumps(doc.to_json()) ), doc )[-1] if res is None else  spacy.tokens.Doc(spacy.nlp.vocab).from_json(json.loads(res) ) for snt, res in zip(snts, redis.r.mget([f"snt:{snt}" for snt in snts]) ) ]
trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
mkf_input		= lambda i, snt, gec, toklist, gec_toklist, doc, diffmerge,pid=0: 	{"pid":pid, "sid":i, "snt":snt, "tok": toklist,  #"offset":-1,"len":-1,"re_sntbr":0,  normally, offset =0
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  #"tag":[t.tag_ for t in doc],
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": gec, "diff": trans_diff_merge( toklist , gec_toklist) if diffmerge else trans_diff( toklist , gec_toklist)	}

if not hasattr(spacy, 'nlp'):
	from spacy.lang import en
	spacy.sntbr		= (inst := en.English(), inst.add_pipe("sentencizer"))[0]
	spacy.sntpid	= lambda essay: (pid:=0, [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid))[-1] for snt in  spacy.sntbr(essay).sents] )[-1]
	spacy.nlp		= spacy.load('en_core_web_sm')

def get_dsk(arr:dict={"essay":"English is a internationaly language which becomes importantly for modern world. In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"}
		, asdsk:bool=True, gec_local:bool=False, topk_gec:int=64, diffmerge:bool=False,  timeout:int=9, ttl:int=79200):  
	''' # 依赖 dskhost 和 gechost	'''
	try:
		essay	= arr.get("essay", arr.get('doc','')).strip()
		if not essay: return {"failed":"empty essay"}
		sntpids = spacy.sntpid(essay)  # [(snt,pid) ]
		snts	= [snt.strip() for snt,pid in sntpids ] 	
		[redis.r.xadd('xsnt-spacy', {'snt':snt}, maxlen=30000) for snt in snts if snt]  # notify:  spacy/gec , added maxlen 2022.10.15

		sntdic	= requests.post(f"http://{gechost}/xgec-snts?name=xsnts&timeout={timeout}&ttl={ttl}", json=snts).json() if not gec_local else {}
		docs	= getdocs(snts, ttl) 
		input	= [ mkf_input(i,snts[i],sntdic[snts[i]], [t.text for t in doc], [t.text for t in (doc if snts[i] == sntdic[snts[i]] else getdoc(sntdic[snts[i]]) ) ], doc, diffmerge)  for i, doc in enumerate(docs)]
		dsk		= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
		return dsk
	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

if __name__ == '__main__':
	print( get_dsk())  