import requests
import json
from modules_api import check_term
import re
from modules_api import wsidCode
from modules_api import extrafunctions
from modules_api import jsonFile
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

# iate
def iate(term, inlang, outlang, outFile, context, wsid, rels):
    answer=[]
    try:
        auth_token=bearenToken()
        hed = {'Authorization': 'Bearer ' +auth_token}
        jsonList=[]
        data = {"query": term,
        "source": inlang,
        "targets": outlang,
        "search_in_fields": [
            0
        ],
        "search_in_term_types": [
            0,
            1,
            2,
            3,
            4
        ],
            "query_operator": 1
        }
        url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
        response = requests.get(url, json=data, headers=hed)
        response2=response.json()
        js=json.dumps(response2)
        #print(js)
        results=[]
        termSearch=[]
        cont=0
        request_query=response2['request']['query']
        
        termSearch.append(term)
        bloq=0
        if('items' in response2.keys()):
            term=response2['items']
            ide=check_term.sctmid_creator()
            definicion_wsid=[]
            ides_wsid=[]
            ides_item=[]
            for item in range(len(term)):#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                results.insert(item, [])
                def_item=[]
                dom=term[item]
                ide_iate=term[item]['id']
                leng=term[item]['language']
                if(inlang in leng):
                    for item2 in range(len(leng[inlang]['term_entries'])):
                        termiate=leng[inlang]['term_entries'][item2]['term_value']
                        if(  termiate == termSearch[cont] ):
                            #print('-se encontro iate exacto-')
                            bloq=1 # bandera de encontrado se enciende en 1
                            if(context==None):
                                context=getContextIate(item, leng, inlang,termSearch[cont] )

                                if(context!=''):
                                    wsid='yes'
                                else:
                                    context=termSearch[cont]
                                    wsid='yes'
                            for target in outlang:
                                get=getInformationIate(target,item, item2,leng, termSearch[cont])
                                results[item].insert(0, item)#item
                                results[item].insert(1, get[0])#def
                                results[item].insert(2, get[1])#pref
                                results[item].insert(3, get[2])#alt
                                results[item].insert(4, target)#target
                                
                                if(target==inlang ):
                                    if(get[0].isalpha()==False ): #get[0]=='' or get[0]=='---'
                                        dom_iat=domain_iate(dom, data, hed)
                                        if(len(get[2])):
                                            joinget2=' '.join(get[2])
                                            def_item.append(joinget2.replace('"', '').replace(',',''))
                                        if(len(dom_iat)):
                                            def_item.append(dom_iat[0].replace('"', '').replace(',',''))
                                    else:
                                        def_item.append(get[0].replace('"', '').replace(',',''))
                join_def_item=' '.join(def_item)
                ides_item.append(item)
                ides_wsid.append(ide_iate)
                definicion_wsid.append(join_def_item)
            if(bloq==1):
                d=(definicion_wsid,ides_item)
                if(wsid=='yes'):
                    maximo=wsidCode.wsidFunction(termSearch[cont],  context,   d)
                    if(maximo[2]!=200):
                        pass
                    elif(maximo[0]!='' and maximo[2]==200):
                        if(len(outFile['skos-xl:prefLabel'][0]['source'])==0):
                            outFile['skos-xl:prefLabel'][0]['source']="https://iate.europa.eu/entry/result/"+str(ide_iate)
                        wsidmax=maximo[1]
                        it=ides_item.index(wsidmax)
                        maxx=ides_wsid[it]
                        outFile['source'].append("https://iate.europa.eu/entry/result/"+str(ide_iate))
                        outFile=fillPrefIate(outFile, results, 'prefLabel', 2, wsidmax, rels, ide_iate)
                        outFile=fillAltIate(outFile, results,  'altLabel', 3, wsidmax, rels, ide_iate)
                        outFile=fillDefinitionIate(outFile, results,  'definition', 1, wsidmax, ide_iate)
                else:
                    closeMatch.append("https://iate.europa.eu/entry/result/"+str(ide_iate))
                    
        cont=cont+1
    except json.decoder.JSONDecodeError:
        response2='{ }'   
    return(outFile)

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

def getContextIate(item, leng, inlang, termSearch):
    context=''
    if(inlang in leng):
        language=leng[inlang]
        for l in language:
            if('term_entries' in language.keys()):
                term_entries=language['term_entries']
                if(len(term_entries)>0):
                    for t in range(len(term_entries)):
                        term_val=language['term_entries'][t]
                        if('contexts' in term_val ):
                            contexts=term_val['contexts']
                            if(len(contexts)>0):
                                for c in range(len(contexts)):
                                    contextsc=contexts[c]
                                    if('context' in contextsc):
                                        if(termSearch in contextsc['context'] ):
                                            context=contextsc['context'].lower()

    #print(context)
    return(context)


