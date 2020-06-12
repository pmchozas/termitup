import requests
import json
import check_term
import re
from unicodedata import normalize
import wsidCode
import extrafunctions
import jsonFile

def eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, rels, file_schema):
    #print(outFile)
    fp=jsonFile.full_pref(outFile)
    prefLabel_full=fp[1]
    targets_pref=fp[0]
    altLabel_full=jsonFile.full_alt(outFile)
    definition_full=jsonFile.full_def(outFile)
    defs=[]
    name=[]
    urilist=[]
    defsnull=[]
    find=0
    if(context==None):
        context=termSearch
        wsid='yes'
    if(wsid=='yes'):
        uri=uri_term_eurovoc(termSearch, lang)
        if(len(uri)):
            #print('-se encontro eurovoc-',uri[0][0], outFile)
            outFile['skos-xl:prefLabel'][0]['source']=uri[0][0]
                    
            find=1
            for i in uri:
                urilist.append(i[0])
                name.append(i[1])
                if(i[2]==''):
                    alt_ev=name_term_eurovoc(i[0],lang, 'altLabel')
                    if(alt_ev!=''):
                        defsnull.append(alt_ev)
                    else:
                        defsnull.append(i[1])
                else:
                    defsnull.append(i[2].replace(',', ''))
                
                
            d=(defsnull, urilist)
            maximo=wsidCode.wsidFunction(termSearch, context,  d)
            print(maximo)
            if(maximo[2]!=200):
                #print('WSID NO 200')
                #closeMatch.append(uri)
                for i in uri:
                    outFile['closeMatch']=i[0]
                    

                
            elif(maximo[0]!='' and maximo[2]==200):
                #print('WSID 200')
                print(maximo)
                maxx=defsnull.index(maximo[0])
                namewsid=name[maxx]
                uriwsid=maximo[1]
                #find_euro.append(uriwsid)
                outFile['exactMatch']=uriwsid
                tars= extrafunctions.check_prefLabel(outFile, targets, rels)
                if(len(tars)>0):
                    for lang in targets:
                        pref_ev=name_term_eurovoc(uriwsid,lang,'prefLabel')
                        if(pref_ev!=''):
                            outFile=extrafunctions.property_add(pref_ev, lang, outFile, 'prefLabel', rels, uriwsid)
                            prefLabel_full.append(pref_ev+'-'+lang)
                            targets_pref.append(lang)
                
                        alt_ev=name_term_eurovoc(uriwsid,lang, 'altLabel')
                        def_ev=def_term_eurovoc( uriwsid,'"'+lang+'"')
                        if(alt_ev!=''):
                            outFile=extrafunctions.property_add(alt_ev, lang, outFile, 'altLabel', rels, uriwsid)
                        if(def_ev!=''):
                            outFile=extrafunctions.property_add(def_ev, lang, outFile, 'definition', rels, uriwsid)

                if(rels==1): #rels define si hara busqueda de relaciones o no 
                    #print('con relaciones')
                    outFile=relations_eurovoc(uriwsid, lang, namewsid,outFile, scheme, file_schema, targets)
                    pass

    else:
        x=''
        #print('WSID NO')

        
    return(outFile)

def uri_term_eurovoc(termSearch, lang): #recoge la uri del termino a buscar
    term='"^'+termSearch+'$"'
    lang='"'+lang+'"'
    answer=[]
    answeruri=''
    val=''
    try:
        url = ("http://sparql.lynx-project.eu/")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        ?c a skos:Concept .
        ?c ?p ?label. 
          FILTER regex(?label, """+term+""", "i" )
          FILTER (lang(?label) = """+lang+""")
          FILTER (?p IN (skos:prefLabel, skos:altLabel ) )
      

        }  
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
            answeruri=''
        else:
            for result in results["results"]["bindings"]:
                answeruri=result["c"]["value"]
                answerl=result["label"]["value"]
                #print(termSearch, answerl)
                if(termSearch.lower() == answerl.lower()):#ATENCION
                    
                    defs=def_term_eurovoc(answeruri, lang)
                    answer.append([answeruri, answerl, defs])

                else:
                    tok=answerl.split(' ')
                    for i in tok:
                        if('(' in i):
                            tok.remove(i)
                            tokt=term.split(' ')
                            if(len(tok)==len(tokt)):
                                defs=def_term_eurovoc(answeruri, lang)
                                answer.append([answeruri, answerl, defs])
                        elif(termSearch == i):
                            defs=def_term_eurovoc(answeruri, lang)
                            #print(answeruri, answerl, '|',defs)
                            answer.append([answeruri, answerl, defs])
                
    except json.decoder.JSONDecodeError:
        answer=[]


    return(answer)


def def_term_eurovoc( uri,lang): #recoge la definicion de la uri de entrada
    definicion=''
    resultado=[]
    url=("http://sparql.lynx-project.eu/")
    query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+uri+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:definition  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
    r=requests.get(url, params={'format': 'json', 'query': query})
    results=json.loads(r.text)
    if (len(results["results"]["bindings"])==0):
        definicion=''
    else:
        for result in results["results"]["bindings"]:
            definicion=result["label"]["value"]
    return(definicion)

