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

def leerContextos(lang, termIn):
    configuration= {
        "es": "contexts/Spain-judgements-ES.ttl",
        "en": "contexts/UK-judgements-EN.ttl",
        "nl": "contexts/Austria-collectiveagreements-DE.ttl",
        "de": "contexts/contracts_de.ttl"
    }
    
    es = '%s'%configuration["es"]
    en = '%s'%configuration["en"]
    nl = '%s'%configuration["nl"]
    de = '%s'%configuration["de"]
    encoding = 'utf-8'
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

#funcion para obtener identificadores
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID
    
#funcion para obtener el baren token (access token)
def obtenerToken(): 
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)

def haceJson(termino, idioma,targets):
    answer=[]
    try:
        auth_token=obtenerToken()
        hed = {'Authorization': 'Bearer ' +auth_token}
        jsonList=[]
        data = {"query": termino,
        "source": idioma,
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
        reponse2=response.json()
        js=json.dumps(reponse2)
        answer.append(reponse2)
        jsondump=json.dumps(answer)

    except json.decoder.JSONDecodeError:
        jsondump='{ }'
        
    return(jsondump)

def getContextIate(item, leng, idioma, termSearch):
    context=''

    if(idioma in leng):
        language=leng[idioma]
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

                        


def getIate(target, item,leng,termSearch):
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
    defi=defi.replace(',', '')
    return(defi, pref, joinSyn)


def iateLists(pref, alt, defi, tar, iate,j, lbloq,prefLabel, synonyms, definicion2, lang, iateIde):

    pref.append(prefLabel[j][:-2])
    alt.append(synonyms[j][:-2])
    defi.append(definicion2[j][:-2])
    tar.append(lang[j][:-2])
    iate.append(iateIde[j][:-2])

    
    return(pref, alt, defi, tar, iate)

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
                defiMax=listdef[posMax]
            else:
                defiMax=''
            if(len(listIde)>0):
                idMax=listIde[posMax]
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
                        defiMax=listdef[posMax]
                    else:
                        defiMax=''
                    if(len(listIde)>0):
                        idMax=listIde[posMax]
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


def resultsEurovoc(termino, idioma, relations, target, context, contextFile, wsid):
    results=[]
    answer=[]
    resultado=''
    relation=''
    new=open('eurovocNO.csv', 'a')
    euronot = csv.writer(new)

    uri=getUriTerm(termino, target, idioma)
    if(len(uri)>0 and uri[0]!=''):
        nameDef=getName(uri, idioma,termino)
        nombres=nameDef[0]
        definiciones=nameDef[1]
        definicionesOnly=nameDef[2]
        d=(definicionesOnly, [])
        if(wsid=='yes'):
            maximo=wsidFunction(termino, context, contextFile, d)
            if(maximo[2]!=200 or maximo[0]==''):
                answer=listEurovoc(relations, uri, idioma,termino)

               
            else:
                m=definicionesOnly.index(maximo[0])
                alta=nombres[m]
                uri=getUriTerm(alta, target, idioma) 
                answer=listEurovoc(relations, uri, idioma,termino)
                
        else:
            uri=getUriTerm(termino, target, idioma) 
            answer=listEurovoc(relations, uri, idioma,termino)
            
          

    else:
        #print('NO ESTA EN EUROVOC', termino)
        euronot.writerow([termino, idioma])
        for relation in relations: 
            answer=results.append([[''], [''], relation])
  
    if(answer==None):
        answer=results
    #barra('Get Eurovoc')
    return(answer)

def listEurovoc(relations, uri, idioma, termino):
    results=[]
    si=[]
    for relation in relations: 
        uriRelation=getRelation(uri, relation)
        nameDef=getName(uriRelation, idioma, termino)
        nombres=nameDef[0]
        definiciones=nameDef[1]
        definicionesOnly=nameDef[2]
        results.append([nombres, uriRelation, relation])
           
    
    return(results)

      
    

#1. funcion que obtiene la uri de cada termino
def getUriTerm(termino,lenguaje, idioma):
    termino2='"'+termino+'"'
    lenguaje2='"'+lenguaje+'"'
    idioma2='"'+idioma+'"'
    resultado=[]
    resultadouri=''
    valor=''
    try:
        url = ("http://sparql.lynx-project.eu/")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        ?c a skos:Concept .
        ?c ?p ?label. 
          FILTER regex(?label, """+termino2+""", "i" )
          FILTER (lang(?label) = """+idioma2+""")
          FILTER (?p IN (skos:prefLabel, skos:altLabel ) )

        }  
        }
        """
        #filter ( contains(?label,?searchTerm) && lang(?label)=?searchLang )
        #filter (regex(?label, "(^)"""+termino+"""($)"))
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            resultadouri=''
        else:
            for result in results["results"]["bindings"]:
                resultadouri=result["c"]["value"]
                resultadol=result["label"]["value"]
                valor=getjustName(resultadouri,idioma )
                if(termino.lower() == valor.lower()):
                    resultado.append(resultadouri)
                else:
                    tok=resultadol.split(' ')
                    for i in tok:
                        if('(' in i):
                            tok.remove(i)
                            tokt=termino.split(' ')
                            if(len(tok)==len(tokt)):
                                resultado.append(resultadouri)
    
    except json.decoder.JSONDecodeError:
        resultado.append('')
            
    return(resultado)

def getjustName(uri,lenguaje):
    nameUri=''
    lenguaje2='"'+lenguaje+'"'
    url=("http://sparql.lynx-project.eu/")
    query="""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?c ?label
    WHERE {
    GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
    VALUES ?c { <"""+uri+"""> }
    VALUES ?searchLang { """+lenguaje2+""" undef } 
    VALUES ?relation { skos:prefLabel  } 
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


#2. funcion que recibe la uri del termino al que sele desea saber su BROADER, obtiene la uri del BROADER 
def getRelation(uri_termino, relacion):
    resultado=[]
    resultadoRel=''

    for i in uri_termino:
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c {<"""+i+"""> }
        VALUES ?relation { skos:"""+relacion+""" } # skos:broader
        ?c a skos:Concept .
        ?c ?relation ?label .    
        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                resultadoRel=''
        else:
            for result in results["results"]["bindings"]:
                resultadoRel=result["label"]["value"]
        resultado.append(resultadoRel)
    
    return(resultado)


#3. funcion que recibe la uri del broader y consulta cual es el termino correspondiente
def getName(uri,lenguaje, termino):
    defs=[]
    defsOnly=[]
    names=[]
    nameUri=''
    valor=''
    for i in uri:
        lenguaje2='"'+lenguaje+'"'
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+i+"""> }
        VALUES ?searchLang { """+lenguaje2+""" undef } 
        VALUES ?relation { skos:prefLabel  } 
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
        valor=getDef( nameUri, i,lenguaje)
        v1=valor[1].replace(',','')
        names.append(valor[0])
        defs.append(v1)
        if(valor[1]!='' and valor[0] in valor[1]):
            defsOnly.append(v1)
      
    return(names, defs,defsOnly)

#3. funcion que recibe la uri del broader y consulta cual es el termino correspondiente
def getDef( nameUri,uriRelation,lenguaje):
    definicion=''
    resultado=[]
    lenguaje2='"'+lenguaje+'"'
    url=("http://sparql.lynx-project.eu/")
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+uriRelation+"""> }
        VALUES ?searchLang { """+lenguaje2+""" undef } 
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
    return(nameUri, definicion)


