import requests
import json
import check_term
import re
from unicodedata import normalize
import wsidCode
import extrafunctions
import jsonFile

def uri_term_eurovoc(termSearch, lang, targets, outFile): #recoge la uri del termino a buscar
    term='"^'+termSearch+'$"'
    lang='"'+lang+'"'
    answer=[]
    answeruri=''
    val=''
    
    '''url = "http://sparql.lynx-project.eu/"
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?c ?label
    WHERE {
    GRAPH <http://lkg.lynx-project.eu/unesco-thesaurus> {
    ?c a skos:Concept .
    ?c ?p ?label. 
      FILTER regex(?label, """+term+""", "i" )
      FILTER (lang(?label) = """+lang+""") )
      

    }  
    }
    """
    headers = {'content-type': 'application/json'}
    #r=requests.get(url, params={'format': 'json', 'query': query})
    #r=requests.get(url, params={ 'query': query})
    #results=json.loads(r.text)
    #print(r)
    response = requests.get(url, json=query, headers=headers)
    response2=response.json()
    js=json.dumps(response2)'''
    response2={
				  "@context": {
				    "skos": "http://www.w3.org/2004/02/skos/core#",
				    "isothes": "http://purl.org/iso25964/skos-thes#",
				    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
				    "owl": "http://www.w3.org/2002/07/owl#",
				    "dct": "http://purl.org/dc/terms/",
				    "dc11": "http://purl.org/dc/elements/1.1/",
				    "uri": "@id",
				    "type": "@type",
				    "lang": "@language",
				    "value": "@value",
				    "graph": "@graph",
				    "label": "rdfs:label",
				    "prefLabel": "skos:prefLabel",
				    "altLabel": "skos:altLabel",
				    "hiddenLabel": "skos:hiddenLabel",
				    "broader": "skos:broader",
				    "narrower": "skos:narrower",
				    "related": "skos:related",
				    "inScheme": "skos:inScheme"
				  },
				  "graph": [
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus",
				      "type": "skos:ConceptScheme",
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "UNESCO Thesaurus"
				        },
				        {
				          "lang": "fr",
				          "value": "Thésaurus de l'UNESCO"
				        },
				        {
				          "lang": "ru",
				          "value": "Тезаурус ЮНЕСКО"
				        },
				        {
				          "lang": "es",
				          "value": "Tesauro de la UNESCO"
				        }
				      ]
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1161",
				      "type": "skos:Concept",
				      "dct:modified": {
				        "type": "http://www.w3.org/2001/XMLSchema#dateTime",
				        "value": "2006-05-23T00:00:00"
				      },
				      "broader": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept206"
				      },
				      "inScheme": {
				        "uri": "http://vocabularies.unesco.org/thesaurus"
				      },
				      "narrower": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1166"
				      },
				      "prefLabel": [
				        {
				          "lang": "es",
				          "value": "Accidente"
				        },
				        {
				          "lang": "ru",
				          "value": "Аварии"
				        },
				        {
				          "lang": "en",
				          "value": "Accidents"
				        },
				        {
				          "lang": "fr",
				          "value": "Accident"
				        }
				      ],
				      "related": [
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept1169"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept1171"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept209"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept1170"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept204"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept653"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept1168"
				        },
				        {
				          "uri": "http://vocabularies.unesco.org/thesaurus/concept1167"
				        }
				      ]
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1166",
				      "type": "skos:Concept",
				      "broader": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      },
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Fires"
				        },
				        {
				          "lang": "ru",
				          "value": "Пожары"
				        },
				        {
				          "lang": "fr",
				          "value": "Feu"
				        },
				        {
				          "lang": "es",
				          "value": "Incendio"
				        }
				      ]
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1167",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "ru",
				          "value": "Ущерб"
				        },
				        {
				          "lang": "fr",
				          "value": "Dégât"
				        },
				        {
				          "lang": "en",
				          "value": "Damage"
				        },
				        {
				          "lang": "es",
				          "value": "Daño"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1168",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Injuries"
				        },
				        {
				          "lang": "es",
				          "value": "Lesión"
				        },
				        {
				          "lang": "ru",
				          "value": "Телесные повреждения"
				        },
				        {
				          "lang": "fr",
				          "value": "Lésion"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1169",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Occupational safety"
				        },
				        {
				          "lang": "es",
				          "value": "Seguridad en el trabajo"
				        },
				        {
				          "lang": "fr",
				          "value": "Sécurité du travail"
				        },
				        {
				          "lang": "ru",
				          "value": "Техника безопасности"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1170",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "es",
				          "value": "Medida de seguridad"
				        },
				        {
				          "lang": "ru",
				          "value": "Меры безопасности"
				        },
				        {
				          "lang": "en",
				          "value": "Safety measures"
				        },
				        {
				          "lang": "fr",
				          "value": "Mesure de sécurité"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept1171",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "ru",
				          "value": "Безопасность на транспорте"
				        },
				        {
				          "lang": "es",
				          "value": "Seguridad del transporte"
				        },
				        {
				          "lang": "fr",
				          "value": "Sécurité des transports"
				        },
				        {
				          "lang": "en",
				          "value": "Transport safety"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept204",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Dangerous materials"
				        },
				        {
				          "lang": "ru",
				          "value": "Опасные материалы"
				        },
				        {
				          "lang": "es",
				          "value": "Sustancia peligrosa"
				        },
				        {
				          "lang": "fr",
				          "value": "Substance dangereuse"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept206",
				      "type": "skos:Concept",
				      "narrower": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      },
				      "prefLabel": [
				        {
				          "lang": "ru",
				          "value": "Бедствия"
				        },
				        {
				          "lang": "es",
				          "value": "Desastre"
				        },
				        {
				          "lang": "en",
				          "value": "Disasters"
				        },
				        {
				          "lang": "fr",
				          "value": "Catastrophe"
				        }
				      ]
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept209",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "ru",
				          "value": "Безопасность"
				        },
				        {
				          "lang": "fr",
				          "value": "Sécurité"
				        },
				        {
				          "lang": "es",
				          "value": "Seguridad"
				        },
				        {
				          "lang": "en",
				          "value": "Safety"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/concept653",
				      "type": "skos:Concept",
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Safety devices"
				        },
				        {
				          "lang": "fr",
				          "value": "Dispositif de sécurité"
				        },
				        {
				          "lang": "ru",
				          "value": "Устройства безопасности"
				        },
				        {
				          "lang": "es",
				          "value": "Dispositivo de seguridad"
				        }
				      ],
				      "related": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      }
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/domain2",
				      "type": [
				        "isothes:ConceptGroup",
				        "http://vocabularies.unesco.org/ontology#Domain",
				        "skos:Collection"
				      ],
				      "skos:member": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/mt2.60"
				      },
				      "prefLabel": [
				        {
				          "lang": "ru",
				          "value": "Естественные науки"
				        },
				        {
				          "lang": "en",
				          "value": "Science"
				        },
				        {
				          "lang": "fr",
				          "value": "Science"
				        },
				        {
				          "lang": "es",
				          "value": "Ciencia"
				        }
				      ]
				    },
				    {
				      "uri": "http://vocabularies.unesco.org/thesaurus/mt2.60",
				      "type": [
				        "isothes:ConceptGroup",
				        "http://vocabularies.unesco.org/ontology#MicroThesaurus",
				        "skos:Collection"
				      ],
				      "skos:member": {
				        "uri": "http://vocabularies.unesco.org/thesaurus/concept1161"
				      },
				      "prefLabel": [
				        {
				          "lang": "en",
				          "value": "Pollution, disasters and safety"
				        },
				        {
				          "lang": "es",
				          "value": "Polución, catástrofes y seguridad"
				        },
				        {
				          "lang": "fr",
				          "value": "Pollution, catastrophes et sécurité"
				        },
				        {
				          "lang": "ru",
				          "value": "Загрязнение окружающей среды, бедствия и безопасность"
				        }
				      ]
				    }
				  ]
				}
    request_query=response2['graph']
        
    if('graph' in response2.keys()):
    	for i in range(len(request_query)):
	    	pref=request_query[i]['prefLabel']
	    	for pos in range(len(pref)):
	    		pref_v=pref[pos]['value']
	    		pref_l=pref[pos]['lang']
	    		if(pref_v.lower()==termSearch.lower()):
	    			pos_unique=i
	    			for j in range(len(pref)):
	    				pref_v2=pref[j]['value']
	    				pref_l2=pref[j]['lang']
		    			if(pref_l2 in targets):
		    				print(pref_v, pref_l2)
		    				outFile=extrafunctions.property_add( pref_v2, pref_l2, outFile, 'prefLabel',2, request_query[pos_unique]['uri'] )
		    				#outFile=extrafunctions.property_add(def_ev, lang, outFile, 'definition', rels, uriwsid)
		    		if('altLabel' in request_query[pos_unique].keys()):
		    			alt=request_query[pos_unique]['altLabel']
		    			for j in range(len(alt)):
		    				alt_v2=alt[j]['value']
		    				alt_l2=alt[j]['lang']
			    			if(alt_l2 in targets):
			    				print(alt_v2, alt_l2)
			    				outFile=extrafunctions.property_add( alt_v2, alt_l2, outFile, 'altLabel',2, request_query[pos_unique]['uri'] )
		    				
			    	if('broader' in request_query[pos_unique].keys()):
			    		br=request_query[pos_unique]['broader']
			    		if(type(br) is dict):
			    			br=request_query[pos_unique]['broader']['uri']
			    			outFile['broader'].append(br)
			    			print(br)
			    		else:
				    		for b in range(len(br)):
				    			bruri=br[b]['uri']
				    			outFile['broader'].append(bruri)
				    			print(bruri)
			    	if('narrower' in request_query[pos_unique].keys()):
			    		na=request_query[pos_unique]['narrower']
			    		if(type(na) is dict):
			    			na=request_query[pos_unique]['narrower']['uri']
			    			outFile['narrower'].append(br)
			    			print(na)
			    		else:
				    		for n in range(len(na)):
				    			nauri=na[n]['uri']
				    			outFile['narrower'].append(nauri)
				    			print(nauri)
			    	if('related' in request_query[pos_unique].keys()):
			    		re=request_query[pos_unique]['related']
			    		if(type(re) is dict):
			    			re=request_query[pos_unique]['related']['uri']
			    			outFile['related'].append(br)
			    			print(re)
			    		else:
			    			for r in range(len(re)):
				    			reuri=re[r]['uri']
				    			outFile['related'].append(reuri)
				    			print(reuri)
    print(outFile)

			    		
			    		
				    		
			    		

		    		

	    			

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
    "related":[],
    "example": "5. los delegados de prevención y, en su defecto, los representantes legales de los trabajadores en el centro de trabajo, que aprecien una probabilidad seria y grave de accidente por la inobservancia de la legislación aplicable en la materia, requerirán al empresario por escrito para que adopte las medidas oportunas que hagan desaparecer el estado de riesgo; si la petición no fuese atendida en un plazo de cuatro días, se dirigirán a la autoridad competente; esta, si apreciase las circunstancias a",
    "topConceptOf": "http://lynx-project.eu/kos/labourlaw"
}
        
    

uri_term_eurovoc('accidente', 'es', ['es', 'en', 'de', 'nl'], outFile)