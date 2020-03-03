import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from os import remove
import collections


#funcion para obtener identificadores
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID

#funcion para crear archivo termino-id
def term_id_file(listTerm, termino, nameFile, tipo ):
    ide=''
    listaTerminoId=[]
    if(tipo=='w'):
        fileNew=open(nameFile+'.csv', 'w')
        readerNew=csv.writer(fileNew)
        if(termino):
            ide=sctmid_creator()
            listaTerminoId.append([termino,ide])
            readerNew.writerow([termino,ide])
        
        else:
            file=open(listTerm+'.csv', 'r')
            reader=csv.reader(file)
            for i in reader: 
                termino=i[0]
                ide=sctmid_creator()
                listaTerminoId.append([termino,ide])
                readerNew.writerow([termino,ide])
    else:
        fileNew=open(nameFile+'.csv', 'a')
        readerNew=csv.writer(fileNew)
        if(termino):
            listaTerminoId=comprobarTermino(termino, nameFile,listaTerminoId)
        
        else:
            file=open(listTerm+'.csv', 'r')
            reader=file.readlines()
            for i in reader: 
                split=i.split(',')
                termino=split[0]
                if('\n' in termino):
                    termino=termino[:-1]
                else:
                    termino=termino
                listaTerminoId=comprobarTermino(termino, nameFile,listaTerminoId)
                

    return(listaTerminoId)

#funcion para comprobar si el termino ya existe en la lista
def comprobarTermino(termino, termId, listaTerminoId):
    ide=''
    nuevotermino=''
    listaTermino=[]
    listaIde=[]
    File=open(termId+'.csv', 'r')
    reader=csv.reader(File)
    File2=open(termId+'.csv', 'a')
    reader2=csv.writer(File2)
    for row in reader:
        termFile=row[0]
        ideFile=row[1]
        listaTermino.append(termFile)
        listaIde.append(ideFile)
    #print(listaTermino)

    if(termino in listaTermino):
        pos=listaTermino.index(termino)
        listaTerminoId.append([termino,listaIde[pos]])
    else:
        #print('es nuevo termino')
        ide=sctmid_creator()
        cide=comprobarIDE(ide, termId)
        listaTerminoId.append([termino,ide])
        reader2.writerow([termino,cide])

    return(listaTerminoId)



def comprobarIDE(ide, termId):
    listaIds=[]
    nuevoide=''
    File=open(termId+'.csv', 'r')
    reader=csv.reader(File)
    for row in reader:
        ideFile=row[1]
        if(ide==ideFile):
            ide=sctmid_creator()
            nuevoide=comprobarIDE(ide, termId)
            #print('ya existe ide', cide)
        else:
            nuevoide=ide

    return(nuevoide)

def archivos_eurovoc(lista, fileEurovoc,idioma, targets):
    broader=open(fileEurovoc+'_br.csv', 'w')
    #broader=csv.writer(b)
    narrower=open(fileEurovoc+'_na.csv', 'w')
    #narrower=csv.writer(n)
    related=open(fileEurovoc+'_re.csv', 'w')
    #related=csv.writer(r)

    cabeceras=[]
    cabeceras2=[]
    cabeceras3=[]
    targets2=[]
    cabeceras.insert(0, [])
    cabeceras[0].insert(0,'prefLabel@'+idioma)
    cabeceras[0].insert(1,'term_id')
    cabeceras[0].insert(2,'broader_uri')
    cabeceras[0].insert(3,'broader_id')

    cabeceras2.insert(0, [])
    cabeceras2[0].insert(0,'prefLabel@'+idioma)
    cabeceras2[0].insert(1,'term_id')
    cabeceras2[0].insert(2,'narrower_uri')
    cabeceras2[0].insert(3,'narrower_id')

    cabeceras3.insert(0, [])
    cabeceras3[0].insert(0,'prefLabel@'+idioma)
    cabeceras3[0].insert(1,'term_id')
    cabeceras3[0].insert(2,'related_uri')
    cabeceras3[0].insert(3,'related_id')
    targets2=targets[::-1]
    c=3
    for target in range(len(targets)):
        c=c+1
        cabeceras[0].insert(target+c, 'brprefLabel@'+targets[target])
        cabeceras2[0].insert(target+c, 'naprefLabel@'+targets[target])
        cabeceras3[0].insert(target+c, 'reprefLabel@'+targets[target])
    c2=0
    while(c2<=(len(cabeceras[0])-1)):
        broader.write(cabeceras[0][c2]+',')
        narrower.write(cabeceras2[0][c2]+',')
        related.write(cabeceras3[0][c2]+',')
        c2=c2+1

    for i in lista:
        termino=i[0]
        ide=i[1]
        broader.write('\n'+termino+', '+ide+',')
        narrower.write('\n'+termino+', '+ide+',')
        related.write('\n'+termino+', '+ide+',')

    
