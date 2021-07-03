from modules_api.TBXTools import *
from os import path
import io
import re

def termex(corpus, lang_in):
    
    with io.open("./corpus.txt",'w',encoding='utf8') as f:      
        f.write(corpus)
    
    # print ("File exists:"+str(path.exists('./data/stop-esp.txt')))
    # print ("File exists:" + str(path.exists('./data/exclusion-regexps.txt'))) 
    # print ("File exists:" + str(path.exists(corpus)))
    # print ("directory exists:" + str(path.exists('myDirectory')))
    # print('terminology extraction')
    # print(corpus)
    # print(lang_in)
    sw_spanish="./data/stop-esp.txt"
    sw_english="./data/stop-eng.txt"
	
    inner_spanish="./data/inner-stop-esp.txt"
    inner_english="./data/inner-stop-eng.txt"
    if(lang_in=="es"):
        lang=lang_in+"p"
    elif(lang_in=="en"):
        lang=lang_in+"g"
    #print(lang)
    extractor=TBXTools()
    extractor.create_project("modules_api/statistical8.sqlite",lang,overwrite=True)
    extractor.load_sl_corpus("./corpus.txt")
    extractor.ngram_calculation(nmin=1,nmax=3,minfreq=3)
    if(lang=="esp"):
        extractor.load_sl_stopwords(sw_spanish)
        extractor.load_sl_inner_stopwords(inner_spanish)
    elif(lang=="eng"):
        extractor.load_sl_stopwords(sw_english)
        extractor.load_sl_inner_stopwords(inner_english)


    extractor.statistical_term_extraction(minfreq=4)
	# aquí junta los términos que son iguales pero están en mayus y en minus
    extractor.case_normalization(verbose=True)
	# esto no sé muy bien lo que hace pero saca menos términos que si no se pone, lo cual es mejor, creo que quita basurilla
    extractor.nest_normalization(verbose=True)
    extractor.regexp_exclusion(verbose=True)
    extractor.load_sl_exclusion_regexps("./data/exclusion-regexps.txt")
    extractor.regexp_exclusion(verbose=True)
	#para extraer unigramas, descomenta esto
	#extractor.select_unigrams("unigrams.txt",position=-1)
    out=extractor.save_term_candidates("./data/estatutoterms2.txt")
    newout=[]
    chars=['\'', '\"', '!', '<', '>', ',', '.', ':']
    for i in out:
        t=i.replace("\t", ",")
        s=re.sub("\d+", "", t)
        # print(s)
        for c in chars:
            if c in s:
                term=s.replace(c, '')
                term=term.strip(",;:. ")
                # print(term)
                newout.append(term)
                newout=list(dict.fromkeys(newout))
    return(newout)

    

   