def lexicalaSearch(languageIn, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+term+"", auth=('upm2', 'XvrPwS4y'))
    answerSearch=search.json()
    return(answerSearch)

def lexicalaSense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('upm2', 'XvrPwS4y'))
    answerSense=sense.json()
    return(answerSense)

def resultsSyns(idioma,termino,targets,context, contextFile,wsid): 
    tradMax=[]
    getsyn=''
    if(termino):
        answer=lexicalaSearch(idioma, termino)
        if('n_results' in answer):
            results=answer['n_results']
            if(results>0):
                definitions=definitionGet(answer)
                if(wsid=='yes'):
                    maximo=wsidFunction(termino,context, contextFile, definitions)
                    if(maximo[2]!=200):
                        maximo=(termino, '')
                        tradMax=traductionGet(maximo, targets)
                        synsTrad=justSyn(tradMax)
                        getsyn=synonymsGet(maximo)
                    else:
                        if(maximo[1]!=''):
                            tradMax=traductionGet(maximo, targets)
                            synsTrad=justSyn(tradMax)
                            getsyn=synonymsGet(maximo)
                        else:
                            getsyn=''
                            tradMax=[]
                else:
                    maximo=(termino, '')
                    tradMax=traductionGet(maximo, targets)
                    synsTrad=justSyn(tradMax)
                    getsyn=synonymsGet(maximo)

    #barra('Get Lexicala')
    return(getsyn, tradMax)

