
from flask import jsonify, abort, request, Blueprint
from flask import Flask,render_template
import requests
from flask_restplus import Resource, Api, fields, reqparse
import json
from random import randint #libreria para random
import re
import os
from os import listdir
from os.path import isfile, isdir
#import time
#import termiup_terminal
from flask import Response
from modules_api import st_extraction
from modules_api import TBXTools
from modules_api import postprocess
from modules_api import conts_log
from modules_api import eurovocCode
from modules_api import Term
from modules_api import iateCode
from modules_api import unescoCode
from modules_api import wikidataCode
from modules_api import thesozCode
from modules_api import stwCode
from modules_api import iloCode
from modules_api import relvalCode

REQUEST_API = Blueprint('term_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route("/")
def index():
    pagetitle = "HomePage"
    return render_template("index.html")

'''
GET EXAMPLE. Still in development. needs to reead the input
'''
@REQUEST_API.route('/term', methods=['GET'])
def term():
    '''
    to read parameters
    '''
    termino = request.args.get('term')
    print(termino)
    
    return Response(json.dumps(termino),  mimetype='application/json')


'''
POST EXAMPLE
'''    
@REQUEST_API.route('/extract_terminology', methods=['POST'])
def extract_terminology():
    
    '''
    to read body of a POST OR PUT
    '''
    

    Corpus = request.args.get('corpus')
    Language = request.args.get('lang_in')
    print('Received:')
    print(Corpus)
    print(Language)
    

    
    terminology = st_extraction.termex(Corpus, Language)
    print(terminology)
   
    return Response(json.dumps(terminology),  mimetype='application/json')



'''
Test Patricia Postprocess
si rompo algo, borrar todo lo de abajo
'''

@REQUEST_API.route('/postproc_terminology', methods=['POST'])
def postproc_terminology():
    
    '''
    to read body of a POST OR PUT
    '''

    Terms = request.args.get('terms')
    Language = request.args.get('source_language')
    tasks= request.args.get('tasks')
    print('Received:')
    #print(Terms)
    print(Language)

    termlist=Terms.split(', ')
    tasklist=tasks.split(', ')
    print(tasklist)
    #Pablo proposal -------------------------------------
    '''
    timeEx=True
    patternBasedClean=True
    pluralClean=True
    numbersClean=True
    accentClean=True
    '''
    
    for t in tasklist:
        if 'timeEx' in tasklist:
            timeEx=True
        else:
            timeEx=False
            
        if 'patterns' in tasklist:
            patternBasedClean=True
        else:
            patternBasedClean=False
       
        if 'plurals' in tasklist:
            pluralClean=True
        else:
            pluralClean=False
    
        if 'numbers' in tasklist:
            numbersClean=True
        else:
            numbersClean=False
        
        if 'accents' in tasklist:
            accentClean=True
        else:
            accentClean=False
            
    print(timeEx)

    # timeEx = request.args.get('timeEx', default=None, type=None)
    
    # print('timex')
    # print(timeEx)
    
    # patternBasedClean = request.args.get('patternBasedClean')
    # pluralClean = request.args.get('pluralClean')
    # numbersClean = request.args.get('numbersClean')
    # accentClean = request.args.get('accentClean')
    
    
    # print(timeEx)
    
    # Aquí estoy forzando todos los parámetros a TRUE. Lo suyo sería que viniesen del servicio web:
    '''
    configurar el swagger json para meterle parametros y leerlos aquí: fijarse en el método /term
    por ejemplo, en el servicio poner el parametro de timex y que reciba 0/1 o true/false
    ejem:     timeEx=true
    
    el parámetro se lee aquí con:
        timeEx = request.args.get('timeEx')
        print(timeEx)
    
    '''
    
    clean_terms= postprocess.preprocessing_terms(termlist, Language, timeEx, patternBasedClean, pluralClean, numbersClean, accentClean)
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(clean_terms),  mimetype='application/json')


