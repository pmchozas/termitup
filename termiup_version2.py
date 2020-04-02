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
prefLabel_full=[]
altLabel_full=[]
definition_full=[]
# clean term
def preProcessingTerm(term):
    termcheck=term.strip('‐').strip('—').strip('–').strip(' ').rstrip('\n').rstrip(' ').replace(' – ', ' ').replace('\t', '').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(' ', '_').replace('\ufeff','')
    return(termcheck)

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
                os.makedirs(tar+"/"+i)
# files
def path(targets, relation):
    listt_arq=[]
    for i in targets:
        if(relation!=''):
            path=i+'/'+relation+'/'
        else:
            path=i+'/'
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
        "nl": "contexts/DNVGL-NL.ttl",
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

# bearen token
def bearenToken(): 
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)

# iate
def iate(term, lang,targets,outFile, context,  contextFile, wsid):
    answer=[]
    try:
        print('Entra iate')
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
        answer.append(response2)
        jsondump=json.dumps(answer)
        results=[]
        termSearch=[]
        cont=0
        termSearch.append(response2['request']['query'])
        bloq=0
        if('items' in response2.keys()):
            term=response2['items']
            ide=sctmid_creator()
            definicion_wsid=[]
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                results.insert(item, [])
                ide_iate=term[item]['id']
                leng=term[item]['language']
                if(leng[lang]['term_entries'][0]['term_value']==termSearch[cont]):
                    if(context==None and len(contextFile)<1):
                        context=getContextIate(item, leng, lang,termSearch[cont] )
                    for target in targets:
                        get=getInformationIate(target,item, leng, termSearch[cont])
                        results[item].insert(0, item)#item
                        results[item].insert(1, get[0])#def
                        results[item].insert(2, get[1])#pref
                        results[item].insert(3, get[1])#alt
                        results[item].insert(4, target)#target
                        if(target==lang and get[0]!='' ):
                            definicion_wsid.append(get[0])
        
            d=(definicion_wsid,[])
            
            if(wsid=='yes'):
                maximo=wsidFunction(termSearch[cont],  context, contextFile,  d)
                if(maximo[2]!=200):
                    outFile=fillPrefIate(outFile, results, 'prefLabel',[], 2, None)
                    outFile=fillAltIate(outFile, results, 'altLabel', 3, None)
                    outFile=fillDefinitionIate(outFile, results,  'definition', 1,None)
                else:
                    item=0
                    wsidmax=0
                    for item in range(len(results)):
                        if(maximo[0] in results[item]):
                            wsidmax=item
                        item=item+1
                    outFile=fillPrefIate(outFile, results, 'prefLabel',[], 2, wsidmax)
                    outFile=fillAltIate(outFile, results,  'altLabel', 3, wsidmax)
                    outFile=fillDefinitionIate(outFile, results,  'definition', 1, wsidmax)
            else:
                outFile=fillPrefIate(outFile, results, 'prefLabel',[], 2, None)
                outFile=fillAltIate(outFile, results, 'altLabel', 3, None)
                outFile=fillDefinitionIate(outFile, results,  'definition', 1,None)

                
        cont=cont+1
    except json.decoder.JSONDecodeError:
        print('No entro iate')
        response2='{ }'
    
    #print(outFile)
    return(outFile)


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
    defi=defi.replace(',', '').replace('"', '').replace("'", '')
    return(defi, pref, joinSyn)


def fillPrefIate(outFile, results, label, langs, col, wsidmax):
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            while(colm<=len(results[i]) and results[i][colTarget].strip(' ') not in langs ):
                if(results[i][colm]!=""):
                    outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                    prefLabel_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                    langs.append(results[i][colTarget].strip(' '))
                colm=colm+5
                colTarget=colTarget+5
    else:
        colm=col
        colTarget=4

        while(colm<=len(results[wsidmax]) and results[wsidmax][colTarget].strip(' ') not in langs ):
            if(results[wsidmax][colm]!=""):
                outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                prefLabel_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget].strip(' '))
                langs.append(results[wsidmax][colTarget].strip(' '))
            colm=colm+5
            colTarget=colTarget+5

    return outFile