#funcion para obtener el baren token (access token)
def obtenerToken(): 
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)

def haceJson(lista, idioma,targets):
    answer=[]
    auth_token=obtenerToken() 
    for i in lista:
        termino=i[0]
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
             "filter_by_domains": [
        "86817304A07344BC8B544B390129ADDF",
        "5B8AB13A1DA9412F8EE914DD40D469E1",
        "70C8DCD591A145A69CBFAC9405AB90E1",
        "1C9C154AD10E4515B60A5AEEB1A04B7C",
        "7593C35C03034FBA9737E2A7EEADDD6A",
        "78481530C8D346EFBC4CE34FBD730476",
        "698DCDA39DF14751BB4E2449B7274C3D",
        "0460ABF0F73B4799BCD7DC5287D810B0",
        "4FEA3CDDFE3B4DD188D9A6E23004B136",
        "0B52BF975B664CD5997CE4DB99EA67D1",
        "1C2BB68922D84C1AB0B6B362EBA5100A",
        "08A084532207495CB9276FE30188048C",
        "DFFE1B0A73624006888F21D57085832A",
        "D8811DC89580413D8B7B2BD77AD18F10",
        "F93ED12A90064881879E66EEA9987598"

            ],
            "query_operator": 1
        }
        url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
        response = requests.get(url, json=data, headers=hed)
        reponse2=response.json()
        js=json.dumps(reponse2)
        answer.append(reponse2)
    jsondump=json.dumps(answer)#se guarda todo en un archivo json
    #hacejsonList.append(jsondump)
    #print(jsondump)
    return(jsondump)




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
                    #print(target,termSearch,len(term_entries))
                    pref=language['term_entries'][0]['term_value']
                    for t in range(len(term_entries)):
                        term_val=language['term_entries'][t]['term_value']
                        if(termSearch is not term_val):
                            syn.append(term_val)
                    syn=syn[0:len(term_entries)]
                    joinSyn='| '.join(syn)
            if('definition' in language.keys()):
                defi=language['definition']

    return( defi, pref, joinSyn)




#funcion que introduce todo en un csv 
def resultsIate(jsonlist, idioma, targets, out,lista):
    data=json.loads(jsonlist)
    resultado=''
    re
    results=[]
    cont=0
    cid=0
    for i in data:
        results.insert(cont, [])
        termSearch=i['request']['query']
        
        if('items' in i.keys()):
            term=i['items']
            termL=lista[cont]
            ide=termL[1]
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                ide_iate=i['items'][item]['id']
                leng=i['items'][item]['language']
                for target in targets:
                    get=getIate(target,item, leng, termSearch)
                    definicion=get[0]
                    prefLabel=get[1]
                    synonyms=get[2]
                    resultado=matrizIate(results,definicion, prefLabel, synonyms, cont, target,ide,termSearch,idioma)        
        else:
            termL=lista[cont]
            ide=termL[1]
            for target in targets:
                definicion=''
                prefLabel=''
                synonyms=''
                resultado=matrizIate(results,definicion, prefLabel, synonyms, cont, target,ide,termSearch,idioma)        
        
        cont=cont+1;
    #print(resultado)
    save=saveFile(resultado, cont, idioma, targets,out)
      
    return(resultado)


