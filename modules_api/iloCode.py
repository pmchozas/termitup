#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 19:20:00 2020

@author: pmchozas
"""


import requests
import json


def enrich_term_ilo(myterm):
    get_uri(myterm)
    get_synonyms(myterm)
    get_translations(myterm)
    get_relations(myterm)
    create_intermediate_ids(myterm)
    return myterm

    

def get_uri(myterm):
    term='"^'+myterm.term+'$"'
    lang='"'+myterm.langIn+'"'
    url = "http://sparql.lynx-project.eu/"
    query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label ?prefEN
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/ilo> {
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
            myterm.ilo_id=bindings[b]['c']['value']
    
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
        GRAPH <http://sparql.lynx-project.eu/graph/ilo> {
        VALUES ?c { <"""+myterm.ilo_id+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:"""+label+"""  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
        print(query)
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                nameUri=''
        else:
            for result in results["results"]["bindings"]:
                nameUri=result["label"]["value"]
                if nameUri != myterm.term:
                    myterm.synonyms_ilo.append(nameUri)

    except json.decoder.JSONDecodeError:
        pass
        
      
    return(nameUri)

def get_translations(myterm): #recoge traducciones

    for lang in myterm.langOut:
            if lang not in myterm.translations_ilo:
                myterm.translations_ilo[lang]=[]
                try:
                    lang1='"'+lang+'"'
                    url=("http://sparql.lynx-project.eu/")
                    labels=['prefLabel','altLabel'] 
                    for label in labels:
                        query="""
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        SELECT ?c ?label
                        WHERE {
                        GRAPH <http://lkg.lynx-project.eu/ilo> {
                        VALUES ?c { <"""+myterm.ilo_id+"""> }
                        VALUES ?searchLang { """+lang1+""" undef } 
                        VALUES ?relation { skos:"""+label+""" } 
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
                                myterm.translations_ilo[lang].append(trans)
                           
            
                except json.decoder.JSONDecodeError:
                    pass
        
      
    return(myterm)


def get_relations(myterm):
    relations=['broader', 'narrower', 'related']
    
    for relation in relations:
        if relation not in myterm.ilo_relations:
            myterm.ilo_relations[relation]=[]
        url=("http://sparql.lynx-project.eu/")
        query2="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/ilo> {
        VALUES ?c {<"""+myterm.ilo_id+"""> }
        VALUES ?relation { skos:"""+relation+""" } 
        ?c a skos:Concept .
        ?c ?relation ?label .    
        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query2})
        rjsonrel=json.loads(r.text)
        print(query2)

        if('results' in rjsonrel.keys()):
            results=rjsonrel['results']
            bindings=results['bindings']
            for b in range(len(bindings)):
                answerRel=bindings[b]['label']['value']    
                if relation == 'broader':
                    myterm.ilo_relations[relation].append(answerRel)
                elif relation == 'narrower':                          
                    myterm.ilo_relations[relation].append(answerRel)
                elif relation == 'related':  
                    myterm.ilo_relations[relation].append(answerRel)
                else: 
                    continue
                
    return(myterm)


def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_ilo)>0:
        myterm.synonyms['ilo']={}
        myterm.synonyms['ilo'][myterm.langIn]=[]        
        for term in myterm.synonyms_ilo:            
            syn_set = {}          
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn
            myterm.synonyms['ilo'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_ilo)>0:
        myterm.translations['ilo']={}
        for lang in myterm.langOut:
            if lang in myterm.translations_ilo.keys():
                myterm.translations['ilo'][lang]=[]                
                for term in myterm.translations_ilo[lang]:
                    trans_set = {}
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term
                    if len(myterm.translations['ilo'][lang])<=0:
                        myterm.translations['ilo'][lang].append(trans_set)
                    else:
                        if 'ilo' in myterm.synonyms:
                            if lang in myterm.synonyms['ilo']:
                                myterm.synonyms['ilo'][lang].append(trans_set)
                            else:
                                myterm.synonyms['ilo'][lang]=[]
                                myterm.synonyms['ilo'][lang].append(trans_set)
                        else:
                            myterm.synonyms['ilo']={}
                            myterm.synonyms['ilo'][lang]=[]
                            myterm.synonyms['ilo'][lang].append(trans_set)
    
    if len(myterm.definitions_ilo)>0:
        myterm.definitions['ilo']={}
        for lang in myterm.definitions_ilo.keys():
            myterm.definitions['ilo'][lang]=[]
            for defi in myterm.definitions_ilo[lang]:
                def_set = {}
                defid=myterm.term+'-'+lang+'-def'
                def_set['def-id']=defid.lower()
                def_set['def-value']=defi
                myterm.definitions['ilo'][lang].append(def_set)

    return myterm