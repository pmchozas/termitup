import requests
import json
from modules_api import wsidCode
import re
#from modules_api import Term

from unicodedata import normalize
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

# bearen token
def bearenToken(): 
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)




''' 
Intento de modularizar de Patri y Pablo

'''

    

def enrich_term_iate(myterm):
    
    # 1 consultas items # 2 creas los vectores con reate_langIn_vector
    request_term_to_iate_withTERM(myterm)
    # 3 hace el wsd con los vectores
    
    get_best_vector(myterm) #que llama a  wsidCode.get_vector_weights()
    # 4 con el mejor, te traes más datos
    #la id
    
    retrieve_best_vector_id(myterm)
    
    retrieve_data_from_best_vector(myterm)
        #traducciones, sinónimos y defis
    get_related_terms_iate(myterm)
    create_intermediate_ids(myterm)
    
    
    return myterm






# def request_term_to_iate(term, inlang, outlang):

#     auth_token=bearenToken()
#     hed = {'Authorization': 'Bearer ' +auth_token}
#     jsonList=[]
#     data = {"query": term,
#     "source": inlang,
#     "targets": outlang,
#     "search_in_fields": [    0     ],
#     "search_in_term_types": [   0,     1,     2,     3,     4
#     ],
#     "query_operator": 1
#     }
#     url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
#     response = requests.get(url, json=data, headers=hed)
#     response2=response.json()
#     #js=json.dumps(response2)
#     doc= json.dumps(response2, ensure_ascii=False,indent=1)
#     #print(doc)
    
#     ## no results
#     items=[]
#     vectors=[]
    
#     if response2['items'] is None:
#         return items, vectors
    
#     for item in response2['items']:
        
#         items.append(item)
#         vectors.append(create_langIn_vector(item, inlang,hed))
        
        
#     return items, vectors, response2  
        
def request_term_to_iate_withTERM(myterm):

    
    auth_token=bearenToken()
    hed = {'Authorization': 'Bearer ' +auth_token}
    jsonList=[]
    data = {"query": myterm.term,
    "source": myterm.langIn,
    "targets": myterm.langOut,
    "search_in_fields": [    0     ],
    "search_in_term_types": [   0,     1,     2,     3,     4
    ],
    "query_operator": 1
    }
    url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
    response = requests.get(url, json=data, headers=hed)
    response2=response.json()
    #js=json.dumps(response2)
    doc= json.dumps(response2, ensure_ascii=False,indent=1)
    #print(doc)
    
    ## no results
    items=[]
    vectors=[]
    
    if response2['items'] is None:
        return items, vectors
    
    for item in response2['items']:
        
        items.append(item)
        vectors.append(create_langIn_vector(item, myterm,hed))
        
    
    myterm.vectors= vectors
    myterm.items=items
    myterm.responseIate=response2
    return myterm  
    


def create_langIn_vector(item, myterm, hed):
    vector=[]
    domain_names = get_domain_names(item, hed)
    vector.extend(domain_names)
    try:
        if  'definition' in item['language'][myterm.langIn]:
         vector.append(item['language'][myterm.langIn]['definition'])
    except:
        pass
    
    
    try:
   
        for entry in item['language'][myterm.langIn]['term_entries']: 
            term_value = entry['term_value']
            vector.append(term_value)
            '''    
            if  'note' in entry:
                note= entry['note']['value']
                vector.append(note)
                
                '''
    except:
        pass
    cleanvector=[]
    for v in vector:
        cleanr = re.compile('<.*?>')
        cleanv = re.sub(cleanr, '', v)
        # print(cleanv)
        cleanvector.append(cleanv)
    return cleanvector
    
def get_best_vector(myterm):
    vector_weights=wsidCode.get_vector_weights(myterm)
    max_weight=max(vector_weights)
    myterm.index_max=vector_weights.index(max_weight)
    best_vector=myterm.vectors[myterm.index_max]
    return best_vector, myterm

def retrieve_best_vector_id(myterm):
    best_item= myterm.responseIate['items'][myterm.index_max]
    myterm.iate_id="https://iate.europa.eu/entry/result/"+str(best_item['id'])
    return myterm

def retrieve_data_from_best_vector(myterm):
#
    best_item= myterm.responseIate['items'][myterm.index_max]
    #print(best_item)
    cleanr = re.compile('<.*?>')
    for lang in best_item['language']:
        language=best_item['language'][lang]
        #print('lang '+lang)
        if lang not in myterm.definitions_iate:
                myterm.definitions_iate[lang]=[]
        
        if 'definition' in language.keys():
            definition=best_item['language'][lang]['definition']
            clean_def = re.sub(cleanr, '', definition)
            myterm.definitions_iate[lang].append(clean_def)
                
        if lang not in myterm.def_ref_iate:
            myterm.def_ref_iate[lang]=[]
            
        if 'definition_references' in language.keys():
            def_ref = best_item['language'][lang]['definition_references'][0]['text']
            clean_def_ref = re.sub(cleanr, '', def_ref)
            myterm.def_ref_iate[lang].append(clean_def_ref)
        
        if lang not in myterm.note_iate:
            myterm.note_iate[lang]=[]

        if 'note' in language.keys():
            note = best_item['language'][lang]['note']['value']
            clean_note = re.sub(cleanr, '', note)
            myterm.note_iate[lang].append(clean_note)


#aquí dependiendo de si lang es langin o langout será sinónimo o traducción. lo de arriba es común a cualquier idioma

