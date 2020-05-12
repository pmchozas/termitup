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
import nltk 
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

# header for Wikidata queries
url = 'https://query.wikidata.org/sparql'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
prefLabel_full=[]
altLabel_full=[]
definition_full=[]
targets_pref=[]
broader_full=[]
narrower_full=[]
related_full=[]
pref_relation=[]
alt_relation=[]
targets_relation=[]
lang_in=''
find_iate=[]
find_euro=[]
find_lexi=[]
find_wiki=[]
dict_domains=[]
closeMatch=[]
scheme=''
ide_file=''
file_schema={}
new_no_find=open('no_find.csv', 'w')
no_find = csv.writer(new_no_find)
name_file=''

# clean term
def preProcessingTerm(term, context, contextFile):
    porter = PorterStemmer()
    lancaster=LancasterStemmer()
    termcheck=term.strip('‐').strip('—').strip('–').strip(' ').rstrip('\n').rstrip(' ').replace(' – ', ' ').replace('/', ' ').replace('\t', '').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace('\ufeff','')
        
    if(' ' not in termcheck and 's' in termcheck[-1:]):
        termcheck=porter.stem(termcheck)

    termcheck2=termcheck.replace(' ', '_')
    
    if(context):
        context=context
        context=reduction_wsid(context)
    elif(contextFile):
        file=open(contextFile, 'r', encoding='utf-8')
        contextFile=file.readlines()
        listt=[]
        for j in contextFile:
            if(term.lower() in j.lower() ):
                context=j.lower()
                context=reduction_wsid(context)
                pass
            elif(termcheck.lower() in j.lower()):
                context=j.lower()
                context=reduction_wsid(context)
                pass

    else:
        contextFile=leerContextos(lang, term)
        for j in contextFile:
            #print(termSearch.lower(),' | ', j[0].lower())
            if(termcheck.lower() == j[0].lower()):
                context=j[1].lower()
                context=reduction_wsid(context)

    #print(context)
    #print(term, '|',termcheck,'|',termcheck2)
    return(termcheck, termcheck2,  context)

def reduction_wsid(text_in):
    out=''
    spl=text_in.split(' ')
    if(len(spl)>250):
        out=''.join(spl[:250])
    else:
        out=text_in
    return(out)

# id creation
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID

# relation folders
def createRelationFolders(targets):
    for tar in targets:
        if(tar in folder):
            pass
        else:
            os.mkdir(tar)

        folders=os.listdir(tar)
        relations=['broader', 'narrower', 'related']
        for i in relations:
            if(i not in folders):
                os.makedirs(name_file+tar+"/"+i)
# files
def path(targets, relation):
    listt_arq=[]
    #targets=['terminosjson']
    for i in targets:
        if(relation!=''):
            path=name_file+i+'/'+relation+'/'
        else:
            path=name_file+i+'/'
        listt = [obj for obj in listdir(path) if isfile(path + obj)]
        listt_arq.append(listt)
    return(listt_arq)

# check
def checkTerm(lang,  termSearch, relation, targets):
    listt_arq=path(targets, relation)
    ide=sctmid_creator()
    termSearch=termSearch.replace('\ufeff', '')
    termSearch=termSearch.replace('_', ' ')
    termSearch=termSearch.lower()
    n=termSearch
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
    n = normalize( 'NFC', n)
    for carps in listt_arq:
        for j in carps:
            if('.DS_Store' not in j):
                slp=j.split('_')
                
                if(len(slp)>2):
                    termfile=slp[:len(slp)-1]
                    termfile=' '.join(termfile)
                    slp2=slp[len(slp)-1].split('.')
                    idefile=slp2[0]
                else:

                    termfile=slp[0]
                    if(len(slp)>1):
                        slp2=slp[1].split('.')
                    idefile=slp2[0]

                

                if(n == termfile):
                    termSearch='1'
                    ide=idefile
                else:
                    termSearch=termSearch
                    if(ide in idefile):
                        ide=sctmid_creator()
                        checkTerm(lang, termSearch, relation, targets)
                    else:
                        ide=ide
    return(ide, termSearch)


def leerContextos(lang, termIn):
    configuration= {
        "es": "contexts/Spain-judgements-ES.ttl",
        "en": "contexts/UK-judgements-EN.ttl",
        "nl": "contexts/DNVGL-NL.ttl",
        "de": "contexts/contracts_de.ttl",
    }

    configuration2= {
        "es": "contexts/Spain-legislation-ES.ttl",
        "en": "contexts/Ireland-legislation-EN.ttl",
        "nl": "contexts/DNVGL-NL.d ttl",
        "de": "contexts/Austria-collectiveagreements-DE.ttl",
    }

    configuration3= {
        "es": "contexts/Spain-collectiveagreements-ES.ttl",
        "en": "contexts/DNVGL-EN.ttl",
        "nl": "contexts/DNVGL-NL.ttl",
        "de": "contexts/Austria-legislation-DE.ttl"
    }
    
    es = '%s'%configuration["es"]
    en = '%s'%configuration["en"]
    nl = '%s'%configuration["nl"]
    de = '%s'%configuration["de"]
    encoding = 'utf-8'
    if(lang=='es'):
        file = open(es, "r")
    elif(lang=='en'):
        file = open(en, "r")
    elif(lang=='de'):
        file = open(de, "r")
    elif(lang=='nl'):
        file = open(nl, "r")

    content = file.readlines()
    
    listt=[]
    listt1=[]
    matrix=[]
    contextlist=[]
    find=[]
    cont=0
    for i in content:
        findword=i.find('skos:Concept')
        if(findword!=-1):
            cont=cont+1
        
    for i in content:     
        findword1=i.find('skos:prefLabel')
        if(findword1!=-1):
            text = i.split('"')
            pref=text[1]    
            listt1.append(pref)
    cont1=0     
    for i in content:     
        findword=i.find('skos:Concept')
        findword2=i.find('lynxlang:hasExample')
        if(findword!=-1):
            matrix.insert(cont,[])
            cont1=cont1+1

        if(findword2!=-1):
            text1 = i.split('"',1)
            pref1=text1[1]
            listt.append(str(pref1)+'|'+str(cont1-1))   

    for i in range(cont):
        matrix[i].insert(0, listt1[i])
        slp=listt[i].split('|')
        matrix[i].insert(1, slp[0])

    limpiar=re.compile("<'\'.*?>")
    for i in matrix:
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

