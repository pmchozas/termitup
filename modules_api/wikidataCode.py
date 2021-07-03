import requests
from modules_api import wsidCode 
from modules_api import extrafunctions
import json
from modules_api import eurovocCode


def enrich_term_wikidata(myterm):
    create_wikidata_vectors(myterm)
    
    get_langIn_data_from_best_vector(myterm)

    get_langOut_data_from_best_vector(myterm)
    
    get_relations_from_best_vector(myterm)
    
    create_intermediate_ids(myterm)
    return(myterm)

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
                term_uri=bindings[i]['item']['value'].split("/")[-1]
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

def get_term_position(myterm):
    context=myterm.context
    myterm.start=context.index(myterm.term)
    length=len(myterm.term)
    myterm.end=myterm.start+length
    return(myterm)


def get_vector_weights(myterm):
    get_term_position(myterm)
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
        url_lkgp_status='http://entity-linking-lynx.apps.cybly.cloud/disambiguate_demo?'
        params={'context': myterm.context, 'start_ind': start, 'end_ind': end,  'senses': value}
        print(params)
        response = requests.post(url_lkgp_status,params=params,headers =hed)
        #response = requests.get('https://apim-88-staging.cloud.itandtel.at/api/entity-linking', params=params)
        code=response.status_code
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
def get_best_vector_id(myterm):
    vector_weights=get_vector_weights(myterm)
    max_weight=max(vector_weights)

    index_max=vector_weights.index(max_weight)
    best_vector=list(myterm.wikidata_vectors)[index_max]
    myterm.wikidata_id="https://www.wikidata.org/wiki/"+best_vector
    
    return best_vector, myterm
   #
    # return best_vector, myterm
                    
    
def get_langIn_data_from_best_vector(myterm):
    results=get_best_vector_id(myterm)
    best_vector=results[0]
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    retrieve_query = """
    SELECT DISTINCT * WHERE {
     wd:WDTMID rdfs:label ?label.
      FILTER (lang(?label) = "LANG")
      OPTIONAL {
        wd:WDTMID schema:description ?desc.
        FILTER (lang(?label) = lang(?desc))
      }
       OPTIONAL {
        wd:WDTMID skos:altLabel ?alt.
        FILTER (lang(?label) = lang(?alt))
      }
    }ORDER BY ?lang
    """
    query = retrieve_query.replace("WDTMID", best_vector).replace("LANG", myterm.langIn)

              
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json()     
    if len(data['results']['bindings']) != 0:
        bindings=data['results']['bindings']
        for i in range(len(bindings)):

                if 'alt' in bindings[i]:
                    alt=bindings[i]['alt']['value']
                    myterm.synonyms_wikidata.append(alt)
                
                if 'desc' in bindings[i]:
                    defi=bindings[i]['desc']['value']
                    if myterm.langIn not in myterm.definitions_wikidata:
                        myterm.definitions_wikidata[myterm.langIn]=[]
                        myterm.definitions_wikidata[myterm.langIn].append(defi)
                    if myterm.langIn in myterm.definitions_wikidata:
                        if defi not in myterm.definitions_wikidata[myterm.langIn]:
                            myterm.definitions_wikidata[myterm.langIn].append(defi)
                else:
                    continue      
    return myterm
                
    
    
def get_langOut_data_from_best_vector(myterm):
    results=get_best_vector_id(myterm)
    best_vector=results[0]
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    for lang in myterm.langOut:
        retrieve_query = """
        SELECT DISTINCT * WHERE {
         wd:WDTMID rdfs:label ?label.
          FILTER (lang(?label) = "LANG")
          OPTIONAL {
            wd:WDTMID schema:description ?desc.
            FILTER (lang(?label) = lang(?desc))
          }
           OPTIONAL {
            wd:WDTMID skos:altLabel ?alt.
            FILTER (lang(?label) = lang(?alt))
          }
        }ORDER BY ?lang
        """
        query = retrieve_query.replace("WDTMID", best_vector).replace("LANG", lang)
        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
        data = r.json()     
        
        if len(data['results']['bindings']) != 0:
            bindings=data['results']['bindings']
            
            for i in range(len(bindings)):
                
                if 'label' in bindings[i]:
                    label=bindings[i]['label']['value']
                    if lang not in myterm.translations_wikidata:
                        myterm.translations_wikidata[lang]=[]
                        myterm.translations_wikidata[lang].append(label)
                    if lang in myterm.translations_wikidata:
                        if label not in myterm.translations_wikidata[lang]:
                            myterm.translations_wikidata[lang].append(label)
                if 'alt' in bindings[i]:
                    alt=bindings[i]['alt']['value']
                    if lang not in myterm.translations_wikidata:
                        myterm.translations_wikidata[myterm.langIn]=[]
                        myterm.translations_wikidata[lang].append(alt)
                    if lang in myterm.translations_wikidata:
                        if alt not in myterm.translations_wikidata[lang]:
                            myterm.translations_wikidata[lang].append(alt)
                        
                if 'desc' in bindings[i]:
                    defi=bindings[i]['desc']['value']
                    if lang not in myterm.definitions_wikidata:
                        myterm.definitions_wikidata[lang]=[]
                        myterm.definitions_wikidata[lang].append(defi)
                    if lang in myterm.definitions_wikidata:
                       if defi not in myterm.definitions_wikidata[lang]:
                           myterm.definitions_wikidata[lang].append(defi)
            else:
                continue   
    
    return myterm
    
    
    
    
    