#por cada term entry, meto su referencia


        for l in myterm.langOut:
            # print('l '+l)
            if lang == l:
                if l not in myterm.translations_iate:
                    myterm.translations_iate[l]=[]

                for entry in best_item['language'][lang]['term_entries']:
                    try:
                        
                        trans=entry['term_value']
                        trans_ref=entry['term_references'][0]['text']
                        clean_trans_ref = re.sub(cleanr, '', trans_ref)
                        myterm.translations_iate[lang].append(trans)
                        myterm.term_ref_iate[trans]=clean_trans_ref
                    except:
                            print('no term ref')
                            


        if lang == myterm.langIn:
            
            for e in best_item['language'][lang]['term_entries']:
                syn=e['term_value']
                if syn != myterm.term:
                    myterm.synonyms_iate.append(syn)
                    syn_ref=e['term_references'][0]['text']
                    clean_syn_ref = re.sub(cleanr, '', syn_ref)
                    myterm.term_ref_iate[syn]=clean_syn_ref


                    
    return myterm


#sacar términos relacionados de las definiciones y notas de uso

def get_related_terms_iate(myterm):
    for value in myterm.definitions_iate.values():
        for item in value:
            rel_id_list= re.findall("IATE:[0-9]{2,10}", item, re.DOTALL)
            for rel_id in rel_id_list:
                myterm.related_ids_iate.append(rel_id)
    
    for value in myterm.note_iate.values():
        for item in value:
            rel_id_list= re.findall("IATE:[0-9]{2,10}", item, re.DOTALL)
            for rel_id in rel_id_list:
                myterm.related_ids_iate.append(rel_id)
    
    myterm.related_ids_iate = list(dict.fromkeys(myterm.related_ids_iate))
    
    return myterm

def create_intermediate_ids(myterm):
    chars=['\'', '\"', '!', '<', '>', ',', '(', ')', '.']
    schema=myterm.schema.lower()
    if ' ' in schema:
        schema=schema.replace(' ', '-')
    for char in chars:
        schema=schema.replace(char, '')
    if len(myterm.synonyms_iate)>0:
        myterm.synonyms['iate']={}
        myterm.synonyms['iate'][myterm.langIn]=[]        
        for term in myterm.synonyms_iate:            
            syn_set = {}          
            syn = term
            if ' ' in syn:
                syn=syn.replace(' ', '-')
            for char in chars:
                syn=syn.replace(char, '')
            synid=schema+'-'+syn+'-'+myterm.langIn
            syn_set['syn-id']=synid.lower()
            syn_set['syn-value']=syn
            myterm.synonyms['iate'][myterm.langIn].append(syn_set)
            
            
    if len(myterm.translations_iate)>0:
        myterm.translations['iate']={}
        for lang in myterm.langOut:
            if lang in myterm.translations_iate.keys():
                myterm.translations['iate'][lang]=[]                
                for term in myterm.translations_iate[lang]:
                    trans_set = {}
                    if ' 'in term:
                        term=term.replace(' ', '-')
                    for char in chars:
                        term=term.replace(char, '')
                    transid=schema+'-'+term+'-'+lang
                    trans_set['trans-id']=transid.lower()
                    trans_set['trans-value']=term
                    myterm.translations['iate'][lang].append(trans_set)
    
    if len(myterm.definitions_iate)>0:
        myterm.definitions['iate']={}
        for lang in myterm.definitions_iate.keys():
            myterm.definitions['iate'][lang]=[]
            for defi in myterm.definitions_iate[lang]:
                def_set = {}
                defid=myterm.term+'-'+lang+'-def'
                def_set['def-id']=defid.lower()
                def_set['def-value']=defi
                myterm.definitions['iate'][lang].append(def_set)

    return myterm


#karens
def get_domain_names(item, hed):
    dict_domains=[]
    code_domain=item['domains']
    list_code=[]
    for i in range(len(code_domain)):
        code=code_domain[i]['code']
        list_code.append(code)
    
    domain=[]
    url= 'https://iate.europa.eu/em-api/domains/_tree'
    response = requests.get(url,  headers=hed)
    response2=response.json()
    its=response2['items']

    for i in range(len(its)):
        code=its[i]['code']
        name=its[i]['name']
        dict_domains.append([name,code])
        subdomain_iate(its[i], dict_domains)

    for i in list_code:
        for j in range(len(dict_domains)):
            code=dict_domains[j]
            if(i == code[1]):
                domain.append(code[0])
    return(domain) 

def domain_iate(item, data, hed):
    dict_domains=[]
    code_domain=item['domains']
    list_code=[]
    for i in range(len(code_domain)):
        code=code_domain[i]['code']
        list_code.append(code)
    
    domain=[]
    url= 'https://iate.europa.eu/em-api/domains/_tree'
    response = requests.get(url,  headers=hed)
    response2=response.json()
    its=response2['items']

    for i in range(len(its)):
        code=its[i]['code']
        name=its[i]['name']
        dict_domains.append([name,code])
        subdomain_iate(its[i], dict_domains)

    for i in list_code:
        for j in range(len(dict_domains)):
            code=dict_domains[j]
            if(i == code[1]):
                domain.append(code[0])
    return(domain)  


def subdomain_iate(its, dict_domains):
    if('subdomains' in its):
        sub=its['subdomains']
        if(len(sub)):
            for j in range(len(sub)):
                code=sub[j]['code']
                name=sub[j]['name']
                dict_domains.append([name,code])
                subdomain_iate(sub[j], dict_domains)
    return(dict_domains)



