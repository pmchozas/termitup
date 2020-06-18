import requests
import json
import check_term
import re
from unicodedata import normalize
import wsidCode
import extrafunctions
import jsonFile
import eurovocCode
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

def prefLabel_unesco(termSearch, lang, targets, outFile, scheme, file_schema, rels): #recoge la uri del termino a buscar
    #print(termSearch, lang)
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
      FILTER (?p IN (skos:prefLabel ) )
      

    }  
    }
    """
    headers = {'content-type': 'text/html; charset=UTF-8'}
    
    r=requests.get(url, params={'format': 'json', 'query': query})
    rjson=json.loads(r.text)
    #print(rjson)
 
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
            #print(termSearch)            
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
    #print(rjson)

    uri=''  
    if('results' in rjson.keys()):
        results=rjson['results']
        bindings=results['bindings']
        for b in range(len(bindings)):
            uri=bindings[b]['c']['value']
            outFile=extrafunctions.property_add( termSearch, lang[1:3], outFile, 'altLabel',rels,uri)    
            
    return(outFile)

def relation_unesco(uri, lang, outFile, targets, scheme, file_schema):
    
    relations=['broader', 'narrower', 'related']
    url=("http://sparql.lynx-project.eu/")
    for relation in relations:
        if(relation not in outFile.keys()):
            outFile[relation]=[]
        #print(relation,'------')
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
    #print(file)       
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
			    		
			    		
				    		
			    		

		    		

	    			
'''
outFile={
    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
    "@type": "skos:Concept",
    "@id": "http://lynx-project.eu/kos/accidente-es",
    "inScheme": "labourlaw",
    "source": "https://dictapi.lexicala.com/senses/ES_SE00000884",
    "closeMatch": 1084327,
    "exactMatch": "https://www.wikidata.org/wiki/Q171558",
    "skos-xl:prefLabel": [
        {
            "@type": "skos-xl:Label",
            "@id": "accidente-es-pref",
            "source": "https://dictapi.lexicala.com/senses/ES_SE00000884",
            "literalForm": {
                "@language": "es",
                "@value": "accidente"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "ongeval-nl-pref",
            "source": "https://dictapi.lexicala.com/senses/ES_SE00000884",
            "literalForm": {
                "@language": "nl",
                "@value": "ongeval"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "Unfall-de-pref",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "de",
                "@value": "Unfall"
            }
        }
    ],
    "skos-xl:altLabel": [
        {
            "@type": "skos-xl:Label",
            "@id": "Unfallart-de-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "de",
                "@value": "Unfallart"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "Unfallgeschehen-de-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "de",
                "@value": "Unfallgeschehen"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "misadventure-en-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "en",
                "@value": "misadventure"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "misfortune-en-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "en",
                "@value": "misfortune"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "mishap-en-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "en",
                "@value": "mishap"
            }
        },
        {
            "@type": "skos-xl:Label",
            "@id": "ongeluk-nl-alt",
            "source": "https://www.wikidata.org/wiki/Q171558",
            "literalForm": {
                "@language": "nl",
                "@value": "ongeluk"
            }
        }
    ],
    "definition": [
        {
            "@language": "es",
            "@value": "suceso inesperado"
        },
        {
            "@language": "de",
            "@value": "unvorhergesehenes, einer Person oder Sache Schaden zufügendes Ereignis"
        }
    ],
    "broader":[],
    "narrower":[],
    "related":['Daño-es',
    'Lesion-es',],
    "example": "5. los delegados de prevención y, en su defecto, los representantes legales de los trabajadores en el centro de trabajo, que aprecien una probabilidad seria y grave de accidente por la inobservancia de la legislación aplicable en la materia, requerirán al empresario por escrito para que adopte las medidas oportunas que hagan desaparecer el estado de riesgo; si la petición no fuese atendida en un plazo de cuatro días, se dirigirán a la autoridad competente; esta, si apreciase las circunstancias a",
    "topConceptOf": "http://lynx-project.eu/kos/labourlaw"
}
        
file_schema={
    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
    "@id": "labourlaw",
    "conceptScheme": "http://lynx-project.eu/kos/labourlaw/",
    "hasTopConcept": [

    ],
    "label": "labour law",
    "creator": "UPM",
    "date": "March 10",
    "description": "Terminological data about Labour Law in Europe."
    } 

file=prefLabel_unesco('accidente', 'es', ['es', 'en', 'de', 'nl'], outFile, 'labour law', file_schema)

print(file)'''