def fillAltIate(outFile, results,  label, col, wsidmax):
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            while(colm<len(results[i]) and results[i][colm].strip(' ') not in prefLabel_full ):
                if(results[i][colm]!=""):
                    outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                    altLabel_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                #langs.append(results[i][colmTarget].strip(' '))
                colm=colm+5
                colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        while(colm<len(results[wsidmax])):# and results[wsidmax][colm].strip(' ') not in prefLabel_full and results[wsidmax][colTarget].strip(' ') not in prefLabel_full ):
            alb=results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget]
            print(prefLabel_full)
            if(results[wsidmax][colm]!="" and alb not in prefLabel_full):
                outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                altLabel_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget])
                #langs.append(results[i][colmTarget].strip(' '))
            colm=colm+5
            colTarget=colTarget+5
    return outFile

def fillDefinitionIate(outFile, results,   label,col, wsidmax):
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


def eurovoc(termSearch, lang, targets, context, contextFile, wsid, outFile, scheme, prefLabel_full, altLabel_full, definition_full):
    #print(outFile)
    defs=[]
    name=[]
    urilist=[]
    defsnull=[]
    uri=uri_term_eurovoc(termSearch, lang)
    if(len(uri)>1):
        for i in uri:
            urilist.append(i[0])
            name.append(i[1])
            defsnull.append(i[2])
            if(i[2]!=''):
                defs.append(i[2])
        d=(defs, [])
        maximo=wsidFunction(termSearch, context, contextFile, d)
        if(maximo[2]!=200):
            pass
        else:
            maxx=defsnull.index(maximo[0])
            namewsid=name[maxx]
            uriwsid=urilist[maxx]
            outFile=relations_eurovoc(uriwsid, lang, namewsid,outFile, scheme)
    else:
        tars=check_prefLabel(outFile, targets)
        uri=uri[0]
        for lang in targets:
            alt_ev=name_term_eurovoc(uri[0],lang, 'altLabel')
            def_ev=def_term_eurovoc( uri[0],'"'+lang+'"')
            if(alt_ev!=''):
                outFile=property_add(alt_ev, lang, outFile, 'altLabel')
            if(def_ev!=''):
                outFile=property_add(def_ev, lang, outFile, 'definition')
        outFile=relations_eurovoc(uri[0], lang, termSearch,outFile, scheme)


    return(outFile)

def uri_term_eurovoc(termSearch, lang):
    term='"'+termSearch+'"'
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
                if(termSearch.lower() == answerl.lower()):
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
    
    except json.decoder.JSONDecodeError:
        answer=[]
            
    return(answer)

def def_term_eurovoc( uri,lang):
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

def getRelation(uri_termino, relation):
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

def name_term_eurovoc(uri,lang,label):
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
        
      
    return(nameUri)



def relations_eurovoc(uri, lang, term, outFile, scheme):
    results=[]
    si=[]
    relations=['broader', 'narrower', 'related']
    for relation in relations: 
        uriRelation=getRelation(uri, relation)
        if(len(uriRelation)>0):
            if('topConceptOf' in outFile.keys()):
                del outFile['topConceptOf']
            for i in uriRelation:
                verify=checkTerm(lang, i[1], relation, targets)
                ide=verify[0]
                termSearch=verify[1]
                outFile[relation].append(ide)
                originalIde=outFile['@id']
                dataEurovoc=eurovoc_file(termSearch, ide, relation, i[0], lang, scheme,  originalIde)

    #print(outFile)
    return(outFile)

