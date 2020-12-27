#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:26:32 2020

@author: pmchozas
"""



class Term:
    term_id=""
    term=""
    context=""
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
    syn_iate_ids={}
    trans_iate_ids={}
    ref_def_iate={}
    note_iate={}
    term_ref_iate={}
    related_ids_iate=[]
    translations_eurovoc={}
    definitions_eurovoc={}
    synonyms_eurovoc=[]
    syn_eurovoc_ids={}
    trans_eurovoc_ids={}
    translations_unesco={}
    definitions_unesco={}
    synonyms_unesco=[]
    syn_unesco_ids={}
    trans_unesco_ids={}
    translations_wikidata={}
    definitions_wikidata={}
    synonyms_wikidata=[]
    syn_wikidata_ids={}
    trans_wikidata_ids={}
    definitions_thesoz={}
    translations_thesoz={}
    synonyms_thesoz=[]
    syn_thesoz_ids={}
    trans_thesoz_ids={}
    definitions_stw={}
    translations_stw={}
    synonyms_stw=[]
    syn_stw_ids={}
    trans_stw_ids={}
    definitions_ilo={}
    translations_ilo={}
    synonyms_ilo=[]
    syn_ilo_ids={}
    trans_ilo_ids={}
    start=0
    end=0
    index_max=0
    best_item_id=0
    eurovoc_relations={}
    unesco_relations={}
    wikidata_relations={}
    thesoz_relations={}
    stw_relations={}
    ilo_relations={}
    translations={}
    synonyms={}
    definitions={}
    relations={}
    ids={}
    preflabels={}
    altlabels={}
    lexical_sense_id=""
    lexical_entry_id=""
    form_id=""
    
    
    ### test
    responseIate=''
    vectors=[]
    items=[]
    
    wikidata_vectors={}
    
    def __init__(self):
        self.term_id=""
        self.term=""
        self.context=""
        self.langIn=""
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
        self.syn_iate_ids={}
        self.trans_iate_ids={}
        self.syn_eurovoc_ids={}
        self.trans_eurovoc_ids={}
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
        self.syn_unesco_ids={}
        self.trans_unesco_ids={}
        self.translations_wikidata={}
        self.definitions_wikidata={}
        self.synonyms_wikidata=[]
        self.syn_wikidata_ids={}
        self.trans_wikidata_ids={}
        self.definitions_thesoz={}
        self.translations_thesoz={}
        self.synonyms_thesoz=[]
        self.syn_thesoz_ids={}
        self.trans_thesoz_ids={}
        self.definitions_stw={}
        self.translations_stw={}
        self.synonyms_stw=[]
        self.syn_stw_ids={}
        self.trans_stw_ids={}
        self.definitions_ilo={}
        self.translations_ilo={}
        self.synonyms_ilo=[]
        self.syn_ilo_ids={}
        self.trans_ilo_ids={}
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
        self.translations={}
        self.synonyms={}
        self.ids={}
        self.definitions={}
        self.relations={}
        self.preflabels={}
        self.altlabels={}
        self.lexical_sense_id=""
        self.lexical_entry_id=""
        self.form_id=""




