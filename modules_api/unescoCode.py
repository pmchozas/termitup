#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:13:37 2020

@author: pmchozas
"""

import requests
import json


def enrich_term_unesco(myterm):
    get_uri(myterm)
    get_synonyms(myterm)
    get_translations(myterm)
    get_relations(myterm)
    

def get_uri(myterm):
    term='"^'+myterm.term+'$"'
    lang='"'+myterm.langIn+'"'
    url = "http://sparql.lynx-project.eu/"
    query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label ?prefEN
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
        ?c a skos:Concept .
        ?c ?p ?label. 
        ?c skos:prefLabel ?prefEN.
          FILTER regex(?label, """+term+""", "i")

          
          FILTER (lang(?prefEN) = """+lang+""")

          FILTER (?p IN ( skos:prefLabel, skos:altLabel ) )
          

        }  
        }
        """
    headers = {'content-type': 'text/html; charset=UTF-8'}
    r=requests.get(url, params={'format': 'json', 'query': query})
    rjson=json.loads(r.text)
    if('results' in rjson.keys()):
        results=rjson['results']
        bindings=results['bindings']
        for b in range(len(bindings)):
            myterm.unesco_id=bindings[b]['c']['value']
    
    return myterm


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
        GRAPH <http://sparql.lynx-project.eu/graph/unesco-thesaurus> {
        VALUES ?c { <"""+myterm.unesco_id+"""> }
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
                    myterm.synonyms_unesco.append(nameUri)

    except json.decoder.JSONDecodeError:
        pass
        
      
    return(nameUri)


def get_translations(myterm): #recoge traducciones
    label=['prefLabel','altLabel'] 
    for l in label:
        for lang in myterm.langOut:
            if lang not in myterm.translations_unesco:
                myterm.translations_unesco[lang]=[]
                try:
                    lang1='"'+lang+'"'
                    url=("http://sparql.lynx-project.eu/")
                    query="""
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    SELECT ?c ?label
                    WHERE {
                    GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
                    VALUES ?c { <"""+myterm.unesco_id+"""> }
                    VALUES ?searchLang { """+lang1+""" undef } 
                    VALUES ?relation { skos:prefLabel  } 
                    ?c a skos:Concept . 
                    ?c ?relation ?label . 
                    filter ( lang(?label)=?searchLang )
                    }
                    }
                    """
                    r=requests.get(url, params={'format': 'json', 'query': query})
                    results=json.loads(r.text)
                    print(query)
    
                    if (len(results["results"]["bindings"])==0):
                            trans=''
                    else:
                        for result in results["results"]["bindings"]:
                            trans=result["label"]["value"]
                            print(trans)
                            myterm.translations_unesco[lang].append(trans)
                           
            
                except json.decoder.JSONDecodeError:
                    pass
        
      
    return(myterm)


def get_relations(myterm):
    relations=['broader', 'narrower', 'related']
    
    for relation in relations:
        if relation not in myterm.unesco_relations:
            myterm.unesco_relations[relation]=[]
        url=("http://sparql.lynx-project.eu/")
        query2="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
        VALUES ?c {<"""+myterm.unesco_id+"""> }
        VALUES ?relation { skos:"""+relation+""" } 
        ?c a skos:Concept .
        ?c ?relation ?label .    
        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query2})
        rjsonrel=json.loads(r.text)

        if('results' in rjsonrel.keys()):
            results=rjsonrel['results']
            bindings=results['bindings']
            for b in range(len(bindings)):
                answerRel=bindings[b]['label']['value']    
                if relation == 'broader':
                    myterm.unesco_relations[relation].append(answerRel)
                elif relation == 'narrower':                          
                    myterm.unesco_relations[relation].append(answerRel)
                elif relation == 'related':  
                    myterm.unesco_relations[relation].append(answerRel)
                else: 
                    continue
                
    return(myterm)       
            