def matrizIate(results,definicion, prefLabel, synonyms, cont, target,ide,termSearch,idioma):
    #print(termSearch)
    results[cont].insert(0, ide)#ide
    if(idioma in target):
        results[cont].insert(1, termSearch)#pref
    else:
        results[cont].insert(1, prefLabel)#pref
    results[cont].insert(2, synonyms)#alt/synonyms
    results[cont].insert(3, definicion)#def
    results[cont].insert(4, target)#def
    return(results)

def saveFile(resultado,cont, idioma,targets,out):
    cabeceras=[]
    targets2=[]
    filenew=open(out+'.csv', 'w')
    cabeceras.insert(0, [])
    cabeceras[0].insert(0,'term_id')
    cabeceras[0].insert(1,'prefLabel@'+idioma)
    cabeceras[0].insert(2,'altLabel@'+idioma)
    cabeceras[0].insert(3,'definition@'+idioma)
    targets2=targets[::-1]
    t=len(targets)-1
    c=3
    for target in range(len(targets)):
        if(idioma != targets[target] ):
            c=c+1
            cabeceras[0].insert(target+c, 'prefLabel@'+targets[target])
            c=c+1
            cabeceras[0].insert(target+c, 'altLabel@'+targets[target])
            c=c+1
            cabeceras[0].insert(target+c, 'definition@'+targets[target])
    
    c2=0
    while(c2<=(len(cabeceras[0])-1)):
        filenew.write(cabeceras[0][c2]+',')
        c2=c2+1
    filenew.write('\n')
    body=[]
    renglon=0
    for row in range(len(resultado)):
        filaP=4
        filaA=5
        filaD=6
        total=1
        colum2=len(resultado[row])-1
        #print('-----------------------------', colum2)
        while( total<= (len(resultado[row]))  ):
            filaT=4
            filaP=4
            filaA=5
            filaD=6
            body.insert(renglon, [])
            body[renglon].insert(0,resultado[row][0])
            #print('---', total, renglon)
            while(filaT<=len(targets)*3):
                #print('2 while', filaT, filaP)
                if(idioma==resultado[row][colum2]):
                    body[renglon].insert(1,resultado[row][colum2-3])
                    body[renglon].insert(2,resultado[row][colum2-2])
                    body[renglon].insert(3,resultado[row][colum2-1])

                else:
                    body[renglon].insert(filaP,resultado[row][colum2-3])
                    body[renglon].insert(filaA,resultado[row][colum2-2])
                    body[renglon].insert(filaD,resultado[row][colum2-1])
                    filaP=filaP+3
                    filaT=filaT+3
                    filaA=filaA+3
                    filaD=filaD+3
                
                colum2=colum2-5
                total=total+5
            renglon=renglon+1
    #print(body)
    filenew.close()
    filenew=open(out+'.csv', 'a')
    readernew=csv.writer(filenew)
    if(len(resultado)==1):
        for i in range(len(body)):
            print(body[i])
    else:
        for i in range(len(body)):
            readernew.writerow(body[i])
            

def resultsEurovoc(listTerm,termino, idioma, relation,targets):
    results=[]
    results2=[]
    resultado=''
    if(termino):
        for target in targets:
        	uriTermino=getUriTerm(termino, target)
        	uriRelation=getRelation(uriTermino, relation) 
        	name=getName(uriRelation, target)
        	print(relation,': ',name)
    elif(listTerm):
        file=open(listTerm+'.csv', 'r')
        reader=csv.reader(file)
        cont=0
        for i in reader: 
            results.insert(cont, [])
            results2.insert(cont, [])
            termino=i[0]
            termid=i[1]
            for target in targets:
                uriTermino=getUriTerm(termino, target)
                uriRelation=getRelation(uriTermino, relation) 
                name=getName(uriRelation, target)
                resultado=asignID(results,termino, termid, uriTermino, uriRelation,name, listTerm, relation,cont,target)
        #print(cont,resultado)
        outFile(resultado,cont,listTerm,idioma,targets,results2,file)

