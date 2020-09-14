import json
import requests
import time
import check_term
import eurovocCode
import spacy
from nltk.corpus import stopwords
from time import time
import trans_id
import re
from unicodedata import normalize
import jsonFile
nlp = spacy.load('es_core_news_sm')
# =========================================
# 
# =========================================
def get_conceptNet_synonyms(term, lang):
    # Given a term, get the synonyms from ConcetpNet of the same language
    # Note that all words are in lower case on ConceptNet, unlike Wikidata
    # Start and end edges should be taken into account
    synonyms = list()
    query_url_pattern = "http://api.conceptnet.io/query?EDGEDIRECTION=/c/LANG/TERM&rel=/r/Synonym&limit=1000"
    
    edge_directions = {"start":"end", "end":"start"}
    for direction in edge_directions.keys():
        query_url = query_url_pattern.replace("EDGEDIRECTION", direction).replace("LANG", lang).replace("TERM", term)
        # print(query_url)
        obj = requests.get(query_url).json()
        for edge_index in range(len(obj['edges'])):
            syn_lang = obj['edges'][edge_index][edge_directions[direction]]["language"]
            if syn_lang == lang:
                synonyms.append(obj['edges'][edge_index][edge_directions[direction]]["label"])
    return list(set(synonyms))

def inducer(T, A, S):
    # Gets T, the list of preferred labels and A, the list of alternative labels
    # Using synonyms of T, S, it induces the semantic relationship that exists between T and A. 
    # S is a dictionary of word as term and dictionary {lang: synonyms} as values.
    semantic_relationship = None
    
    if len(A) and len(T):
        invalid = False


        if " ".join(A).lower() == " ".join(T).lower():
            #print('aqui')
            # They are identical. No semantic relationship should be induced. 
            pass
        
        elif len(T) == len(A) :
            #print('len A == len A')
            case_check = list()
            stop=stopwords.words('spanish')

            for t in T:
                if t not in stop:
                    if t in A :
                        case_check.append(True)
                    else:
                        # check if the language exists
                        if len(S[t]):
                            
                            if True in [True for s_t in S[t] if s_t in A]:
                                #print('True')
                                case_check.append(True)
                            else:
                                #print('False')
                                case_check.append(False)
                        else:
                            invalid = True
            #print(case_check, len(T), case_check.count(True), invalid)

            #if case_check.count(True) < len(T) and not invalid:
            if case_check.count(True) < len(T) and case_check.count(True)>0:
                #print('related')
                semantic_relationship = "related"
            if not invalid and False not in case_check: 
                #print('syn')
                semantic_relationship = "synonymy"
            #else:semantic_relationship = None
            if(case_check.count(False) >case_check.count(True) ):
                semantic_relationship = None


        elif len(T) < len(A):
            case_check = list()
            for t in T:
                if t in A:
                    case_check.append(True)
                else:
                    # check if the language exists
                    if len(S[t]):
                        if True in [True for s_t in S[t] if s_t in A]:
                            case_check.append(True)
                        else:
                            case_check.append(False)
                    else:
                        case_check.append(False)

            # print(case_check)
            if False not in case_check:
                semantic_relationship = "narrower"

        elif len(T) > len(A):
            case_check = True
            for a in A:
                # Find all the synonyms of the existing terms
                syns = list()
                for term_syn in S.values():
                    if len(term_syn):
                        syns = syns + term_syn
                    else:
                        pass

                syns = list(set(syns))
                #print('sysn set', syns)

                if len(syns):
                    #if([True for s_t in syns if a in s_t])
                    if not (a in T ):
                        case_check = False
                    #if not (a in T or True in [True for s_t in syns if a in s_t]):
                    #    case_check = False
                else:
                    invalid = True
            #print(case_check, invalid)
            #if case_check is True and invalid is False:
            #   pass
            if not invalid and case_check:
                semantic_relationship = "broader"

        else:
            pass
    #print(semantic_relationship)
    return semantic_relationship