def editFileSchema(scheme):
    file_schema={
    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
    "@id": "labourlaw",
    "conceptScheme": "http://lynx-project.eu/kos/labourlaw/",
    "hasTopConcept": [

    ],
    "label": "labour law",
    "creator": "UPM",
    "date": "March 10",
    "description": "Terminological data about Labour Law in Europe."
    }
    
    
    return(file_schema)

  
def file_html(schema, pref, ide, lang):
    try:
        with open('schemas/file_html.json') as f:
            file = json.load(f)
        
        
        file[schema][0][lang].append({'prefLabel':pref, 'ide':ide, 'lang':lang})
        f.close()

        with open('schemas/file_html.json', 'w') as new:
            json.dump(file, new, indent=4,ensure_ascii=False)
    except json.decoder.JSONDecodeError:
       error=''
        #print('JSONDecodeError')
    


# bearen token
def bearenToken(): 
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)

# iate
def iate(term, lang,targets,outFile, context,   wsid, rels):
    answer=[]
    try:
        auth_token=bearenToken()
        hed = {'Authorization': 'Bearer ' +auth_token}
        jsonList=[]
        data = {"query": term,
        "source": lang,
        "targets": targets,
        "search_in_fields": [
            0
        ],
        "search_in_term_types": [
            0,
            1,
            2,
            3,
            4
        ],
            "query_operator": 1
        }
        url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
        response = requests.get(url, json=data, headers=hed)
        response2=response.json()
        js=json.dumps(response2)
        print(js)
        results=[]
        termSearch=[]
        cont=0
        termSearch.append(response2['request']['query'])
        bloq=0
        if('items' in response2.keys()):
            
            term=response2['items']
            ide=sctmid_creator()
            definicion_wsid=[]
            ides_wsid=[]
            ides_item=[]
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                results.insert(item, [])
                dom=term[item]
                ide_iate=term[item]['id']
                leng=term[item]['language']
                if(lang in leng):
                    if(termSearch[cont] == leng[lang]['term_entries'][0]['term_value']  ):
                        print('-se encontro iate-')
                        bloq=1 # bandera de encontrado se enciende en 1
                        if(context==None):
                            context=getContextIate(item, leng, lang,termSearch[cont] )
                            if(context!=''):
                                wsid='yes'
                            else:
                                context=termSearch[cont]
                                wsid='yes'
                        for target in targets:
                            get=getInformationIate(target,item, leng, termSearch[cont])
                            
                            results[item].insert(0, item)#item
                            results[item].insert(1, get[0])#def
                            results[item].insert(2, get[1])#pref
                            results[item].insert(3, get[2])#alt
                            results[item].insert(4, target)#target
                            
                            if(target==lang ):
                                if(get[0]==''):
                                    dom_iat=domain_iate(dom, data, hed)
                                    if(len(get[2])):
                                        for i in get[2]:
                                            definicion_wsid.append(i)
                                            ides_item.append(item)
                                            ides_wsid.append(ide_iate)
                                    else:
                                        if(len(dom_iat)):
                                            #for i in dom_iat:
                                            definicion_wsid.append(dom_iat[0])
                                            ides_item.append(item)
                                            ides_wsid.append(ide_iate)
                                    '''else:
                                        if(len(get[2])):
                                            for i in get[2]:
                                                definicion_wsid.append(i)
                                                ides_item.append(item)
                                                ides_wsid.append(ide_iate)'''
                                else:
                                    definicion_wsid.append(get[0])
                                    ides_item.append(item)
                                    ides_wsid.append(ide_iate)
            #print(definicion_wsid)
            if(bloq==1):
                d=(definicion_wsid,ides_item)
                
                if(wsid=='yes'):
                    maximo=wsidFunction(termSearch[cont],  context,   d)
                    #print(maximo)
                    if(maximo[2]!=200):
                        print('WSID NO 200')
                        closeMatch.append("https://iate.europa.eu/entry/result/"+str(ide_iate))
                    
                    elif(maximo[0]!='' and maximo[2]==200):
                        print('WSID 200')
                        wsidmax=maximo[1]
                        it=ides_item.index(wsidmax)
                        maxx=ides_wsid[it]
                        find_iate.append(maxx)
                        
                        outFile=fillPrefIate(outFile, results, 'prefLabel', 2, wsidmax, rels, maxx)
                        outFile=fillAltIate(outFile, results,  'altLabel', 3, wsidmax, rels, maxx)
                        outFile=fillDefinitionIate(outFile, results,  'definition', 1, wsidmax, maxx)
                else:
                    print('WSID NO')
                    closeMatch.append("https://iate.europa.eu/entry/result/"+str(ide_iate))
                    
        cont=cont+1
    except json.decoder.JSONDecodeError:
        #print('JSONDecodeError')
        response2='{ }'
    
        
    #print(outFile)
    return(outFile)

def domain_iate(item, data, hed):
    code_domain=item['domains']
    list_code=[]
    for i in range(len(code_domain)):
        code=code_domain[i]['code']
        list_code.append(code)
    
    domain=[]
    url= 'https://iate.europa.eu/em-api/domains/_tree'
    response = requests.get(url,  headers=hed)
    response2=response.json()
    its=response2['items']

    for i in range(len(its)):
        code=its[i]['code']
        name=its[i]['name']
        dict_domains.append([name,code])
        subdomain_iate(its[i], dict_domains)

    #print(dict_domains)
    #print(list_code)
    for i in list_code:
        for j in range(len(dict_domains)):
            code=dict_domains[j]
            if(i == code[1]):
                domain.append(code[0])
    return(domain)  


def subdomain_iate(its, dict_domains):
    if('subdomains' in its):
        sub=its['subdomains']
        if(len(sub)):
            for j in range(len(sub)):
                code=sub[j]['code']
                name=sub[j]['name']
                dict_domains.append([name,code])
                subdomain_iate(sub[j], dict_domains)
    return(dict_domains)