def getRelation(uri_termino, relation, lang): #recoge la uri de la relacion a buscar 
    answer=[]
    answerRel=''
    try:
        for i in uri_termino:
            url=("http://sparql.lynx-project.eu/")
            query="""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?c ?label
            WHERE {
            GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
            VALUES ?c {<"""+i+"""> }
            VALUES ?relation { skos:"""+relation+""" } # skos:broader
            ?c a skos:Concept .
            ?c ?relation ?label .    
            }  
            }
            """
            r=requests.get(url, params={'format': 'json', 'query': query})
            results=json.loads(r.text)
            if (len(results["results"]["bindings"])==0):
                    answerRel=''
            else:
                for result in results["results"]["bindings"]:
                    answerRel=result["label"]["value"]
                    name=name_term_eurovoc(answerRel,lang,'prefLabel')
                    answer.append([answerRel, name, relation])
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError')
    
    return(answer)

def name_term_eurovoc(uri,lang,label): #recoge el nombre equivalente a la uri de entrada
    try:
        nameUri=''
        lang='"'+lang+'"'
        url=("http://sparql.lynx-project.eu/")
        query="""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?c ?label
        WHERE {
        GRAPH <http://sparql.lynx-project.eu/graph/eurovoc> {
        VALUES ?c { <"""+uri+"""> }
        VALUES ?searchLang { """+lang+""" undef } 
        VALUES ?relation { skos:"""+label+"""  } 
        ?c a skos:Concept . 
        ?c ?relation ?label . 
        filter ( lang(?label)=?searchLang )
        }
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                nameUri=''
        else:
            for result in results["results"]["bindings"]:
                nameUri=result["label"]["value"]
    except json.decoder.JSONDecodeError:
        #print('json.decoder.JSONDecodeError')
        pass
        
      
    return(nameUri)

def relations_eurovoc(uri, lang, term, outFile, scheme, file_schema, targets):
    results=[]
    relations=['broader', 'narrower', 'related']
    for relation in relations:
        uriRelation=getRelation([uri], relation, lang)
        #print('----------', relation)
        if(len(uriRelation)>0):
            for i in uriRelation:
                verify=check_term.checkTerm(lang, i[1], relation, targets,'')
                ide=verify[0]
                termSearch=verify[1]
                if(termSearch!='1'):
                    outFile[relation].append(ide)
                    originalIde=outFile['@id']
                    dataEurovoc=eurovoc_file(termSearch, ide, relation, i[0], lang, scheme,  originalIde, file_schema, outFile,targets)

    #print(outFile)
    return(outFile)

def eurovoc_file(termSearch, ide, relation, iduri, lang, scheme,  originalIde, file_schema, outFile,targets):
    termSearch=termSearch.replace('/', ' ')
    #print('-----', termSearch,'------', relation)
    if('topConceptOf' in outFile.keys() and relation=='broader'):
        del outFile['topConceptOf']
        file_schema['hasTopConcept'].append(ide)
    data={}
    data={'@context':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': termSearch+'-'+lang,'inScheme': scheme.replace(' ',''), "exactMatch":iduri, '@type':'skos:Concept','skos-xl:prefLabel':'','skos-xl:altLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }
    #"exactMatch":iduri

    data['skos-xl:prefLabel']=[]
    data['skos-xl:altLabel']=[]
    data['definition']=[]
    '''del pref_relation[0:len(pref_relation)]
    del alt_relation[0:len(alt_relation)]
    del targets_relation[0:len(targets_relation)]'''
    if(len(data['skos-xl:prefLabel'])==0):
        data['skos-xl:prefLabel'].append({'@type':'skos-xl:Label', '@id':termSearch.strip(' ')+'-'+lang+'-pref', 'source': '', 'literalForm':{'@language':lang, '@value': termSearch.strip(' ')}})
    
    #print('-',data['skos-xl:prefLabel'], len(data['skos-xl:prefLabel']))
    data=eurovoc(termSearch, lang, targets, None,  'yes', data, scheme, 2, file_schema)
    del data['definition']
    
        #pref_relation.append(termSearch+'-'+lang)
        #targets_relation.append(lang)
    
    if(len(data['skos-xl:altLabel'])==0):
        del data['skos-xl:altLabel']
    if('broader' in relation and termSearch!=''):
        data['narrower']=[]
        data['narrower'].append(originalIde)
        #data['narrower'].append({'@language':lang+'_'+originalIde, '@value':termSearch})

    elif('narrower' in relation and termSearch!=''):
        data['broader']=[]
        data['broader'].append(originalIde)
        #data['broader'].append({'@language':lang+'_'+originalIde, '@value':termSearch})

    elif('related' in relation and termSearch!=''):
        data['related']=[]
        data['related'].append(originalIde)
        #data['related'].append({'@language':lang+'_'+originalIde, '@value':termSearch})



    data=jsonFile.outFile_full(data)
    n=termSearch.replace(' ', '_').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I
                )
    n = normalize( 'NFC', n)
    lang_in='es'
    newFile=lang_in+'/'+relation+'/'+n+'_'+lang+'.jsonld'
    #file_schema['hasTopConcept'].append(ide)
    #newFile='terminosjson/'+relation+'/'+n+'_'+ide+'.jsonld'

    #print('------')
    #print(data)
    with open(newFile, 'w') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
    #print('RELATION-----')
    #print(data)
              
    return(data)