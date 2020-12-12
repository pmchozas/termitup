#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:32:39 2020

@author: pmchozas
"""
import requests
import json
import re

def enrich_term_thesoz(myterm):
    get_uri(myterm)
    get_definition(myterm)
    get_relations(myterm)
    get_synonyms(myterm)
    get_translations(myterm)
    create_intermediate_ids(myterm)
    return myterm

def get_uri(myterm): #recoge la uri del termino a buscar
    term='"^'+myterm.term+'$"'
    lang='"'+myterm.langIn+'"'
    try:
        url = ("http://sparql.lynx-project.eu/")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE   {
        GRAPH <http://lkg.lynx-project.eu/thesoz> {
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
                myterm.thesoz_id=answeruri
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
            GRAPH <http://lkg.lynx-project.eu/thesoz> {
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
                myterm.definitions_thesoz[myterm.langIn]=definition
                
    except json.decoder.JSONDecodeError:
        pass

    return(myterm)


def get_relations(myterm): #recoge la uri de la relacion a buscar 
    reltypes=['broader', 'narrower', 'related']
    try:
        for rel in reltypes:
            if rel not in myterm.thesoz_relations:
                myterm.thesoz_relations[rel]=[]
                url=("http://sparql.lynx-project.eu/")
                query="""
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?c ?label
                WHERE {
                GRAPH <http://lkg.lynx-project.eu/thesoz> {
                VALUES ?c {<"""+myterm.thesoz_id+"""> }
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
                            myterm.thesoz_relations[rel].append(answerRel)
                        elif rel == 'narrower':                         
                            myterm.thesoz_relations[rel].append(answerRel)
                        elif rel == 'related':                          
                            myterm.thesoz_relations[rel].append(answerRel)
                        else: 
                            continue
    
    
                #         name=name_term_eurovoc(answerRel,lang,'prefLabel')
                #         answer.append([answerRel, name, relation])
    except json.decoder.JSONDecodeError:
        pass
    
    return(myterm)

#los resultados de altlabel son mu reguleros
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
        GRAPH <http://lkg.lynx-project.eu/thesoz> {
        VALUES ?c { <"""+myterm.thesoz_id+"""> }
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
                    myterm.synonyms_thesoz.append(nameUri)

    except json.decoder.JSONDecodeError:
        pass
        
      
    return(nameUri)

def get_translations(myterm): #recoge traducciones
    label=['prefLabel','altLabel'] 
    for l in label:
        print(l)
        for lang in myterm.langOut:
            if lang not in myterm.translations_thesoz:
                myterm.translations_thesoz[lang]=[]
                try:
                    lang1='"'+lang+'"'
                    url=("http://sparql.lynx-project.eu/")
                    query="""
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    SELECT ?c ?label
                    WHERE {
                    GRAPH <http://lkg.lynx-project.eu/thesoz> {
                    VALUES ?c { <"""+myterm.thesoz_id+"""> }
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
                    print(results)
    
                    if (len(results["results"]["bindings"])==0):
                            trans=''
                    else:
                        for result in results["results"]["bindings"]:
                            trans=result["label"]["value"]
                            myterm.translations_thesoz[lang].append(trans)
                           
            
                except json.decoder.JSONDecodeError:
                    pass
        
      
    return(myterm)

def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_thesoz)>0:
        myterm.synonyms['thesoz']={}
        myterm.synonyms['thesoz'][myterm.langIn]=[]        
        for term in myterm.synonyms_thesoz:            
            syn_set = {}          
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn
            myterm.synonyms['thesoz'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_thesoz)>0:
        myterm.translations['thesoz']={}
        for lang in myterm.langOut:
            if lang in myterm.translations_thesoz.keys():
                myterm.translations['thesoz'][lang]=[]                
                for term in myterm.translations_thesoz[lang]:
                    trans_set = {}
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term
                    myterm.translations['thesoz'][lang].append(trans_set)
    
    if len(myterm.definitions_thesoz)>0:
        myterm.definitions['thesoz']={}
        for lang in myterm.definitions_thesoz.keys():
            myterm.definitions['thesoz'][lang]=[]
            for defi in myterm.definitions_thesoz[lang]:
                def_set = {}
                defid=myterm.term+'-'+lang+'-def'
                def_set['def-id']=defid.lower()
                def_set['def-value']=defi
                myterm.definitions['thesoz'][lang].append(def_set)

    return myterm