def justSyn(tradMax):
    joinSyns=''
    if(len(tradMax)>0):
        slp=tradMax[0].split(',')
        listaSinonimos=[]
        answer=lexicalaSearch(slp[1], slp[0])
        results=answer['n_results']
        if(results>0):
            if('synonyms' in answer.keys() ):
                syn=answer['synonyms']
                if(len(syn)>0):
                    for j in range(len(syn)):
                        synonym=syn[j]
                        listaSinonimos.append(synonym)
        joinSyns=','.join(listaSinonimos)
    return(joinSyns)



def synonymsGet(maximo):
    listaSinonimos=[]
    answer=lexicalaSense(maximo[1])
    if('synonyms' in answer.keys() ):
        syn=answer['synonyms']
        if(len(syn)>0):
            for j in range(len(syn)):
                 synonym=syn[j]
                 listaSinonimos.append(synonym)
    joinSyns=','.join(listaSinonimos)
    return(joinSyns)
    

                
def definitionGet(answer):
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




def traductionGet(maximo, targets):
    textList=[]
    jsonTrad=lexicalaSense(maximo[1])
    if('translations' in jsonTrad.keys()):
        translations=jsonTrad['translations']
        for j in targets:
            if(j in translations):
                idiomas=translations[j]
                if('text' in idiomas):
                    text=idiomas['text']
                    textList.append(text+','+ j)
                else:
                    for k in range(len(idiomas)):
                        text=idiomas[k]['text']
                        textList.append(text+','+ j)


    return(textList)


def fileJson(termSearchIn, prefLabel, altLabel,definition,idioma,lang, eurovoc,iate, lexicala, scheme, dataRetriever, targets):  
    
    newFile=''
    data={}
    dataContext={}
    si=[]
    sipref=[]
    sialt=[]
        
    br=eurovoc[0][0][0]
    na=eurovoc[1][0][0]
    rel=eurovoc[2][0][0]
    if(br=='' ):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@id': ide, '@type':'skos:Concept', 'inScheme': scheme.replace(' ',''), "source":"https://iate.europa.eu/entry/result/"+iate[0], 'prefLabel':'' ,'altLabel':'' ,'definition':'' ,'topConceptOf': 'http://lynx-project.eu/kos/'+scheme.replace(' ','')}
    else:
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@id': ide, '@type':'skos:Concept', 'inScheme': scheme.replace(' ',''), "source":"https://iate.europa.eu/entry/result/"+iate[0], 'prefLabel':'' ,'altLabel':'' ,'definition':'' }
        

        
    if(br!=''):
        data['broader']=[]
    if(na!=''):
        data['narrower']=[]
    if(rel!=''):
        data['related']=[]

    data['prefLabel']=[]
    data['altLabel']=[]
    data['definition']=[]


    for i in range(len(prefLabel)):
        if(lang[i]==idioma ):
            if(prefLabel[i]!='' and lang[i] not in si ):
                si.append(idioma)
                sipref.append(termSearch.strip(' '))
                data['prefLabel'].append({'@language':idioma, '@value':termSearch.strip(' ')})
        else:
            if(prefLabel[i]!='' and lang[i] not in si):
                si.append(lang[i])
                sipref.append(prefLabel[i].strip(' '))
                data['prefLabel'].append({'@language':lang[i], '@value':prefLabel[i].strip(' ')})
        
   
    for i in range(len(altLabel)):
        if(altLabel[i]!=''):
            s_alt=altLabel[i].split('|')
            for j in s_alt:
                if( j!='' and j.strip(' ') not in sipref and j.strip(' ') not in sialt and j not in sipref):
                    sialt.append(j.strip(' '))
                    data['altLabel'].append({'@language':lang[i], '@value':j.strip(' ')})
        
        
    if(lexicala[0]!=''):
        data['altLabel'].append({'@language':idioma, '@value':lexicala[0].strip(' ')})

    for i in lexicala[1]:
        s_lex=i.split(',')
        if(s_lex[1]!='' and s_lex[0] not in si):
            data['altLabel'].append({'@language':s_lex[1], '@value':s_lex[0].strip(' ')})
        
    for i in range(len(definition)):
        if(definition[i]!=''):
            data['definition'].append({'@language':lang[i], '@value':definition[i].strip(' ')})

    if(len(data['altLabel'])==0):
        del data['altLabel']
        
       
    if(len(data['definition'])==0):
        del data['definition']
        
    for i in eurovoc:
        t=list(set(i[0]))
        u=list(set(i[1]))
        relationsEurovoc(t, u, idioma,data, i[2], scheme, ide, targets)
            
    
    n=termSearchIn.replace(' ', '_').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
    n = normalize( 'NFC', n)
    newFile=idioma+'/'+n+'_'+ide+'.jsonld'
    with open(newFile, 'w') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
        
    if(dataRetriever=='yes'):
        data=dataRetrieverFunction(newFile, idioma, scheme, ide, targets )
    else:
        data=data
    #print(data)
    return(data)
        
        
