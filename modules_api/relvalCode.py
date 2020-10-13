#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 13:09:13 2020

@author: pmchozas
"""
import requests


#devuelve sinónimos en el idioma de entrada




def get_conceptNet_synonyms(myterm):
    # Given a term, get the synonyms from ConcetpNet of the same language
    # Note that all words are in lower case on ConceptNet, unlike Wikidata
    # Start and end edges should be taken into account
    synonyms = list()
    query_url_pattern = "http://api.conceptnet.io/query?EDGEDIRECTION=/c/LANG/TERM&rel=/r/Synonym&limit=1000"
    
    edge_directions = {"start":"end", "end":"start"}
    for direction in edge_directions.keys():
        query_url = query_url_pattern.replace("EDGEDIRECTION", direction).replace("LANG", myterm.langIn).replace("TERM", myterm.term)
        # print(query_url)
        obj = requests.get(query_url).json()
        for edge_index in range(len(obj['edges'])):
            syn_lang = obj['edges'][edge_index][edge_directions[direction]]["language"]
            if syn_lang == myterm.langIn:
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

