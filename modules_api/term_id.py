#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:55:46 2020

@author: pmchozas
"""


import re
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

    uri=schema+'-'+term+'-'+lang
    myterm.term_id=uri
    
    return myterm
    


# myterm=Term.Term()
# myterm.term="worker's statute"
# myterm.langIn='en'
# myterm.schema='test'


# test=create_id(myterm)

# print(myterm.term_id)
