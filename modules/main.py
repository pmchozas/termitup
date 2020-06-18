import argparse
import os
import preprocess_term
import check_term
import jsonFile
import iateCode
import eurovocCode
import wikidataCode
import re
from unicodedata import normalize
import json
import csv
import trans_id
import relval
import statistical_patri
import postprocess
import unesco
import logging
import conts_log
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
'''logging.basicConfig(filename='myapp.log',
    filemode='w+',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)'''


def all_process(interm, context, contextFile, lang, targets, scheme, lang_in, file_schema, clean, coling):

    term=preprocess_term.preProcessingTerm(interm, context, contextFile, lang)
    #print(term)
    context=term[2]
    check=check_term.checkTerm(lang,term[0], '', targets, '')
    ide=check[0]
    ide_file=ide
    termSearch=check[1]
    print('TERM A BUSCAR:----------- ', termSearch)
    if(termSearch!='1'):
        rels=1
        note=''
        
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", termSearch), 0, re.I
        )
        n = normalize( 'NFC', n)
        outFile=jsonFile.jsonFile(ide, scheme, rels, note, context, termSearch, lang_in, file_schema, n)
        #
        print('------EUROVOC')
        outFile=eurovocCode.eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, 1, file_schema)
        
        print('------UNESCO')
        outFile=unesco.prefLabel_unesco(termSearch, lang, targets, outFile, scheme, file_schema, 1)

        print('------IATE')
        outFile=iateCode.iate(termSearch, lang,targets, outFile, context, wsid, 1)
        
        print('------WIKI DATA')
        outFile=wikidataCode.wikidata_retriever(termSearch, lang, context,  targets, outFile, 1, wsid)

        

        outFile=jsonFile.outFile_full(outFile)
        outFile=jsonFile.fix(outFile, note, context, termSearch)

        outFile=relval.main(outFile, file_schema, targets, clean, lang_in, context)
        idenuew=ide.split('/')
        n=idenuew[-1].replace(' ', '_').replace('\ufeff','')
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", n), 0, re.I
        )
        n = normalize( 'NFC', n)
        newFile='data/output/'+n+'.jsonld'
        with open(newFile, 'w') as file:
            json.dump(outFile, file, indent=4,ensure_ascii=False)
             
    name='data/output/'+scheme.replace(' ', '_')+'.json'
    with open(name, 'w') as new:
        json.dump(file_schema, new, indent=4,ensure_ascii=False)


#---------------------------------MAIN---------------------------------------------------------------

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
targets=args.targets.split(' ')
context=args.context
contextFile=args.contextFile
wsid=args.wsid
scheme=args.schema
DR=args.DR
creator=args.creator
date=args.date
description=args.description
keywords=args.keywords
corpus=args.corpus
coling=args.coling
raiz=os.getcwd()
folder=os.listdir(raiz)
#jsonFile.createRelationFolders(targets, folder)
lang_in=lang


if(corpus):
    print('---------CORPUS')
    
    out=statistical_patri.main(corpus)
    clean=postprocess.main(out)
    file_schema=jsonFile.editFileSchema(scheme)
    #print(clean)
    for i in clean: 
        if(i):
            interm=i
            all_process(interm, context, contextFile, lang, targets, scheme, lang_in, file_schema, clean, coling)
    conts_log.main()

if(term):
    print('---------SOLO TERMINO')
    name_file=''
    file_schema=jsonFile.editFileSchema(scheme)
    all_process(term, context, contextFile, lang, targets, scheme, lang_in, file_schema, [], coling)
    conts_log.main()
    
        
if(listTerm):
    print('---------LISTA')
    name_file=''
    file_schema=jsonFile.editFileSchema(scheme)

    listread=[]
    txt=0
    if(listTerm[-4:]=='.txt'):
        file=open(listTerm, 'r', encoding='utf-8')
        read=file.readlines()
        txt=1
    else:
        file=open(listTerm+'.csv', 'r', encoding='utf-8')
        read=csv.reader(file)
    cont=0
    for i in read: 
        if(i):
            if(txt==1):
                interm=i[:-1]
            else:
                interm=i[0]
            all_process(interm, context, contextFile, lang, targets, scheme, lang_in, file_schema, [], coling)
    conts_log.main()



