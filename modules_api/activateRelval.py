#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:18:18 2021

@author: pmchozas
"""
from modules_api.Term import Term
from modules_api import relvalCode
import re
import unidecode

def validate_syns(myterm, reslist):
    synonyms=""
    for resource in reslist:
        if resource in myterm.synonyms.keys():
            if myterm.langIn in myterm.synonyms[resource].keys():
                for syn in myterm.synonyms[resource][myterm.langIn]:
                    synonyms=synonyms+ syn["syn-value"]+", "
    synonyms=synonyms.strip(' ')
    synonyms=synonyms.strip(',')
    term_in=myterm.term
    lang_in=myterm.langIn
                    
    relval_result=relvalCode.relation_validation(term_in, lang_in, synonyms)
    return relval_result
def create_id(term, lang, schema):
    chars=['\'', '\"', '!', '<', '>', ',']
    term=term.lower()
    lang=lang.lower()
    schema=schema.lower()
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
    term_id=unidecode.unidecode(uri)
    
    return term_id
def create_concepts(myterm, relval_result):
    if len(relval_result['synonymy'])>0:
        myterm.synonyms['relval']={}
        myterm.synonyms['relval'][myterm.langIn]=[]        
        for synonym in relval_result['synonymy']:
            syn_set={
                "syn-id":create_id(synonym, myterm.langIn, myterm.schema),
                "syn-value":synonym
                }
            myterm.synonyms['relval'][myterm.langIn].append(syn_set)
    if len(relval_result['broader'])>0:
        myterm.relations_relval['broader']=[]
        for broader in relval_result['broader']:
             br_id=create_id(broader, myterm.langIn, myterm.schema)
             myterm.relations_relval['broader'].append(br_id)
    if len(relval_result['narrower'])>0:
        myterm.relations_relval['narrower']=[]
        for narrower in relval_result['narrower']:
             na_id=create_id(narrower, myterm.langIn, myterm.schema)
             myterm.relations_relval['narrower'].append(na_id)
    if len(relval_result['related'])>0:
        myterm.relations_relval['related']=[]
        for related in relval_result['related']:
             re_id=create_id(related, myterm.langIn, myterm.schema)
             myterm.relations_relval['related'].append(re_id)
        
    
    return myterm

# TESTING
# reslist=['eurovoc']    
# myterm=Term()   
# myterm.schema="test"
# myterm.term="contrato"
# myterm.langIn="es"
# myterm.synonyms={'eurovoc': {'es': [{'syn-id': 'test-derecho-contractual-es', 'syn-value': 'Derecho contractual'}, {'syn-id': 'test-compromiso-es', 'syn-value': 'compromiso'}, {'syn-id': 'test-conclusión-de-contrato-es', 'syn-value': 'conclusión de contrato'}, {'syn-id': 'test-firma-de-contrato-es', 'syn-value': 'firma de contrato'}], 'en': [{'trans-id': 'test-conclusion-of-a-contract-en', 'trans-value': 'conclusion of a contract'}, {'trans-id': 'test-contract-law-en', 'trans-value': 'contract law'}, {'trans-id': 'test-contractual-agreement-en', 'trans-value': 'contractual agreement'}, {'trans-id': 'test-contractual-commitment-en', 'trans-value': 'contractual commitment'}, {'trans-id': 'test-law-of-contract-en', 'trans-value': 'law of contract'}]}}

# # print(validate_syns(myterm, reslist))
# relval_result={'synonymy': ['acuerdo'], 'broader': ['documento'], 'narrower': ['conclusión de contrato', 'firma de contrato'], 'related': ['trabajador'], 'non-related': ['derecho contractual', 'compromiso']}
# create_concepts(myterm, relval_result)
# # print(myterm.synonyms)
# print(myterm.relations_relval)
