def eurovoc_file(termSearch, ide, relation, iduri, lang, scheme,  originalIde):
    data={}
    #print(termSearch, ide, relation, iduri, lang, scheme,  originalIde)
    if('broader' in relation and termSearch!=''):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
        data['prefLabel']=[]
        data['narrower']=[]
        data['prefLabel'].append({'@language':lang, '@value':termSearch})
        data['narrower'].append(originalIde)

    elif('narrower' in relation and termSearch!=''):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
        data['prefLabel']=[]
        data['broader']=[]
        data['prefLabel'].append({'@language':lang, '@value':termSearch})
        data['broader'].append(originalIde)

    elif('related' in relation and termSearch!=''):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
        data['prefLabel']=[]
        data['related']=[]
        data['prefLabel'].append({'@language':lang, '@value':termSearch})
        data['related'].append(originalIde)
    '''
    elif('broader' not in relation):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'' }
    elif('narrower' not in relation):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'' }
    elif('related' not in relation):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'' }
    '''
   
    #print(data)  
    n=termSearch.replace(' ', '_').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I
                )
    n = normalize( 'NFC', n)
    newFile=lang+'/'+relation+'/'+n+'_'+ide+'.jsonld'
    #with open(newFile, 'w') as file:
    #    json.dump(data, file, indent=4,ensure_ascii=False)
              
    return(data)


def lexicala(lang, term, targets, context, contextFile, outFile, wsid, prefLabel_full, altLabel_full, definition_lexicala):
    answer=lexicala_term(lang, term)
    if('n_results' in answer):
        results=answer['n_results']
        if(results>0):
            if(wsid=='yes'):
                definitions=definition_lexicala(answer)
                maximo=wsidFunction(term,context, contextFile, definitions)
                if(maximo[2]!=200):
                    pass
                else:
                    alt_lex=altLabel_lexicala(maximo, targets)
                    def_lex=maximo[0]
                    if(len(alt_lex)>0):
                        for i in alt_lex:
                            outFile=property_add(i[0], i[1], outFile, 'altLabel')
                    if(def_lex!=''):
                        outFile=property_add(def_lex, lang, outFile, 'definition')
    return(outFile)


def lexicala_term(lang, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+lang+"&text="+term+"", auth=('upm2', 'XvrPwS4y'))
    answerSearch=search.json()
    return(answerSearch)

def lexicala_sense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('upm2', 'XvrPwS4y'))
    answerSense=sense.json()
    return(answerSense)

def definition_lexicala(answer):
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
    return(listaDefinition, listaId)

def altLabel_lexicala(maximo, targets):
    traductions=[]
    jsonTrad=lexicala_sense(maximo[1])
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


