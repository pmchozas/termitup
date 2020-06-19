import requests
import json
def wsidFunction(termIn, context,   definitions):
    #print(termIn,'|', context.lower(),'|',   definitions)
    defiMax=''
    idMax=''
    posMax=0
    code=0

    if(context):
        pesos=[]
        context=context.lower()
        start=context.index(termIn.lower())
        longTerm=len(termIn)
        end=context.index(termIn.lower())+longTerm
        
        listdef=definitions[0]
        listIde=definitions[1]
        print('CONTEXT---',context)
        print('START---', start)
        print('END---', end)
        print('DEINITIONS---',definitions[0])
        print('----Entrando WSDI----')
        response = requests.post('http://el-flask-88-staging.cloud.itandtel.at/api/disambiguate_demo',
                params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitions[0]}, 
                headers ={'accept': 'application/json',
                    'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
            }
        )
        code=response.status_code
        print('CODE WSID',code)
        #print('response', response)
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
            print(pesos)
            if(code==200):
                max_item = max(pesos)
                #print(max_item)
                posMax=pesos.index(max_item)
                #print(posMax)
                if(len(listdef)>0 and (posMax)<len(listdef)):
                    #print(len(listdef), posMax)
                    defiMax=listdef[posMax]
                else:
                    defiMax=''
                if(len(listIde)>0 and (posMax)<len(listIde)):
                    idMax=listIde[posMax]
                else:
                    idMax=''
        except json.decoder.JSONDecodeError:
            pass
    
    return(defiMax, idMax,code)
        