# =========================================
# main
# =========================================
# Read the configuration file
def main(outFile, file_schema, targets, clean, lang_in):
    print("============ Relval")

    # ================
    if('skos-xl:prefLabel' in outFile.keys()):
        pref=outFile['skos-xl:prefLabel']
        for i in range(len(pref)):
            altLabel_induction = dict()
            #print(pref[i]['literalForm'])
            lang=pref[i]['literalForm']['@language']
            value1=pref[i]['literalForm']['@value']
            T=pref[i]['literalForm']['@value'].lower().split()
            #print('T: ', T, lang)
            S = dict()
            for t in T:
                if t not in S:
                    S[t] = get_conceptNet_synonyms(t, lang)
            # S = get_conceptNet_synonyms(T.replace(" ", "_"), lang)
            #print("T:", T, "lang:", lang, "S:", S)
            #print(S)
            if len(S):
                if ('skos-xl:altLabel' in outFile.keys()):
                    alt=outFile['skos-xl:altLabel']
                    for j in alt:
                        #print(alt[i]['literalForm'])
                        #print(j)
                        item1=j
                        value2=j['literalForm']['@value']
                        A=j['literalForm']['@value'].lower().split()
                        language=j['literalForm']['@language']
                        #print('A: ', A, language)
                        if(lang=='es'):
                            if len(A):
                                # Go for axiom induction    
                                T_A_relationship = inducer(T, A, S)
                                altLabel_induction[" ".join(A)] = T_A_relationship
                                #print('T: ', T, 'A: ',A, 'S: ', S)
                                #print("A:", A, "SR:", T_A_relationship)
                                #print('--------------------------')
                                if(T_A_relationship!=None):
                                    if(T_A_relationship!='synonymy'):
                                        print('T: ', T, 'A: ',A, 'S: ', S)
                                        print("A:", A, "SR:", T_A_relationship)
                                        print('--------------------------')
                                        ind=alt.index(item1)
                                        #print(item1, ind)
                                        del outFile["skos-xl:altLabel"][ind]
                                        check=check_term.checkTerm(lang,value2, '', [language], '')
                                        ide=check[0]
                                        ide_file=ide
                                        termSearch=check[1]
                                        #print('TERM A BUSCAR:----------- ', termSearch)
                                        if(termSearch!='1'):
                                            eurovocCode.eurovoc_file(termSearch, ide, T_A_relationship, 'uri', language, 'labourlaw',  outFile["@id"], file_schema, outFile,targets)
                                        full=jsonFile.full_rels(outFile, T_A_relationship)
                                        cadena = re.sub('[/,+.;:/)([]]*', '',  value2)
                                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                                                            normalize( "NFD", cadena), 0, re.I
                                            )
                                        n = normalize( 'NFC', n)
                                        uri=n.replace(' ','-')+'-'+lang

                                        if(uri not in full):
                                            if(T_A_relationship not in outFile.keys()):
                                                outFile[T_A_relationship]=[]
                                                outFile[T_A_relationship].append(uri)
                                            else:
                                                outFile[T_A_relationship].append(uri)
                                        
                if (len(clean)):
                   
                    for j in clean:
                        #print(alt[i]['literalForm'])
                        item1=j
                        value2=j
                        A=j.lower().split()
                        language=lang_in
                        #print('A: ', A, language)
                        if(language=='es'):
                            if len(A):
                                # Go for axiom induction    
                                T_A_relationship = inducer(T, A, S)
                                altLabel_induction[" ".join(A)] = T_A_relationship
                                if(T_A_relationship!=None):
                                    if(T_A_relationship!='synonymy'):
                                        print('T: ', T, 'A: ',A, 'S: ', S)
                                        print("A:", A, "SR:", T_A_relationship)
                                        print('--------------------------')
                                        
                                        
                                        #ide=trans_id.trans_ID(value2, lang)
                                        full=jsonFile.full_rels(outFile, T_A_relationship)
                                        cadena = re.sub('[/,+.;:/)([]]*', '',  value2)
                                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                                                            normalize( "NFD", cadena), 0, re.I
                                            )
                                        n = normalize( 'NFC', n)
                                        uri=n.replace(' ','-')+'-'+lang
                                        if(uri not in full):
                                            if(T_A_relationship not in outFile.keys()):
                                                outFile[T_A_relationship]=[]
                                                outFile[T_A_relationship].append(uri)
                                            else:
                                                outFile[T_A_relationship].append(uri)
                                
            else:
                # No synonyms found on ConceptNet"
                altLabel_induction = {}
    #print(outFile)
    return (outFile)
                





