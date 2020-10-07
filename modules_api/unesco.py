#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:13:37 2020

@author: pmchozas
"""

import requests
import json

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
    print(rjson)
    
    return myterm