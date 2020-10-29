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
    ilo_id=""
    context=""
    schema=""
    frequency=""
    jurisdiction=""
    translations_iate={}
    definitions_iate={}
    synonyms_iate=[]
    ref_def_iate={}
    note_iate={}
    term_ref_iate={}
    related_ids_iate=[]
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
    definitions_ilo={}
    translations_ilo={}
    synonyms_ilo=[]
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
        self.term=""
        self.langIn=""
        self.translations_iate= {}
        self.langOut=[]
        self.source=""
        self.iate_id=""
        self.eurovoc_id=""
        self.unesco_id=""
        self.wikidata_id=""
        self.thesoz_id=""
        self.stw_id=""
        self.ilo_id=""
        self.context=""
        self.schema=""
        self.frequency=""
        self.jurisdiction=""
        self.translations_iate={}
        self.definitions_iate={}
        self.synonyms_iate=[]
        self.def_ref_iate={}
        self.note_iate={}
        self.term_ref_iate={}
        self.related_ids_iate=[]
        self.translations_eurovoc={}
        self.definitions_eurovoc={}
        self.synonyms_eurovoc=[]
        self.translations_unesco={}
        self.definitions_unesco={}
        self.synonyms_unesco=[]
        self.translations_wikidata={}
        self.definitions_wikidata={}
        self.synonyms_wikidata=[]
        self.definitions_thesoz={}
        self.translations_thesoz={}
        self.synonyms_thesoz=[]
        self.definitions_stw={}
        self.translations_stw={}
        self.synonyms_stw=[]
        self.definitions_ilo={}
        self.translations_ilo={}
        self.synonyms_ilo=[]
        self.start=0
        self.end=0
        self.index_max=0
        self.best_item_id=0
        self.eurovoc_relations={}
        self.unesco_relations={}
        self.wikidata_relations={}
        self.thesoz_relations={}
        self.stw_relations={}
        self.ilo_relations={}





