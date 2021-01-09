#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:55:46 2020

@author: pmchozas
"""


import re
import unidecode
# import Term



def create_id(myterm):
    chars=['\'', '\"', '!', '<', '>', ',']
    term=myterm.term.lower()
    lang=myterm.langIn.lower()
    schema=myterm.schema.lower()
    for c in chars:
        term=term.replace(c, '')

    if ' ' in term:
        term=re.sub(' ', '-', term)
    else:
        term=term

    if ' ' in schema:
        schema=re.sub(' ', '-', schema)
    else:
        schema=schema

    uri=schema+'-'+term+'-'+lang
    myterm.term_id=unidecode.unidecode(uri)
    
    return myterm

def create_ontolex_ids(myterm):
    term_id=myterm.term_id
    myterm.lexical_sense_id=term_id+'-sen'
    myterm.lexical_entry_id=term_id+'-len'
    myterm.form_id=term_id+'-form'
    
    return myterm


# myterm=Term.Term()
# myterm.term="worker's statute"
# myterm.langIn='en'
# myterm.schema='test'


# test=create_id(myterm)

# print(myterm.term_id)
