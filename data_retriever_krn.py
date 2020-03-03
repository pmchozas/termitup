# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:45:08 2019
 @author: Sina Ahmadi - Patricia Martín Chozas  .

"""
import requests
from random import randint
import os
import requests
import json
import time

# =========================================
# 
# =========================================
def get_conceptNet_synonyms(term, lang="es"):
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
            # They are identical. No semantic relationship should be induced. 
            pass
        
        elif len(T) == len(A):
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
                        invalid = True

            if case_check.count(True) < len(T):
                semantic_relationship = "related"
            if not invalid and False not in case_check: 
                semantic_relationship = "synonymy"

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
                if len(syns):
                    if not (a in T or True in [True for s_t in syns if a in s_t]):
                        case_check = False
                else:
                    invalid = True

            if not invalid and case_check:
                semantic_relationship = "broader"

        else:
            pass

    return semantic_relationship

# =========================================
# main
# =========================================
# Read the configuration file
print("============ Reading the configuration file")
with open("configuration.json", 'r') as f:
    configuration = json.load(f)

idioma='es'
#term_id_file_dir = 'IDs/scterm_dict_%s.csv'%configuration["run_id"]
wikidata_output_file_name = idioma+"/participación_LT4185663.json"
'''not_found_file_name = "Log/not_found_%s.txt"%configuration["run_id"]
induction_dir = "Induction/%s.json"%configuration["run_id"]
filtered_output_dir = "Output/%s.json"%configuration["run_id"]
evaluation_results_dir = "Evaluation/%s.txt"%configuration["run_id"]'''

source_file = open(configuration["source_file_dir"], "r")
terms = [t for t in source_file.read().split("\n")]
# print(terms)
'''
TERM_ID_MAP = dict()
# Check if ID-term file exists
if os.path.isfile(term_id_file_dir):
    id_term = open(term_id_file_dir,'r').read().split("\n")
    TERM_ID_MAP = {t.split(", ")[0]: t.split(", ")[1] if len(t) else None for t in id_term}
# otherwise create a new one
else:
    a = open(term_id_file_dir,'w+')
    for t in terms:
        TERM_ID_MAP[t] = sctmid_creator()
        a.write(t+ ', '+ TERM_ID_MAP[t] + '\n')
    a.close()
'''
# ================
if configuration["retrieve_ConceptNet"]:
    print("====== Retrieving data from ConceptNet:")
    print(configuration["retrieve_ConceptNet"])
    print(wikidata_output_file_name)
    with open(wikidata_output_file_name, 'r') as f:
        retrieved_wikidata = json.load(f)
    all_inductions = list()
    #for item in retrieved_wikidata:
    induced_relationships = list()
        #for trans in item["translations"]:
        #    altLabel_induction = dict()
            #print(trans["name"].lower())
    for pref in retrieved_wikidata["skos:prefLabel"]:
        altLabel_induction = dict()
        #T = retrieved_wikidata["skos:inScheme"].lower().split()
        T=pref["@value"].lower().split()
        lang = pref["@language"]
        S = dict()
        for t in T:
            if t not in S:
                #print(t, lang)
                S[t] = get_conceptNet_synonyms(t, lang)
                #print(S[t])
            # S = get_conceptNet_synonyms(T.replace(" ", "_"), lang)
        print("T:", T, "lang:", lang, "S:", S)
        if len(S):
            for altLabel in retrieved_wikidata["skos:altLabel"]:
                A = altLabel["@value"].lower().split()
                if len(A):
                        # Go for axiom induction
                    T_A_relationship = inducer(T, A, S)
                    altLabel_induction[" ".join(A)] = T_A_relationship
                    print("A:", A, "SR:", T_A_relationship)
            else:
                # No synonyms found on ConceptNet"
                altLabel_induction = {}
                
            induced_relationships.append({"T":" ".join(T), "lang": lang, "S": S, "A": altLabel_induction})
            # Not to get timeout from ConceptNet API
            time.sleep(2)
        all_inductions.append(induced_relationships)
    '''
    print("==== Saving induced data.")
    with open(induction_dir, "w") as f:
        json.dump(all_inductions, f)
    # print(json.dumps(all_inductions, indent=4, sort_keys=True))
    # for trans in example["translations"]:
    #     for key, value in trans.items():
    #         print(key, value)
    # print(example.keys())
    # synonyms = get_conceptNet_synonyms("en", "discrimination")
    # print(synonyms)'''
