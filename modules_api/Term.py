#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:26:32 2020

@author: pmchozas
"""

'''
no son todos obligatorios, no?
'''

class Term:
    term=""
    langIn=""
    langOut=[]
    source=""
    iate_id=""
    eurovoc_id=""
    unesco_id=""
    wikidata_id=""
    thesoz_id=""
    stw_id=""
    context=""
    schema=""
    frequency=""
    jurisdiction=""
    translations_iate={}
    definitions_iate={}
    synonyms_iate=[]
    translations_eurovoc={}
    definitions_eurovoc={}
    synonyms_eurovoc=[]
    translations_unesco={}
    definitions_unesco={}
    synonyms_unesco=[]
    translations_wikidata={}
    definitions_wikidata={}
    synonyms_wikidata=[]
    definitions_thesoz={}
    translations_thesoz={}
    synonyms_thesoz=[]
    definitions_stw={}
    translations_stw={}
    synonyms_stw=[]
    start=0
    end=0
    index_max=0
    best_item_id=0
    eurovoc_relations={}
    unesco_relations={}
    wikidata_relations={}
    thesoz_relations={}
    stw_relations={}
    
    
    ### test
    responseIate=''
    vectors=[]
    items=[]
    
    wikidata_vectors={}
    
    def __init__(self):
        self.term='term'
        self.lang='lang'