def wikidata_retriever(term, lang, context, contextFile, targets):
    url = 'https://query.wikidata.org/sparql'
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
    #print(term)
    query = retrieve_query.replace("TERM", term).replace("LANG", lang)
    SRCTERM = "\"" + term + "\"" + "@" + lang
    #print(SRCTERM) We have to save this in the skos as well
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json()
    
    if len(data['results']['bindings']) != 0:
        bindings=data['results']['bindings']
        for i in range(len(bindings)):
            iduri.append(bindings[i]['item']['value'].split("/")[-1])
            definition.append(bindings[i]['desc']['value'].replace(',', ''))

        d=(definition,[])

        maximo=wsidFunction(term,  context, contextFile,  d)
        
        relations_retrieved = dict()
        if( maximo[2]==200):
            posMax=definition.index(maximo[0])
            item_id=iduri[posMax]
            target="', '".join(targets)
            target="'"+target+"'"
            query = original_query.replace("WDTMID", item_id).replace("TARGETS", target)
            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
            data = r.json()
            
            
            
            query = altLabel_query.replace("WDTMID", item_id).replace("TARGETS", target)
            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
            altLabel_response = r.json()
            
            bindings2=altLabel_response['results']['bindings']
            
            for i in range(len(bindings2)):
                if('altLabel' in bindings2[i]):
                    AL=bindings2[i]['altLabel']['value']
                    langAL=bindings2[i]['altLabel']['xml:lang']
                    altLabel.append([AL, langAL])
            #print(altLabel)

            # Retrieve narrower and broader concepts
            relation_type = ["narrower", "broader"]
            
            for relation in relation_type:
                if relation == "narrower":
                    concept_query = narrower_concept_query
                    relation_id = "naTerm"
                else:
                    concept_query = broader_concept_query
                    relation_id = "brTerm"

                query = concept_query.replace("WDTMID", item_id)
                r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                concept_response = r.json()
                # extract concepts and get its id (the URL is returned by default)
                concepts_list = [item[relation_id]["value"].split("/")[-1] if len(item[relation_id]["value"]) else None for item in concept_response["results"]["bindings"]]
                 
                # Retrieve terms of the concepts
                concepts_dict = dict()
                if len(concepts_list):
                    for concept in concepts_list:
                        concept_terms = dict()
                        query = term_query.replace("WDTMID", concept).replace("TARGETS", target)
                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                        for item in r.json()["results"]["bindings"]:
                            concept_terms[item["lang"]["value"]] = item["name"]["value"]
                        concepts_dict[concept] = concept_terms
                else:
                    concepts_dict = {}

                relations_retrieved[relation] = concepts_dict
        else:
            pass
            #print(relations_retrieved)
    return(altLabel, relations_retrieved)


def wsidFunction(termIn, context, contextFile,  definitions):
    defiMax=''
    idMax=''
    posMax=0
    code=0

    if(context):
        pesos=[]
        start=context.index(termIn)
        longTerm=len(termIn)
        end=context.index(termIn)+longTerm
        listdef=definitions[0]
        listIde=definitions[1]
        definitionsJoin=', '.join(listdef)
        response = requests.post(
            'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
            params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
            headers ={'accept': 'application/json',
                'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
            }
        )
        code=response.status_code
        try:
            pesos=response.json()
            max_item = max(pesos, key=int)
            posMax=pesos.index(max_item)
            if(len(listdef)>0):
                defiMax=listdef[posMax-1]
            else:
                defiMax=''
            if(len(listIde)>0):
                idMax=listIde[posMax-1]
            else:
                idMax=''
        except json.decoder.JSONDecodeError:
            pesos=[]
            defiMax=''
            idMax=''
        
        
        #barra('Desambiguando context')
    elif(contextFile):
        for i in contextFile:
            contextTerm=i[0]
            if(termIn in contextTerm):
                pesos=[]
                context=i[1]
                start=i[2]
                end=i[3]
                listdef=definitions[0]
                listIde=definitions[1]
                definitionsJoin=', '.join(listdef)
                response = requests.post(
                                'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
                                params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                                headers ={'accept': 'application/json',
                                        'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
                                        }
                                )
               
                code=response.status_code
                try:
                    pesos=response.json()
                    max_item = max(pesos, key=int)
                    posMax=pesos.index(max_item)
                    if(len(listdef)>0):
                        defiMax=listdef[posMax-1]
                    else:
                        defiMax=''
                    if(len(listIde)>0):
                        idMax=listIde[posMax-1]
                    else:
                        idMax=''
                except json.decoder.JSONDecodeError:
                    pesos=[]
                    defiMax=''
                    idMax=''
                break
            else:
                defiMax=''
                idMax=''

        
    return(defiMax, idMax,code)

def check_prefLabel(outFile, targets):
    targetsNull=[]
    prefLabel=outFile['prefLabel']
    altLabel=outFile['altLabel']
    definition=outFile['definition']
    
    for i in range(len(targets)):
        if(targets[i] in prefLabel[i]['@language']):
            targetsNull.append(targets[i])
    
    return(targetsNull)