def relationsEurovoc(relationList, uriList, idioma,data, relationEuro, scheme, ideOriginal, targets):
    ide=''
    for i in range(len(relationList)):
        relation=relationList[i]
        uri=uriList[i]
        if(relation!=''):
            try:
                verify=verificar(idioma,  relation, relationEuro, targets)
                ide=verify[0]
                termSearch=verify[1]
            except RecursionError:
                ide=sctmid_creator()
                termSearch=relation
            if(ide!='' and termSearch!=''):
                if(relationEuro in data.keys()):
                    data[relationEuro].append(ide)
                    dataEurovoc=fileEurovoc(termSearch, ide, relation, uri, idioma, scheme, relationEuro, ideOriginal)
                    editFileSchema(scheme, data, ide)
               
                    n=termSearch.replace(' ','')
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                    normalize( "NFD", n), 0, re.I
                        )
                    n = normalize( 'NFC', n)
                    with open(idioma+'/'+relationEuro+'/'+n+'_'+ide+'.jsonld', 'w') as file:
                        json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
    
        else:
            if( 'broader' in relationEuro and relation==''):
                editFileSchema(scheme, data, ideOriginal)
    return(ide)   
        
def fileEurovoc(termSearch, ide, relation, iduri, idioma, scheme, relationEuro, ideOriginal):
    data={}
    if('broader' in relationEuro):
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
    else:
        data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': ide,'inScheme': scheme.replace(' ',''), "sameAs":iduri, '@type':'skos:Concept','prefLabel':'' }
    
    data['prefLabel']=[]
    data['narrower']=[]
    if(relation!=''):
        data['prefLabel'].append({'@language':idioma, '@value':relation})
        data['narrower'].append(ideOriginal)
              
    return(data)

def editFileSchema(scheme, data, ide):
    name=scheme.replace(' ','')+'_schema.json'
    
    with open('schemas/'+name) as f:
        file = json.load(f)
    file["hasTopConcept"].append(ide)
    f.close()
    with open('schemas/'+name, 'w') as new:
        json.dump(file, new, indent=4,ensure_ascii=False)
    
    with open('schemas/'+scheme.replace(' ','')+'_schema.jsonld', 'w') as new:
        json.dump(file, new, indent=4,ensure_ascii=False)
    

   
def fileContext(scheme, termSearch, ide, carpeta, idioma):
    dataContext={}
    dataContext={'@context':'', 'prefLabel':'skos:prefLabel', 'altLabel':'skos:altLabel','notation':'skos:notation','definition':'skos:definition','source':'dc:source','creator':'dc:source', "description":"dc:description",'date':'dc:date' }
    dataContext['@context']={"@base":"http://lynx-project.eu/kos/"+scheme.replace(' ','')+"/", "dcterms": "http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#",  "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc":"http://purl.org/dc/elements/1.1/","skos":"http://www.w3.org/2004/02/skos/core#","owl":"http://www.w3.org/2002/07/owl#","conceptScheme":{ '@id':'skos:ConceptScheme', '@type':'@id'},"inScheme":{ '@id':'skos:inScheme','@type':'@id'},'broader':{ '@id':'skos:broader','@type':'@id'},'narrower':{ '@id':'skos:narrower','@type':'@id'},'related':{'@id':'skos:related','@type':'@id'},'hasTopConcept':{ '@id':'skos:hasTopConcept','@type':'@id'},'topConceptOf':{ '@id':'skos:topConceptOf','@type':'@id'}}
    path=idioma+'/'
    lista_arq = [obj for obj in listdir(path) ]
    if('contextsFiles' in lista_arq):
        pass
    else:
        os.mkdir(idioma+'/contextsFiles/')
    with open(idioma+'/contextsFiles/'+termSearch+'_'+ide+'.jsonld', 'w') as file:
        json.dump(dataContext, file, indent=4,ensure_ascii=False)

