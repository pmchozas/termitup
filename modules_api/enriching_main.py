import argparse
import os
#from modules_api import check_term
from modules_api import jsonFile
from modules_api import iateCode
from modules_api import eurovocCode
from modules_api import unesco
#import lexicalaCode
from modules_api import wikidataCode
import re
from unicodedata import normalize
import json
import csv
#import trans_id
from modules_api import unesco
import logging
from modules_api import conts_log
from modules_api import frecuency
import time


def enriching_terms(termlist, inlang, outlang, corpus, schema, iate, eurovoc, wikidata, unesco):
    wsid='yes'
    outFile=jsonFile.jsonFile(ide, schema, rels, note, context, termSearch, lang_in, file_schema, n, freq)

    if(iate):
        outFile=iateCode.iate(termlist, inlang, outlang, corpus, schema, wsid)

    if(eurovoc):
        outFile=eurovocCode.eurovoc(termlist, inlang, outlang, corpus, schema, wsid)

#Pregunta para Karen: por qué se llama prefLabel_unesco y no unesco como en el resto de códigos? hace algo diferente?
#creo que habría que unificar todo
    
    if(unesco):
        outFile=unesco.prefLabel_unesco(termlist, inlang, outlang, corpus, schema, wsid)
    if(wikidata):
        outFile=wikidataCode.wikidata_retriever(termlist, inlang, outlang, corpus, schema, wsid)



    outFile=jsonFile.outFile_full(outFile)
    outFile=jsonFile.fix(outFile, note, context, termSearch)

    outFile=jsonFile.topConcept(outFile,  file_schema)
    idenuew=ide.split('/')
    n=idenuew[-1].replace(' ', '_').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", n), 0, re.I)
    n = normalize( 'NFC', n)
    newFile='../data/output/'+n+'.jsonld'
        #with open(newFile, 'w') as file:
        #    json.dump(outFile, file, indent=4,ensure_ascii=False)
               
    name='../data/output/'+schema.replace(' ', '_')+'.json'
    with open(name, 'w') as new:
        json.dump(file_schema, new, indent=4,ensure_ascii=False)

'''       
    if(termSearch!='1'):
        print('TERM A BUSCAR:----------- ', termSearch)
        conts_log.information('\n','----- Source Term: '+ termSearch+' -----')
        rels=1
        note=''
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", termSearch), 0, re.I
        )
        n = normalize( 'NFC', n)
        f1=open('../data/estatutoterms_mx.txt', 'r')
        freqlist=f1.readlines()
        f2=open('../data/clean_terms_freq4.txt', 'r')
        cleanlist=f2.readlines()
        freq=frecuency.frequencyTerm(freqlist, termSearch)
'''
        
        #print('------EUROVOC')
        
        #print('------UNESCO')
        #outFile=unesco.prefLabel_unesco(termSearch, lang, targets, outFile, scheme, file_schema, 1)

        #print('------IATE')
        #outFile=iateCode.iate(termSearch, lang,targets, outFile, context, wsid, 1)
        
        #if(coling==None):
         #   print('------LEXICALA')
         #   outFile=lexicalaCode.lexicala(lang, termSearch, targets, context,  outFile, wsid, 1)
        
        #print('------WIKI DATA')
        #outFile=wikidataCode.wikidata_retriever(termSearch, lang, context,  targets, outFile, 1, wsid)

        




#---------------------------------MAIN---------------------------------------------------------------
'''
parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search")
parser.add_argument("--lang", help="Source language")
parser.add_argument("--targets", help="Source language out")
parser.add_argument("--context", help="Contexto")
parser.add_argument("--contextFile", help="Archivo de contextos")
parser.add_argument("--wsid", help="")
parser.add_argument("--schema", help="")
parser.add_argument("--DR", help="")
parser.add_argument("--creator", help="")
parser.add_argument("--date", help="")
parser.add_argument("--description", help="")
parser.add_argument("--keywords", help="")
parser.add_argument("--corpus", help="")
parser.add_argument("--coling", help="")

args=parser.parse_args()

term=args.sourceTerm
listTerm=args.sourceFile
lang=args.lang
#targets=args.targets.split(' ')
#context=args.context
#contextFile=args.contextFile
#wsid=args.wsid
#scheme=args.schema
#DR=args.DR
#creator=args.creator
#date=args.date
#description=args.description
#keywords=args.keywords
corpus=args.corpus
coling=args.coling
raiz=os.getcwd()
folder=os.listdir(raiz)
lang_in=lang
print(lang_in)
#os.remove('myapp.log')
logg=open('myapp.log', 'w')
logging.basicConfig(filename='myapp.log',
format='%(asctime)s, %(levelname)s %(message)s',
datefmt='%H:%M:%S',
level=logging.DEBUG)

    
corpus=corpus.lower()
terminology_extraction=statistical_patri.main(corpus, lang_in) #module 1
clean=postprocess.main(terminology_extraction, lang_in) #modulo 2


#file_schema=jsonFile.editFileSchema() # step 3 [Write json file] 


#for i in clean: # step 4 [if clean is not empty, next step]
    #if(i): 
        #interm=i
        #module1(iterm, corpus, clean, lang_in)
        #all_process(interm, context, contextFile, lang, targets, scheme, lang_in, file_schema, clean, coling)
#conts_log.main()





conts_log.contFinal()

'''