def getContextIate(item, leng, lang, termSearch):
    context=''
    if(lang in leng):
        language=leng[lang]
        for l in language:
            if('term_entries' in language.keys()):
                term_entries=language['term_entries']
                if(len(term_entries)>0):
                    for t in range(len(term_entries)):
                        term_val=language['term_entries'][t]
                        if('contexts' in term_val ):
                            contexts=term_val['contexts']
                            if(len(contexts)>0):
                                for c in range(len(contexts)):
                                    contextsc=contexts[c]
                                    if('context' in contextsc):
                                        if(termSearch in contextsc['context'] ):
                                            context=contextsc['context']
    #print(context)
    return(context)


def getInformationIate(target, item, leng,termSearch):
    defi=''
    pref=''
    term_val=''
    syn=[]
    joinSyn=''
    if(target in leng):
        language=leng[target]
        for l in language:
            if('term_entries' in language.keys()):
                term_entries=language['term_entries']
                if(len(term_entries)>0):
                    pref=language['term_entries'][0]['term_value']
                    for t in range(len(term_entries)):
                        term_val=language['term_entries'][t]['term_value']
                        
                        if(termSearch is not term_val):
                            syn.append(term_val)
                    syn=syn[0:len(term_entries)]
                    joinSyn='| '.join(syn)
            if('definition' in language.keys()):
                defi=language['definition']

    
    defi=re.sub(r'<[^>]*?>', '', defi)
    defi=defi.replace(',', '').replace('"', '').replace("'", '').replace(':', '').replace('.','').replace('(','').replace(')','').replace('IATE','')
    defi=re.sub(r'[0-9]', '', defi)
    return(defi,pref, syn)


