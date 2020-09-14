import requests
import json
import check_term
import re
from unicodedata import normalize
import wsidCode
import extrafunctions
import jsonFile
import unesco
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

def eurovoc(termSearch, lang, targets, context,  wsid, outFile, scheme, rels, file_schema):
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
            if(rels!=2):
                if(len(outFile['skos-xl:prefLabel'][0]['source'])==0 ):
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
                
            if(rels==2):  
                for u in urilist:
                    uriwsid=u
                    #if(uriwsid not in outFile['closeMatch']):
                    #    outFile['closeMatch'].append(uriwsid)
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
            else:
                d=(defsnull, urilist)
                #print('--', termSearch)
                maximo=wsidCode.wsidFunction(termSearch, context,  d)
                
                if(maximo[2]!=200):
                    pass
                elif(maximo[0]!='' and maximo[2]==200):
                    maxx=defsnull.index(maximo[0])
                    namewsid=name[maxx]
                    uriwsid=maximo[1]
                    outFile['closeMatch'].append(uriwsid)
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
                        outFile=relations_eurovoc(uriwsid, lang, namewsid,outFile, scheme, file_schema, targets)
                        pass

    else:
        pass

        
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
                            answer.append([answeruri, answerl, defs])
                
    except json.decoder.JSONDecodeError:
        pass


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
        pass
    
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
        pass
        
      
    return(nameUri)

def relations_eurovoc(uri, lang, term, outFile, scheme, file_schema, targets):
    results=[]
    relations=['broader', 'narrower', 'related']
    for relation in relations:
        uriRelation=getRelation([uri], relation, lang)
        if(len(uriRelation)>0):
            for i in uriRelation:
                verify=check_term.checkTerm(lang, i[1], relation, targets,'')
                ide=verify[0]
                termSearch=verify[1]
                if(termSearch!='1'):
                    originalIde=outFile['@id']
                    dataEurovoc=eurovoc_file(termSearch, ide, relation, i[0], lang, scheme,  originalIde, file_schema, outFile,targets)
                full=jsonFile.full_rels(outFile, relation)
                cadena = re.sub('[/,+.;:/)([]]*', '',  termSearch)
                n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                    normalize( "NFD", cadena), 0, re.I
                )
                n = normalize( 'NFC', n)
                uri=n.replace(' ','-')+'-'+lang

                if(uri not in full):
                    logging.info('FOUND (Eurovoc-relation-'+relation+'): '+cadena+' lang: '+lang[1:3])
                    outFile[relation].append(uri)
    #print(outFile)
    return(outFile)

def eurovoc_file(termSearch, ide, relation, iduri, lang, scheme,  originalIde, file_schema, outFile,targets):
    #print('eurovoc_file', relation)
    termSearch2=termSearch
    if(termSearch[-6:]=='unesco'):
        termSearch=termSearch[:-6]
    termSearch=termSearch.replace('/', ' ')
    
 
    data={}
    data={'@contextfile':'http://lynx-project.eu/doc/jsonld/skosterm.json','@type':'skos:Concept', '@id': termSearch.replace(' ', '-')+'-'+lang,'inScheme': scheme.replace(' ',''), "closeMatch":iduri, '@type':'skos:Concept','skos-xl:prefLabel':'','skos-xl:altLabel':'',"topConceptOf":"http://lynx-project.eu/kos/"+scheme.replace(' ','') }

    data['skos-xl:prefLabel']=[]
    data['skos-xl:altLabel']=[]
    data['definition']=[]
    
    if(termSearch2[-6:]!='unesco'):
        if(lang!='de'):
            termSearch=termSearch.lower()
            #print('RELACION: ',termSearch)
            data=eurovoc(termSearch, lang, targets, None,  'yes', data, scheme, 2, file_schema)
        del data['definition']
    else:
        if(lang!='de'):
            termSearch2=termSearch2.lower()
            #print('RELACION: ',termSearch2[:-6])
            data=unesco.prefLabel_unesco(termSearch2[:-6], lang, targets, data, scheme, file_schema, 2)
        if('definition' in data.keys()):
            del data['definition']


    if(len(data['skos-xl:prefLabel'])==0):
        data['skos-xl:prefLabel'].append({'@type':'skos-xl:Label', '@id':termSearch.strip(' ').replace(' ', '-')+'-'+lang+'-pref',  'literalForm':{'@language':lang, '@value': termSearch.strip(' ')}})
        del data['closeMatch']
    
    if(len(data['skos-xl:altLabel'])==0):
        del data['skos-xl:altLabel']
    originalIde_split=originalIde.split('/')
    if('broader' in relation and termSearch!=''):
        data['narrower']=[]
        data['narrower'].append(originalIde_split[-1])
        
    elif('narrower' in relation and termSearch!=''):
        data['broader']=[]
        data['broader'].append(originalIde_split[-1])
        
    elif('related' in relation and termSearch!=''):
        data['related']=[]
        data['related'].append(originalIde_split[-1])
        
    if('broader' in data.keys()):
        del data['topConceptOf']

    data=jsonFile.outFile_full(data)
    if(lang!='de'):
        n=termSearch.replace(' ', '-').replace('\ufeff','').lower()
    else:
        n=termSearch.replace(' ', '-').replace('\ufeff','')
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", n), 0, re.I
                )
    n = normalize( 'NFC', n)
    newFile='../data/output/'+n+'-'+lang+'.jsonld'

    with open(newFile, 'w') as file:
        json.dump(data, file, indent=4,ensure_ascii=False)

    return(data)