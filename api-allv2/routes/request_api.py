
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
from routes import termiup_terminal


REQUEST_API = Blueprint('term_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route("/")
def index():
    pagetitle = "HomePage"
    return render_template("index.html")

@REQUEST_API.route('/term/<string:term>/<string:source_language>/<string:target_languages>/<string:context>/<string:wsid>/<string:relation_validation>/<string:schema>', methods=['GET'])
def get(term,source_language,target_languages,context,wsid,relation_validation,schema):
    

    scheme=schema
    dataRetriever=relation_validation
    termino=term
    idioma=source_language
    targets=target_languages.split(' ')
    contextlist='' 
    contextFile=None 
    lista=[]
    lista.append(termino)
    context=None
    print(termino,'--',context)
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        contextF=csv.reader(file)
        contextFile=[]
        for i in contextF:
            contextFile.append([i[0], i[1],i[2],i[3]])
    
    else:
        print('entro')
        print(idioma)
        contextFile=termiup_terminal.leerContextos(idioma, termino)

    jsonlist=termiup_terminal.haceJson(lista, idioma,targets)
    res=termiup_terminal.all(jsonlist, idioma, targets, context, contextFile,  wsid, scheme, dataRetriever)
    print(res)
    return jsonify(res),200
      