def outFile(resultado,cont,listTerm,idioma,targets,results2,file):
    
    resultado2=[]
    resultado2=resultado[::-1]
    #print(resultado2)
    file.close()
        
    cabeceras=[]
    targets2=[]
    filenew=open(listTerm+'.csv', 'w')
    readernew=csv.writer(filenew) 
    cabeceras.insert(0, [])
    cabeceras[0].insert(0,'prefLabel@'+idioma)
    cabeceras[0].insert(1,'term_id')
    cabeceras[0].insert(2,relation+'_uri')
    cabeceras[0].insert(3,relation+'_id')
    targets2=targets[::-1]
    for target in range(len(targets)):
        cabeceras[0].insert(target+4, relation[:2]+'prefLabel@'+targets[target])
    c2=0
    while(c2<=(len(cabeceras[0])-1)):
        filenew.write(cabeceras[0][c2]+',')
        c2=c2+1
    filenew.write('\n')
    
    #print(resultado2)
    body=[]
    adecuado=(len(resultado2[0])/len(targets))-1
    resultado2=resultado2[1:]
    for row in range(len(resultado2)):
        colum=3
        colum2=4
        body.insert(row, [])
        body[row].insert(0,resultado2[row][0])
        body[row].insert(1,resultado2[row][1])
        body[row].insert(2,resultado2[row][2])
        body[row].insert(3,resultado2[row][3])
        while(colum2<=len(resultado2[row])):
            body[row].insert(colum+1, resultado2[row][colum2])
            colum2=colum2+5
    filenew.close()
    #print(body)
    filenew=open(listTerm+'.csv', 'a')
    readernew=csv.writer(filenew)
    
    for i in range(len(body)):
        readernew.writerow(body[i])
    
      
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

def asignID(results,termino, termid, uriTermino, uriRelation,name, listTerm, relation, cont,target):
    #print(name)
    results[cont].insert(0, termino)
    results[cont].insert(1, termid)
    results[cont].insert(2, uriTermino)
    if(uriTermino!=''):
        if(uriTermino in results):
            uri=results[cont][3]
        else:
            results[cont].insert(3, sctmid_creator()) 
    else:
        results[cont].insert(3, '') 
    results[cont].insert(4, name)
    return(results)

def lexicalaSearch(languageIn, term):
	search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+term+"", auth=('987123456', '987123456'))
	answerSearch=search.json()
	return(answerSearch)

def lexicalaSense(maximo):
	sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('987123456', '987123456'))
	answerSense=sense.json()
	return(answerSense)

def resultsSyns(idioma,listTerm,termino,targets,context, contextFile,out): 
    
    filenew=open(out+'.csv', 'w')
    readernew=csv.writer(filenew)
    if(termino):
        answer=lexicalaSearch(idioma, termino)
        results=answer['n_results']
        if(results>0):
            definitions=definitionGet(answer)
            maximo=wsid(termino,context, contextFile, definitions)
            tradMax=traductionGet(maximo, targets)
            synsTrad=justSyn(tradMax)
            getsyn=synonymsGet(maximo)
            print(termino, maximo[0], maximo[1], getsyn, tradMax, synsTrad)
            readernew.writerow([termino, maximo[0], maximo[1], getsyn,tradMax, synsTrad])
    else:
        file=open(listTerm+'.csv', 'r')
        reader=csv.reader(file)
        for i in reader: 
            termino=i[0]
            answer=lexicalaSearch(idioma, termino)
            results=answer['n_results']
            listaSinonimos=[]
            if(results>0):
                definitions=definitionGet(answer)
                maximo=wsid(termino,context,contextFile, definitions)
                if(maximo[0]!=''):
                    tradMax=traductionGet(maximo, targets)
                    synsTrad=justSyn(tradMax)
                    getsyn=synonymsGet(maximo)
                    print(termino, maximo, getsyn)
                    readernew.writerow([termino, maximo[0], maximo[1], getsyn,tradMax,synsTrad])
                else:
                    readernew.writerow([termino, '', '', getsyn,tradMax,synsTrad])
                #    print('Archivo de contexto en otro lenguaje')
    #fileout(termIn, maximo, getsyn)

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

