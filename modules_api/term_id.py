#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:55:46 2020

@author: pmchozas
"""


import re



def create_id(myterm):
    if ' ' in myterm.term:
        term=re.sub(' ', '-',  myterm.term)
    else:
        term=myterm.term.lower()
    lang=myterm.langIn
    schema=myterm.schema
    uri=schema+'-'+term+'-'+lang
    myterm.term_id=uri
    
    return myterm
    


# myterm=Term.Term()
# myterm.term='pez espada'
# myterm.langIn='es'
# myterm.schema='test'


# test=create_id(myterm)

# print(myterm.term_id)
