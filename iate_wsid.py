import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
import os
from os import remove
import collections
from os import listdir
from os.path import isfile, isdir

def leerContextos(lang):
    f=open("readcontexts.json", 'r')
    configuration = json.load(f)
    
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
            start=row2.index(row1)
            tam=len(row1)
            end=row2.index(row1)+tam
        contextlist.append([row1,row2[:-1], start, end])
        #print(row1,row2[:-1], start, end)

        #ex.writerow([row1,row2, start, end])
    return(contextlist)

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

def haceJson(lista, idioma,targets):
    answer=[]
    auth_token=obtenerToken() 
    for i in lista[0]:
        if(i[:-1]=='\n'):
            termino=i[:-1]
        else:
            termino=i

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
    #print(jsondump)
    return(jsondump)




def getIate(target, item,leng,termSearch):
    defi=''
    defi_final=''
    pref=''
    term_val=''
    syn=[]
    joinSyn=''
    contx=''
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
            '''if('context' in language.keys()):
                contxg=language['context']
                for i in range(len(contx)):
                    contx=
                #defi=language['definition']'''
                
    '''
    if('[' in defi):        
        pos1=defi.index('[')
        pos2=defi.index(']')
        defi1=defi[:pos1]
        defi2=defi[pos2+1:]
        defi=defi1+defi2
    
    if('<' in defi):        
        pos1=defi.index('<')
        pos2=defi.index('>')
        defi1=defi[:pos1]
        defi2=defi[pos2+1:]
        defi=defi1+defi2
    '''
    defi=re.sub(r'<[^>]*?>', '', defi)
    defi=defi.replace(',', '')
    
    return( defi, pref, joinSyn)




#funcion que introduce todo en un csv 
def resultsIate(jsonlist, idioma, targets, context, contextFile, lista):
    data=json.loads(jsonlist)
    resultado=''
    results=[]
    termSearch=[]
    cont=0
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
            pref=[]
            alt=[]
            defi=[]
            tar=[]
            lbloq=[]
            iateIde=[]
            iate=[]
            eurovoc=[]
            euro=[]
            termSearch[cont]
            term=i['items']
            ide=sctmid_creator()
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                ide_iate=i['items'][item]['id']
                leng=i['items'][item]['language']
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
                    relations=['broader', 'narrower', 'related']
                    eurovoc.append(resultsEurovoc(termSearch[cont], idioma, relations, target))
                    #print(eurovoc)
                bloq=bloq+1
            d=(definicion_in,[])
            if(context):
                maximo=wsid(termSearch[cont],  context, contextFile,  d)
            elif(contextFile):
                file=open(contextFile+'.csv', 'r')
                contextFile=csv.reader(file)
                maximo=wsid(termSearch[cont],  context, contextFile,  d)
            else:
                contextFile=leerContextos(idioma)
                maximo=wsid(termSearch[cont],  context, contextFile,  d)
            print(maximo)
            m=definicion.index(maximo[0])
            b=lbloq[m]
            for j in range(len(lbloq)):
                if(str(b) in prefLabel[j][-1:]):
                    pref.append(prefLabel[j][:-2])
                    alt.append(synonyms[j][:-2])
                    defi.append(definicion2[j][:-2])
                    tar.append(lang[j][:-1])
                    iate.append(iateIde[j][:-2])
                    euro.append(eurovoc[j])
            
            lexicala=resultsSyns(idioma,termSearch[cont],targets,context, contextFile)
            fileJson(termSearch[cont], pref, alt, defi,idioma, tar, euro,iate, lexicala)
            
            
        cont=cont+1;
    return(resultado)

def wsid(termIn, context, contextFile,  definitions):
    #print('-----',termIn, context, contextFile,  definitions)
    defiMax=''
    idMax=''
    posMax=0
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
        print(response.status_code)
        if(response.status_code==200):
            pesos=response.json()
        else:
            pesos=[]
        if(len(pesos)>0 and len(listdef)>0):
            max_item = max(pesos, key=int)
            posMax=pesos.index(max_item)
            defiMax=listdef[posMax]
            idMax=listIde[posMax]
        else:
            defiMax=''
            idMax=''
    
    elif(contextFile):
        for i in contextFile:
            contextTerm=i[0]
            if(termIn in contextTerm):
                context=i[1]
                pesos=[]
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
                print(response.status_code)
                if(response.status_code==200):
                    pesos=response.json()
                else:
                    pesos=[]
                if(len(pesos)>0 and len(listdef)>0):
                    max_item = max(pesos, key=int)
                    posMax=pesos.index(max_item)
                    defiMax=listdef[posMax]
                    if(len(listIde)>0):
                        idMax=listIde[posMax]
                    else:
                        idMax=''
                else:
                    defiMax=''
                    idMax=''
                break
            else:
                defiMax=''
                idMax=''

    #print(defiMax, idMax)       
    return(defiMax, idMax)

