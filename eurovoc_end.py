import argparse
import csv #libreria para exportar a excel o csv 
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper import SPARQLWrapper, XML
import csv
import multiprocessing
import time 
import requests #libreria para querys en api
from random import randint #libreria para random

#import pandas as pd
def obtenerResultado(args):
    nameFileRead=args.sourceFile
    termino=args.sourceTerm
    typeFile=args.type
    newFile=args.targetFile
    relacion=args.query
    lenguaje=args.lang
    termId=args.termId
    print(relacion)
    c=0
    resultado=[]
    listaBroader_en=[]
    listaBroader_es=[]
    listaBroader_de=[]
    listaBroader_nl=[]
    resultado.insert(0, [])
    listaRelacion=[]
    filenew=open(newFile+'.csv', typeFile)
    readernew=csv.writer(filenew) 
    #readernew.writerow(['prefLabel@en', 'term_id', 'broader_uri', 'broader_id','brprefLabel@en', 'brprefLabel@es','brprefLabel@de','brprefLabel@nl'])
    
    if(nameFileRead):
        if(lenguaje=='todos'):
            lista=open(nameFileRead, newline='')
            lector=csv.reader(lista)
            for i in lector:
                resultado.insert(c, [])
                ide=i[1]
                termino=i[0]
                resultado[c].insert(0, termino)
                resultado[c].insert(1, ide)

            
                uri_termino_en=queryTERMINO_URI(termino, 'en')
                uri_broader_en=queryURI(uri_termino_en, relacion)
                broader_en=queryNOMBRE(uri_broader_en, 'en')
                listaBroader_en.append(broader_en)
                ideBroaders_en=uri_broader_en.split('/')
                ideBroader_en=ideBroaders_en[-1]
                resultado[c].insert(2, uri_broader_en)
                resultado[c].insert(3, ideBroader_en)
                resultado[c].insert(4, broader_en)
          
           
                uri_termino_es=queryTERMINO_URI(termino, 'es')
                uri_broader_es=queryURI(uri_termino_es, relacion)
                broader_es=queryNOMBRE(uri_broader_es, 'es')
                listaBroader_es.append(broader_es)
                ideBroaders_es=uri_broader_es.split('/')
                ideBroader_es=ideBroaders_es[-1]
                resultado[c].insert(5, broader_es)
            
                uri_termino_de=queryTERMINO_URI(termino, 'de')
                uri_broader_de=queryURI(uri_termino_de, relacion)
                broader_de=queryNOMBRE(uri_broader_de, 'de')
                listaBroader_de.append(broader_de)
                ideBroaders_de=uri_broader_de.split('/')
                ideBroader_de=ideBroaders_de[-1]
                resultado[c].insert(6, broader_de)
            
                uri_termino_nl=queryTERMINO_URI(termino, 'nl')
                uri_broader_nl=queryURI(uri_termino_nl, relacion)
                broader_nl=queryNOMBRE(uri_broader_nl, 'nl')
                listaBroader_nl.append(broader_nl)
                ideBroaders_nl=uri_broader_nl.split('/')
                ideBroader_nl=ideBroaders_nl[-1]
                resultado[c].insert(7, broader_nl)

                c=c+1


            asignID(termino, resultado, newFile, relacion,termId)
            print("*****-- Busqueda terminada --*****")
        else:
            for i in lector:
                ide=i[1]
                termino=i[0]
                uri_termino=queryTERMINO_URI(termino, lenguaje)
                uri=queryURI(uri_termino, relacion)
                broader=queryNOMBRE(uri,lenguaje)
                listaRelacion.append(broader)
                ideR=uri.split('/')
                ideR1=ideR[-1]
                #readernew.writerow([termino, ide, uri, ideR1, broader ])
                asignID(termino, resultado, newFile, relacion,termId)
          
    else:
        print('solo termino')
        uri_termino=queryTERMINO_URI(termino, lenguaje)
        uri=queryURI(uri_termino, relacion)
        broader=queryNOMBRE(uri,lenguaje)
        listaRelacion.append(broader)
        ideR=uri.split('/')
        ideR1=ideR[-1]
        #print(termino, resultado, newFile, relacion, termId)
        #readernew.writerow([termino, ide, uri, ideR1, broader ])
        asignID(termino, resultado, newFile, relacion,termId)