def property_add( value, lang, outFile, label ):
    label_file=outFile[label] 
    if(len(label_file)==0):
        if(label=='altLabel'):
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
            if(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in prefLabel_full and alb not in altLabel_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    altLabel_full.append(alb)
            elif(label=='definition'):
                dlb=value.strip(' ')+'-'+lang
                if(dlb not in definition_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    definition_full.append(dlb)
    return(outFile)


def jsonFile(ide, scheme):  
    newFile=''
    data={}
    data={
    '@context':'',
    '@id': ide,
    '@type':'skos:Concept',
    'inScheme': scheme.replace(' ',''),
    "source":"https://iate.europa.eu/entry/result/",
    "sameAs":"https://www.wikidata.org/wiki/Q22687",
    "sameAs":"http://eurovoc.europa.eu/4738",
    'prefLabel':'' ,
    'altLabel':'' ,
    'definition':'' ,
    'topConceptOf': 'http://lynx-project.eu/kos/'+scheme.replace(' ','')}
    
    data['@context']={"@base": "http://lynx-project.eu/kos/",
            "dcterms": "http://purl.org/dc/terms/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc": "http://purl.org/dc/elements/1.1/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "conceptScheme": {
                "@id":"skos:ConceptScheme",
                "@type":"@id"
                },
            "inScheme": {
                "@id":"skos:inScheme",
                "@type": "@id"
                },
            "broader": {
                "@id":"skos:broader",
                "@type": "@id"
                },
            "narrower": {
                "@id":"skos:narrower",
                "@type": "@id"
                },
            "related": {
                "@id":"skos:related",
                "@type": "@id"
                },
            "hasTopConcept": {
                "@id":"skos:hasTopConcept",
                "@type": "@id"
                },
            "topConceptOf": {
                "@id":"skos:topConceptOf",
                "@type": "@id"
                },
            "prefLabel": "skos:prefLabel",
            "altLabel": "skos:altLabel",
            "notation": "skos:notation",
            "definition": "skos:definition",
            "source":"dc:source",
            "creator":"dc:creator",
            "label" : "rdfs:label",
            "description":"dc:description",
            "date":"dc:date",
            "sameAs":"owl:sameAs"
        }
    data['prefLabel']=[]
    data['altLabel']=[]
    data['definition']=[]
    data['broader']=[]
    data['narrower']=[]
    data['related']=[]
    return(data)
        
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


if(term):
    listread=[]
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        contextF=csv.reader(file)
        contextFile=[]
        for i in contextF:
            contextFile.append([i[0], i[1],i[2],i[3]])
    else:
        contextFile=leerContextos(lang, term)
    
    check=checkTerm(lang,term, '', targets)
    ide=check[0]
    termSearch=check[1]
    print('TERM A BUSCAR: ', termSearch)
    if(termSearch!='1'):
        outFile=jsonFile(ide, scheme)
        outFile=iate(termSearch, lang,targets, outFile, context,contextFile, wsid)
        outFile=eurovoc(termSearch, lang, targets, context, contextFile, wsid, outFile, scheme, prefLabel_full, altLabel_full, definition_full)
        outFile=lexicala(lang, term, targets, context, contextFile, outFile, wsid, prefLabel_full, altLabel_full, definition_lexicala)
        outFile=wikidata_retriever(termSearch, lang, context, contextFile, targets)
    print(outFile)
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
        contextFile=leerContextos(lang)
    
    listread=[]
    file=open(listTerm+'.csv', 'r', encoding='utf-8')
    read=csv.reader(file)
    cont=0

    for i in read:
        term=preProcessingTerm(i[0])
        check=checkTerm(lang,term, '', targets)
        ide=check[0]
        termSearch=check[1]
        cont=cont+1
        print('TERM A BUSCAR: ',i[0],'|',term,'|', termSearch, '|',cont)
        if(termSearch!='1'):
            jsonlist=iate(termSearch, lang,targets)
            all(jsonlist, lang, targets,context, contextFile,  wsid,scheme, DR)
        else:
            listread.append(term)
    