def fileJson(termSearch, prefLabel, altLabel,definition,idioma,lang, eurovoc,iate, lexicala):
    #print(termSearch, prefLabel, altLabel,definition,idioma,lang)
    raiz=os.getcwd()
    carpeta=os.listdir(raiz)
    if(idioma in carpeta):
        print('')
    else:
        os.mkdir(idioma)
    
    ide=sctmid_creator()
    verify=verificar(idioma, ide, termSearch)
    ide=verify[0]
    termSearch=verify[1]
    if(termSearch!=''):
        data={}
        data={'@context':'','@id': ide, '@type':'skos:Concept', 'skos:inScheme': termSearch, "owl:sameAs":"https://iate.europa.eu/entry/result/"+iate[0],'skos:topConceptOf':ide, 'skos:prefLabel':'' }
        data['@context']={"dcterms": "http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#",  "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc":"http://purl.org/dc/elements/1.1/","skos":"http://www.w3.org/2004/02/skos/core#","owl":"http://www.w3.org/2002/07/owl#","skos:broader":{ '@type':'@id'},"skos:inScheme":{ '@type':'@id'},'skos:related':{ '@type':'@id'},'skos:narrower':{ '@type':'@id'},'skos:hasTopConcept':{ '@type':'@id'},'skos:topConceptOf':{ '@type':'@id'}}
        data['skos:prefLabel']=[]
        data['skos:altLabel']=[]
        data['skos:definition']=[]
        
        br=eurovoc[0][0][0].split('|')
        na=eurovoc[0][1][0].split('|')
        re=eurovoc[0][2][0].split('|')

        if(br[0]!=''):
            data['skos:broader']=[]
        if(na[0]!=''):
            data['skos:narrower']=[]
        if(re[0]!=''):
            data['skos:related']=[]
        
        for i in range(len(prefLabel)):
            if(lang[i][:-1]==idioma):
                if(prefLabel[i]!=''):
                    data['skos:prefLabel'].append({'@language':lang[i][:-1], '@value':termSearch})
            else:
                if(prefLabel[i]!=''):
                    data['skos:prefLabel'].append({'@language':lang[i][:-1], '@value':prefLabel[i]})
        for i in range(len(altLabel)):
            if(altLabel[i]!=''):
                s_alt=altLabel[i].split('|')
                for j in s_alt:
                    if(j != prefLabel[i] and j!=''):
                        data['skos:altLabel'].append({'@language':lang[i][:-1], '@value':j})
        
        data['skos:altLabel'].append({'@language':idioma, '@value':lexicala[0]})
        
        #print(lexicala[1])
        for i in lexicala[1]:
            s_lex=i.split(',')
            data['skos:altLabel'].append({'@language':s_lex[1], '@value':s_lex[0]})
        
        for i in range(len(definition)):
            if(definition[i]!=''):
                data['skos:definition'].append({'@language':lang[i][:-1], '@value':definition[i]})

        
        for i in eurovoc:
            broader=i[0]
            for i in range(len(broader)):
                slrp=broader[i].split('|')
                if(slrp[0]!=''):
                    ide_broader=sctmid_creator()
                    verify=verificar(idioma, ide_broader, slrp[0])
                    ideB=verify[0]
                    termSearchB=verify[1]
                    data['skos:broader'].append(ide_broader)
                    dataEurovoc=fileEurovoc(termSearchB, ideB, slrp[0], slrp[1], idioma)
                    carpetas=os.listdir(idioma)
                    if('broader' in carpetas):
                        with open(idioma+'/'+'broader/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                            json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    else:
                        os.makedirs(idioma+"/broader")
                    with open(idioma+'/'+'broader/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                        json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    #print(termSearchB)
                     
        for i in eurovoc:
            narrower=i[1]
            for i in range(len(narrower)):
                slrp=narrower[i].split('|')
                if(slrp[0]!=''):
                    ide_narrower=sctmid_creator()
                    verify=verificar(idioma, ide_narrower, slrp[0])
                    ideB=verify[0]
                    termSearchB=verify[1]
                    data['skos:narrower'].append(ide_narrower)
                    dataEurovoc=fileEurovoc(termSearchB, ideB, slrp[0], slrp[1], idioma)
                    carpetas=os.listdir(idioma)
                    if('narrower' in carpetas):
                        with open(idioma+'/'+'narrower/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                            json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    else:
                        os.makedirs(idioma+"/narrower")
                    with open(idioma+'/'+'narrower/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                        json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    #print(termSearchB)
           
        for i in eurovoc:
            related=i[2]
            for i in range(len(related)):
                slrp=related[i].split('|')
                if(slrp[0]!=''):
                    ide_related=sctmid_creator()
                    verify=verificar(idioma, ide_related, slrp[0])
                    ideB=verify[0]
                    termSearchB=verify[1]
                    data['skos:related'].append(ide_related)
                    dataEurovoc=fileEurovoc(termSearchB, ideB, slrp[0], slrp[1], idioma)
                    carpetas=os.listdir(idioma)
                    if('related' in carpetas):
                        with open(idioma+'/'+'related/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                            json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    else:
                        os.makedirs(idioma+"/related")
                    with open(idioma+'/'+'related/'+termSearchB+'_'+ideB+'.json', 'w') as file:
                        json.dump(dataEurovoc, file, indent=4,ensure_ascii=False)
                    #print(termSearchB)
        
        with open(idioma+'/'+termSearch+'_'+ide+'.json', 'w') as file:
            json.dump(data, file, indent=4,ensure_ascii=False)
        
def fileEurovoc(termSearch, ide, relation, iduri, idioma):
    #print(relation[0])
    data={}
    data={'@context':'','@id': ide, '@type':'skos:Concept', 'skos:inScheme': termSearch, 'skos:topConceptOf':ide,"owl:sameAs":iduri, 'skos:prefLabel':'' }
    data['@context']={"dcterms": "http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#",  "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc":"http://purl.org/dc/elements/1.1/","skos":"http://www.w3.org/2004/02/skos/core#","owl":"http://www.w3.org/2002/07/owl#","skos:broader":{ '@type':'@id'},"skos:inScheme":{ '@type':'@id'},'skos:related':{ '@type':'@id'},'skos:narrower':{ '@type':'@id'},'skos:hasTopConcept':{ '@type':'@id'},'skos:topConceptOf':{ '@type':'@id'}}
    data['skos:prefLabel']=[]
    if(relation!=''):
        data['skos:prefLabel'].append({'@language':idioma, '@value':relation})
    return(data)

def verificar(idioma, ide, termSearch):
    path=idioma+'/'
    lista_arq = [obj for obj in listdir(path) if isfile(path + obj)]
    
    for i in lista_arq:
        slp=i.split('_')
        idefile=slp[1]
        termfile=slp[0]
        
        if(termSearch in termfile):
            print('ya existe termino', termfile)
            termSearch=''
        else:
            termSearch=termSearch
            if(ide in idefile):
                print('ya existe ide del termino', termfile)
                ide=sctmid_creator()
                verificar(idioma, ide)
            else:
                ide=ide

    return(ide, termSearch)


def resultsEurovoc(termino, idioma, relations, target):
    #print(termino, target)
    results=[]
    results2=[]
    resultado=''
    relation=''
    for relation in relations:
        uriTermino=getUriTerm(termino, target)
        uriRelation=getRelation(uriTermino, relation) 
        name=getName(uriRelation, target)
        results.append([name+'|'+uriRelation])
    #print(results)
    return(results)

#1. funcion que obtiene la uri de cada termino
def getUriTerm(termino,lenguaje):
    termino2='"'+termino+'"'
    lenguaje2='"'+lenguaje+'"'
    resultado=''
    resultadouri=''
    url = ("http://publications.europa.eu/webapi/rdf/sparql")
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    select ?c ?label
    from <http://eurovoc.europa.eu/100141>
    where
    {
    VALUES ?searchTerm { """+termino2+""" }
    VALUES ?searchLang { """+lenguaje2+""" }
    VALUES ?relation {skos:prefLabel}
    ?c a skos:Concept .
    ?c ?relation ?label .
    filter (regex(?label, "(^)"""+termino+"""($)"))
    }
    """
    r=requests.get(url, params={'format': 'json', 'query': query})
    results=json.loads(r.text)
    
    if (len(results["results"]["bindings"])==0):
        resultadouri=''
    else:
        for result in results["results"]["bindings"]:
            resultadouri=result["c"]["value"]
            resultadol=result["label"]["value"]
    return(resultadouri)

#2. funcion que recibe la uri del termino al que sele desea saber su BROADER, obtiene la uri del BROADER 
def getRelation(uri_termino, relacion):
    resultado=''
    url=("http://publications.europa.eu/webapi/rdf/sparql")
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        select ?c ?label         
        from <http://eurovoc.europa.eu/100141>        
        where       
        {      
        VALUES ?c {<"""+uri_termino+"""> }
        VALUES ?relation { skos:"""+relacion+""" } # skos:broader
        ?c a skos:Concept .
        ?c ?relation ?label .
        }
 
 
    """
    r=requests.get(url, params={'format': 'json', 'query': query})
    results=json.loads(r.text)
    if (len(results["results"]["bindings"])==0):
            resultado=''
    else:
        for result in results["results"]["bindings"]:
            resultado=result["label"]["value"]
        
    return(resultado)


#3. funcion que recibe la uri del broader y consulta cual es el termino correspondiente
def getName(uri_broader,lenguaje):
    resultado=''
    lenguaje2='"'+lenguaje+'"'
    url=("http://publications.europa.eu/webapi/rdf/sparql")
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
        select ?c ?label 
        from <http://eurovoc.europa.eu/100141> 
        where 
        {
        VALUES ?c { <"""+uri_broader+"""> }
        VALUES ?searchLang { """+lenguaje2+""" undef } 
        VALUES ?relation { skos:prefLabel  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        """
    r=requests.get(url, params={'format': 'json', 'query': query})
    results=json.loads(r.text)
    if (len(results["results"]["bindings"])==0):
            resultado=''
    else:
        for result in results["results"]["bindings"]:
            resultado=result["label"]["value"]
           
    return(resultado)

def lexicalaSearch(languageIn, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+term+"", auth=('987123456', '987123456'))
    answerSearch=search.json()
    return(answerSearch)

def lexicalaSense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('987123456', '987123456'))
    answerSense=sense.json()
    return(answerSense)

def resultsSyns(idioma,termino,targets,context, contextFile): 
    
    if(termino):
        answer=lexicalaSearch(idioma, termino)
        results=answer['n_results']
        if(results>0):
            definitions=definitionGet(answer)
            #print(termino,context, contextFile, definitions)
            maximo=wsid(termino,context, contextFile, definitions)
            if(maximo[1]!=''):
                tradMax=traductionGet(maximo, targets)
                synsTrad=justSyn(tradMax)
                getsyn=synonymsGet(maximo)
            else:
                getsyn=''
                tradMax=[]
            #print(termino, maximo[0], maximo[1], getsyn, tradMax, synsTrad)
    return(getsyn, tradMax)

def justSyn(tradMax):
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
    print('jsonTrad',jsonTrad)
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


parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search")
parser.add_argument("--lang", help="Source language")
parser.add_argument("--targets", help="Source language out")
parser.add_argument("--context", help="Contexto")
parser.add_argument("--contextFile", help="Archivo de contextos")
#parser.add_argument("apiName", help="Name of the api: 'iate', 'eurovoc' or 'syns'") 
args=parser.parse_args()

#nameapi=args.apiName
#if(nameapi=='iate'):
termino=args.sourceTerm
listTerm=args.sourceFile
idioma=args.lang
targets=args.targets.split(' ')
context=args.context
contextFile=args.contextFile
if(termino):
    lista=[]
    lista.append([termino+'\n'])
    jsonlist=haceJson(lista, idioma,targets)
    resultsIate( jsonlist, idioma, targets,context, contextFile, lista)
    
else:
    lista=[]
    file=open(listTerm+'.csv', 'r')
    read=file.readlines()
    lista.append(read)
    jsonlist=haceJson(lista, idioma,targets)
    resultsIate( jsonlist, idioma, targets,context, contextFile, lista)

#FILE
#python3 iate_wsid.py --sourceFile term_es --lang es --targets "es en de nl" --contextFile contextos_salida iate
#term_es = nombre de mi archivo sin extension [solo lee archivos .csv], contextos_salida es el archivo de mis contextos en español [solo lee archivos .csv, con el formato que esta este]
#TERM
#python3 iate_wsid.py --sourceTerm término --lang es --targets "es en de nl" --contextFile contextos_salida iate