def getInformationIate(target, item,item2, leng,termSearch):
    defi=''
    pref=''
    term_val=''
    syn=[]
    joinSyn=''
    if(target in leng):
        language=leng[target]
        for l in language:
            if('term_entries' in language.keys()):
                term_entries=language['term_entries']
                if(len(term_entries)>0):
                    pref=language['term_entries'][0]['term_value']
                    for t in range(len(term_entries)):
                        term_val=language['term_entries'][t]['term_value']
                        
                        if(termSearch is not term_val):
                            syn.append(term_val)
                    syn=syn[0:len(term_entries)]
                    joinSyn='| '.join(syn)
            if('definition' in language.keys()):
                defi=language['definition']


    
    defi=re.sub(r'<[^>]*?>', '', defi)
    defi=defi.replace(',', '').replace('"', '').replace("'", '').replace(':', '').replace('.','').replace('(','').replace(')','').replace('IATE','')
    defi=re.sub(r'[0-9]', '', defi)
    return(defi,pref, syn)


def fillPrefIate(outFile, results, label, col, wsidmax, rels, maxx):  
    fp=jsonFile.full_pref(outFile)
    prefLabel_full=fp[1]
    targets_pref=fp[0]
    uri="https://iate.europa.eu/entry/result/"+str(maxx)

    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            if(rels==1 or rels==2):
                while(colm<=len(results[i]) and results[i][colTarget].strip(' ') not in targets_pref):
                    acento=re.search("[áéíóúÁÉÍÓÚ]+", results[i][colm])
                    if(acento!=None):
                        sin=quit_tilds(results[i][colm])
                        print(results[i][colm],'-', sin)
                    if(results[i][colm]!=""):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", results[i][colm]), 0, re.I)
                        n = normalize( 'NFC', n)
                        outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[i][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[i][colTarget], '@value': results[i][colm].strip(' ')}})
                        prefLabel_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                        targets_pref.append(results[i][colTarget].strip(' '))
                        logging.info('FOUND (Iate-prefLabe)l: '+results[i][colm]+' lang: '+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
            else:
                while(colm<=len(results[i]) and results[i][colTarget].strip(' ') not in targets_relation):
                    if(results[i][colm]!=""):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", results[i][colm]), 0, re.I)
                        n = normalize( 'NFC', n)
                        outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[i][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[i][colTarget], '@value': results[i][colm].strip(' ')}})
                        pref_relation.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                        targets_relation.append(results[i][colTarget].strip(' '))
                        logging.info('FOUND (Iate-prefLabe)l: '+results[i][colm]+' lang: '+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        if(rels==1 or rels==2):
            while(colm<=len(results[wsidmax]) and results[wsidmax][colTarget].strip(' ') not in targets_pref ):
                if(results[wsidmax][colm]!=""):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", results[wsidmax][colm]), 0, re.I)
                    n = normalize( 'NFC', n)
                    outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[wsidmax][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[wsidmax][colTarget], '@value': results[wsidmax][colm].strip(' ')}})
                    prefLabel_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget].strip(' '))
                    targets_pref.append(results[wsidmax][colTarget].strip(' '))
                    logging.info('FOUND (Iate-prefLabe)l: '+results[wsidmax][colm]+' lang: '+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
        else:
            while(colm<=len(results[wsidmax]) and results[wsidmax][colTarget].strip(' ') not in targets_relation ):
                if(results[wsidmax][colm]!=""):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", results[wsidmax][colm]), 0, re.I)
                    n = normalize( 'NFC', n)
                    outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[wsidmax][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[wsidmax][colTarget], '@value': results[wsidmax][colm].strip(' ')}})
                    pref_relation.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget].strip(' '))
                    targets_relation.append(results[wsidmax][colTarget].strip(' '))
                    logging.info('FOUND (Iate-prefLabe)l: '+results[wsidmax][colm]+' lang: '+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5

    return outFile

def fillAltIate(outFile, results,  label, col, wsidmax, rels, maxx):
    fp=jsonFile.full_pref(outFile)
    prefLabel_full=fp[1]
    targets_pref=fp[0]
    altLabel_full=jsonFile.full_alt(outFile)
    uri="https://iate.europa.eu/entry/result/"+str(maxx)
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            if(rels==1 or rels==2):
                while(colm<len(results[i])): 
                    for j in results[i][colm]:
                        alb=j.strip(' ')+'-'+results[i][colTarget]
                        if(j!="" and alb not in prefLabel_full and alb not in altLabel_full and results[i][colTarget] not in targets_pref):
                            n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                            normalize( "NFD", j), 0, re.I)
                            n = normalize( 'NFC', n)
                            outFile['skos-xl:prefLabel'].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[i][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[i][colTarget], '@value': j.strip(' ')}})
                            prefLabel_full.append(j.strip(' ')+'-'+results[i][colTarget])
                            targets_pref.append(results[i][colTarget])
                            logging.info('FOUND (Iate-prefLabe)l: '+j+' lang: '+results[i][colTarget])
                        elif(j!="" and alb not in prefLabel_full and alb not in altLabel_full):
                            outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':j.strip(' ').replace(' ', '-')+'-'+results[i][colTarget]+'-alt', 'source': uri, 'literalForm':{'@language':results[i][colTarget], '@value': j.strip(' ')}})
                            altLabel_full.append(j.strip(' ')+'-'+results[i][colTarget])
                            logging.info('FOUND (Iate-altLabel): '+j+' lang: '+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
            else:
                while(colm<len(results[i])):
                    for j in results[i][colm]: 
                        alb=j.strip(' ')+'-'+results[i][colTarget]
                        if(j!="" and alb not in pref_relation and alb not in alt_relation):
                            n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                            normalize( "NFD", j), 0, re.I)
                            n = normalize( 'NFC', n)
                            outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[i][colTarget]+'-alt', 'source': uri, 'literalForm':{'@language':results[i][colTarget], '@value': j.strip(' ')}})
                            alt_relation.append(j.strip(' ')+'-'+results[i][colTarget])
                            logging.info('FOUND (Iate-altLabel): '+j+' lang: '+results[i][colTarget])
                    colm=colm+5
                    colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        if(rels==1 or rels==2):
            while(colm<len(results[wsidmax])):
                for j in results[wsidmax][colm]:
                    alb=j.strip(' ')+'-'+results[wsidmax][colTarget]
                    if(j!="" and alb not in prefLabel_full and alb not in altLabel_full and results[wsidmax][colTarget] not in targets_pref):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", j), 0, re.I)
                        n = normalize( 'NFC', n)
                        outFile['skos-xl:prefLabel'].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[wsidmax][colTarget]+'-pref', 'source': uri, 'literalForm':{'@language':results[wsidmax][colTarget], '@value': j.strip(' ')}})
                        prefLabel_full.append(j.strip(' ')+'-'+results[wsidmax][colTarget])
                        targets_pref.append(results[wsidmax][colTarget])
                        logging.info('FOUND (Iate-prefLabe)l: '+j+' lang: '+results[wsidmax][colTarget])
                    elif(j!="" and alb not in prefLabel_full and alb not in altLabel_full):
                        outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':j.strip(' ').replace(' ', '-')+'-'+results[wsidmax][colTarget]+'-alt', 'source': uri, 'literalForm':{'@language':results[wsidmax][colTarget], '@value': j.strip(' ')}})
                        altLabel_full.append(j.strip(' ')+'-'+results[wsidmax][colTarget])
                        logging.info('FOUND (Iate-altLabel): '+j+' lang: '+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
        else:
            while(colm<len(results[wsidmax])):
                for j in results[wsidmax][colm]:
                    alb=j.strip(' ')+'-'+results[wsidmax][colTarget]
                    if(j!="" and alb not in pref_relation and alb not in alt_relation):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", j), 0, re.I)
                        n = normalize( 'NFC', n)
                        outFile['skos-xl:'+label].append({'@type':'skos-xl:Label', '@id':n.strip(' ').replace(' ', '-')+'-'+results[wsidmax][colTarget]+'-alt', 'source': uri, 'literalForm':{'@language':results[wsidmax][colTarget], '@value': j.strip(' ')}})
                        alt_relation.append(j.strip(' ')+'-'+results[wsidmax][colTarget])
                        logging.info('FOUND (Iate-altLabel): '+j+' lang: '+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
    return outFile

def fillDefinitionIate(outFile, results,   label,col, wsidmax, maxx):
    definition_full=jsonFile.full_def(outFile)
    if(wsidmax==None):
        for i in range(len(results)):
            colm=col
            colTarget=4
            while(colm<len(results[i]) ):
                if(results[i][colm]!=""):
                    outFile[label].append({'@language':results[i][colTarget], '@value':results[i][colm].strip(' ')})
                    definition_full.append(results[i][colm].strip(' ')+'-'+results[i][colTarget])
                    logging.info('FOUND (Iate-definition): '+results[i][colm]+' lang: '+results[wsidmax][colTarget])
                colm=colm+5
                colTarget=colTarget+5
    else:
        colm=col
        colTarget=4
        while(colm<len(results[wsidmax]) ):
            if(results[wsidmax][colm]!=""):
                outFile[label].append({'@language':results[wsidmax][colTarget], '@value':results[wsidmax][colm].strip(' ')})
                definition_full.append(results[wsidmax][colm].strip(' ')+'-'+results[wsidmax][colTarget])
                logging.info('FOUND (Iate-definition): '+results[wsidmax][colm]+' lang: '+results[wsidmax][colTarget])
            colm=colm+5
            colTarget=colTarget+5

    return outFile