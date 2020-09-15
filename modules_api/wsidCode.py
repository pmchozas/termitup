import requests
import json
from modules_api import conts_log
from time import time

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
            response = requests.post('http://el-fastapi-88-staging.cloud.itandtel.at/docs#/WSD/disambiguate_demo_disambiguate_demo_post',
                    params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitions[0]}, 
                    headers ={'accept': 'application/json',
                        'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
                }
            )
            code=response.status_code
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
        