def fillPrefIate(outFile, results, label, col, wsidmax, rels, maxx):
    
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            if(rels==1):
                while(colm<=len(results[i]) and results[i][colTarget].strip(' ') not in targets_pref):
                    if(results[i][colm]!=""):
                        outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                        prefLabel_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                        targets_pref.append(results[i][colTarget].strip(' '))
                        file_html(scheme, results[i][colm].strip(' '), ide_file, results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
            else:
                while(colm<=len(results[i]) and results[i][colTarget].strip(' ') not in targets_relation):
                    if(results[i][colm]!=""):
                        outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                        pref_relation.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                        targets_relation.append(results[i][colTarget].strip(' '))
                        file_html(scheme, results[i][colm].strip(' '), ide_file, results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5

    else:
        colm=col
        colTarget=4
        if(rels==1):
            while(colm<=len(results[wsidmax]) and results[wsidmax][colTarget].strip(' ') not in targets_pref ):
                if(results[wsidmax][colm]!=""):
                    outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                    prefLabel_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget].strip(' '))
                    targets_pref.append(results[wsidmax][colTarget].strip(' '))
                    file_html(scheme, results[wsidmax][colm].strip(' '), ide_file, results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
        else:
            while(colm<=len(results[wsidmax]) and results[wsidmax][colTarget].strip(' ') not in targets_relation ):
                if(results[wsidmax][colm]!=""):
                    outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                    pref_relation.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget].strip(' '))
                    targets_relation.append(results[wsidmax][colTarget].strip(' '))
                    file_html(scheme, results[wsidmax][colm].strip(' '), ide_file, results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5

    return outFile

def fillAltIate(outFile, results,  label, col, wsidmax, rels, maxx):
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            if(rels==1):
                while(colm<len(results[i])): 
                    for j in results[i][colm]:
                        alb=j.strip(' ')+'-'+results[i][colTarget]
                        if(j!="" and alb not in prefLabel_full and alb not in altLabel_full and results[i][colTarget] not in targets_pref):
                            outFile['prefLabel'].append({'@language':results[i][colTarget], '@value':j.strip(' ')})
                            prefLabel_full.append(j.strip(' ')+'-'+results[i][colTarget])
                            targets_pref.append(results[i][colTarget])
                        elif(j!="" and alb not in prefLabel_full and alb not in altLabel_full):
                            outFile[label].append({'@language':results[i][colTarget], '@value':j.strip(' ')})
                            altLabel_full.append(j.strip(' ')+'-'+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
            else:
                while(colm<len(results[i])):
                    for j in results[i][colm]: 
                        alb=j.strip(' ')+'-'+results[i][colTarget]
                        if(j!="" and alb not in pref_relation and alb not in alt_relation):
                            outFile[label].append({'@language':results[i][colTarget], '@value':j.strip(' ')})
                            alt_relation.append(j.strip(' ')+'-'+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        if(rels==1):
            while(colm<len(results[wsidmax])):
                for j in results[wsidmax][colm]:
                    alb=j.strip(' ')+'-'+results[wsidmax][colTarget]
                    if(j!="" and alb not in prefLabel_full and alb not in altLabel_full):
                        outFile[label].append({'@language':results[wsidmax][colTarget], '@value':j.strip(' ')})
                        altLabel_full.append(j.strip(' ')+'-'+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
        else:
            while(colm<len(results[wsidmax])):
                for j in results[wsidmax][colm]:
                    alb=j.strip(' ')+'-'+results[wsidmax][colTarget]
                    if(j!="" and alb not in pref_relation and alb not in alt_relation):
                        outFile[label].append({'@language':results[wsidmax][colTarget], '@value':j.strip(' ')})
                        alt_relation.append(j.strip(' ')+'-'+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
    return outFile

def fillDefinitionIate(outFile, results,   label,col, wsidmax, maxx):
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            while(colm<len(results[i]) ):
                if(results[i][colm]!=""):
                    outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                    definition_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                    #langs.append(results[i][colTarget].strip(' '))
                colm=colm+5
                colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        while(colm<len(results[wsidmax]) ):
            if(results[wsidmax][colm]!=""):
                outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                definition_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget])
                #langs.append(results[wsidmax][colTarget].strip(' '))
            colm=colm+5
            colTarget=colTarget+5

    return outFile


def eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, rels):
    #print(outFile)
    
    defs=[]
    name=[]
    urilist=[]
    defsnull=[]
    find=0
    if(context==None):
        context=termSearch
        wsid='yes'
    if(wsid=='yes'):
        uri=uri_term_eurovoc(termSearch, lang)
        if(len(uri)):
            print('-se encontro eurovoc-')
            find=1
            for i in uri:
                urilist.append(i[0])
                name.append(i[1])
                if(i[2]==''):
                    alt_ev=name_term_eurovoc(i[0],lang, 'altLabel')
                    if(alt_ev!=''):
                        defsnull.append(alt_ev)
                    else:
                        defsnull.append(i[1])
                else:
                    defsnull.append(i[2].replace(',', ''))
                
                
            d=(defsnull, urilist)
            
            maximo=wsidFunction(termSearch, context,  d)
            #print(maximo)
            if(maximo[2]!=200):
                print('WSID NO 200')
                for i in uri:
                    closeMatch.append(i[0])
                    

                
            elif(maximo[0]!='' and maximo[2]==200):
                print('WSID 200')
                maxx=defsnull.index(maximo[0])
                namewsid=name[maxx]
                uriwsid=maximo[1]
                find_euro.append(uriwsid)
                tars=check_prefLabel(outFile, targets, rels)
                if(len(tars)>0):
                    for lang in targets:
                        pref_ev=name_term_eurovoc(uriwsid,lang,'prefLabel')
                        if(pref_ev!=''):
                            outFile=property_add(pref_ev, lang, outFile, 'prefLabel', rels, uriwsid)
                            prefLabel_full.append(pref_ev+'-'+lang)
                            targets_pref.append(lang)
                
                        alt_ev=name_term_eurovoc(uriwsid,lang, 'altLabel')
                        def_ev=def_term_eurovoc( uriwsid,'"'+lang+'"')
                        if(alt_ev!=''):
                            outFile=property_add(alt_ev, lang, outFile, 'altLabel', rels, uriwsid)
                        if(def_ev!=''):
                            outFile=property_add(def_ev, lang, outFile, 'definition', rels, uriwsid)

                if(rels==1): #rels define si hara busqueda de relaciones o no 
                    outFile=relations_eurovoc(uriwsid, lang, namewsid,outFile, scheme)
    

    else:
        print('WSID NO')

        
    return(outFile)

def uri_term_eurovoc(termSearch, lang): #recoge la uri del termino a buscar
    term='"'+termSearch+'$"'
    lang='"'+lang+'"'
    answer=[]
    answeruri=''
    val=''
    try:
        url = ("http://sparql.lynx-project.eu/")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        ?c a skos:Concept .
        ?c ?p ?label. 
          FILTER regex(?label, """+term+""", "i" )
          FILTER (lang(?label) = """+lang+""")
          FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
      

        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            answeruri=''
        else:
            for result in results["results"]["bindings"]:
                answeruri=result["c"]["value"]
                answerl=result["label"]["value"]
                #print(termSearch, answerl)
                if(termSearch.lower() == answerl.lower()):#ATENCION
                    
                    defs=def_term_eurovoc(answeruri, lang)
                    answer.append([answeruri, answerl, defs])
                else:
                    tok=answerl.split(' ')
                    for i in tok:
                        if('(' in i):
                            tok.remove(i)
                            tokt=term.split(' ')
                            if(len(tok)==len(tokt)):
                                defs=def_term_eurovoc(answeruri, lang)
                                answer.append([answeruri, answerl, defs])
                        elif(termSearch == i):
                            defs=def_term_eurovoc(answeruri, lang)
                            #print(answeruri, answerl, '|',defs)
                            answer.append([answeruri, answerl, defs])
                
    except json.decoder.JSONDecodeError:
        answer=[]
    #print('answer', answer, len(answer))   
    #if(len(answer)<1):
    #    answer=uri_term_eurovoc2(termSearch, lang)


    return(answer)


def uri_term_eurovoc2(termSearch, lang): #recoge la uri del termino a buscar
    term='"'+termSearch+' (UE)"'
    #print(term)
    lang='"'+lang+'"'
    answer=[]
    answeruri=''
    val=''
    try:
        url = ("http://sparql.lynx-project.eu/")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        ?c a skos:Concept .
        ?c ?p ?label. 
          FILTER regex(?label, """+term+""" )
          FILTER (lang(?label) = """+lang+""")
          FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
      

        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            answeruri=''
        else:
            for result in results["results"]["bindings"]:
                answeruri=result["c"]["value"]
                answerl=result["label"]["value"]
                #print(termSearch, answerl)
                if(termSearch.lower() == answerl.lower()):#ATENCION
                    
                    defs=def_term_eurovoc(answeruri, lang)
                    answer.append([answeruri, answerl, defs])
                else:
                    tok=answerl.split(' ')
                    for i in tok:
                        if('(' in i):
                            tok.remove(i)
                            tokt=term.split(' ')
                            if(len(tok)==len(tokt)):
                                defs=def_term_eurovoc(answeruri, lang)
                                answer.append([answeruri, answerl, defs])
                        elif(termSearch == i):
                            defs=def_term_eurovoc(answeruri, lang)
                            #print(answeruri, answerl, '|',defs)
                            answer.append([answeruri, answerl, defs])
                
    except json.decoder.JSONDecodeError:
        answer=[]
    #print('answer2', answer, len(answer))  
  
        
    return(answer)

def def_term_eurovoc( uri,lang): #recoge la definicion de la uri de entrada
    definicion=''
    resultado=[]
    url=("http://sparql.lynx-project.eu/")
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+uri+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:definition  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
    r=requests.get(url, params={'format': 'json', 'query': query})
    results=json.loads(r.text)
    if (len(results["results"]["bindings"])==0):
        definicion=''
    else:
        for result in results["results"]["bindings"]:
            definicion=result["label"]["value"]
    return(definicion)

def getRelation(uri_termino, relation, lang): #recoge la uri de la relacion a buscar 
    answer=[]
    answerRel=''
    for i in uri_termino:
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c {<"""+i+"""> }
        VALUES ?relation { skos:"""+relation+""" } # skos:broader
        ?c a skos:Concept .
        ?c ?relation ?label .    
        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                answerRel=''
        else:
            for result in results["results"]["bindings"]:
                answerRel=result["label"]["value"]
                name=name_term_eurovoc(answerRel,lang,'prefLabel')
                answer.append([answerRel, name, relation])
    
    return(answer)

def name_term_eurovoc(uri,lang,label): #recoge el nombre equivalente a la uri de entrada
    try:
        nameUri=''
        lang='"'+lang+'"'
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+uri+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:"""+label+"""  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                nameUri=''
        else:
            for result in results["results"]["bindings"]:
                nameUri=result["label"]["value"]
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
        
      
    return(nameUri)



def relations_eurovoc(uri, lang, term, outFile, scheme):
    results=[]
    relations=['broader', 'narrower', 'related']
    for relation in relations:
        uriRelation=getRelation([uri], relation, lang)
        if(len(uriRelation)>0):
            if('topConceptOf' in outFile.keys()):
                del outFile['topConceptOf']
            for i in uriRelation:
                verify=checkTerm(lang, i[1], relation, targets)
                ide=verify[0]
                termSearch=verify[1]
                if(termSearch!='1'):
                    outFile[relation].append(ide)
                    originalIde=outFile['@id']
                    dataEurovoc=eurovoc_file(termSearch, ide, relation, i[0], lang, scheme,  originalIde)

    #print(outFile)
    return(outFile)



def eurovoc_file(termSearch, ide, relation, iduri, lang, scheme,  originalIde):
    termSearch=termSearch.replace('/', ' ')
    print('-----', termSearch,'------')
    data={}
    data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "exactMatch":iduri, '@type':'skos:Concept','prefLabel':'','altLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
    #"exactMatch":iduri
    data['prefLabel']=[]
    data['altLabel']=[]
    data['definition']=[]
    del pref_relation[0:len(pref_relation)]
    del alt_relation[0:len(alt_relation)]
    del targets_relation[0:len(targets_relation)]

    #print(data) 

    data=iate(termSearch, lang,targets, data, None, 'yes',0)
    data=eurovoc(termSearch, lang, targets, None,  'yes', data, scheme, 0)
    data=lexicala(lang, termSearch, targets, None,  data, 'yes', 0)
    data=wikidata_retriever(termSearch, lang, None,  targets, data, 0, 'yes')
    del data['definition']
    if(len(data['prefLabel'])==0):
        data['prefLabel'].append({'@language':lang, '@value':termSearch})
        pref_relation.append(termSearch+'-'+lang)
        targets_relation.append(lang)
    
    if(len(data['altLabel'])==0):
        del data['altLabel']
    if('broader' in relation and termSearch!=''):
        data['narrower']=[]
        data['narrower'].append(originalIde)

    elif('narrower' in relation and termSearch!=''):
        data['broader']=[]
        data['broader'].append(originalIde)

    elif('related' in relation and termSearch!=''):
        data['related']=[]
        data['related'].append(originalIde)

    #file_schema['hasTopConcept'].append(ide)
    
    n=termSearch.replace(' ', '_').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I
                )
    n = normalize( 'NFC', n)
    newFile=name_file+lang_in+'/'+relation+'/'+n+'_'+ide+'.jsonld'
    #newFile='terminosjson/'+relation+'/'+n+'_'+ide+'.jsonld'
    with open(newFile, 'w') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
              
    return(data)


def lexicala(lang, term, targets, context,  outFile, wsid, rels):
    try:
        answer=lexicala_term(lang, term)
        if('n_results' in answer):
            results=answer['n_results']
            if(results>0):
                print('-se encontro lexicala-')
                definitions=definition_lexicala(answer, lang)
                if(context==None):
                    context=term
                    wsid='yes'

                if(wsid=='yes'):
                    maximo=wsidFunction(term,context,  definitions)
                    #print(maximo)
                    if(maximo[2]!=200):
                        print('WSID NO 200')
                        closeMatch.append('https://dictapi.lexicala.com/senses/'+definitions[1][0])
                        
                    elif(maximo[0]!='' and maximo[2]==200):
                        print('WSID 200')
                        find_lexi.append(maximo[1])
                        tars=check_prefLabel(outFile, targets, rels)
                        if(len(tars)>0):
                            pref_lex=altLabel_lexicala(maximo[1], targets)
                            if(len(pref_lex)>0):
                                for i in pref_lex:
                                    outFile=property_add(i[0], i[1], outFile, 'prefLabel', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                            
                        alt_lex=altLabel_lexicala(maximo[1], targets)
                        def_lex=maximo[0]
                        if(len(alt_lex)>0):
                            for i in alt_lex:
                                outFile=property_add(i[0], i[1], outFile, 'altLabel', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                        if(def_lex!=''):
                            outFile=property_add(def_lex, lang, outFile, 'definition', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                else:
                    print('WSID NO')
    except json.decoder.JSONDecodeError:
        error=''
        #print('JSONDecodeError')
    return(outFile)


def lexicala_term(lang, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+lang+"&text="+term+"", auth=('upm2', 'XvrPwS4y'))
    answerSearch=search.json()
    return(answerSearch)

def lexicala_sense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('upm2', 'XvrPwS4y'))
    answerSense=sense.json()
    return(answerSense)

def definition_lexicala(answer,lang):
    listaDefinition=[]
    listaId=[]
    sense0=answer['results'][0]
    if('senses' in sense0.keys()):
        sense1=sense0['senses']
        for i in range(len(sense1)):
            if('definition' in sense1[i].keys()):
                id_definitions=sense1[i]['id']
                definitions=sense1[i]['definition']
                listaDefinition.append(definitions.replace(',', ''))
                listaId.append(id_definitions)
            else:
                pref_lex=altLabel_lexicala(sense1[i]['id'], lang)
                if(len(pref_lex)):
                    for j in pref_lex:
                        listaDefinition.append(j[0])
                        listaId.append(sense1[i]['id'])

            

    return(listaDefinition, listaId)

def altLabel_lexicala(maximo, targets):
    traductions=[]
    jsonTrad=lexicala_sense(maximo)
    if('translations' in jsonTrad.keys()):
        translations=jsonTrad['translations']
        for j in targets:
            if(j in translations):
                langs=translations[j]
                if('text' in langs):
                    text=langs['text']
                    traductions.append([text,j])
                else:
                    for k in range(len(langs)):
                        text=langs[k]['text']
                        traductions.append([text,j])


    return(traductions)


def wikidata_retriever(term, lang, context,  targets, outFile, rels, wsid):
    if(context==None):
        wsid='no'
    retrieve_query = """
        SELECT * {
       ?item rdfs:label "TERM"@LANG.
       ?item schema:description ?desc.
      FILTER (lang(?desc) = "LANG")
      }
    """

    original_query = """
    SELECT DISTINCT ?article ?lang ?name ?desc WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
      OPTIONAL {
        wd:WDTMID schema:description ?desc.
        FILTER (lang(?name) = lang(?desc))
      }
    }ORDER BY ?lang
    """

    altLabel_query = """
    SELECT DISTINCT ?article ?altLabel ?lang WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
      OPTIONAL {
        wd:WDTMID skos:altLabel ?altLabel.
        FILTER (lang(?name) = lang(?altLabel))
      }
    }ORDER BY ?lang
    """

    narrower_concept_query = """
    SELECT DISTINCT ?naTerm WHERE {
        ?naTerm wdt:P279 wd:WDTMID .
      }
    """

    broader_concept_query = """
    SELECT DISTINCT ?brTerm WHERE {
        wd:WDTMID wdt:P279 ?brTerm .   
    }
    """

    term_query = """
    SELECT DISTINCT ?lang ?name WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
    }ORDER BY ?lang
    """

    Wikidata_dataset = dict()
    definition=[]
    iduri=[]
    altLabel=[]
    query = retrieve_query.replace("TERM", term).replace("LANG", lang)
    SRCTERM = "\"" + term + "\"" + "@" + lang
    #print(SRCTERM) We have to save this in the skos as well
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json()
    
    if len(data['results']['bindings']) != 0:
        print('-se encontro wiki-')
        bindings=data['results']['bindings']
        for i in range(len(bindings)):
            iduri.append(bindings[i]['item']['value'].split("/")[-1])
            definition.append(bindings[i]['desc']['value'].replace(',', ''))
        
        if(context==None):
            context=term
            wsid='yes'
        if(wsid=='yes'):
            d=(definition,iduri)
            maximo=wsidFunction(term,  context,   d)
            #print(maximo)
            relations_retrieved = dict()
            
            if( maximo[2]!=200):
                print('WSID NO 200', iduri)
                closeMatch.append('https://www.wikidata.org/wiki/'+iduri[0])
                #outFile=wsid_wiki_no(outFile, targets, iduri, original_query, altLabel_query, narrower_concept_query, broader_concept_query, term_query, rels)
            
            elif(maximo[0]!='' and maximo[2]==200):
                print('WSID 200')
                tars=check_prefLabel(outFile, targets, rels)
                if(len(tars)>0):
                    target="', '".join(tars)
                    target="'"+target+"'"

                    try:
                        query = original_query.replace("WDTMID", maximo[1]).replace("TARGETS", target)
                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                        data = r.json()
                        bindings=data['results']['bindings']
                        if(len(bindings)>0):
                            find_wiki.append(maximo[1])
                            for i in range(len(bindings)):
                                if('name' in bindings[i]):
                                    prefLabel_wiki=bindings[i]['name']['value']
                                    lang_pr_wiki=bindings[i]['name']['xml:lang']
                                    #print(prefLabel_wiki, lang_pr_wiki)
                                    outFile=property_add( prefLabel_wiki, lang_pr_wiki, outFile, 'prefLabel' , rels, "https://www.wikidata.org/wiki/"+maximo[1])
                                if('desc' in bindings[i]):
                                    definition_wiki=bindings[i]['desc']['value']
                                    lang_pr_wiki=bindings[i]['name']['xml:lang']
                                    outFile=property_add( definition_wiki, lang_pr_wiki, outFile, 'definition' , rels, "https://www.wikidata.org/wiki/"+maximo[1])
                    except json.decoder.JSONDecodeError:
                        error=''
                        #print('JSONDecodeError')
                target="', '".join(targets)
                target="'"+target+"'"
                query = altLabel_query.replace("WDTMID", maximo[1]).replace("TARGETS", target)
                r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                altLabel_response = r.json()
                bindings=altLabel_response['results']['bindings']
                
                for i in range(len(bindings)):
                    if('altLabel' in bindings[i]):
                        altLabel_wiki=bindings[i]['altLabel']['value']
                        lang_al_wiki=bindings[i]['altLabel']['xml:lang']
                        outFile=property_add( altLabel_wiki, lang_al_wiki, outFile, 'altLabel', rels, "https://www.wikidata.org/wiki/"+maximo[1])
                
                if(rels==5):
                    # Retrieve narrower and broader concepts
                    relation_type = ["narrower", "broader"]
                    
                    for relation in relation_type:
                        if relation == "narrower":
                            concept_query = narrower_concept_query
                            relation_id = "naTerm"
                        else:
                            concept_query = broader_concept_query
                            relation_id = "brTerm"

                        query = concept_query.replace("WDTMID", maximo[1])
                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                        concept_response = r.json()
                        
                        concepts_list = [item[relation_id]["value"].split("/")[-1] if len(item[relation_id]["value"]) else None for item in concept_response["results"]["bindings"]]
                       
                       
                        if len(concepts_list):
                            for concept in concepts_list:
                                try:
                                    query = term_query.replace("WDTMID", concept).replace("TARGETS", target)
                                    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                                    for item in r.json()["results"]["bindings"]:
                                        lang=item["name"]["xml:lang"]
                                        concept_terms = item["name"]["value"]
                                        verify=checkTerm(lang, concept_terms, relation, targets)
                                        ide=verify[0]
                                        termSearch=verify[1]
                                        if(termSearch!='1'):
                                            outFile[relation].append(ide)
                                            originalIde=outFile['@id']
                                            dataEurovoc=eurovoc_file(termSearch, ide, relation, 'https://www.wikidata.org/wiki/'+concept, lang, scheme,  originalIde)
                                except json.decoder.JSONDecodeError:
                                    error=''
                                    #print('JSONDecodeError')

        else:
            print('WSID NO')
            #outFile=wsid_wiki_no(outFile, targets, iduri, original_query, altLabel_query, narrower_concept_query, broader_concept_query, term_query, rels)

    return(outFile)

def wsid_wiki_no(outFile, targets, iduri, original_query, altLabel_query, narrower_concept_query, broader_concept_query, term_query, rels):
    tars=check_prefLabel(outFile, targets, rels)
    target="', '".join(tars)
    target="'"+target+"'"
    if(len(tars)>0):
        for idterm in iduri:
            query = original_query.replace("WDTMID", idterm).replace("TARGETS", target)
            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
            data = r.json()
            bindings=data['results']['bindings']
            if(len(bindings)>0):
                for i in range(len(bindings)):
                    if('name' in bindings[i]):
                        prefLabel_wiki=bindings[i]['name']['value']
                        lang_pr_wiki=bindings[i]['name']['xml:lang']
                        outFile=property_add( prefLabel_wiki, lang_pr_wiki, outFile, 'prefLabel' , rels)
                    if('desc' in bindings[i]):
                        definition_wiki=bindings[i]['desc']['value']
                        lang_pr_wiki=bindings[i]['desc']['xml:lang']
                        outFile=property_add( definition_wiki, lang_pr_wiki, outFile, 'definition', rels)   
    target="', '".join(targets)
    target="'"+target+"'"
    for idterm in iduri:    
        query = altLabel_query.replace("WDTMID", idterm).replace("TARGETS", target)
        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
        altLabel_response = r.json()
        bindings=altLabel_response['results']['bindings']

        for i in range(len(bindings)):
            if('altLabel' in bindings[i]):
                altLabel_wiki=bindings[i]['altLabel']['value']
                lang_al_wiki=bindings[i]['altLabel']['xml:lang']
                outFile=property_add( altLabel_wiki, lang_al_wiki, outFile, 'altLabel', rels )
                    
    if(rels==1):                
        # Retrieve narrower and broader concepts
        relation_type = ["narrower", "broader"]
        for relation in relation_type:
            if relation == "narrower":
                concept_query = narrower_concept_query
                relation_id = "naTerm"
            else:
                concept_query = broader_concept_query
                relation_id = "brTerm"

            for idterm in iduri:
                query = concept_query.replace("WDTMID", idterm)
                r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                concept_response = r.json()
                concepts_list = [item[relation_id]["value"].split("/")[-1] if len(item[relation_id]["value"]) else None for item in concept_response["results"]["bindings"]]
                if len(concepts_list):
                    for concept in concepts_list:
                        query = term_query.replace("WDTMID", concept).replace("TARGETS", target)
                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                        for item in r.json()["results"]["bindings"]:
                            concept_terms = item["name"]["value"]
                            verify=checkTerm(lang, concept_terms, relation, targets)
                            ide=verify[0]
                            termSearch=verify[1]
                            if(termSearch!='1'):
                                outFile[relation].append(ide)
                                originalIde=outFile['@id']
                                dataEurovoc=eurovoc_file(termSearch, ide, relation, 'iduri', lang, scheme,  originalIde)
    return(outFile)

def reduction_defs(list_in):
    list_out=[]
    for i in list_in:
        spl=i.split(' ')
        if(len(spl)>250):
            list_out.append(''.join(spl[:250]))
        else:
            list_out.append(i)
        #print(out)
    return(list_out)

def wsidFunction(termIn, context,   definitions):
    
    defiMax=''
    idMax=''
    posMax=0
    code=0

    if(context):
        context=context.lower().replace('\n', '')
        pesos=[]
        start=context.index(termIn)
        longTerm=len(termIn)
        end=context.index(termIn)+longTerm
        listdef=reduction_defs(definitions[0])
        listIde=definitions[1]
        definitionsJoin=', '.join(listdef)
        print('CONTEXT---',context)
        print('START---', start)
        print('END---', end)
        print('DEINITIONS---',definitionsJoin)
        print('----Entrando WSDI----')
        response = requests.post('http://el-flask-88-staging.cloud.itandtel.at/api/disambiguate_demo',
                params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                headers ={'accept': 'application/json',
                    'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
            }
        )
        code=response.status_code
        print('CODE WSID',code)
        print('response', response)
        req = response.request

        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method = req.method
        uri = req.url
        data = req.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
        headers = " -H ".join(headers)
        print(command.format(method=method, headers=headers, data=data, uri=uri))
        
        try:
            pesos=response.json()
            print(pesos)
            if(code==200):
                max_item = max(pesos, key=int)
                posMax=pesos.index(max_item)
                if(len(listdef)>0 and (posMax)<len(listdef)):
                    #print(len(listdef), posMax)
                    defiMax=listdef[posMax-1]
                else:
                    defiMax=''
                if(len(listIde)>0 and (posMax)<len(listIde)):
                    idMax=listIde[posMax-1]
                else:
                    idMax=''
        except json.decoder.JSONDecodeError:
            print('JSONDecodeError WSID')
            pesos=[]
            defiMax=''
            idMax=''
            
    print('----Saliendo WSDI----')
        
    return(defiMax, idMax,code)

def check_prefLabel(outFile, targets, rels):
    targetsNull=[]
    prefLabel=outFile['prefLabel']
    if(rels==1):
        for i in range(len(targets)):
            if(targets[i] not in targets_pref):
                targetsNull.append(targets[i])
    else:
        for i in range(len(targets)):
            if(targets[i] not in targets_relation):
                targetsNull.append(targets[i])
    
    return(targetsNull)

def property_add( value, lang, outFile, label,rels, uri ):
    label_file=outFile[label] 
    if(rels==1):
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in prefLabel_full and lang not in targets_pref):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    prefLabel_full.append(plb)
                    targets_pref.append(lang)
                    file_html(scheme, value.strip(' '), ide_file, lang)
                
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in prefLabel_full and alb not in altLabel_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    altLabel_full.append(alb)
            elif(label=='definition'):
                dlb=value.strip(' ')+'-'+lang
                if(dlb not in definition_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    definition_full.append(dlb)
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in prefLabel_full and lang not in targets_pref ):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        prefLabel_full.append(plb)
                        targets_pref.append(lang)
                        file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in prefLabel_full and alb not in altLabel_full):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        altLabel_full.append(alb)
                elif(label=='definition'):
                    dlb=value.strip(' ')+'-'+lang
                    if(dlb not in definition_full):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        definition_full.append(dlb)
    else:
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in pref_relation and lang not in targets_relation):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    pref_relation.append(plb)
                    targets_relation.append(lang)
                    file_html(scheme, value.strip(' '), ide_file, lang)
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in pref_relation and lang not in targets_relation):
                    outFile['prefLabel'].append({'@language':lang, '@value':value.strip(' ')})
                    pref_relation.append(alb)
                    targets_relation.append(lang)
                elif(alb not in pref_relation and alb not in alt_relation):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    alt_relation.append(alb)
            
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in pref_relation and lang not in targets_relation ):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        pref_relation.append(plb)
                        targets_relation.append(lang)
                        file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in pref_relation and lang not in targets_relation):
                        outFile['prefLabel'].append({'@language':lang, '@value':value.strip(' ')})
                        pref_relation.append(alb)
                        targets_relation.append(lang)
                    elif(alb not in pref_relation and alb not in alt_relation):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        alt_relation.append(alb)
    return(outFile)