def fileScheme(scheme, idioma,creator, date, description, keywords):
    dataScheme={}
    dataScheme={"@context": "http://lynx-project.eu/doc/jsonld/skosterm.json", "@id": scheme.replace(' ',''), "conceptScheme":"http://lynx-project.eu/kos/"+scheme.replace(" ","")+"/", "hasTopConcept": "", "label":scheme, "creator": creator, "date":date, "description": description}
    dataScheme['hasTopConcept']=[]
    for i in keywords:
        dataScheme['hasTopConcept'].append({'@value':i.strip(' ')})
    
    path=idioma+'/'
    lista_arq = [obj for obj in listdir(path) ]
    if('schemeFiles' in lista_arq):
        pass
    else:
        os.mkdir(idioma+'/schemeFiles/')
    with open(idioma+'/schemeFiles/'+scheme.replace(' ','')+'_schema'+'.jsonld', 'w') as file:
        json.dump(dataScheme, file, indent=4,ensure_ascii=False)

def path(idioma, targets, relation):
    lista_arq=[]
    for i in targets:
        if(relation!=''):
            path=i+'/'+relation+'/'
        else:
            path=i+'/'
        lista = [obj for obj in listdir(path) if isfile(path + obj)]
        lista_arq.append(lista)
    return(lista_arq)


def verificar(idioma,  termSearch, relation, targets):
    lista_arq=path(idioma, targets, relation)
    ide=sctmid_creator()
    termSearch=termSearch.replace('\ufeff', '')
    termSearch=termSearch.replace('_', ' ')
    termSearch=termSearch.lower()
    n=termSearch
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
    n = normalize( 'NFC', n)
    for carps in lista_arq:
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
                        verificar(idioma, termSearch, relation, targets)
                    else:
                        ide=ide
    return(ide, termSearch)


def get_conceptNet_synonyms(term, lang="es"):
    synonyms = list()
    query_url_pattern = "http://api.conceptnet.io/query?EDGEDIRECTION=/c/LANG/TERM&rel=/r/Synonym&limit=1000"
    edge_directions = {"start":"end", "end":"start"}
    for direction in edge_directions.keys():
        query_url = query_url_pattern.replace("EDGEDIRECTION", direction).replace("LANG", lang).replace("TERM", term)
        obj = requests.get(query_url).json()
        for edge_index in range(len(obj['edges'])):
            syn_lang = obj['edges'][edge_index][edge_directions[direction]]["language"]
            if syn_lang == lang:
                synonyms.append(obj['edges'][edge_index][edge_directions[direction]]["label"])
    return list(set(synonyms))

def inducer(T, A, S):
    semantic_relationship = None
    if len(A) and len(T):
        invalid = False
        if " ".join(A).lower() == " ".join(T).lower():
            pass
        elif len(T) == len(A):
            case_check = list()
            for t in T:
                if t in A:
                    case_check.append(True)
                else:
                    if len(S[t]):
                        if True in [True for s_t in S[t] if s_t in A]:
                            case_check.append(True)
                        else:
                            case_check.append(False)
                    else:
                        invalid = True
            if case_check.count(True) < len(T):
                semantic_relationship = "related"
            if not invalid and False not in case_check: 
                semantic_relationship = "synonymy"
        elif len(T) < len(A):
            case_check = list()
            for t in T:
                if t in A:
                    case_check.append(True)
                else:
                    if len(S[t]):
                        if True in [True for s_t in S[t] if s_t in A]:
                            case_check.append(True)
                        else:
                            case_check.append(False)
                    else:
                        case_check.append(False)

            if False not in case_check:
                semantic_relationship = "narrower"

        elif len(T) > len(A):
            case_check = True
            for a in A:
                syns = list()
                for term_syn in S.values():
                    if len(term_syn):
                        syns = syns + term_syn
                    else:
                        pass

                syns = list(set(syns))
                if len(syns):
                    if not (a in T or True in [True for s_t in syns if a in s_t]):
                        case_check = False
                else:
                    invalid = True

            if not invalid and case_check:
                semantic_relationship = "broader"
        else:
            pass

    return semantic_relationship

