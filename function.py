# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:48:05 2020

@author: Pablo
"""

from modules_api.Term import Term




def generateFakeTerm():
    myterm= Term()
    myterm.source =''
    myterm.term_id="9999999"
    myterm.term="empresario"
    
    myterm.context= "el empresario de la empresa le bajó el salario al trabajador, el contratista del proyecto mandó al empleador a casa"
    myterm.iate_id="https://iate.europa.eu/entry/result/1621645"
   
    myterm.langIn="es"
    myterm.langOut=['en','de']
    myterm.schema='text'
  
    myterm.translations_iate={}
    
    tradu_en = []
    tradu_en.append('entrepeneur')
    tradu_en.append('superboss')
    
    tradu_de = []
    tradu_de.append('Unternehmer')
    tradu_de.append('Waghner')
    
    
    myterm.translations_iate = {k: v for k, v in (('en', tradu_en), ('de',tradu_de))}
    
    
    
    
    
    
    
    myterm.synonyms_iate=[]
    myterm.synonyms_iate.append('emprendedor')
    myterm.synonyms_iate.append('empresauro')

 
    return myterm
    
   

    
    
  


def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_iate)>0:
        myterm.synonyms['iate']={}
        myterm.synonyms['iate'][myterm.langIn]=[]
        
        for term in myterm.synonyms_iate:
            
            syn_set = {}
            
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn
            
            
            myterm.synonyms['iate'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_iate)>0:
        myterm.translations['iate']={}
        for lang in myterm.langOut:
            print(lang)
            if lang in myterm.translations_iate.keys():
                print('sí que hay lang en iate '+lang)
                myterm.translations['iate'][lang]=[]
                print(myterm.translations)
                for term in myterm.translations_iate[lang]:
                    trans_set = {}
                    print(term)

                    print(myterm.trans_iate_ids)
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term
                    print(myterm.trans_iate_ids)
                    myterm.translations['iate'][lang].append(trans_set)
            print('TRANSLATIONS')
            print(myterm.translations)
    return myterm



Term1 = generateFakeTerm()

create_intermediate_ids(Term1)