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
    get_uri(myterm) #primero recogemos la uri 
    #aquí hacemos desambiguación???
    get_definition(myterm) #recogemos definicion si hay para construir vector (creo)
    get_relations(myterm) #recogemos broader, narrower, related
    get_synonyms(myterm)  #recogemos sinónimos en el langin
    get_translations(myterm)
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



def get_definition(myterm): #recoge la definicion de la uri de entrada si la hay
    try:
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
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            definition=''
        else:
            for result in results["results"]["bindings"]:
                definition=result["label"]["value"]
                myterm.definitions_eurovoc[myterm.langIn]=definition
                
    except json.decoder.JSONDecodeError:
        pass

    return(myterm)



def get_relations(myterm): #recoge la uri de la relacion a buscar 
    reltypes=['broader', 'narrower', 'related']
    try:
        for rel in reltypes:
            if rel not in myterm.eurovoc_relations:
                myterm.eurovoc_relations[rel]=[]
                url=("http://sparql.lynx-project.eu/")
                query="""
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?c ?label
                WHERE {
                GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                VALUES ?c {<"""+myterm.eurovoc_id+"""> }
                VALUES ?relation { skos:"""+rel+""" } # skos:broader
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
                        if rel == 'broader':
                            
                            myterm.eurovoc_relations[rel].append(answerRel)
                            myterm.euro_br.append(answerRel)
                        elif rel == 'narrower':
                            
                            myterm.eurovoc_relations[rel].append(answerRel)
                            myterm.euro_na.append(answerRel)
                        elif rel == 'related':
                            
                            myterm.eurovoc_relations[rel].append(answerRel)
                            myterm.euro_re.append(answerRel)
                        else: 
                            continue
    
    
                #         name=name_term_eurovoc(answerRel,lang,'prefLabel')
                #         answer.append([answerRel, name, relation])
    except json.decoder.JSONDecodeError:
        pass
    
    return(myterm)
                    
def get_synonyms(myterm): #recoge sinónimos
    try:
        nameUri=''
        label="altLabel"
        lang='"'+myterm.langIn+'"'
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+myterm.eurovoc_id+"""> }
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
                if nameUri != myterm.term:
                    myterm.synonyms_eurovoc.append(nameUri)

    except json.decoder.JSONDecodeError:
        pass
        
      
    return(nameUri)





def get_translations(myterm): #recoge traducciones
    label=['prefLabel','altLabel'] 
    for l in label:
        for lang in myterm.langOut:
            if lang not in myterm.translations_eurovoc:
                myterm.translations_eurovoc[lang]=[]
                try:
                    lang1='"'+lang+'"'
                    url=("http://sparql.lynx-project.eu/")
                    query="""
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    SELECT ?c ?label
                    WHERE {
                    GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                    VALUES ?c { <"""+myterm.eurovoc_id+"""> }
                    VALUES ?searchLang { """+lang1+""" undef} 
                    VALUES ?relation { skos:"""+l+"""  } 
                    ?c a skos:Concept . 
                    ?c ?relation ?label . 
                    filter ( lang(?label)=?searchLang )
                    }
                    }
                    """
                    r=requests.get(url, params={'format': 'json', 'query': query})
                    results=json.loads(r.text)
    
                    if (len(results["results"]["bindings"])==0):
                            trans=''
                    else:
                        for result in results["results"]["bindings"]:
                            trans=result["label"]["value"]
                            myterm.translations_eurovoc[lang].append(trans)
                           
            
                except json.decoder.JSONDecodeError:
                    pass
        
      
    return(myterm)
            
    