def get_relations_from_best_vector(myterm):
    myterm.wikidata_relations['narrower']=[]
    myterm.wikidata_relations['broader']=[]
    results=get_best_vector_id(myterm)
    best_vector=results[0]
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    narrower_query = """
    SELECT DISTINCT ?naTerm WHERE {
        ?naTerm wdt:P279 wd:WDTMID .
      }
    """

    broader_query = """
    SELECT DISTINCT ?brTerm WHERE {
        wd:WDTMID wdt:P279 ?brTerm .   
    }
    """
    na_query = narrower_query.replace("WDTMID", best_vector)
    br_query = broader_query.replace("WDTMID", best_vector)
    na = requests.get(url, params={'format': 'json', 'query': na_query}, headers=headers)
    br = requests.get(url, params={'format': 'json', 'query': br_query}, headers=headers)
    
    na_data = na.json() 
    br_data = br.json() 
    
    if len(br_data['results']['bindings']) != 0:
        br_bindings=br_data['results']['bindings']    
        for b in br_bindings:
            myterm.wikidata_relations['broader'].append(b['brTerm']['value'])
        
    if len(na_data['results']['bindings']) != 0:
        na_bindings=na_data['results']['bindings']
        for n in na_bindings:
            myterm.wikidata_relations['narrower'].append(n['naTerm']['value'])

            
        #print(na_bindings)
    

            
    return myterm


def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_wikidata)>0:
        myterm.synonyms['wikidata']={}
        myterm.synonyms_ontolex['wikidata']={}
        myterm.synonyms['wikidata'][myterm.langIn]=[]  
        myterm.synonyms_ontolex['wikidata'][myterm.langIn]=[]
        for term in myterm.synonyms_wikidata:            
            syn_set = {}          
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn.replace('-', ' ')
            myterm.synonyms['wikidata'][myterm.langIn].append(syn_set)
            myterm.synonyms_ontolex['wikidata'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_wikidata)>0:
        myterm.translations['wikidata']={}
        myterm.translations_ontolex['wikidata']={}
        for lang in myterm.langOut:
            if lang in myterm.translations_wikidata.keys():
                myterm.translations['wikidata'][lang]=[]        
                myterm.translations_ontolex['wikidata'][lang]=[] 
                for term in myterm.translations_wikidata[lang]:
                    trans_set = {}
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term.replace('-', ' ')
                    myterm.translations_ontolex['wikidata'][lang].append(trans_set)
                    if len(myterm.translations['wikidata'][lang])<=0:
                        myterm.translations['wikidata'][lang].append(trans_set)
                    else:
                        if 'wikidata' in myterm.synonyms:
                            if lang in myterm.synonyms['wikidata']:
                                myterm.synonyms['wikidata'][lang].append(trans_set)
                            else:
                                myterm.synonyms['wikidata'][lang]=[]
                                myterm.synonyms['wikidata'][lang].append(trans_set)
                        else:
                            myterm.synonyms['wikidata']={}
                            myterm.synonyms['wikidata'][lang]=[]
                            myterm.synonyms['wikidata'][lang].append(trans_set)
    
    if len(myterm.definitions_wikidata)>0:
        myterm.definitions['wikidata']={}
        for lang in myterm.definitions_wikidata.keys():
            myterm.definitions['wikidata'][lang]=[]
            for defi in myterm.definitions_wikidata[lang]:
                def_set = {}
                defid=myterm.term+'-'+lang+'-def'
                def_set['def-id']=defid.lower()
                def_set['def-value']=defi
                myterm.definitions['wikidata'][lang].append(def_set)

    return myterm

'''
def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_wikidata)>0:
        for term in myterm.synonyms_wikidata:
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            myterm.syn_wikidata_ids[term]=synid.lower()
    
    if len(myterm.translations_wikidata)>0:
        for lang in myterm.langOut:
            if lang in myterm.translations_wikidata.keys():
                for term in myterm.translations_wikidata[lang]:
                    trans = term
                    if ' 'in trans:
                        trans=trans.replace(' ', '-')
                    for char in chars:
                        trans=trans.replace(char, '')
                    transid=schema+'-'+trans+'-'+lang
                    myterm.trans_wikidata_ids[term]=transid.lower()

    return myterm
   ''' 
    
    
    
    