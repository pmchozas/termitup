import requests
import json
from modules_api import check_term
import re
from unicodedata import normalize
from modules_api import wsidCode
from modules_api import extrafunctions
from modules_api import jsonFile
from modules_api import eurovocCode
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

def prefLabel_unesco(termSearch, lang, targets, outFile, scheme, file_schema, rels): #recoge la uri del termino a buscar
    term='"^'+termSearch+'$"'
    for targ in targets:
        lang='"'+targ+'"'
        file={}
        url = "http://sparql.lynx-project.eu/"
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label ?prefEN
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
        ?c a skos:Concept .
        ?c ?p ?label. 
        ?c skos:prefLabel ?prefEN.
          FILTER regex(?label, """+term+""", "i")

          
          FILTER (lang(?prefEN) = """+lang+""")

          FILTER (?p IN ( skos:prefLabel, skos:altLabel ) )
          

        }  
        }
        """
    headers = {'content-type': 'text/html; charset=UTF-8'}
    
    r=requests.get(url, params={'format': 'json', 'query': query})
    rjson=json.loads(r.text)

    uri=''  
    if('results' in rjson.keys()):
        results=rjson['results']
        bindings=results['bindings']
        for b in range(len(bindings)):
            uri=bindings[b]['c']['value']
            #print('-se encontro unesco exacto-')
            if(rels!=2):
                if(len(outFile['skos-xl:prefLabel'][0]['source'])==0):
                    outFile['skos-xl:prefLabel'][0]['source']=uri
                    outFile['closeMatch'].append(uri)
            #print(termSearch) 
            print(termSearch, lang[1:3])           
            outFile=extrafunctions.property_add( termSearch, lang[1:3], outFile, 'prefLabel',rels,uri) 
            outFile=altLabel_unesco(termSearch, lang[1:3], targets, outFile, scheme, file_schema, rels)   
            if(rels==1):  
                outFile=relation_unesco(uri, lang, outFile, targets, scheme, file_schema)
    
    return(outFile)

def altLabel_unesco(termSearch, lang, targets, outFile, scheme, file_schema, rels): #recoge la uri del termino a buscar
    term='"^'+termSearch+'$"'
    lang='"'+lang+'"'
    file={}
    url = "http://sparql.lynx-project.eu/"
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?c ?label
    WHERE {
    GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
    ?c a skos:Concept .
    ?c ?p ?label. 
      FILTER regex(?label, """+term+""", "i" )
      FILTER (lang(?label) = """+lang+""") 
      FILTER (?p IN (skos:altLabel ) )

    }  
    }
    """
    headers = {'content-type': 'text/html; charset=UTF-8'}
    
    r=requests.get(url, params={'format': 'json', 'query': query})
    rjson=json.loads(r.text)

    uri=''  
    if('results' in rjson.keys()):
        results=rjson['results']
        bindings=results['bindings']
        for b in range(len(bindings)):
            uri=bindings[b]['c']['value']
            print(termSearch, lang[1:3])
            outFile=extrafunctions.property_add( termSearch, lang[1:3], outFile, 'altLabel',rels,uri)    
            
    return(outFile)

def relation_unesco(uri, lang, outFile, targets, scheme, file_schema):
    
    relations=['broader', 'narrower', 'related']
    url=("http://sparql.lynx-project.eu/")
    for relation in relations:
        if(relation not in outFile.keys()):
            outFile[relation]=[]
        query2="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
        VALUES ?c {<"""+uri+"""> }
        VALUES ?relation { skos:"""+relation+""" } 
        ?c a skos:Concept .
        ?c ?relation ?label .    
        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query2})
        rjsonrel=json.loads(r.text)

        
        uri_re=[]  
        if('results' in rjsonrel.keys()):
            results=rjsonrel['results']
            bindings=results['bindings']
            for b in range(len(bindings)):
                uri_re=bindings[b]['label']['value']
                outFile=termRel_unesco(uri_re, lang, outFile, relation, targets, scheme, file_schema) 
     
    return(outFile)

def termRel_unesco(uri_re, lang, outFile, relation, targets, scheme, file_schema):
    url=("http://sparql.lynx-project.eu/")
    query3="""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?c ?label
    WHERE {
    GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
    VALUES ?c { <"""+uri_re+"""> }
    VALUES ?searchLang { """+lang+""" undef } 
    VALUES ?relation { skos:prefLabel  } 
    ?c a skos:Concept . 
    ?c ?relation ?label . 
    filter ( lang(?label)=?searchLang )
    }
    }
    """
    r=requests.get(url, params={'format': 'json', 'query': query3})
    rjsonterm=json.loads(r.text)

    term_rel=''  
    if('results' in rjsonterm.keys()):
        results=rjsonterm['results']
        bindings=results['bindings']

        for b in range(len(bindings)):
            term_rel=bindings[b]['label']['value']
            #print(uri_re, term_rel)

            verify=check_term.checkTerm(lang, term_rel, relation, targets,'')
            ide=verify[0]
            termSearch=verify[1]
            if(termSearch!='1'):
                originalIde=outFile['@id']
                eurovocCode.eurovoc_file(termSearch+'unesco', ide, relation,uri_re, lang[1:3], scheme,  originalIde, file_schema, outFile,targets)

            full=jsonFile.full_rels(outFile, relation)
            #print(full)
            cadena = re.sub('[/,+.;:/)([]]*', '',  term_rel)
            n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                normalize( "NFD", cadena), 0, re.I
            )
            n = normalize( 'NFC', n)
            uri=n.replace(' ','-')+'-'+lang[1:3]

            if(uri not in full):
                #print(full)
                logging.info('FOUND (Unesco-relation-'+relation+'): '+cadena+' lang: '+lang[1:3]) 
                outFile[relation].append(uri)



    #print(outFile)
    return(outFile)
			    		
			    		

