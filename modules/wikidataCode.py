import requests
import wsidCode 
import extrafunctions
import json
import eurovocCode
url = 'https://query.wikidata.org/sparql'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def wikidata_retriever(term, lang, context,  targets, outFile, rels, wsid):
    if(context==None):
        wsid='no'
    retrieve_query = """
        SELECT * {
       ?item rdfs:label "TERM"@LANG.
       ?item schema:description ?desc.
      FILTER (lang(?desc) = "LANG")
      }
    """

    original_query = """
    SELECT DISTINCT ?article ?lang ?name ?desc WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
      OPTIONAL {
        wd:WDTMID schema:description ?desc.
        FILTER (lang(?name) = lang(?desc))
      }
    }ORDER BY ?lang
    """

    altLabel_query = """
    SELECT DISTINCT ?article ?altLabel ?lang WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
      OPTIONAL {
        wd:WDTMID skos:altLabel ?altLabel.
        FILTER (lang(?name) = lang(?altLabel))
      }
    }ORDER BY ?lang
    """

    narrower_concept_query = """
    SELECT DISTINCT ?naTerm WHERE {
        ?naTerm wdt:P279 wd:WDTMID .
      }
    """

    broader_concept_query = """
    SELECT DISTINCT ?brTerm WHERE {
        wd:WDTMID wdt:P279 ?brTerm .   
    }
    """

    term_query = """
    SELECT DISTINCT ?lang ?name WHERE {
      ?article schema:about wd:WDTMID;
               schema:inLanguage ?lang;
               schema:name ?name.
      FILTER(?lang in (TARGETS))  
    }ORDER BY ?lang
    """

    Wikidata_dataset = dict()
    definition=[]
    iduri=[]
    altLabel=[]
    query = retrieve_query.replace("TERM", term).replace("LANG", lang)
    SRCTERM = "\"" + term + "\"" + "@" + lang
    #print(SRCTERM) We have to save this in the skos as well
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json()
    try:
        if len(data['results']['bindings']) != 0:
            print('-se encontro wiki-')
            bindings=data['results']['bindings']
            for i in range(len(bindings)):
                iduri.append(bindings[i]['item']['value'].split("/")[-1])
                definition.append(bindings[i]['desc']['value'].replace(',', ''))
            
            if(context==None):
                context=term
                wsid='yes'
            if(wsid=='yes'):
                d=(definition,iduri)
                maximo=wsidCode.wsidFunction(term,  context,   d)
                #print(maximo)
                relations_retrieved = dict()
               
                if( maximo[2]!=200):
                    #outFile['closeMatch']='https://www.wikidata.org/wiki/'+iduri[0]
                    pass
                elif(maximo[0]!='' and maximo[2]==200):
                    if(len(outFile['skos-xl:prefLabel'][0]['source'])==0):
                        outFile['skos-xl:prefLabel'][0]['source']='https://www.wikidata.org/wiki/'+maximo[1]

                    tars=extrafunctions.check_prefLabel(outFile, targets, rels)
                    if(len(tars)>0):
                        target="', '".join(tars)
                        target="'"+target+"'"

                        try:
                            query = original_query.replace("WDTMID", maximo[1]).replace("TARGETS", target)
                            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                            data = r.json()
                            bindings=data['results']['bindings']
                            if(len(bindings)>0):
                                #find_wiki.append(maximo[1])
                                outFile['closeMatch'].append('https://www.wikidata.org/wiki/'+maximo[1])
                                for i in range(len(bindings)):
                                    if('name' in bindings[i]):
                                        prefLabel_wiki=bindings[i]['name']['value']
                                        lang_pr_wiki=bindings[i]['name']['xml:lang']
                                        #print(prefLabel_wiki, lang_pr_wiki)
                                        outFile=extrafunctions.property_add( prefLabel_wiki, lang_pr_wiki, outFile, 'prefLabel' , rels, "https://www.wikidata.org/wiki/"+maximo[1])
                                    if('desc' in bindings[i]):
                                        definition_wiki=bindings[i]['desc']['value']
                                        lang_pr_wiki=bindings[i]['name']['xml:lang']
                                        outFile=extrafunctions.property_add( definition_wiki, lang_pr_wiki, outFile, 'definition' , rels, "https://www.wikidata.org/wiki/"+maximo[1])
                        except json.decoder.JSONDecodeError:
                            error=''
                            #print('JSONDecodeError')
                    target="', '".join(targets)
                    target="'"+target+"'"
                    query = altLabel_query.replace("WDTMID", maximo[1]).replace("TARGETS", target)
                    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                    altLabel_response = r.json()
                    bindings=altLabel_response['results']['bindings']
                    
                    for i in range(len(bindings)):
                        if('altLabel' in bindings[i]):
                            altLabel_wiki=bindings[i]['altLabel']['value']
                            lang_al_wiki=bindings[i]['altLabel']['xml:lang']
                            outFile=extrafunctions.property_add( altLabel_wiki, lang_al_wiki, outFile, 'altLabel', rels, "https://www.wikidata.org/wiki/"+maximo[1])
                    
                    if(rels==5):
                        # Retrieve narrower and broader concepts
                        relation_type = ["narrower", "broader"]
                        
                        for relation in relation_type:
                            if relation == "narrower":
                                concept_query = narrower_concept_query
                                relation_id = "naTerm"
                            else:
                                concept_query = broader_concept_query
                                relation_id = "brTerm"

                            query = concept_query.replace("WDTMID", maximo[1])
                            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                            concept_response = r.json()
                            
                            concepts_list = [item[relation_id]["value"].split("/")[-1] if len(item[relation_id]["value"]) else None for item in concept_response["results"]["bindings"]]
                           
                           
                            if len(concepts_list):
                                for concept in concepts_list:
                                    try:
                                        query = term_query.replace("WDTMID", concept).replace("TARGETS", target)
                                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                                        for item in r.json()["results"]["bindings"]:
                                            lang=item["name"]["xml:lang"]
                                            concept_terms = item["name"]["value"]
                                            verify=checkTerm(lang, concept_terms, relation, targets)
                                            ide=verify[0]
                                            termSearch=verify[1]
                                            if(termSearch!='1'):
                                                outFile[relation].append(ide)
                                                originalIde=outFile['@id']
                                                dataEurovoc=eurovoc_file(termSearch, ide, relation, 'https://www.wikidata.org/wiki/'+concept, lang, scheme,  originalIde)
                                    except json.decoder.JSONDecodeError:
                                        error=''
                                        #print('JSONDecodeError')

            else:
                x=''
                #print('WSID NO')
                #outFile=wsid_wiki_no(outFile, targets, iduri, original_query, altLabel_query, narrower_concept_query, broader_concept_query, term_query, rels)
    except json.decoder.JSONDecodeError:
                        error=''
    return(outFile)

