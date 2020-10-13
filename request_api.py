
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
import time
import termiup_terminal
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
    json_data = request.json
    Corpus = json_data['corpus']  
    Language = json_data['language']
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
    json_data = request.json
    Terms = json_data['terms']
    Language = json_data['language']
    print('Received:')
    #print(Terms)
    print(Language)

    termlist=Terms.split(', ')
    

    #Pablo proposal -------------------------------------
    '''
    timeEx=True
    patternBasedClean=True
    pluralClean=True
    numbersClean=True
    accentClean=True
    '''

    timeEx = request.args.get('timeEx')
    patternBasedClean = request.args.get('patternBasedClean')
    pluralClean = request.args.get('pluralClean')
    numbersClean = request.args.get('numbersClean')
    accentClean = request.args.get('accentClean')
    
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


#Karen Patricia Enriching
@REQUEST_API.route('/enriching_terminology', methods=['POST'])
def enrinching_terminology():
    
    
   # to read body of a POST OR PUT
    myterm=Term.Term()
    json_data = request.json
    myterm.term = json_data['terms']
    myterm.langIn = json_data['source_language']
    
    corpus = json_data['corpus']
    myterm.schema = json_data['schema_name']  
    
    
    lang=json_data['target_language']
    myterm.langOut=lang.split(', ')
    

    print('Received:')
    #print(Terms)
    print(myterm.langIn)
    print(myterm.langOut)
    print(corpus)
    print(myterm.schema)
    #termlist=terms.split(', ')
    

    #iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True


    #myterm.freq = request.args.get('frequency')
    #iate = request.args.get('iate')
    iate=True
    eurovoc=True
    unesco=True
    wikidata=True
    thesoz=True
    stw=True
    # eurovoc = request.args.get('eurovoc')
    # unesco = request.args.get('unesco')
    # wikidata = request.args.get('wikidata')




    

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
            'STW Relations': myterm.stw_relations
            
            }
        

        
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(data),  mimetype='application/json')

