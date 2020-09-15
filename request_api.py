
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
    timeEx=True
    patternBasedClean=True
    pluralClean=True
    numbersClean=True
    accentClean=True
    
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
    
    '''
    to read body of a POST OR PUT
    '''
    json_data = request.json
    Terms = json_data['terms']
    Inlang = json_data['source_language']
    Outlang = json_data['target_language']
    Corpus = json_data['corpus']
    Schema = json_data['schema_name']  

    print('Received:')
    #print(Terms)
    print(Inlang)
    print(Outlang)
    print(Corpus)
    print(Schema)
    termlist=Terms.split(', ')
    

    #Pablo proposal -------------------------------------
    iate=True
    eurovoc=True
    unesco=True
    wikidata=True
    
    # Aquí estoy forzando todos los parámetros a TRUE. Lo suyo sería que viniesen del servicio web:
    '''
    configurar el swagger json para meterle parametros y leerlos aquí: fijarse en el método /term
    por ejemplo, en el servicio poner el parametro de timex y que reciba 0/1 o true/false
    ejem:     timeEx=true
    
    el parámetro se lee aquí con:
        timeEx = request.args.get('timeEx')
        print(timeEx)
    
    '''
    
    enriching_terms= main.enriching_terms(termlist, Inlang, Outlang, iate, eurovoc, unesco, wikidata, schema)
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(clean_terms),  mimetype='application/json')