#Patricia Enriching
@REQUEST_API.route('/enriching_terminology', methods=['POST'])
def enrinching_terminology():
    

   # to read body of a POST OR PUT


    

        
    

    # print('Received:')
    # #print(Terms)
    # print(myterm.langIn)
    # print(myterm.langOut)
    # print(corpus)
    # print(myterm.schema)
    # #termlist=terms.split(', ')
    

    #iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True


    #myterm.freq = request.args.get('frequency')
    #iate = request.args.get('iate')
        
    json_data = request.json    
    resources= json_data['resources']  
    reslist=resources.split(', ')
    for r in reslist:
        if 'iate' in reslist:
            iate=True
        else:
            iate=False
            
        if 'eurovoc' in reslist:
            eurovoc=True
        else:
            eurovoc=False
       
        if 'unesco' in reslist:
            unesco=True
        else:
            unesco=False
    
        if 'wikidata' in reslist:
            wikidata=True
        else:
            wikidata=False
        
        if 'stw' in reslist:
            stw=True
        else:
            stw=False     
            
        if 'thesoz' in reslist:
            thesoz=True
        else:
            thesoz=False        
        
        if 'ilo' in reslist:
            ilo=True
        else:
            ilo=False 
            
        # if 'ilo' in reslist:
        #     ilo=True
        # else:
        #     ilo=False 
        
    
    
    # iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True
    # thesoz=True
    # stw=True
    # eurovoc = request.args.get('eurovoc')
    # unesco = request.args.get('unesco')
    # wikidata = request.args.get('wikidata')
    myterms=[]
    
    
    corpus = json_data['corpus']

    terms= json_data['terms']
    termlist=terms.split(', ')             
    
    all_data=[]   
    for t in termlist:
        print(t)
        myterm=Term.Term()
        myterm.term = t
        myterm.langIn = json_data['source_language']
        myterm.schema = json_data['schema_name']
        lang= json_data['target_languages']
        myterm.langOut=lang.split(', ')
        term_data= enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw, ilo)
        all_data.append(term_data)
        del myterm 
            

    # for myterm in myterms:
        
    #     print(myterm.term)
    #     term_data=enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw)
    #     all_data.append(term_data)

        
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(all_data),  mimetype='application/json')

def enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw, ilo):
    
    

    

    if iate == True:
        iateCode.enrich_term_iate(myterm, corpus)
        # print(myterm.term)
        # print(myterm.synonyms_iate)
        # print(myterm.translations_iate)
        # print(myterm.definitions_iate)
        
    if eurovoc == True:
        eurovocCode.enrich_term_eurovoc(myterm)
        #la api no funciona porque eurovocCode.get_definition no funciona, lo demás sí.
    if unesco == True:
        unescoCode.enrich_term_unesco(myterm)
    if wikidata==True:
        wikidataCode.enrich_term_wikidata(myterm, corpus)
    if thesoz == True:
        thesozCode.enrich_term_thesoz(myterm)
    if stw == True:
        stwCode.enrich_term_stw(myterm)
    if ilo == True:
        iloCode.enrich_term_ilo(myterm)
        
    data={
            'Source Term' : myterm.term,
            'IATE ID': myterm.iate_id,
            'IATE Synonyms': myterm.synonyms_iate,
            'IATE Translations': myterm.translations_iate,
            'IATE Definitions': myterm.definitions_iate, #tengo que revisar si este código está sobreescribiendo , problemas con diccionarios
            'EUROVOC ID': myterm.eurovoc_id,
            'EUROVOC Synonyms': myterm.synonyms_eurovoc,
            'EUROVOC Relations': myterm.eurovoc_relations,
            'EUROVOC Definitions': myterm.definitions_eurovoc,
            'EUROVOC Translations': myterm.translations_eurovoc,
            'UNESCO ID': myterm.unesco_id,
            'UNESCO Synonyms': myterm.synonyms_unesco,
            'UNESCO Translations': myterm.translations_unesco,
            'UNESCO Relations': myterm.unesco_relations,
            'WIKIDATA ID': myterm.wikidata_id,
            'WIKIDATA Synonyms': myterm.synonyms_wikidata,
            'WIKIDATA Translations': myterm.translations_wikidata,
            'WIKIDATA Definitions': myterm.definitions_wikidata,
            'WIKIDATA Relations': myterm.wikidata_relations,
            'THESOZ ID': myterm.thesoz_id,
            'THESOZ Synonyms': myterm.synonyms_thesoz,
            'THESOZ Translations': myterm.translations_thesoz,
            'THESOZ Definitions': myterm.definitions_thesoz,
            'THESOZ Relations': myterm.thesoz_relations,
            'STW ID': myterm.stw_id,
            'STW Synonyms': myterm.synonyms_stw,
            'STW Translations': myterm.translations_stw, 
            'STW Definitions': myterm.definitions_stw,
            'STW Relations': myterm.stw_relations,
            'ILO ID': myterm.ilo_id,
            'ILO Synonyms': myterm.synonyms_ilo,
            'ILO Translations': myterm.translations_ilo,
            'ILO Relations': myterm.ilo_relations
            
            }


    return data

@REQUEST_API.route('/relation_validation', methods=['POST'])
def relation_validation():
    
    return
