import requests
def reduction_defs(list_in):
    list_out=[]
    for i in list_in:
        spl=i.split(' ')
        if(len(spl)>250):
            list_out.append(''.join(spl[:250]))
        else:
            list_out.append(i)
        #print(out)
    return(list_out)

def wsidFunction(termIn, context,   definitions):
    
    defiMax=''
    idMax=''
    posMax=0
    code=0

    if(context):
        context=context.lower().replace('\n', '')
        pesos=[]
        start=context.index(termIn)
        longTerm=len(termIn)
        end=context.index(termIn)+longTerm
        listdef=reduction_defs(definitions[0])
        listIde=definitions[1]
        definitionsJoin=', '.join(listdef)
        print('CONTEXT---',context)
        print('START---', start)
        print('END---', end)
        print('DEINITIONS---',definitionsJoin)
        print('----Entrando WSDI----')
        response = requests.post('http://el-flask-88-staging.cloud.itandtel.at/api/disambiguate_demo',
                params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
                headers ={'accept': 'application/json',
                    'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
            }
        )
        code=response.status_code
        print('CODE WSID',code)
        print('response', response)
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
                max_item = max(pesos, key=int)
                posMax=pesos.index(max_item)
                if(len(listdef)>0 and (posMax)<len(listdef)):
                    #print(len(listdef), posMax)
                    defiMax=listdef[posMax-1]
                else:
                    defiMax=''
                if(len(listIde)>0 and (posMax)<len(listIde)):
                    idMax=listIde[posMax-1]
                else:
                    idMax=''
        except json.decoder.JSONDecodeError:
            print('JSONDecodeError WSID')
            pesos=[]
            defiMax=''
            idMax=''
            
    print('----Saliendo WSDI----')
    return(defiMax, idMax,code)
        