def crearRelaciones(relacion, retrieved_wikidata,  A,idioma, scheme, ide, targets):
    skos=relacion
    if(skos in retrieved_wikidata.keys()):
        relat=retrieved_wikidata[skos]
    else:
        retrieved_wikidata[skos]=[]
    cambio=' '.join(A)
    verify=verificar(idioma,  cambio, relacion, targets)
    ideB=verify[0]
    termSearchB=verify[1]
    if(termSearchB!='1'):
        retrieved_wikidata[skos].append(ideB)
        dataEurovoc=fileEurovoc(termSearchB, ideB, cambio, '-', idioma, scheme,skos, ide)
        n=termSearchB.replace(' ', '_').replace('\ufeff','')
        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I
                )
        n = normalize( 'NFC', n)
        newFile=idioma+'/'+relacion+'/'+n+'_'+ideB+'.jsonld'
        with open(newFile, 'w') as file:
            json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
        
    return(retrieved_wikidata)
def dataRetrieverFunction(newFile, idioma, scheme, ide, targets):
    #print("============ Reading the configuration file")
    configuration={
        "source_file_dir": "backup/July16/scterm_dict.csv",
        "gold_concepts_dir": "backup/July16/goldstandard.json",
        "retrieve_wikidata": "backup/July16/scterm_dict.csv",
        "retrieve_ConceptNet": "backup/July16/goldstandard.json",
    }

    
    wikidata_output_file_name =newFile
    source_file=configuration["source_file_dir"]
    terms = [t for t in source_file.split("\n")]
    
    if configuration["retrieve_ConceptNet"]:
        #print("====== Retrieving data from ConceptNet:")
        with open(wikidata_output_file_name, 'r') as f:
            retrieved_wikidata = json.load(f)
        all_inductions = list()
        induced_relationships = list()
        for pref in retrieved_wikidata["prefLabel"]:
            altLabel_induction = dict()
            T=pref["@value"].lower().split()
            lang = pref["@language"]
            S = dict()
            for t in T:
                if t not in S:
                    S[t] = get_conceptNet_synonyms(t, lang)
            if len(S):
                for altLabel in retrieved_wikidata["altLabel"]:
                    A = altLabel["@value"].lower().split()
                    
                    if len(A):
                        T_A_relationship = inducer(T, A, S)
                        altLabel_induction[" ".join(A)] = T_A_relationship
                        
                        if(T_A_relationship=='related'):
                            #print('RELATED', T_A_relationship, A)
                            retrieved_wikidata=crearRelaciones('related',retrieved_wikidata,A,idioma, scheme,ide, targets)
                            retrieved_wikidata["altLabel"].remove(altLabel)

                        elif(T_A_relationship=='narrower'):
                            #print('NARROWE', T_A_relationship, A)
                            retrieved_wikidata=crearRelaciones('narrower',retrieved_wikidata,A,idioma, scheme,ide, targets)
                            retrieved_wikidata["altLabel"].remove(altLabel)
                        elif(T_A_relationship=='broader'):
                            #print('BROADER', T_A_relationship, A)
                            retrieved_wikidata=crearRelaciones('broader ',retrieved_wikidata,A,idioma, scheme,ide, targets)
                            retrieved_wikidata["altLabel"].remove(altLabel)

                        elif(T_A_relationship=='synonymy'):
                            pass
                        
            else:
                # No synonyms found on ConceptNet"
                altLabel_induction = {}
            induced_relationships.append({"T":" ".join(T), "lang": lang, "S": S, "A": altLabel_induction})
            # Not to get timeout from ConceptNet API
            time.sleep(2)
        all_inductions.append(induced_relationships)
        f.close()

        with open(wikidata_output_file_name, 'w') as file:
            json.dump(retrieved_wikidata, file, indent=4,ensure_ascii=False)
    return(retrieved_wikidata)
       

