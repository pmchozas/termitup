#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:16:07 2020

@author: pmchozas
"""

import os
import json
from rdflib import Graph, Literal

def rml_converter(json_data):
    print('RML CONVERTER')
    print(json_data)
    json_object = json.dumps(json_data)
    source_term = json_data["Source Term"]
    source_term_context = json_data["Source Term Context"]
    source_lang = json_data["Source Language"]
    with open('modules_api/input.json', 'w') as json_file:
    #with open('input.json', 'w') as json_file:
        json_file.write(json_object)
    json_file.close()
    
    
    os.system("java -jar modules_api/rmlmapper.jar -m modules_api/mapping.rml.ttl -o modules_api/output.nt -d")
    #os.system("java -jar rmlmapper.jar -m mapping.rml.ttl -o output.nt -d")
    g = Graph()
    rdf_file=g.parse("modules_api/output.nt", format="nt")
    #rdf_file=g.parse("output.nt", format="nt")
    for t in rdf_file.triples((None, None, Literal(source_term))):
        rdf_file.remove(t)
        rdf_file.add((t[0],t[1],Literal(t[2],lang=source_lang)))
    
    
    for t in rdf_file.triples((None, None, Literal(source_term_context))):
        rdf_file.remove(t)
        rdf_file.add((t[0],t[1],Literal(t[2],lang=source_lang)))
    
    #print(rdf_file.serialize(format="turtle").decode("UTF-8"))
    return(rdf_file)


# json_data= {
#     "Source Term ID":"hola",
#     "Source Term":"worker",
#     "Source Term Context":"the worker signed an employment agreement and now works in a company with a salary and team work is important and labour law is more important",
#     "Source Language":"en"
#     }


# test = rml_converter(json_data)