def jsonFile(ide, scheme, rels, note, context, term, lang_in):  
    newFile=''
    data={}
    
    data={
        '@context':"http://lynx-project.eu/doc/jsonld/skosterm.json",
        '@type':'skos:Concept',
        '@id': ide,
        'inScheme': scheme.replace(' ',''),
        'source':'',
        'source':'',
        'closeMatch':'',
        'exactMatch':'',
        'exactMatch':'',
        'prefLabel':'' ,
        'altLabel':'' ,
        'definition':'' ,
        'note':'' ,
        'example': '',
        'topConceptOf': 'http://lynx-project.eu/kos/'+scheme.replace(' ','')}


    data['prefLabel']=[]
    data['altLabel']=[]
    data['definition']=[]
    data['prefLabel'].append({'@language':lang_in, '@value':term.strip(' ')})
    prefLabel_full.append(term.strip(' ')+'-'+lang_in)
    targets_pref.append(lang_in.strip(' '))

    if(rels==1):
        data['broader']=[]
        data['narrower']=[]
        data['related']=[]

    return(data)

def fix(outFile, find_iate, find_euro, find_lexi, find_wiki, note, context, termin):
    if(len(find_lexi)==0 and len(find_euro)==0 and len(find_iate)==0 and len(find_wiki)==0):
        #outFile['prefLabel'].append({'@language':lang_in, '@value':termin.strip(' ')})
        #prefLabel_full.append(termin.strip(' ')+'-'+lang_in)
        #targets_pref.append(lang_in.strip(' '))
        
        if(len(closeMatch)>0):
            outFile['closeMatch']=closeMatch[0]
        if(context):
            no_find.writerow([termin.strip(' '), 'con contexto'])
        else:
            no_find.writerow([termin.strip(' '), 'sin contexto'])


    if(len(note)):
        outFile['note']=note

    if(context):
        outFile['example']=context
    if(len(outFile['prefLabel'])==0):
        del outFile['prefLabel']
    if(len(outFile['altLabel'])==0):
        del outFile['altLabel']
    if(len(outFile['definition'])==0):
        del outFile['definition']
    if(len(outFile['broader'])==0):
        del outFile['broader']
    if(len(outFile['narrower'])==0):
        del outFile['narrower']
    if(len(outFile['related'])==0):
        del outFile['related']

    if(len(find_euro) and len(find_wiki)):
        outFile['exactMatch']=find_euro[0]
        outFile['exactMatch']='https://www.wikidata.org/wiki/'+find_wiki[0]
        pass
    elif(len(find_euro) and len(find_wiki)==0):
        outFile['exactMatch']=find_euro[0]
        pass
    elif(len(find_wiki) and len(find_euro)==0):
        outFile['exactMatch']='https://www.wikidata.org/wiki/'+find_wiki[0]
        pass
    elif(len(find_wiki)==0 and len(find_euro)==0):
        del outFile['exactMatch']

    if(len(find_iate) and len(find_lexi)):
        outFile['source']="https://iate.europa.eu/entry/result/"+str(find_iate[0])
        outFile['source']="https://dictapi.lexicala.com/senses/"+find_lexi[0]
        pass
    elif(len(find_iate) and len(find_lexi)==0):
        outFile['source']="https://iate.europa.eu/entry/result/"+str(find_iate[0])
        pass
    elif(len(find_lexi) and len(find_iate)==0):
        outFile['source']="https://dictapi.lexicala.com/senses/"+find_lexi[0]
        pass
    elif(len(find_lexi)==0 and len(find_iate)==0):
        del outFile['source']
    
    if(len(note)==0):
        del(outFile['note'])
    if(context==None):
        del(outFile['example'])

    del(outFile['closeMatch'])


    return(outFile)
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
folder=os.listdir(raiz)

createRelationFolders(targets)

lang_in=lang



if(term):
    print('solo termino')
    name_file=''
    listread=[]
    term=preProcessingTerm(term, context, contextFile)
    context=term[2]
    print(context)
    check=checkTerm(lang,term[1], '', targets)
    ide=check[0]
    ide_file=ide
    termSearch=check[1]
    print('TERM A BUSCAR: ', termSearch)
    if(termSearch!='1'):
        rels=1
        outFile=jsonFile(ide, scheme, rels, '',context, termSearch, lang_in)
        print('------IATE')
        outFile=iate(termSearch, lang,targets, outFile, context, wsid,1)
        print('------EUROVOC')
        outFile=eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, 1)
        print('------LEXICALA')
        outFile=lexicala(lang, termSearch, targets, context,  outFile, wsid, 1)
        print('------WIKI DATA')
        outFile=wikidata_retriever(termSearch, lang, context,  targets, outFile, 1, wsid)
        
        note=''
        outFile=fix(outFile, find_iate, find_euro, find_lexi, find_wiki, note, context, termSearch)
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
    

