import argparse
import csv #libreria para exportar a excel o csv 
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper import SPARQLWrapper, XML
import csv
import multiprocessing
import time 
import requests #libreria para querys en api

#import pandas as pd
def obtenerResultado(args):
    nameFileRead=args.sourceFile
    termino=args.sourceTerm
    typeFile=args.type
    newFile=args.targetFile
    relacion=args.query
    lenguaje=args.lang
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
    readernew.writerow(['prefLabel@en', 'term_id', 'broader_uri', 'broader_id','brprefLabel@en', 'brprefLabel@es','brprefLabel@de','brprefLabel@nl'])
    
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


            for r in resultado[1:]:
                joinr=','.join(r)
                filenew.write(joinr+'\n')
                
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
                readernew.writerow([termino, ide, uri, ideR1, broader ])
          
    else:
        uri_termino=queryTERMINO_URI(termino, lenguaje)
        uri=queryURI(uri_termino, relacion)
        broader=queryNOMBRE(uri,lenguaje)
        listaRelacion.append(broader)
        ideR=uri.split('/')
        ideR1=ideR[-1]
            
        readernew.writerow([termino, ide, uri, ideR1, broader ])


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

  

parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search") #nombre de archivo a leer
parser.add_argument("--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms") #tipo de archivo lectura o escritura (w/a)
parser.add_argument("--targetFile", help="Name of the target file")
parser.add_argument("query", help="Broader, narrower or related")
parser.add_argument("lang", help="Target language. Type 'todos' to search in en, es, de, nl ")

args=parser.parse_args()
obtenerResultado(args)