def wsid(termIn, context, contextFile,  definitions):
    defiMax=''
    idMax=''
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
        if(response.json()):
            pesos=response.json()
        else:
            pesos=[]
        if(len(pesos)>0):
            max_item = max(pesos, key=int)
            posMax=pesos.index(max_item)
            defiMax=listdef[posMax]
            idMax=listIde[posMax]
        else:
            defiMax=''
            idMax=''
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        reader=csv.reader(file)
        for i in reader:
            contextTerm=i[0]
            if(termIn in contextTerm):
                context=i[1]
                pesos=[]
                start=i[2]
                end=i[3]
                listdef=definitions[0]
                listIde=definitions[1]
                definitionsJoin=', '.join(listdef)
                #print(termIn, contextTerm, context, start, end, definitionsJoin)
                response = requests.post(
                                'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
                                params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                                headers ={'accept': 'application/json',
                                        'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
                                        }
                                )
                if(response.json()):
                    pesos=response.json()
                else:
                    pesos=[]
                if(len(pesos)>0):
                    max_item = max(pesos, key=int)
                    posMax=pesos.index(max_item)
                    defiMax=listdef[posMax]
                    idMax=listIde[posMax]
                else:
                    defiMax=''
                    idMax=''
    return(defiMax, idMax)


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



parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search") #nombre de archivo a leer
parser.add_argument("--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms") #tipo de archivo lectura o escritura (w/a)
parser.add_argument("--termId", help="Name of the termino_id file, to save terms and ids") #nombre de archivo termino-id
parser.add_argument("--targetFile", help="Name of the target file")
parser.add_argument("--euroSource", help="Name of the eurovoc source file without extension")
parser.add_argument("--lang", help="Source language")
parser.add_argument("--targets", help="Source language out")
parser.add_argument("--relation", help="Name of the relation") 
parser.add_argument("--context", help="Contexto")
parser.add_argument("--contextFile", help="Archivo de contextos")
parser.add_argument("apiName", help="Name of the api: 'iate', 'eurovoc' or 'syns'") 
args=parser.parse_args()

nameapi=args.apiName
if(nameapi=='iate'):
    typeFile=args.type
    if(typeFile=='new'):
        tipo='w'
    else:
        tipo='a'
    termino=args.sourceTerm
    listTerm=args.sourceFile
    termId=args.termId
    idioma=args.lang
    targets=args.targets.split(' ')
    fileEurovoc=args.euroSource
    out=args.targetFile
    lista=term_id_file(listTerm, termino, termId, tipo)
    #print(lista)
    if(fileEurovoc):
        archivos_eurovoc(lista, fileEurovoc,idioma,targets)
    jsonlist=haceJson(lista, idioma,targets)
    resultado=resultsIate( jsonlist, idioma, targets, out,lista)
elif(nameapi=='eurovoc'):
    termino=args.sourceTerm
    listTerm=args.sourceFile
    idioma=args.lang
    targets=args.targets.split(' ')
    relation=args.relation
    resultsEurovoc(listTerm,termino, idioma, relation,targets)
elif(nameapi=='syns'):
    listTerm=args.sourceFile
    termino=args.sourceTerm
    idioma=args.lang
    targets=args.targets.split(' ')
    context=args.context
    contextFile=args.contextFile
    out=args.targetFile
    resultsSyns(idioma,listTerm,termino,targets,context, contextFile,out)
