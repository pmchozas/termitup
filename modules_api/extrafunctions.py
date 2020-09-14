import json
import jsonFile
import re
from unicodedata import normalize
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)


def check_prefLabel(outFile, targets, rels):
    targetsNull=[]
    #print(outFile)
    prefLabel=outFile['skos-xl:prefLabel']
    fp=jsonFile.full_pref(outFile)
    targets_pref=fp[0]
    if(rels==1 or rels==2):
        for i in range(len(targets)):
            if(targets[i] not in targets_pref):
                targetsNull.append(targets[i])
    else:
        for i in range(len(targets)):
            if(targets[i] not in targets_relation):
                targetsNull.append(targets[i])
    
    return(targetsNull)

def property_add( value, lang, outFile, label,rels, uri ):
    if('eurovoc' in uri):
        resource='Eurovoc'
    if('unesco' in uri):
        resource='Unesco'
    if('wikidata' in uri):
        resource='Wikidata'
    if('lexicala' in uri):
        resource='Lexicala'



    if(label=='definition'):
        label_file=outFile[label]
    else:
        label_file=outFile['skos-xl:'+label] 
    fp=jsonFile.full_pref(outFile)
    prefLabel_full=fp[1]
    targets_pref=fp[0]
    altLabel_full=jsonFile.full_alt(outFile)
    definition_full=jsonFile.full_def(outFile)
 
    if(rels==1 or rels==2):
        if(len(label_file)==0):
            if(label=='prefLabel'):

                plb=value.strip(' ')+'-'+lang
                if(plb not in prefLabel_full and lang not in targets_pref):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                    )
                    n = normalize( 'NFC', n)
                    n2= n.replace(' ', '-')
                    label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    prefLabel_full.append(plb)
                    targets_pref.append(lang)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in prefLabel_full and alb not in altLabel_full):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                    )
                    n = normalize( 'NFC', n)
                    n2= n.replace(' ', '-')
                    label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    altLabel_full.append(alb)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
            elif(label=='definition'):
                dlb=value.strip(' ')+'-'+lang
                if(dlb not in definition_full):
                    label_file.append({'@language':lang, '@value': value.strip(' ')})
                    definition_full.append(dlb)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in prefLabel_full and lang not in targets_pref ):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                        )
                        n = normalize( 'NFC', n)
                        n2= n.replace(' ', '-')
                       
                        label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        prefLabel_full.append(plb)
                        targets_pref.append(lang)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in prefLabel_full and alb not in altLabel_full):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                        )
                        n = normalize( 'NFC', n)
                        n2= n.replace(' ', '-')
                        label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        altLabel_full.append(alb)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                elif(label=='definition'):
                    dlb=value.strip(' ')+'-'+lang
                    if(dlb not in definition_full):
                        label_file.append({'@language':lang, '@value': value.strip(' ')})
                        definition_full.append(dlb)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
    else:
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in pref_relation and lang not in targets_relation):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                    )
                    n = normalize( 'NFC', n)
                    n2= n.replace(' ', '-')
                    label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    pref_relation.append(plb)
                    targets_relation.append(lang)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in pref_relation and lang not in targets_relation):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                    )
                    n = normalize( 'NFC', n)
                    n2= n.replace(' ', '-')
                    label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    pref_relation.append(alb)
                    targets_relation.append(lang)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                elif(alb not in pref_relation and alb not in alt_relation):
                    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                    )
                    n = normalize( 'NFC', n)
                    n2= n.replace(' ', '-')
                    label_file.append({'@language':lang, '@value':n.strip(' ')})
                    alt_relation.append(alb)
                    logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
            
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in pref_relation and lang not in targets_relation ):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                        )
                        n = normalize( 'NFC', n)
                        n2= n.replace(' ', '-')
                        label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        pref_relation.append(plb)
                        targets_relation.append(lang)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in pref_relation and lang not in targets_relation):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                        )
                        n = normalize( 'NFC', n)
                        n2= n.replace(' ', '-')
                        label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        pref_relation.append(alb)
                        targets_relation.append(lang)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
                    elif(alb not in pref_relation and alb not in alt_relation):
                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", value), 0, re.I
                        )
                        n = normalize( 'NFC', n)
                        n2= n.replace(' ', '-')
                        label_file.append({'@type':'skos-xl:Label', '@id':n2.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        alt_relation.append(alb)
                        logging.info('FOUND ('+resource+'-'+label+'): '+value+' lang: '+lang)
    return(outFile)

   