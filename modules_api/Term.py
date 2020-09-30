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
    langOut=""
    source=""
    term_id=""
    context=""
    jurisdiction=""
    translations={}
    definitions={}
    synonyms=[]
    
    
    ### test
    responseIate=''
    vectors=[]
    items=[]
    
    def __init__(self):
        self.term='term'
        self.lang='lang'
        self.translations={
            "lang1":"term1",
            "lang2":"term2"
            }
        self.definitions={
            "lang1":"defi1",
            "lang2":"defi2"
            }
        self.synonyms=["synonym1", "synonym2"]




