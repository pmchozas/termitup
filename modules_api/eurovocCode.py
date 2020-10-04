#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 11:59:19 2020

@author: pmchozas
"""
import requests
import json
import re
from unicodedata import normalize
# from modules_api import wsidCode
# from modules_api import extrafunctions
# from modules_api import jsonFile
# from modules_api import unesco
# import logging

#from modules_api import Term


def enrich_term_eurovoc(myterm):
    get_uri(myterm) #primero recogemos la uri y los resultados de la llamada
    get_definition(myterm)
    return myterm


def get_uri(myterm): #recoge la uri del termino a buscar
    term='"^'+myterm.term+'$"'
    lang='"'+myterm.langIn+'"'
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
                #answerl=result["label"]["value"]
                myterm.eurovoc_id=answeruri
    except:
        print('no term')

    return myterm


#get_definition no funciona, la anterior sí.

def get_definition(myterm): #recoge la definicion de la uri de entrada
    definition=''
    url=("http://sparql.lynx-project.eu/")
    term='"^'+myterm.term+'$"'
    lang='"'+myterm.langIn+'"'
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+term+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:definition  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
    r=requests.get(url, params={'format': 'json', 'query': query})
    print(r)
    results=json.loads(r.text)
    print(results)
    if (len(results["results"]["bindings"])==0):
        definition=''
    else:
        for result in results["results"]["bindings"]:
            definition=result["label"]["value"]
            myterm.definitions_eurovoc[myterm.langIn]=definition
    return(myterm)
                    



            
            
