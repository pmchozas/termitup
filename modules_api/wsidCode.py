#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 17:57:46 2020

@author: pmchozas
"""


import requests
import json
from modules_api import conts_log
from time import time
from modules_api import Term


'''
la función get_term_position devuelve la posición del término en el corpus, que es requerida por invoke_wsid
'''
def get_term_position(myterm):
    context=myterm.context
    myterm.start=context.index(myterm.term)
    length=len(myterm.term)
    myterm.end=myterm.start+length
    return(myterm)
    

'''
get_vector_weights es una versión simplificada de wsid_function creada por Patri para la Api
'''
def get_vector_weights(myterm):
    get_term_position(myterm)
    auth_token = getToken()
    
    start=myterm.start
    end=myterm.end
    hed = {
                   'Authorization': 'Bearer ' + auth_token, 
                   'accept': 'application/json',
                   'Content-Type': 'application/json'
    }    
    valuelist=list()
    #la llamada va fuera del for
    url_lkgp_status='https://apis.lynx-project.eu/api/entity-linking/disambiguate_demo?'
    
    for vector in myterm.vectors:
        # print(vector)
        params={'context': myterm.context, 'start_ind': start, 'end_ind': end,  'senses': vector}
        # print(params)
        response = requests.post(url_lkgp_status,params=params,headers =hed)
        # print(response)
        #response = requests.get('https://apim-88-staging.cloud.itandtel.at/api/entity-linking', params=params)
        #code=response.status_code
        #print(response)
        #print(code)
        #req = response.request
        #command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        #method = req.method
        #uri = req.url
        #data = req.body
        #headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
        #headers = " -H ".join(headers)
        #print(command.format(method=method, headers=headers, data=data, uri=uri))
        # print('value get_vector_weights')
        
        value=response.json()
        # print(value)
        valuelist.append(value[0])
    

    return valuelist   



def getToken():
    f = open("modules_api/client_id.txt",encoding="utf8")
    client_id=f.read().strip()
    f = open("modules_api/client_secret.txt",encoding="utf8")
    client_secret=f.read().strip()
    url_authen='https://keycloak-secure-88-staging.cloud.itandtel.at/auth/realms/Lynx/protocol/openid-connect/token'
    grant_type = "client_credentials"
    data = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret
        #"scope": scope
    }
    auth_response = requests.post(url_authen, data=data)
    # Read token from auth response
    auth_response_json = auth_response.json()
    auth_token = auth_response_json["access_token"]
    return auth_token



def wsidFunction(termIn, listcontext,   definitions):
    #print(termIn,'|', context.lower(),'|',   definitions)
    start_time=time()
    conts_log.information('-----WSID----','')
    defiMax=str
    uri_max=str
    index_max=0
    code=0
    index_max_list=list()
    posDefs=list()
    pesos_max_list=list()
    uri_max_list=list()
    if(listcontext):
        cont=0
        for s in definitions[0]:
            conts_log.information('Senses: '+s,'')
            #print('Senses: ',s)

        for context in listcontext:
            pesos=[]
            context=context.lower()
            conts_log.information('Context: '+context,'')
            termIn=termIn.lower()
            start=context.index(termIn)
            longTerm=len(termIn)
            end=context.index(termIn.lower())+longTerm
            
            listdef=definitions[0]
            listIde=definitions[1]
            
            #print('CONTEXT---',cont,context)
            #print('START---', start)
            #print('END---', end)
            #print('SENSES---',definitions[0])
            #print('----Entrando WSDI----')
            auth_token = getToken()
            #print(auth_token)
            hed = {
                   'Authorization': 'Bearer ' + auth_token, 
                   'accept': 'application/json',
                   'Content-Type': 'application/json'
                  }
                
            url_lkgp_status='https://apim-88-staging.cloud.itandtel.at/api/entity-linking/disambiguate_demo?'
            params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitions[0]}
            response = requests.post(url_lkgp_status,params=params,headers =hed)
            #response = requests.get('https://apim-88-staging.cloud.itandtel.at/api/entity-linking', params=params)
            code=response.status_code
            #code=200
            #print('CODE WSID',code)
            #print('response', response)
            if(code!=200):
                conts_log.error('Wsid code: ', code)
            req = response.request

            command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
            method = req.method
            uri = req.url
            data = req.body
            headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
            headers = " -H ".join(headers)
            #print(command.format(method=method, headers=headers, data=data, uri=uri))
            
            try:
                pesos=response.json()
                #print(pesos)
                if(code==200):
                    peso_max = max(pesos)#se obtiene el peso maximo 
                    #print('1. ', peso_max)
                    index_max=pesos.index(peso_max)#se obtiene el indice del peso maximo
                    #print('2. ', index_max)
                    index_max_list.append(index_max)#lista con indices de pesos maximos
                    #print('3. ', index_max_list)
                    pesos_max_list.append(pesos[index_max])#lista con pesos maximos 
                    #print('4. ', pesos_max_list)

                    if(len(listdef)):
                        defiMax=listdef[index_max]#definicion maxima 
                        #print('5. ', defiMax)
                        posDefs.append(defiMax)#lista con definiciones maximas
                        #print('6. ', posDefs)
                    
                    if(len(listIde)):
                        uri_max=listIde[index_max]#uri maximo
                        uri_max_list.append(uri_max)#lista con uri maximas
                        #print('7. ', uri_max)
                        #print('8. ', uri_max_list)
                    
            except json.decoder.JSONDecodeError:
                pass
            cont=cont+1
    #print(index_max, defiMax, uri_max)
    max1=int
    valid=str
    valid_context=str
    if(len(index_max_list)):
        max1=max(index_max_list)#maximo de todos los pesos maximos 
        index_max1=index_max_list.index(max1)
        valid=posDefs[index_max1]
        uri_max=uri_max_list[index_max1]

        #print('9. ', max1, index_max1, valid, uri_max)
        max2=max(pesos_max_list)
        index_max2=pesos_max_list.index(max2)
        #contx=pesos_max_list[max2]
        valid_context=listcontext[index_max2]

        #print('10. ', max2, index_max2, valid_context)


        #print('--------->',max1, valid, uri_max, valid_context)
    #print('Result context: '+str(valid_context), 'Result sense: '+str(valid))
    conts_log.information('Result context: '+str(valid_context), 'Result sense: '+str(valid))
    elapsed_time=time()-start_time
    conts_log.information('Time wsid: '+str(elapsed_time),'')
    conts_log.information('-------------','')
    return(valid, uri_max,code, valid_context)
        