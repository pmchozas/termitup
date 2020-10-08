import requests
from modules_api import wsidCode 
from modules_api import extrafunctions
import json
from modules_api import eurovocCode




    

def create_wikidata_vectors(myterm):
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    retrieve_query = """
        SELECT * {
       ?item rdfs:label "TERM"@LANG.
       ?item schema:description ?desc.
      FILTER (lang(?desc) = "LANG")
      OPTIONAL {
        ?item skos:altLabel ?altLabel.
      FILTER (lang(?altLabel) = "LANG")  
      }
      }
    """
    query = retrieve_query.replace("TERM", myterm.term).replace("LANG", myterm.langIn)

              
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json()    

    urilist=list()
    try:
        if len(data['results']['bindings']) != 0:
            #print('-se encontro wiki-')
            bindings=data['results']['bindings']
            for i in range(len(bindings)):
                term_uri=bindings[i]['item']['value']
                urilist.append(term_uri)
                for uri in urilist:
                    if uri not in myterm.wikidata_vectors:
                        myterm.wikidata_vectors[uri]=[]
                        if 'altLabel' in bindings[i]:
                            alt=bindings[i]['altLabel']['value']
                            myterm.wikidata_vectors[uri].append(alt)
                        if 'desc' in bindings[i]:
                            defi=bindings[i]['desc']['value']
                            myterm.wikidata_vectors[uri].append(defi)
                        else:
                            continue
                    
    except:
        pass
    
    return myterm

def get_term_position(myterm, corpus):
    myterm.start=corpus.index(myterm.term)
    length=len(myterm.term)
    myterm.end=myterm.start+length
    return(myterm)


def get_vector_weights(myterm, corpus):
    get_term_position(myterm, corpus)
    #auth_token = getToken()
    
    start=myterm.start
    end=myterm.end
    hed = {
                #   'Authorization': 'Bearer ' + auth_token, 
                   'accept': 'application/json'
                #   'Content-Type': 'application/json'
    }    
    valuelist=list()
    
    for key, value in myterm.wikidata_vectors.items() :
        url_lkgp_status='http://el-fastapi-88-staging.cloud.itandtel.at/disambiguate_demo?'
        params={'context': corpus, 'start_ind': start, 'end_ind': end,  'senses': value}
        #print(params)
        response = requests.post(url_lkgp_status,params=params,headers =hed)
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
        data=response.json()
        
        valuelist.append(data[0])
    return valuelist   
#esto no funciona 
def get_best_vector_id(myterm, corpus):
    vector_weights=get_vector_weights(myterm, corpus)
    max_weight=max(vector_weights)
    print(max_weight)
    myterm.index_max=vector_weights.index(max_weight)
    print(myterm.index_max)
    best_vector=myterm.wikidata_vectors[myterm.index_max]
    # return best_vector, myterm
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    