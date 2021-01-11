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
    create_intermediate_ids(myterm)
    return myterm


def get_uri(myterm): #recoge la uri del termino a buscar
    term='"^'+myterm.term+'$"'
    plural='"^'+myterm.term+'s'+'$"'
    euterm='"^'+myterm.term+' \\\(EU\\\)'+'$"'
    ueterm='"^'+myterm.term+' \\\(UE\\\)'+'$"'
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
        # print(query)
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            print('NEXT')
            try:
                url = ("http://sparql.lynx-project.eu/")
                query = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?c ?label
                WHERE {
                GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                ?c a skos:Concept .
                ?c ?p ?label. 
                  FILTER regex(?label, """+plural+""", "i" )
                  FILTER (lang(?label) = """+lang+""")
                  FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
              
        
                }  
                }
                """
                print(query)
                r=requests.get(url, params={'format': 'json', 'query': query})
                results=json.loads(r.text)
            
                if (len(results["results"]["bindings"])==0):
                    print('NEXT EU')
                    try:
                        url = ("http://sparql.lynx-project.eu/")
                        query = """
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        SELECT ?c ?label
                        WHERE {
                        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                        ?c a skos:Concept .
                        ?c ?p ?label. 
                          FILTER regex(?label, """+euterm+""", "i" )
                          FILTER (lang(?label) = """+lang+""")
                          FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
                      
                
                        }  
                        }
                        """
                        print(query)
                        r=requests.get(url, params={'format': 'json', 'query': query})
                        results=json.loads(r.text)
                    
                        if (len(results["results"]["bindings"])==0):
                            answeruri=''
                            print('NEXT UE')
                            try:
                                url = ("http://sparql.lynx-project.eu/")
                                query = """
                                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                                SELECT ?c ?label
                                WHERE {
                                GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                                ?c a skos:Concept .
                                ?c ?p ?label. 
                                  FILTER regex(?label, """+ueterm+""", "i" )
                                  FILTER (lang(?label) = """+lang+""")
                                  FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
                              
                        
                                }  
                                }
                                """
                                # print(query)
                                r=requests.get(url, params={'format': 'json', 'query': query})
                                results=json.loads(r.text)
                                
                                if (len(results["results"]["bindings"])==0):
                                    answeruri=''
                                    print('NO URI')
                                else:
                                    for result in results["results"]["bindings"]:
                                        answeruri=result["c"]["value"]
                                        #answerl=result["label"]["value"]
                                        myterm.eurovoc_id=answeruri

                            except:
                                print('no term')

                        else:
                            for result in results["results"]["bindings"]:
                                answeruri=result["c"]["value"]
                                #answerl=result["label"]["value"]
                                myterm.eurovoc_id=answeruri
                    except:
                         print('no term')     
                else:
                    for result in results["results"]["bindings"]:
                        answeruri=result["c"]["value"]
                        #answerl=result["label"]["value"]
                        myterm.eurovoc_id=answeruri
                
            except:
                print('no term')            
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
                # print(query)
                if (len(results["results"]["bindings"])==0):
                        answerRel=''
                else:
                    for result in results["results"]["bindings"]:
                        answerRel=result["label"]["value"]
                        if rel == 'broader':                         
                            myterm.eurovoc_relations[rel].append(answerRel)
                        elif rel == 'narrower':                         
                            myterm.eurovoc_relations[rel].append(answerRel)
                        elif rel == 'related':                          
                            myterm.eurovoc_relations[rel].append(answerRel)
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
    
    for lang in myterm.langOut:
        if lang not in myterm.translations_eurovoc:
                myterm.translations_eurovoc[lang]=[]
                try:
                    lang1='"'+lang+'"'
                    url=("http://sparql.lynx-project.eu/")
                    labels=['prefLabel', 'altLabel']
                    for label in labels:
                        query="""
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        SELECT ?c ?label
                        WHERE {
                        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
                        VALUES ?c { <"""+myterm.eurovoc_id+"""> }
                        VALUES ?searchLang { """+lang1+""" undef} 
                        VALUES ?relation { skos:"""+label+"""  } 
                        ?c a skos:Concept . 
                        ?c ?relation ?label . 
                        filter ( lang(?label)=?searchLang )
                        }
                        }
                        """
                        r=requests.get(url, params={'format': 'json', 'query': query})
                        results=json.loads(r.text)
                        # print(query)
        
                        if (len(results["results"]["bindings"])==0):
                                trans=''
                        else:
                            for result in results["results"]["bindings"]:
                                trans=result["label"]["value"]
                                trans=trans.replace('(', '')
                                trans=trans.replace(')', '')
                                print(trans)
                                myterm.translations_eurovoc[lang].append(trans)
                except:
                    continue
                           

      
    return(myterm)
            
def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_eurovoc)>0:
        myterm.synonyms['eurovoc']={}
        myterm.synonyms_ontolex['eurovoc']={}
        myterm.synonyms['eurovoc'][myterm.langIn]=[]  
        myterm.synonyms_ontolex['eurovoc'][myterm.langIn]=[]
        for term in myterm.synonyms_eurovoc:            
            syn_set = {}          
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn.replace('-', ' ')
            myterm.synonyms['eurovoc'][myterm.langIn].append(syn_set)
            myterm.synonyms_ontolex['eurovoc'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_eurovoc)>0:
        myterm.translations['eurovoc']={}
        myterm.translations_ontolex['eurovoc']={}
        for lang in myterm.langOut:
            if lang in myterm.translations_eurovoc.keys():
                myterm.translations['eurovoc'][lang]=[] 
                myterm.translations_ontolex['eurovoc'][lang]=[] 
                for term in myterm.translations_eurovoc[lang]:
                    trans_set = {}
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term.replace('-', ' ')
                    # print(trans_set)
                    myterm.translations_ontolex['eurovoc'][lang].append(trans_set) 
                    if len(myterm.translations['eurovoc'][lang])<=0:
                        myterm.translations['eurovoc'][lang].append(trans_set)
                    else:
                        if 'eurovoc' in myterm.synonyms:
                            if lang in myterm.synonyms['eurovoc']:
                                myterm.synonyms['eurovoc'][lang].append(trans_set)
                            else:
                                myterm.synonyms['eurovoc'][lang]=[]
                                myterm.synonyms['eurovoc'][lang].append(trans_set)
                        else:
                            myterm.synonyms['eurovoc']={}
                            myterm.synonyms['eurovoc'][lang]=[]
                            myterm.synonyms['eurovoc'][lang].append(trans_set)
                            
    
    if len(myterm.definitions_eurovoc)>0:
        myterm.definitions['eurovoc']={}
        for lang in myterm.definitions_eurovoc.keys():
            myterm.definitions['eurovoc'][lang]=[]
            for defi in myterm.definitions_eurovoc[lang]:
                def_set = {}
                defid=myterm.term+'-'+lang+'-def'
                def_set['def-id']=defid.lower()
                def_set['def-value']=defi
                myterm.definitions['eurovoc'][lang].append(def_set)

    return myterm






















