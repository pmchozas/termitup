
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


REQUEST_API = Blueprint('term_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route("/")
def index():
    pagetitle = "HomePage"
    return render_template("index.html")

@REQUEST_API.route('/term', methods=['GET'])
def term():
    termino = request.args.get('term')
    idioma = request.args.get('source_language')
    targets1 = request.args.get('target_languages')
    context1 = request.args.get('context')
    wsid = request.args.get('wsid')
    dataRetriever = request.args.get('relation_validation')
    scheme = request.args.get('schema')
    targets=targets1.split(' ')
    contextlist='' 
    contextFile=None 
    context=context1
    context=None
    ide=termiup_terminal.sctmid_creator()
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile+'.csv', 'r')
        contextF=csv.reader(file)
        contextFile=[]
        for i in contextF:
            contextFile.append([i[0], i[1],i[2],i[3]])
    
    else:
        contextFile=termiup_terminal.leerContextos(idioma, termino)

    jsonlist=termiup_terminal.haceJson(termino, idioma,targets)
    res=termiup_terminal.all(jsonlist, idioma, targets, context, contextFile,  wsid, scheme, dataRetriever,ide)
    print(res)
    return Response(json.dumps(res),  mimetype='application/json')
      
