import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from unicodedata import normalize
import os
from os import remove
import collections
from os import listdir
from os.path import isfile, isdir
import time
from progress.bar import Bar, ChargingBar
import os, time, random

# header for Wikidata queries
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def leerContextos(lang, termIn):
    configuration= {
        "es": "contexts/Spain-judgements-ES.ttl",
        "es": "contexts/Spain-legislation-ES.ttl",
        "es": "contexts/Spain-collectiveagreements-ES.ttl",
        "en": "contexts/UK-judgements-EN.ttl",
        "en": "contexts/DNVGL-EN.ttl",
        "en": "contexts/Ireland-judgements-EN.ttl",
        "en": "contexts/Ireland-legislation-EN.ttl",
        "en": "contexts/UK-collectiveagreements-EN.ttl",
        "en": "contexts/UK-legislation-EN.ttl",
        "nl": "contexts/DNVGL-NL.ttl",
        "de": "contexts/contracts_de.ttl"
        "de": "contexts/Austria-collectiveagreements-DE.ttl"
        "de": "contexts/Austria-legislation-DE.ttl"
    }
    
    es = '%s'%configuration["es"]
    en = '%s'%configuration["en"]
    nl = '%s'%configuration["nl"]
    de = '%s'%configuration["de"]
    encoding = 'utf-8'
    print(es)
    if(lang=='es'):
        archivo = open(es, "r")
    elif(lang=='en'):
        archivo = open(en, "r")
    elif(lang=='de'):
        archivo = open(de, "r")
    elif(lang=='nl'):
        archivo = open(nl, "r")

    contenido = archivo.readlines()
    
    lista=[]
    lista1=[]
    matriz=[]
    contextlist=[]
    find=[]
    cont=0
    for i in contenido:
        encuentra=i.find('skos:Concept')
        if(encuentra!=-1):
            cont=cont+1
        
    for i in contenido:     
        encuentra1=i.find('skos:prefLabel')
        if(encuentra1!=-1):
            text = i.split('"')
            pref=text[1]    
            lista1.append(pref)
    cont1=0     
    for i in contenido:     
        encuentra=i.find('skos:Concept')
        encuentra2=i.find('lynxlang:hasExample')
        if(encuentra!=-1):
            matriz.insert(cont,[])
            cont1=cont1+1

        if(encuentra2!=-1):
            text1 = i.split('"',1)
            pref1=text1[1]
            lista.append(str(pref1)+'|'+str(cont1-1))   

    for i in range(cont):
        matriz[i].insert(0, lista1[i])
        slp=lista[i].split('|')
        matriz[i].insert(1, slp[0])

    limpiar=re.compile("<'\'.*?>")
    for i in matriz:
        r=''.join(i[0])
        r2=''.join(i[1])
        row1 = re.sub(r'<[^>]*?>','', r)
        row1 = row1.replace('@es;','')
        row2 = re.sub(r'<[^>]*?>','', r2)
        row2 = row2.replace('@es;','').replace('\\','').replace('"','')
        if(row1 in row2):
            contextlist.append([row1,row2[:-1]])
        
    for i in contextlist:
        if(termIn in i[0] and len(find)==0):
            start=i[1].index(termIn)
            tam=len(termIn)
            end=i[1].index(termIn)+tam
            find.append([termIn,i[1], start, end])
    return(find)


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

termino=args.sourceTerm
listTerm=args.sourceFile
idioma=args.lang
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

raiz=os.getcwd()
carpeta=os.listdir(raiz)
for tar in targets:
    if(tar in carpeta):
        pass
    else:
        os.mkdir(tar)

    carpetas=os.listdir(tar)
    relationes=['broader', 'narrower', 'related']
    for i in relationes:
        if(i not in carpetas):
            os.makedirs(tar+"/"+i)


if(termino):
    lista=[]
    listaread=[]
    lista.append(termino)
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        contextF=csv.reader(file)
        contextFile=[]
        for i in contextF:
            contextFile.append([i[0], i[1],i[2],i[3]])
    else:
        contextFile=leerContextos(idioma, termino)
    
    '''verify=verificar(idioma,termino, '', targets)
    ide=verify[0]
    termSearch=verify[1]
    print('TERMINO A BUSCAR: ', termSearch)
    if(termSearch!='1'):
        jsonlist=haceJson(termSearch, idioma,targets)
        all(jsonlist, idioma, targets,context, contextFile,  wsid,scheme, DR)
    else:
        listaread.append(termino)
        n=termino.replace(' ', '_').replace('\ufeff','')
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
        n = normalize( 'NFC', n)

        with open(idioma+'/'+n+'_'+ide+'.jsonld', 'r') as file:
            data = json.load(file)

    creator='UPM'
    date="March 9 20"
    description="Linked Terminology containing terminological data about Labour Law in Europe."
    keywords=["Labour law", "Work", "Company"]
    '''
else:
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        contextF=csv.reader(file)
        contextFile=[]
        for i in contextF:
            contextFile.append([i[0], i[1], i[2],i[3]])
    else:
        contextFile=leerContextos(idioma)
    
    lista=[]
    listaread=[]
    file=open(listTerm+'.csv', 'r', encoding='utf-8')
    read=csv.reader(file)
    cont=0

    for i in read:
        termino=preProcessTerm(i[0])
        verify=verificar(idioma,termino, '', targets)
        ide=verify[0]
        termSearch=verify[1]
        cont=cont+1
        print('TERMINO A BUSCAR: ',i[0],'|',termino,'|', termSearch, '|',cont)
        if(termSearch!='1'):
            jsonlist=haceJson(termSearch, idioma,targets)
            all(jsonlist, idioma, targets,context, contextFile,  wsid,scheme, DR)
        else:
            listaread.append(termino)
    