#1. funcion que obtiene la uri de cada termino
def queryTERMINO_URI(termino,lenguaje):
    termino2='"'+termino+'"'
    lenguaje2='"'+lenguaje+'"'
    resultado=''
    resultadouri=''
    sparql = SPARQLWrapper("http://publications.europa.eu/webapi/rdf/sparql")
    sparql.setQuery("""
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
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    
    if (len(results["results"]["bindings"])==0):
        resultadouri=''
    else:
        for result in results["results"]["bindings"]:
            resultadouri=result["c"]["value"]
            resultadol=result["label"]["value"]
    return(resultadouri)

#2. funcion que recibe la uri del termino al que sele desea saber su BROADER, obtiene la uri del BROADER 
def queryURI(uri_termino, relacion):
    resultado=''
    sparql = SPARQLWrapper("http://publications.europa.eu/webapi/rdf/sparql")
    sparql.setQuery("""
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
 
 
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if (len(results["results"]["bindings"])==0):
            resultado=''
    else:
        for result in results["results"]["bindings"]:
            resultado=result["label"]["value"]
        
    return(resultado)

#3. funcion que recibe la uri del broader y consulta cual es el termino correspondiente
def queryNOMBRE(uri_broader,lenguaje):
    resultado=''
    lenguaje2='"'+lenguaje+'"'
    sparql = SPARQLWrapper("http://publications.europa.eu/webapi/rdf/sparql")
    sparql.setQuery("""
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
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if (len(results["results"]["bindings"])==0):
            resultado=''
            #print(resultado)
    else:
        for result in results["results"]["bindings"]:
            resultado=result["label"]["value"]
            #print('CONCEPTO DE BROADER:', resultado)
           
    return(resultado)
def sctmid_creator():
    numb = randint(1000000, 9999999)

    SCTMID = "LT" + str(numb)
    return SCTMID

def comprobarIDE(ide):
    listaIds=[]
    nuevoide=''
    with open('termino_id.csv', newline='') as File:
        reader=csv.reader(File)
        for row in reader:
            identificador=row[0]
            listaIds.append(identificador)
            if(ide==identificador):
                nuevoide=sctmid_creator()
            else:
                nuevoide=ide
    return(nuevoide)
  
def asignID(termIdFile, resultado, outFile, relacion,termId):
    nuevoid=''
    File1=open(termId+'.csv', 'a')
    File2=open(outFile+'.csv', 'w')
    listwriter1=[]
    listwriter2=[]
    if(relacion=='broader'):
        listwriter2.append(['prefLabel@en', 'term_id', 'broader_uri', 'broader_id', 'prefLabel@en', 'prefLabel@es', 'prefLabel@de', 'prefLabel@nl'])
    elif(relacion=='narrower'):
        listwriter2.append(['prefLabel@en', 'term_id', 'narrower_uri', 'narrower_id', 'prefLabel@en', 'prefLabel@es', 'prefLabel@de', 'prefLabel@nl'])
    elif(relacion=='related'):
        listwriter2.append(['prefLabel@en', 'term_id', 'related_uri', 'related_id', 'prefLabel@en', 'prefLabel@es', 'prefLabel@de', 'prefLabel@nl'])
    

    nuevosids=[]
    listUris=[]
    idebueno=''
    lines=[]
    for i in resultado[1:]:
        if(len(i)>1):
            uri=i[2]
            if(uri!="-"):
                listUris.append(uri)
    repetido = []
    unico = []
    for x in listUris:
        if x not in unico:
            ide=sctmid_creator()
            nuevoid=comprobarIDE(ide)
            nuevosids.append(nuevoid)
            unico.append([x,nuevoid])
        else:
            if x not in repetido:
                repetido.append(x)
    c=0
    for row in resultado[1:]:
        if(len(row)>1):
            listwriter1.insert(c, [])
            listwriter2.insert(c, [])
            pref=row[0]
            termid=row[1]
            broaderuri=row[2]
            broaderid=row[3]
            prefen=row[4]
            prefes=row[5]
            prefde=row[6]
            prefnl=row[7]
            for t in unico:
                if(broaderuri==t[0] ):
                    idebueno=t[1]
                elif(broaderuri==''):
                    idebueno=''
            #print(idebueno, broaderuri)
            if(idebueno!='-' or len(row)<1):
                listwriter1[c].insert(0, prefen)
                listwriter1[c].insert(1, idebueno)
            idurisplit=broaderuri.split('/')
            iduri=idurisplit[-1]
            #print(iduri)
            listwriter2.append([pref,termid,iduri,idebueno, prefen, prefes, prefde, prefnl])
            
            idebueno='-'
            c=c+1

    for r in listwriter1[1:]:
        if(len(r)>1):
            joinr=','.join(r)
            File1.write(joinr+'\n')
    for r in listwriter2[2:]:
        if(len(r)>1 or r==''):
            joinr=','.join(r)
            File2.write(joinr+'\n')




    
parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search") #nombre de archivo a leer
parser.add_argument("--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms") #tipo de archivo lectura o escritura (w/a)
parser.add_argument("--termId", help="Name of the termino_id file, to save terms and ids") #nombre de archivo termino-id
parser.add_argument("--targetFile", help="Name of the target file")
parser.add_argument("query", help="Broader, narrower or related")
parser.add_argument("lang", help="Target language. Type 'todos' to search in en, es, de, nl ")

args=parser.parse_args()
obtenerResultado(args)



#####EJECUTAR########
#python3 eurovoc_end.py --sourceTerm discrimination --type w --termId termino_id_eurovoc --targetFile eurovocout broader todos
# karenvazquez$ python3 eurovoc_end.py --sourceFile 10term.csv --type w --termId termino_id_eurovoc --targetFile eurovocout broader todos
#####################

