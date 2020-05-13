import argparse
import os
import preprocess_term
import check_term
import jsonFile
import iateCode
import globales
import eurovocCode
import lexicalaCode
import wikidataCode
import globales
import re
from unicodedata import normalize
import json

lang_in=''
name_file=''
find_iate=globales.find_iate
find_lexi=globales.find_lexi
find_wiki=globales.find_wiki
find_euro=globales.find_euro
targets=globales.targets
print(targets)


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

args=parser.parse_args()

term=args.sourceTerm
listTerm=args.sourceFile
lang=args.lang
targetsargs=args.targets.split(' ')
context=args.context
contextFile=args.contextFile
wsid=args.wsid
scheme=args.schema
DR=args.DR
creator=args.creator
date=args.date
description=args.description
keywords=args.keywords

raiz=os.getcwd()
folder=os.listdir(raiz)
for i in targetsargs:
    targets.append(i)
jsonFile.createRelationFolders(targets,folder,name_file)

lang_in=lang

print(targets)
if(term):
    print('solo termino')
    name_file=''
    listread=[]
    #term=preProcessingTerm(term, context, contextFile)
    term=preprocess_term.preProcessingTerm(term, context, contextFile,lang)
    context=term[2]
    #print(context)
    check=check_term.checkTerm(lang,term[1], '', targets)
    ide=check[0]
    ide_file=ide
    termSearch=check[1]
    print('TERM A BUSCAR: ', termSearch)
    if(termSearch!='1'):
        rels=1
        outFile=jsonFile.jsonFile(ide, scheme, rels, '',context, termSearch, lang_in)
        #print(out)
        print('------IATE')
        outFile=iateCode.iate(termSearch, lang,targets, outFile, context, wsid,1)
        #print(outFile)
        print('------EUROVOC')
        outFile=eurovocCode.eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, 1)
        #print(outFile)
        print('------LEXICALA')
        outFile=lexicalaCode.lexicala(lang, termSearch, targets, context,  outFile, wsid, 1)
        print('------WIKI DATA')
        outFile=wikidataCode.wikidata_retriever(termSearch, lang, context,  targets, outFile, 1, wsid)
        
        note=''
        outFile=jsonFile.fix(outFile, find_iate, find_euro, find_lexi, find_wiki, note, context, termSearch)
        n=termSearch.replace(' ', '_').replace('\ufeff','')
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I)
        n = normalize( 'NFC', n)
        newFile=lang+'/'+n+'_'+ide+'.jsonld'
        with open(newFile, 'w') as file:
            json.dump(outFile, file, indent=4,ensure_ascii=False)
        
else:
    print('---------LISTA')
    name_file=''
    file_schema=editFileSchema(scheme)
    listread=[]
    file=open(listTerm+'.csv', 'r', encoding='utf-8')
    read=csv.reader(file)
    cont=0
    for i in read: 
        if(i):
            #print(i)
            term=preProcessingTerm(i[0], None, contextFile)
            #print(term)
            context=term[2]
            check=checkTerm(lang,term[0], '', targets)
            ide=check[0]
            ide_file=ide
            termSearch=check[1]
            print('TERM A BUSCAR:----------- ', termSearch)
            if(termSearch!='1'):
                rels=1
                del prefLabel_full[0:len(prefLabel_full)]
                del altLabel_full[0:len(altLabel_full)]
                del targets_pref[0:len(targets_pref)]
                del definition_full[0:len(definition_full)]
                del broader_full[0:len(broader_full)]
                del narrower_full[0:len(narrower_full)]
                del related_full[0:len(related_full)]
                del find_iate[0:len(find_iate)]
                del find_euro[0:len(find_euro)]
                del find_lexi[0:len(find_lexi)]
                del find_wiki[0:len(find_wiki)]
                
                note=''
                outFile=jsonFile(ide, scheme, rels, note, context, termSearch, lang_in)
                print('------IATE')
                outFile=iate(termSearch, lang,targets, outFile, context, wsid, 1)
                #print(find_iate, find_euro, find_wiki)
                print('------EUROVOC')
                outFile=eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, 1)
                #print(find_iate, find_euro, find_wiki)
                print('------LEXICALA')
                outFile=lexicala(lang, termSearch, targets, context,  outFile, wsid, 1)
                #print(find_iate, find_euro, find_wiki)
                print('------WIKI DATA')
                outFile=wikidata_retriever(termSearch, lang, context,  targets, outFile, 1, wsid)
                
                outFile=fix(outFile, find_iate, find_euro, find_lexi, find_wiki, note, context, termSearch)
                n=termSearch.replace(' ', '_').replace('\ufeff','')
                n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", n), 0, re.I
                )
                n = normalize( 'NFC', n)
                #newFile=lang+'/'+n+'_'+ide+'.jsonld'
                newFile=name_file+lang+'/'+n+'_'+ide+'.jsonld'
                #newFile='terminosjson/'+n+'_'+ide+'.jsonld'
                with open(newFile, 'w') as file:
                    json.dump(outFile, file, indent=4,ensure_ascii=False)
        
    name='schemas/'+listTerm+'_'+scheme+'.json'

    with open(name, 'w') as new:
        json.dump(file_schema, new, indent=4,ensure_ascii=False)
 