elif(nameapi=='all'):
	termino=args.sourceTerm
	idioma=args.lang
	targets=args.targets.split(' ')
	context=[['pactada','1. La duración de la jornada de trabajo será la pactada en los convenios colectivos o contratos de trabajo.','48','55']
['duración','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','3','11']
['descanso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','72','80']
['preaviso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','156','164']
['acuerdo','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','53','60']
['semanales','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','77','86']
['límite','cuál es el límite de la jornada laboral','11','17']
['trabajador','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','123','133']
['convenio','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','12','20']
['manera','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','252','258']
['jornada','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','172','179']
['hora','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','198','202']
['prestación','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','209','219']
['defecto','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','40','47']
['trabajo','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','223','230']
['ley','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','114','117']
['empresa','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','70','77']
['caso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','43','47']
['promedio','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','110','118']
['días','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','181','185']
['cómputo','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','122','129']
['Sección','Sección 5. Tiempo de trabajo','0','7']
['semanal','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','90','97']
['conjunto','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','142','150']
['cuantía','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','84','91']
['Salario','Artículo 27. Salario mínimo interprofesional.','13','20']
['productividad','b) La productividad media nacional alcanzada.','6','19']
['participación','c) El incremento de la participación del trabajo en la renta nacional.','23','36']
['renta','c) El incremento de la participación del trabajo en la renta nacional.','55','60']
['salario','2. El salario mínimo interprofesional en su cuantía es inembargable.','6','13']
['incremento','c) El incremento de la participación del trabajo en la renta nacional.','6','16']
['coyuntura','d) La coyuntura económica general.','6','15']
['Gobierno','1. El Gobierno fijará previa consulta con las organizaciones sindicales y asociaciones empresariales más representativas anualmente el salario mínimo interprofesional teniendo en cuenta:','6','14']
['estructura','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','65','75']
['trabajo','c) El incremento de la participación del trabajo en la renta nacional.','41','48']
['caso','Igualmente se fijará una revisión semestral para el caso de que no se cumplan las previsiones sobre el índice de precios citado.','52','56']
['revisión','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','3','11']
['cómputo','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','153','160']
['Sección','Sección 4. Salarios y garantías salariales','0','7']
['cuantía','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','322','329']
['duración','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','159','167']
['descanso','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','133','141']
['modalidad','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','147','156']
['contrato','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','174','182']
['acuerdo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','166','173']
['superior','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','51','59']
['pago','Qué requisitos de pago de horas extras existen','18','22']
['carácter','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','107','115']
['carácter','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','107','115']
['apartado','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','102','110']
['apartado','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','102','110']
['valor','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','384','389']
['convenio','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','209','217']
['actividad','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','148','157']
['jornada','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','198','205']
['hora','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','31','35']
['colocación','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','221','231']
['pacto','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','491','496']
['Gobierno','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','3','11']
['ramas','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','139','144']
['meses','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','163','168']
['trabajo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','71','78']
['anual','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','217','222']
['caso','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','357','361']
['cómputo','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','209','216']
['realizadas','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','553','563']
['párrafo','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','36','43']
['consideración','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','14','27']
['Sección','Sección 5. Tiempo de trabajo','0','7']
['artículo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','181','189']
['situación','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','255','264']
['ausencia','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','479','487']
['proporción','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','340','350']
['contrato','Sección 3. Elementos y eficacia del contrato de trabajo','37','45']
['admisión','Se prohíbe la admisión al trabajo a los menores de dieciséis años.','14','22']
['eficacia','Sección 3. Elementos y eficacia del contrato de trabajo','24','32']
['Trabajo','Artículo 6. Trabajo de los menores.','12','19']
['trabajo','Se prohíbe la admisión al trabajo a los menores de dieciséis años.','26','33']
['edad','Cuál es la edad mínima para trabajar','11','15']
['Sección','Sección 3. Elementos y eficacia del contrato de trabajo','0','7']
['cuyos','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','97','102']
['lactancia','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','152','161']
['ámbito','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','139','145']
['sector','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','146','152']
['posesión','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','170','178']
['duración','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','134','142']
['periodo','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','99','106']
['contrato','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','21','29']
['incapacidad','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','19','30']
['superior','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','79','87']
['mes','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','93','96']
['título','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','182','188']
['práctica','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','59','67']
['efecto','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','162','168']
['efecto','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','162','168']
['máster','A los efectos de este artículo los títulos de grado máster y en su caso doctorado correspondientes a los estudios universitarios no se considerarán la misma titulación salvo que al ser contratado por primera vez mediante un contrato en prácticas el trabajador estuviera ya en posesión del título superior de que se trate.','54','60']
['trabajador','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','33','43']
['convenio','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','51','59']
['salario','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','275','282']
['antig√ºedad','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','172','182']
['vigencia','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','231','239']
['equivalente','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','346','357']
['sesenta','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','152','159']
['grado','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','192','197']
['nivel','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','243','248']
['virtud','c) Ning√∫n trabajador podrá estar contratado en prácticas en la misma o distinta empresa por tiempo superior a dos años en virtud de la misma titulación o certificado de profesionalidad.','122','128']
['retribución','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','6','17']
['término','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','9','16']
['meses','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','265','270']
['trabajo','Tampoco se podrá estar contratado en prácticas en la misma empresa para el mismo puesto de trabajo por tiempo superior a dos años aunque se trate de distinta titulación o distinto certificado de profesionalidad.','91','98']
['paternidad','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','164','174']
['empresa','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','61','68']
['formación','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','115','124']
['fines','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','102','107']
['cómputo','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','192','199']
['obtención','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','43','52']
['Sección','Sección 4. Modalidades del contrato de trabajo','0','7']
['objeto','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','336','342']
['titulación','Tampoco se podrá estar contratado en prácticas en la misma empresa para el mismo puesto de trabajo por tiempo superior a dos años aunque se trate de distinta titulación o distinto certificado de profesionalidad.','159','169']
['exceder','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','66','73']
['riesgo','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','41','47']
['establecidos','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','401','413']
['empleo','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','280','286']
['marco','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','229','234']
['programas','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','515','524']
['sistema','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','239','246']
['sistema','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','239','246']
['duración','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','338','346']
['contrato','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','3','11']
['texto','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','575','580']
['límite','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','318','324']
['alternancia','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','131','142']
['actividad','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','146','155']
['letras','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','421','427']
['Ley','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','597','600']
['régimen','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','120','127']
['cualificación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','68','81']
['edad','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','328','332']
['empresa','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','182','189']
['aplicación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','465','475']
['formación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','20','29']
['Sección','Sección 4. Modalidades del contrato de trabajo','0','7']
['objeto','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','58','64']
['artículo','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','440','448']
['aprendizaje','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','35','46']
['establecidos','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','122','134']
['atención','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','7','15']
['aceptación','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','298','308']
['renuncia','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','65','73']
['duración','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','90','98']
['ordinarias','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','442','452']
['respecto','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','334','342']
['incompatibilidad','2. Necesidades formativas siempre que se acredite la incompatibilidad horaria.','55','71']
['contrato','3. Incompatibilidad con otro contrato a tiempo parcial.','30','38']
['adición','5. Se consideran horas complementarias las realizadas como adición a las horas ordinarias pactadas en el contrato a tiempo parcial conforme a las siguientes reglas:','59','66']
['preaviso','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','102','110']
['recibo','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','320','326']
['pactadas','Estas horas complementarias no se computarán a efectos de los porcentajes de horas complementarias pactadas que se establecen en la letra c).','99','107']
['semanales','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','162','171']
['relevo','Artículo 12. Contrato a tiempo parcial y contrato de relevo','53','59']
['efecto','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','54','60']
['efecto','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','54','60']
['trabajador','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','244','254']
['convenio','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','409','417']
['materia','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','91','98']
['empresario','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','193','203']
['condiciones','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','43','54']
['jornada','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','102','109']
['conducta','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','548','556']
['cotización','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','121','131']
['sesenta','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','291','298']
['hora','d) El trabajador deberá conocer el día y la hora de realización de las horas complementarias pactadas con un preaviso mínimo de tres días salvo que el convenio establezca un plazo de preaviso inferior.','44','48']
['letras','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','130','136']
['porcentaje','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','188','198']
['pacto','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','21','26']
['realización','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','6','17']
['carencia','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','168','176']
['incumplimiento','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','160','174']
['retribución','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','244','255']
['bases','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','112','117']
['enunciadas','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','52','62']
['trabajo','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','129','136']
['celebración','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','210','221']
['momento','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','196','203']
['caso','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','152','156']
['cómputo','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','175','182']
['realizadas','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','43','53']
['citado','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','250','256']
['Seguridad','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','137','146']
['posterioridad','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','258','271']
['Sección','Sección 4. Modalidades del contrato de trabajo','0','7']
['letra','Estas horas complementarias no se computarán a efectos de los porcentajes de horas complementarias pactadas que se establecen en la letra c).','132','137']
['objeto','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','453','459']
['plazo','d) El trabajador deberá conocer el día y la hora de realización de las horas complementarias pactadas con un preaviso mínimo de tres días salvo que el convenio establezca un plazo de preaviso inferior.','175','180']
['artículo','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','69','77']
['exceder','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','53','60']
['perjuicio','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','7','16']
['nocturno','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','21','29']
['noche','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','64','69']
['Trabajo','Artículo 36. Trabajo nocturno trabajo a turnos y ritmo de trabajo','13','20']
['trabajo','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','13','20']
['ritmo','Artículo 36. Trabajo nocturno trabajo a turnos y ritmo de trabajo','50','55']
['Sección','Sección 5. Tiempo de trabajo','0','7']
['ampliaciones','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','89','101']
['regla','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','150','155']
['duración','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','266','274']
['periodo','Cuánto es el periodo mínimo de descanso semanal','13','20']
['descanso','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','27','35']
['mañana','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','215','221']
['regímenes','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','146','155']
['fijación','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','134','142']
['régimen','Cuál es el régimen del descanso semanal','11','18']
['trabajo','cuál es el máximo de días de trabajo ininterrumplido','29','36']
['aplicación','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','13','23']
['días','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','104','108']
['derecho','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','25','32']
['Sección','Sección 5. Tiempo de trabajo','0','7']
['artículo','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','63','71']
['semanal','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','36','43']
['tarde','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','180','185']
['establecidos','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','571','583']
['fecha','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','165','170']
['productividad','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','421','434']
['técnica','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','289','296']
['trabajador','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','39','49']
['residencia','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','231','241']
['salario','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','212','219']
['decisión','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','14','22']
['indemnización','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','180','193']
['existencia','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','255','265']
['empresario','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','53','63']
['organización','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','437','449']
['actividad','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','530','539']
['traslado','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','15','23']
['compensación','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','108','120']
['centro','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','117','123']
['antelación','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','126','136']
['meses','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','260','265']
['trabajo','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','128','135']
['extinción','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','138','147']
['empresa','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','104','111']
['razones','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','269','276']
['caso','Cuáles son los derechos del trabajador en caso de que la empresa decida trasladar su centro de trabajo','42','46']
['producción','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','318','328']
['días','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','204','208']
['derecho','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','57','64']
['Movilidad','Artículo 40. Movilidad geográfica','13','22']
['Sección','Sección 1. Movilidad funcional y geográfica','0','7']
['supuesto','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','391','399']
['itinerantes','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','146','157']]
	relation=['broader', 'narrower', 'related']
	resultsIate(termino, jsonlist, idioma, targets)
	resultsEurovoc(termino, idioma, relation)
	resultsSyns(idioma,termino,targets,context)






  
  
###:termitup karenvazquez$ python3 searchterm.py "maternity leave" en --relation broader eurovoc
###:termitup karenvazquez$ python3 searchterm.py discrimination en "es en de nl" iate      



#IATE FILE
#python3 search.py --sourceFile 10term --type new --termId termino_id --targetFile salida10 --euroSource salida_eurovoc --lang en --targets "en es de nl" iate
#IATE TERM
#python3 search.py --sourceTerm discrimination --type new --termId termino_id --targetFile salida10 --euroSource salida_eurovoc --lang en --targets "en es de nl" iate


#EUROVOC FILE (ya no es necesario dar archivo de salida, pues el archivo de entrada se llena y es el resultado)
#python3 search.py --sourceFile salida_eurovoc_br --lang en --targets "en es de nl" --relation broader eurovoc
#EUROVOC TERM
#python3 search.py --sourceTerm "maternity leave" --lang en --targets "en es de nl" --relation broader eurovoc

#SYNS FILE 
# python3 search.py --sourceFile 10term --lang es --targets "en es" --contextFile contextos_salida syns
#python3 search.py --sourceFile term_es --targetFile salida_lexicala --lang es --targets "en es de nl" --contextFile contextos_salida syns