#funcion que introduce todo en un csv 
def all(jsonlist, idioma, targets, context, contextFile,  wsid, scheme, dataRetriever):
    data=json.loads(jsonlist)
    resultado=''
    fin=''
    results=[]
    termSearch=[]
    cont=0
    new=open('iateNO.csv', 'a')
    iatenot = csv.writer(new)

    for i in data:
        results.insert(cont, [])
        termSearch.append(i['request']['query'])
        bloq=0
        if('items' in i.keys()):
            lang=[]
            definicion=[]
            definicion2=[]
            definicion_in=[]
            prefLabel=[]
            synonyms=[]
            lbloq=[]
            iateIde=[]
            eurovoc=''
            euro=[]
            term=i['items']
            ide=sctmid_creator()
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                ide_iate=i['items'][item]['id']
                leng=i['items'][item]['language']
                #barra('Get Iate')
                if(context==None and len(contextFile)<1):
                    context=getContextIate(item, leng, idioma,termSearch[cont] )
                for target in targets:
                    get=getIate(target,item, leng, termSearch[cont])
                    
                    if(target==idioma and get[0]!='' ):
                        definicion_in.append(get[0])

                    lbloq.append(bloq)
                    definicion.append(get[0])
                    definicion2.append(get[0]+':'+str(bloq))
                    prefLabel.append(get[1]+':'+str(bloq))
                    synonyms.append(get[2]+':'+str(bloq))
                    lang.append(target+':'+str(bloq)) 
                    iateIde.append(str(ide_iate)+':'+str(bloq))
                    
                bloq=bloq+1
            d=(definicion_in,[])
            pref=[]
            alt=[]
            defi=[]
            tar=[]
            iate=[]
            if(wsid=='yes'):
                maximo=wsidFunction(termSearch[cont],  context, contextFile,  d)
                #print(maximo[0], maximo[1], maximo[2])
                
                if(maximo[2]!=200):
                    for j in range(len(lbloq)):
                        iateList=iateLists(pref, alt, defi, tar, iate,j, lbloq,prefLabel, synonyms, definicion2, lang, iateIde)
                else:
                    m=definicion.index(maximo[0])
                    b=lbloq[m]
                    for j in range(len(lbloq)):
                        if(str(b) in prefLabel[j][-1:]):
                            iateList=iateLists(pref, alt, defi, tar, iate,j, lbloq,prefLabel, synonyms, definicion2, lang, iateIde)      
            else:
                j=0
                iateList=iateLists(pref, alt, defi, tar, iate,j,lbloq,prefLabel, synonyms, definicion2, lang, iateIde)
            
            relations=['broader', 'narrower', 'related']
            euro=resultsEurovoc(termSearch[cont], idioma, relations, target,  context, contextFile, wsid)
            lexicala=resultsSyns(idioma,termSearch[cont],targets,context, contextFile,wsid)
            fin=fileJson(termSearch[cont], iateList[0], iateList[1], iateList[2],idioma, iateList[3], euro,iateList[4], lexicala, scheme, dataRetriever, targets)
            
            
        else:
            #print('NO ESTA EN IATE',termSearch[cont])
            iatenot.writerow([termSearch[cont], idioma])
            for target in targets:
                lang=[]
                definicion=[]
                definicion2=[]
                definicion_in=[]
                prefLabel=[]
                synonyms=[]
                pref=[]
                alt=[]
                defi=[]
                tar=[]
                lbloq=[]
                iateIde=[]
                iate=[]
                eurovoc=''
                euro=[]
                pref.append(termSearch[cont])
                defi.append('')
                alt.append('|')
                tar.append(idioma)
                iate.append('')

            relations=['broader', 'narrower', 'related']
            euro=resultsEurovoc(termSearch[cont], idioma, relations, target,  context, contextFile, wsid)
            lexicala=resultsSyns(idioma,termSearch[cont],targets,context, contextFile,wsid)
            fin=fileJson(termSearch[cont], pref, alt, defi,idioma, tar, euro,iate, lexicala, scheme, dataRetriever, targets)
            #print(fin)

        cont=cont+1;
    
    return(fin)
def preProcessTerm(term):
    termino=term.strip('‐').strip('—').strip('–').strip(' ').rstrip('\n').rstrip(' ').replace(' – ', ' ').replace('\t', '').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(' ', '_').replace('\ufeff','')
    return(termino)

def barra(var):
    bar2 = ChargingBar('Procesando: '+var, max=100)
    for num in range(100):
        time.sleep(random.uniform(0, 0.02))
        bar2.next()
    bar2.finish()
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
    
    verify=verificar(idioma,termino, '', targets)
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
        #print(data)

    creator='UPM'
    date="March 9 20"
    description="Linked Terminology containing terminological data about Labour Law in Europe."
    keywords=["Labour law", "Work", "Company"]
    
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
            #lista.append(termino)
            jsonlist=haceJson(termSearch, idioma,targets)
            all(jsonlist, idioma, targets,context, contextFile,  wsid,scheme, DR)
        else:
            listaread.append(termino)
    