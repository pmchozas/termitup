
from flask import jsonify, abort, request, Blueprint
from flask import Flask
import requests
from flask_restplus import Resource, Api, fields, reqparse
import json
from random import randint #libreria para random
import re
import os
from os import listdir
from os.path import isfile, isdir
import time
from routes import termiup


REQUEST_API = Blueprint('term_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/term/<string:termino>,<string:idioma>,<string:targets>,<string:context>,<string:wsid>,<string:dataRetriever>,<string:schema>', methods=['GET'])
def get(termino,idioma,targets,context,wsid,dataRetriever,schema):
    
    targets=targets.split(' ')
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
        contextFile=termiup.leerContextos(idioma, termino)

    jsonlist=termiup.haceJson(lista, idioma,targets)
    res=termiup.all(jsonlist, idioma, targets, context, contextFile,  wsid, schema, dataRetriever)
    print(res)
    return jsonify(res),200
      