def wsid_wiki_no(outFile, targets, iduri, original_query, altLabel_query, narrower_concept_query, broader_concept_query, term_query, rels):
    tars=extrafunctions.check_prefLabel(outFile, targets, rels)
    target="', '".join(tars)
    target="'"+target+"'"
    if(len(tars)>0):
        for idterm in iduri:
            query = original_query.replace("WDTMID", idterm).replace("TARGETS", target)
            r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
            data = r.json()
            bindings=data['results']['bindings']
            if(len(bindings)>0):
                for i in range(len(bindings)):
                    if('name' in bindings[i]):
                        prefLabel_wiki=bindings[i]['name']['value']
                        lang_pr_wiki=bindings[i]['name']['xml:lang']
                        outFile=extrafunctions.property_add( prefLabel_wiki, lang_pr_wiki, outFile, 'prefLabel' , rels)
                    if('desc' in bindings[i]):
                        definition_wiki=bindings[i]['desc']['value']
                        lang_pr_wiki=bindings[i]['desc']['xml:lang']
                        outFile=extrafunctions.property_add( definition_wiki, lang_pr_wiki, outFile, 'definition', rels)   
    target="', '".join(targets)
    target="'"+target+"'"
    for idterm in iduri:    
        query = altLabel_query.replace("WDTMID", idterm).replace("TARGETS", target)
        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
        altLabel_response = r.json()
        bindings=altLabel_response['results']['bindings']

        for i in range(len(bindings)):
            if('altLabel' in bindings[i]):
                altLabel_wiki=bindings[i]['altLabel']['value']
                lang_al_wiki=bindings[i]['altLabel']['xml:lang']
                outFile=extrafunctions.property_add( altLabel_wiki, lang_al_wiki, outFile, 'altLabel', rels )
                    
    if(rels==1):                
        # Retrieve narrower and broader concepts
        relation_type = ["narrower", "broader"]
        for relation in relation_type:
            if relation == "narrower":
                concept_query = narrower_concept_query
                relation_id = "naTerm"
            else:
                concept_query = broader_concept_query
                relation_id = "brTerm"

            for idterm in iduri:
                query = concept_query.replace("WDTMID", idterm)
                r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                concept_response = r.json()
                concepts_list = [item[relation_id]["value"].split("/")[-1] if len(item[relation_id]["value"]) else None for item in concept_response["results"]["bindings"]]
                if len(concepts_list):
                    for concept in concepts_list:
                        query = term_query.replace("WDTMID", concept).replace("TARGETS", target)
                        r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
                        for item in r.json()["results"]["bindings"]:
                            concept_terms = item["name"]["value"]
                            verify=checkTerm(lang, concept_terms, relation, targets)
                            ide=verify[0]
                            termSearch=verify[1]
                            if(termSearch!='1'):
                                outFile[relation].append(ide)
                                originalIde=outFile['@id']
                                dataEurovoc=eurovocCode.eurovoc_file(termSearch, ide, relation, 'iduri', lang, scheme,  originalIde)
    return(outFile)

