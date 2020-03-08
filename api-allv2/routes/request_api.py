"""prueba"""
from flask import jsonify, abort, request, Blueprint
from flask import Flask
import requests
from flask_restplus import Resource, Api, fields, reqparse
import json
from random import randint #libreria para random
import re
import os
from os import listdir
from os.path import isfile, isdir


REQUEST_API = Blueprint('term_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/term/<string:termino>,<string:idioma>,<string:targets>,<string:context>', methods=['GET'])
def get(termino, idioma,targets, context):
    targets=targets.split(' ')
    contextlist=''
    if(context):
        context=''
        context=context
    else:
        configuration= {
            "es": "contexts/Spain-judgements-ES.ttl",
            "en": "contexts/UK-judgements-EN.ttl",
            "nl": "contexts/Austria-collectiveagreements-DE.ttl",
            "de": "contexts/Austria-legislation-DE.ttl"
        
        }
        
        es = '%s'%configuration["es"]
        en = '%s'%configuration["en"]
        nl = '%s'%configuration["nl"]
        de = '%s'%configuration["de"]
        encoding = 'utf-8'
        if(idioma=='es'):
            archivo = open(es, "r")
        elif(idioma=='en'):
            archivo = open(en, "r")
        elif(idioma=='de'):
            archivo = open(de, "r")
        elif(idioma=='nl'):
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

        #limpiar=re.compile("<'\'.*?>")
        for i in matriz:
            r=''.join(i[0])
            r2=''.join(i[1])
            #row1 = re.sub(r'<[^>]*?>','', r)
            row1 = r.replace('@es;','')
            #row2 = re.sub(r'<[^>]*?>','', r2)
            row2 = r2.replace('@es;','').replace('\\','').replace('"','')
            if(row1 in row2):
                start=row2.index(row1)
                tam=len(row1)
                end=row2.index(row1)+tam
            contextlist.append([row1,row2[:-1], start, end])
    contextFile=contextlist
    lista=[]
    lista.append([termino+'\n'])
    answer=[]
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    for i in lista[0]:
        if(i[:-1]=='\n'):
            termino=i[:-1]
        else:
            termino=i

        hed = {'Authorization': 'Bearer ' +access}
        jsonList=[]
        data = {"query": termino,
        "source": idioma,
        "targets": targets,
        "search_in_fields": [0],
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
    data=json.loads(jsondump)
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
            eurovoc=[]
            lbloq=[]
            iateIde=[]
            termSearch[cont]
            term=i['items']
            numb = randint(1000000, 9999999)
            ide = "LT" + str(numb)
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                ide_iate=i['items'][item]['id']
                leng=i['items'][item]['language']
                for target in targets:
                    #get=getIate(target,item, leng, termSearch[cont])
                    #def getIate(target, item,leng,termSearch):
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
                    #defi=re.sub(r'<[^>]*?>', '', defi)
                    defi=defi.replace(',', '')
                    #print( defi, pref, joinSyn)
                    if(target==idioma and defi!='' ):
                        definicion_in.append(defi)

                    lbloq.append(bloq)
                    definicion.append(defi)
                    definicion2.append(defi+':'+str(bloq))
                    prefLabel.append(pref+':'+str(bloq))
                    synonyms.append(joinSyn+':'+str(bloq))
                    lang.append(target+':'+str(bloq)) 
                    iateIde.append(str(ide_iate)+':'+str(bloq))
                    #eurovoc 
                bloq=bloq+1
            definitions=(definicion_in,[])
            
            defiMax=''
            idMax=''
            posMax=0
            termIn=termSearch[cont]
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
                        headers ={'accept': 'application/json','X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'}
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
            m=definicion.index(defiMax)
            b=lbloq[m]
            pref=[]
            alt=[]
            defi=[]
            tar=[]
            iate=[]
            euro=[]
            for j in range(len(lbloq)):
                if(str(b) in prefLabel[j][-1:]):
                    pref.append(prefLabel[j][:-2])
                    alt.append(synonyms[j][:-2])
                    defi.append(definicion2[j][:-2])
                    tar.append(lang[j][:-1])
                    iate.append(iateIde[j][:-2])
                    #euro.append(eurovoc[j])
            #lexicala=resultsSyns(idioma,termSearch[cont],targets,context, contextFile)
            #def resultsSyns(idioma,termino,targets,context, contextFile): 

            search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+idioma+"&text="+termIn+"", auth=('987123456', '987123456'))
            answerSearch=search.json()
            results=answerSearch['n_results']
            if(results>0):
                listaDefinition=[]
                listaId=[]
                sense0=answerSearch['results'][0]
                if('senses' in sense0.keys()):
                    sense1=sense0['senses']
                    for i in range(len(sense1)):
                        if('definition' in sense1[i].keys()):
                            id_definitions=sense1[i]['id']
                            definitions=sense1[i]['definition']
                            listaDefinition.append(definitions.replace(',', ''))
                            listaId.append(id_definitions)
                #print(listaDefinition, listaId)
                #maximo=wsid(termino,context, contextFile, definitions)
                defiMax=''
                idMax=''
                posMax=0
                termIn=termSearch[cont]
                if(context and termIn in context):
                    pesos=[]
                    start=context.index(termIn)
                    longTerm=len(termIn)
                    end=context.index(termIn)+longTerm
                    listdef=listaDefinition
                    listIde=listaId
                    definitionsJoin=', '.join(listdef)
                    response = requests.post(
                            'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
                            params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                            headers ={'accept': 'application/json','X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'}
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
                else:
                    pesos=[]
                    start=0
                    longTerm=len(termIn)
                    end=start+longTerm
                    listdef=listaDefinition
                    listIde=listaId
                    definitionsJoin=', '.join(listdef)
                    response = requests.post(
                            'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
                            params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                            headers ={'accept': 'application/json','X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'}
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
                
                joinSyns=''
                textList=''
                if(defiMax!=''):
                    textList=[]
                    sense = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('987123456', '987123456'))
                    jsonTrad=sense.json()
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

                    slp=textList[0].split(',')
                    listaSinonimos=[]
                    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+slp[1]+"&text="+slp[0]+"", auth=('987123456', '987123456'))
                    answerSearch=search.json()
                    results=answerSearch['n_results']
                    if(results>0):
                        if('synonyms' in answerSearch.keys() ):
                            syn=answer['synonyms']
                            if(len(syn)>0):
                                for j in range(len(syn)):
                                    synonym=syn[j]
                                    listaSinonimos.append(synonym)
                    joinSyns=','.join(listaSinonimos)
                    listaSinonimos=[]
                    sense = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('987123456', '987123456'))
                    answerSense=sense.json()
                    if('synonyms' in answerSense.keys() ):
                        syn=answer['synonyms']
                        if(len(syn)>0):
                            for j in range(len(syn)):
                                synonym=syn[j]
                                listaSinonimos.append(synonym)
                    joinSyns=','.join(listaSinonimos)
                    
                else:
                    getsyn=''
                    tradMax=[]
            
            #print(joinSyns, textList)
            #fileJson(termSearch[cont], pref, alt, defi,idioma, tar, euro,iate, lexicala)
            #def fileJson(termSearch, prefLabel, altLabel,definition,idioma,lang, eurovoc,iate, lexicala):
            #print(termSearch, prefLabel, altLabel,definition,idioma,lang)
            termSearch=termIn
            newFile=''
            raiz=os.getcwd()
            carpeta=os.listdir(raiz)
            if(idioma in carpeta):
                print('')
            else:
                os.mkdir(idioma)
            
            #verify=verificar(idioma,termSearch)
            #def verificar(idioma,  termSearch):
            path=idioma+'/'
            lista_arq = [obj for obj in listdir(path) if isfile(path + obj)]
            numb = randint(1000000, 9999999)
            ide = "LT" + str(numb)
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
                        numb = randint(1000000, 9999999)
                        ide = "LT" + str(numb)
                    else:
                        ide=ide

            #print(ide, termSearch)
            if(termSearch!=''):
                data={}
                data={'@context':'','@id': ide, '@type':'skos:Concept', 'skos:inScheme': termSearch, "owl:sameAs":"https://iate.europa.eu/entry/result/"+iate[0],'skos:topConceptOf':ide, 'skos:prefLabel':'' }
                data['@context']={"dcterms": "http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#",  "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "dc":"http://purl.org/dc/elements/1.1/","skos":"http://www.w3.org/2004/02/skos/core#","owl":"http://www.w3.org/2002/07/owl#","skos:broader":{ '@type':'@id'},"skos:inScheme":{ '@type':'@id'},'skos:related':{ '@type':'@id'},'skos:narrower':{ '@type':'@id'},'skos:hasTopConcept':{ '@type':'@id'},'skos:topConceptOf':{ '@type':'@id'}}
                data['skos:prefLabel']=[]
                data['skos:altLabel']=[]
                data['skos:definition']=[]
                '''
                br=eurovoc[0][0][0].split('|')
                na=eurovoc[0][1][0].split('|')
                re=eurovoc[0][2][0].split('|')

                if(br[0]!=''):
                    data['skos:broader']=[]
                if(na[0]!=''):
                    data['skos:narrower']=[]
                if(re[0]!=''):
                    data['skos:related']=[]
                '''
                
                for i in range(len(pref)):
                    if(tar[i][:-1]==idioma):
                        if(pref[i]!=''):
                            data['skos:prefLabel'].append({'@language':tar[i][:-1], '@value':termSearch})
                    else:
                        if(pref[i]!=''):
                            data['skos:prefLabel'].append({'@language':tar[i][:-1], '@value':prefLabel[i]})
                for i in range(len(alt)):
                    if(alt[i]!=''):
                        s_alt=alt[i].split('|')
                        for j in s_alt:
                            if(j != pref[i] and j!=''):
                                data['skos:altLabel'].append({'@language':tar[i][:-1], '@value':j})
                
                data['skos:altLabel'].append({'@language':idioma, '@value':joinSyns})
                
                #print(lexicala[1])
                for i in textList:
                    s_lex=i.split(',')
                    data['skos:altLabel'].append({'@language':s_lex[1], '@value':s_lex[0]})
                    
                for i in range(len(defi)):
                    if(defi[i]!=''):
                        data['skos:definition'].append({'@language':tar[i][:-1], '@value':defi[i]})

                
                newFile=idioma+'/'+termSearch+'_'+ide+'.json'

                #with open(newFile, 'w') as file:
                    #json.dump(data, file, indent=4,ensure_ascii=False)
                #dataRetriever(newFile)
                print(data)
        return jsonify(data),200 

        cont=cont+1;
        
                                        



                  






  


