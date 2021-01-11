
from flask import jsonify, abort, request, Blueprint
from flask import Flask,render_template
import requests
from flask_restplus import Resource, Api, fields, reqparse
import json
from random import randint #libreria para random
import re
import os
from Unidecode import unidecode
from os import listdir
from os.path import isfile, isdir
#import time
#import termiup_terminal
from flask import Response
from modules_api import st_extraction
from modules_api import TBXTools
from modules_api import postprocess
from modules_api import conts_log
from modules_api import eurovocCode
from modules_api import Term
from modules_api import iateCode
from modules_api import unescoCode
from modules_api import wikidataCode
from modules_api import thesozCode
from modules_api import stwCode
from modules_api import iloCode
from modules_api import relvalCode
from modules_api import contextCode
from modules_api import term_id
from modules_api import rmlCode
from flask_rdf.flask import returns_rdf
from rdflib import Graph

REQUEST_API = Blueprint("term_api", __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route("/")
def index():
    pagetitle = "HomePage"
    return render_template("index.html")

"""
GET EXAMPLE. Still in development. needs to reead the input
"""
@REQUEST_API.route("/term", methods=["GET"])
def term():
    """
    to read parameters
    """
    termino = request.args.get("term")
    print(termino)
    
    return Response(json.dumps(termino),  mimetype="application/json")


"""
POST EXAMPLE
"""    
@REQUEST_API.route("/extract_terminology", methods=["POST"])
def extract_terminology():
    
    """
    to read body of a POST OR PUT
    """
    

    Corpus = request.args.get("corpus")
    Language = request.args.get("lang_in")
    print("Received:")
    print(Corpus)
    print(Language)
    

    
    terminology = st_extraction.termex(Corpus, Language)
    print(terminology)
   
    return Response(json.dumps(terminology),  mimetype="application/json")



"""
Test Patricia Postprocess
si rompo algo, borrar todo lo de abajo
"""

@REQUEST_API.route("/postproc_terminology", methods=["POST"])
def postproc_terminology():
    
    """
    to read body of a POST OR PUT
    """

    Terms = request.args.get("terms")
    Language = request.args.get("source_language")
    tasks= request.args.get("tasks")
    print("Received:")
    #print(Terms)
    print(Language)

    termlist=Terms.split(", ")
    tasklist=tasks.split(", ")
    print(tasklist)
    #Pablo proposal -------------------------------------
    """
    timeEx=True
    patternBasedClean=True
    pluralClean=True
    numbersClean=True
    accentClean=True
    """
    
    for t in tasklist:
        if "timeEx" in tasklist:
            timeEx=True
        else:
            timeEx=False
            
        if "patterns" in tasklist:
            patternBasedClean=True
        else:
            patternBasedClean=False
       
        if "plurals" in tasklist:
            pluralClean=True
        else:
            pluralClean=False
    
        if "numbers" in tasklist:
            numbersClean=True
        else:
            numbersClean=False
        
        if "accents" in tasklist:
            accentClean=True
        else:
            accentClean=False
            
    print(timeEx)

    # timeEx = request.args.get("timeEx", default=None, type=None)
    
    # print("timex")
    # print(timeEx)
    
    # patternBasedClean = request.args.get("patternBasedClean")
    # pluralClean = request.args.get("pluralClean")
    # numbersClean = request.args.get("numbersClean")
    # accentClean = request.args.get("accentClean")
    
    
    # print(timeEx)
    
    # Aquí estoy forzando todos los parámetros a TRUE. Lo suyo sería que viniesen del servicio web:
    """
    configurar el swagger json para meterle parametros y leerlos aquí: fijarse en el método /term
    por ejemplo, en el servicio poner el parametro de timex y que reciba 0/1 o true/false
    ejem:     timeEx=true
    
    el parámetro se lee aquí con:
        timeEx = request.args.get("timeEx")
        print(timeEx)
    
    """
    
    clean_terms= postprocess.preprocessing_terms(termlist, Language, timeEx, patternBasedClean, pluralClean, numbersClean, accentClean)
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(clean_terms),  mimetype="application/json")


#Patricia Enriching
@REQUEST_API.route("/enriching_terminology", methods=["POST"])
def enrinching_terminology():
    

   # to read body of a POST OR PUT


    

        
    

    # print("Received:")
    # #print(Terms)
    # print(myterm.langIn)
    # print(myterm.langOut)
    # print(corpus)
    # print(myterm.schema)
    # #termlist=terms.split(", ")
    

    #iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True


    #myterm.freq = request.args.get("frequency")
    #iate = request.args.get("iate")
        
    json_data = request.json
        
    resources= json_data["resources"]  
    reslist=resources.split(", ")
    
    for r in reslist:
        if "iate" in reslist:
            iate=True
        else:
            iate=False
            
        if "eurovoc" in reslist:
            eurovoc=True
        else:
            eurovoc=False
       
        if "unesco" in reslist:
            unesco=True
        else:
            unesco=False
    
        if "wikidata" in reslist:
            wikidata=True
        else:
            wikidata=False
        
        if "stw" in reslist:
            stw=True
        else:
            stw=False     
            
        if "thesoz" in reslist:
            thesoz=True
        else:
            thesoz=False        
        
        if "ilo" in reslist:
            ilo=True
        else:
            ilo=False 
            
        # if "ilo" in reslist:
        #     ilo=True
        # else:
        #     ilo=False 
        
    
    
    # iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True
    # thesoz=True
    # stw=True
    # eurovoc = request.args.get("eurovoc")
    # unesco = request.args.get("unesco")
    # wikidata = request.args.get("wikidata")
    myterms=[]
    
    
    corpus = json_data["corpus"]

    terms= json_data["terms"]
    termlist=terms.split(", ")             
    
    all_data=[]
    for t in termlist:
        print(t)
        myterm=Term.Term()
        myterm.term = t
        myterm.langIn = json_data["source_language"]
        myterm.schema = json_data["schema_name"]
        lang= json_data["target_languages"]
        output_format=json_data["output_format"]
        myterm.langOut=lang.split(", ")
        term_id.create_id(myterm)
        
        term_data= enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw, ilo, reslist, output_format)
        all_data.append(term_data)
        del myterm 
            

    # for myterm in myterms:
        
    #     print(myterm.term)
    #     term_data=enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw)
    #     all_data.append(term_data)

        
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(all_data),  mimetype="application/json")


def enrinching_terminology_internal(json_data):
    
    
    resources= json_data["resources"]  
    reslist=resources.split(", ")
    for r in reslist:
        if "iate" in reslist:
            iate=True
        else:
            iate=False
            
        if "eurovoc" in reslist:
            eurovoc=True
        else:
            eurovoc=False
       
        if "unesco" in reslist:
            unesco=True
        else:
            unesco=False
    
        if "wikidata" in reslist:
            wikidata=True
        else:
            wikidata=False
        
        if "stw" in reslist:
            stw=True
        else:
            stw=False     
            
        if "thesoz" in reslist:
            thesoz=True
        else:
            thesoz=False        
        
        if "ilo" in reslist:
            ilo=True
        else:
            ilo=False 
            
        # if "ilo" in reslist:
        #     ilo=True
        # else:
        #     ilo=False 
        
    
    
    # iate=True
    # eurovoc=True
    # unesco=True
    # wikidata=True
    # thesoz=True
    # stw=True
    # eurovoc = request.args.get("eurovoc")
    # unesco = request.args.get("unesco")
    # wikidata = request.args.get("wikidata")
    myterms=[]
    
    
    corpus = json_data["corpus"]

    terms= json_data["terms"]
    termlist=terms.split(", ")             
    
    all_data=[]
    for t in termlist:
        print(t)
        myterm=Term.Term()
        myterm.term = t
        myterm.langIn = json_data["source_language"]
        myterm.schema = json_data["schema_name"]
        lang= json_data["target_languages"]
        myterm.langOut=lang.split(", ")
        term_id.create_id(myterm)
        output_format=json_data["output_format"]
        term_data= enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw, ilo, reslist, output_format)
        all_data.append(term_data)
        del myterm 
            

    # for myterm in myterms:
        
    #     print(myterm.term)
    #     term_data=enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw)
    #     all_data.append(term_data)

        
    
    #clean_terms = postprocess.clean_terms(termlist, Language) #patri method
    #print(clean_terms)
   
    return Response(json.dumps(all_data),  mimetype="application/json")


def enrich_term(myterm, corpus, iate, eurovoc, unesco, wikidata, thesoz, stw, ilo, reslist, output_format):
    
    myterm.ids["ids"]={}
    myterm.relations["relations"]={}
    
    if len(corpus)>400:
    
        contextCode.extract_context(myterm, corpus)
    else:
        myterm.context=corpus

    if iate == True:
        iateCode.enrich_term_iate(myterm)
        myterm.ids["ids"]["iate"]=myterm.iate_id    
    if eurovoc == True:
        eurovocCode.enrich_term_eurovoc(myterm)
        myterm.ids["ids"]["eurovoc"]=myterm.eurovoc_id
        myterm.relations["relations"]["eurovoc"]=myterm.eurovoc_relations
    if unesco == True:
        unescoCode.enrich_term_unesco(myterm)
        myterm.ids["ids"]["unesco"]=myterm.unesco_id
        myterm.relations["relations"]["unesco"]=myterm.unesco_relations
    if wikidata==True:
        wikidataCode.enrich_term_wikidata(myterm)
        myterm.ids["ids"]["wikidata"]=myterm.wikidata_id
        myterm.relations["relations"]["wikidata"]=myterm.wikidata_relations
    if thesoz == True:
        thesozCode.enrich_term_thesoz(myterm)
        myterm.relations["relations"]["thesoz"]=myterm.thesoz_relations
        myterm.relations["relations"]["thesoz"]=myterm.thesoz_relations
    if stw == True:
        stwCode.enrich_term_stw(myterm)
        myterm.ids["ids"]["stw"]=myterm.stw_id
        myterm.relations["relations"]["stw"]=myterm.stw_relations
    if ilo == True:
        iloCode.enrich_term_ilo(myterm)
        myterm.ids["ids"]["ilo"]=myterm.ilo_id
        myterm.relations["relations"]["ilo"]=myterm.ilo_relations

    if output_format == "skos": 
        
        skos_data={
                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                    "@type": "skos:Concept",
                    "@id": myterm.term_id,
                    "inScheme": myterm.schema,
                    "example": {
                        "@language":myterm.langIn,
                        "@value":myterm.context
                        },
                    "source":[],
                    "closeMatch":[],
                    "prefLabel":[],
                    "altLabel":[],
                    "definition":[],
                    "broader":[],
                    "narrower":[],
                    "related":[],
                    "note":[]
                    
        
                }
        
    
        src_pref={
            "@language":myterm.langIn,
            "@value":myterm.term
            }
        
        skos_data["prefLabel"].append(src_pref)
        
        
        
        for langout in myterm.langOut:
            
            setPrefLang=  set()
            setPrefTerm= set()
            control_dict=[]
            
            for resource in reslist:
                if resource in myterm.synonyms.keys():
                    if myterm.langIn in myterm.synonyms[resource].keys():
                        for syn in myterm.synonyms[resource][myterm.langIn]:
                            syn_set={
                                "@language":myterm.langIn,
                                "@value": syn["syn-value"]
                                }
                            skos_data["altLabel"].append(syn_set)

                if resource in myterm.translations.keys():
                    if langout in myterm.translations[resource].keys():
                       for trans_set in myterm.translations[resource][langout]:
    
                           value= trans_set["trans-value"]
                           ispref=True
                           if(langout in setPrefLang):
                               ispref=False
    
                           setPrefLang.add(langout) 
                           setPrefTerm.add(value) 
                                                 
                           trans_pref={
                                "@language":langout,
                                "@value":trans_set["trans-value"]
                                }
                           if trans_pref not in control_dict:
                               control_dict.append(trans_pref)
                               if(ispref):
                                   skos_data["prefLabel"].append(trans_pref)
                               else:
                                   skos_data["altLabel"].append(trans_pref)   
                           else:
                               continue
                               
                                         
        
        if iate == True:
            skos_data["source"].append(myterm.iate_id)
            if len(myterm.related_ids_iate)>0:
                for related in myterm.related_ids_iate:
                    skos_data["related"].append(related)
            
            if len(myterm.note_iate)>0:
                for lang in myterm.note_iate.keys():
                    for note in myterm.note_iate[lang]:
                        note_set={
                            "@language":lang,
                            "@value":note,
                            }
                        skos_data["note"].append(note_set)
            
            if len(myterm.definitions_iate)>0:
                for lang in myterm.definitions_iate.keys():
                    for defi in myterm.definitions_iate[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
                
        if eurovoc == True:
            skos_data["closeMatch"].append(myterm.eurovoc_id)
            if len(myterm.definitions_eurovoc)>0:
                for lang in myterm.definitions_eurovoc.keys():
                    for defi in myterm.definitions_eurovoc[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.eurovoc_relations) >0:
                if "broader" in myterm.eurovoc_relations.keys():
                    for broader in myterm.eurovoc_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.eurovoc_relations.keys():
                    for narrower in myterm.eurovoc_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.eurovoc_relations.keys():
                    for related in myterm.eurovoc_relations["related"]:
                        skos_data["related"].append(related)            
    
        if wikidata == True:
            skos_data["closeMatch"].append(myterm.wikidata_id)
            if len(myterm.definitions_wikidata)>0:
                for lang in myterm.definitions_wikidata.keys():
                    for defi in myterm.definitions_wikidata[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.wikidata_relations) >0:
                if "broader" in myterm.wikidata_relations.keys():
                    for broader in myterm.wikidata_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.wikidata_relations.keys():
                    for narrower in myterm.wikidata_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.wikidata_relations.keys():
                    for related in myterm.wikidata_relations["related"]:
                        skos_data["related"].append(related)     
    
        if unesco == True:
            skos_data["closeMatch"].append(myterm.unesco_id)
            if len(myterm.definitions_unesco)>0:
                for lang in myterm.definitions_unesco.keys():
                    for defi in myterm.definitions_unesco[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.unesco_relations) >0:
                if "broader" in myterm.unesco_relations.keys():
                    for broader in myterm.unesco_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.unesco_relations.keys():
                    for narrower in myterm.unesco_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.unesco_relations.keys():
                    for related in myterm.unesco_relations["related"]:
                        skos_data["related"].append(related)
                        
        if ilo == True:
            skos_data["closeMatch"].append(myterm.ilo_id)
            if len(myterm.definitions_ilo)>0:
                for lang in myterm.definitions_ilo.keys():
                    for defi in myterm.definitions_ilo[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.ilo_relations) >0:
                if "broader" in myterm.ilo_relations.keys():
                    for broader in myterm.ilo_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.ilo_relations.keys():
                    for narrower in myterm.ilo_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.ilo_relations.keys():
                    for related in myterm.ilo_relations["related"]:
                        skos_data["related"].append(related)
                        
        if stw == True:
            skos_data["closeMatch"].append(myterm.stw_id)
            if len(myterm.definitions_stw)>0:
                for lang in myterm.definitions_stw.keys():
                    for defi in myterm.definitions_stw[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.stw_relations) >0:
                if "broader" in myterm.stw_relations.keys():
                    for broader in myterm.stw_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.stw_relations.keys():
                    for narrower in myterm.stw_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.stw_relations.keys():
                    for related in myterm.stw_relations["related"]:
                        skos_data["related"].append(related)
    
        if thesoz == True:
            skos_data["closeMatch"].append(myterm.thesoz_id)
            if len(myterm.definitions_thesoz)>0:
                for lang in myterm.definitions_thesoz.keys():
                    for defi in myterm.definitions_thesoz[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        skos_data["definition"].append(def_set)
            if len(myterm.thesoz_relations) >0:
                if "broader" in myterm.thesoz_relations.keys():
                    for broader in myterm.thesoz_relations["broader"]:
                        skos_data["broader"].append(broader)
                if "narrower" in myterm.thesoz_relations.keys():
                    for narrower in myterm.thesoz_relations["narrower"]:
                        skos_data["narrower"].append(narrower)
                if "related" in myterm.thesoz_relations.keys():
                    for related in myterm.thesoz_relations["related"]:
                        skos_data["related"].append(related)
        
        for key in list(skos_data.keys()):
            if skos_data[key] == [] or skos_data[key] == "" or skos_data[key] == {}:
                del skos_data[key]

                
                # del skos_data[key]
        print(skos_data)
            
        rdf_data=skos_data
    
    elif output_format == "ontolex":
        term_id.create_ontolex_ids(myterm)
        
        ontolex_data=[]
        concept_data={
                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                    "@type": "skos:Concept",
                    "@id": myterm.term_id,
                    "inScheme": myterm.schema,
                    "isReferenceOf":[],
                    "source":[],
                    "closeMatch":[],
                    "broader":[],
                    "narrower":[],
                    "related":[]

                }
        
        
        sense_data={
                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                    "@type": "ontolex:LexicalSense",
                    "@id": myterm.lexical_sense_id,
                    "reference":myterm.term_id,
                    "isSenseOf":myterm.lexical_entry_id,
                    "usageExample": {
                        "@language":myterm.langIn,
                        "@value":myterm.context
                        },
                    "definition":[],
                    "note":[]                    

            }
        entry_data={
                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                    "@type": "ontolex:LexicalEntry",
                    "@id": myterm.lexical_entry_id,
                    "sense":myterm.lexical_sense_id,
                    "form":myterm.form_id,
                    "writtenRep":{
                        "@language": myterm.langIn,
                        "@value":myterm.term
                        }
                    
            }
        source_set_id={
            "@id": myterm.lexical_sense_id
            }
        concept_data["isReferenceOf"].append(source_set_id)
        
        if iate == True:
            concept_data["source"].append(myterm.iate_id)
            if len(myterm.related_ids_iate)>0:
                for related in myterm.related_ids_iate:
                    concept_data["related"].append(related)
            
            if len(myterm.note_iate)>0:
                for lang in myterm.note_iate.keys():
                    for note in myterm.note_iate[lang]:
                        note_set={
                            "@language":lang,
                            "@value":note,
                            }
                        sense_data["note"].append(note_set)
            
            if len(myterm.definitions_iate)>0:
                for lang in myterm.definitions_iate.keys():
                    for defi in myterm.definitions_iate[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
                
        if eurovoc == True:
            concept_data["closeMatch"].append(myterm.eurovoc_id)
            if len(myterm.definitions_eurovoc)>0:
                for lang in myterm.definitions_eurovoc.keys():
                    for defi in myterm.definitions_eurovoc[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.eurovoc_relations) >0:
                if "broader" in myterm.eurovoc_relations.keys():
                    for broader in myterm.eurovoc_relations["broader"]:
                        concept_data["broader"].append(broader)
                if "narrower" in myterm.eurovoc_relations.keys():
                    for narrower in myterm.eurovoc_relations["narrower"]:
                        concept_data["narrower"].append(narrower)
                if "related" in myterm.eurovoc_relations.keys():
                    for related in myterm.eurovoc_relations["related"]:
                        concept_data["related"].append(related)            
    
        if wikidata == True:
            concept_data["closeMatch"].append(myterm.wikidata_id)
            if len(myterm.definitions_wikidata)>0:
                for lang in myterm.definitions_wikidata.keys():
                    for defi in myterm.definitions_wikidata[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.wikidata_relations) >0:
                if "broader" in myterm.wikidata_relations.keys():
                    for broader in myterm.wikidata_relations["broader"]:
                        concept_data["broader"].append(broader)
                if "narrower" in myterm.wikidata_relations.keys():
                    for narrower in myterm.wikidata_relations["narrower"]:
                        concept_data["narrower"].append(narrower)
                if "related" in myterm.wikidata_relations.keys():
                    for related in myterm.wikidata_relations["related"]:
                        concept_data["related"].append(related)     
    
        if unesco == True:
            concept_data["closeMatch"].append(myterm.unesco_id)
            if len(myterm.definitions_unesco)>0:
                for lang in myterm.definitions_unesco.keys():
                    for defi in myterm.definitions_unesco[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.unesco_relations) >0:
                if "broader" in myterm.unesco_relations.keys():
                    for broader in myterm.unesco_relations["broader"]:
                        concept_data["broader"].append(broader)
                if "narrower" in myterm.unesco_relations.keys():
                    for narrower in myterm.unesco_relations["narrower"]:
                        concept_data["narrower"].append(narrower)
                if "related" in myterm.unesco_relations.keys():
                    for related in myterm.unesco_relations["related"]:
                        concept_data["related"].append(related)
                        
        if ilo == True:
            concept_data["closeMatch"].append(myterm.ilo_id)
            if len(myterm.definitions_ilo)>0:
                for lang in myterm.definitions_ilo.keys():
                    for defi in myterm.definitions_ilo[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.ilo_relations) >0:
                if "broader" in myterm.ilo_relations.keys():
                    for broader in myterm.ilo_relations["broader"]:
                        sense_data["broader"].append(broader)
                if "narrower" in myterm.ilo_relations.keys():
                    for narrower in myterm.ilo_relations["narrower"]:
                        sense_data["narrower"].append(narrower)
                if "related" in myterm.ilo_relations.keys():
                    for related in myterm.ilo_relations["related"]:
                        concept_data["related"].append(related)
                        
        if stw == True:
            concept_data["closeMatch"].append(myterm.stw_id)
            if len(myterm.definitions_stw)>0:
                for lang in myterm.definitions_stw.keys():
                    for defi in myterm.definitions_stw[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.stw_relations) >0:
                if "broader" in myterm.stw_relations.keys():
                    for broader in myterm.stw_relations["broader"]:
                        concept_data["broader"].append(broader)
                if "narrower" in myterm.stw_relations.keys():
                    for narrower in myterm.stw_relations["narrower"]:
                        concept_data["narrower"].append(narrower)
                if "related" in myterm.stw_relations.keys():
                    for related in myterm.stw_relations["related"]:
                        concept_data["related"].append(related)
    
        if thesoz == True:
            concept_data["closeMatch"].append(myterm.thesoz_id)
            if len(myterm.definitions_thesoz)>0:
                for lang in myterm.definitions_thesoz.keys():
                    for defi in myterm.definitions_thesoz[lang]:
                        def_set={
                            "@language":lang,
                            "@value":defi,
                            }
                        sense_data["definition"].append(def_set)
            if len(myterm.thesoz_relations) >0:
                if "broader" in myterm.thesoz_relations.keys():
                    for broader in myterm.thesoz_relations["broader"]:
                        concept_data["broader"].append(broader)
                if "narrower" in myterm.thesoz_relations.keys():
                    for narrower in myterm.thesoz_relations["narrower"]:
                        concept_data["narrower"].append(narrower)
                if "related" in myterm.thesoz_relations.keys():
                    for related in myterm.thesoz_relations["related"]:
                        concept_data["related"].append(related)
        
         
        for resource in reslist:
            if resource in myterm.synonyms_ontolex.keys():
                if myterm.langIn in myterm.synonyms_ontolex[resource].keys():  
                    for syn_set in myterm.synonyms_ontolex[resource][myterm.langIn]:
                        syn_id=unidecode.unidecode(syn_set["syn-id"])
                        syn_sense_id=syn_id+"-sen"
                        syn_entry_id=syn_id+"-len"
                        syn_form_id=syn_id+"-form"
                        syn_value=syn_set["syn-value"]
                        senserel_id=myterm.lexical_sense_id+'-senrel-'+syn_sense_id
                        
                        syn_set_id={
                            "@id": syn_sense_id
                            }
                           
                        concept_data["isReferenceOf"].append(syn_set_id)
                           
                        syn_sense_data={
                                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                    "@type": "ontolex:LexicalSense",
                                    "@id": syn_sense_id,
                                    "reference":myterm.term_id,
                                    "isSenseOf":syn_entry_id                
                
                            }
                        syn_entry_data={
                                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                    "@type": "ontolex:LexicalEntry",
                                    "@id": syn_entry_id ,
                                    "sense": syn_sense_id,
                                    "form": syn_form_id,
                                    "writtenRep":{
                                        "@language": myterm.langIn,
                                        "@value":syn_value
                                                }
                    
                            }
                           
                        vartrans_syn_data={
                                    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                    "@type": "vartrans:senseRelation",
                                    "@id": senserel_id ,
                                    "category": "lexinfo:synonym",
                                    "relates": []
                                    
                               }
                        vartrans_syn_data['relates'].append(source_set_id)
                        vartrans_syn_data['relates'].append(syn_set_id)
                        ontolex_data.append(syn_sense_data) 
                        ontolex_data.append(syn_entry_data) 
                        ontolex_data.append(vartrans_syn_data)  
            
            if resource in myterm.translations_ontolex.keys():
                for lang in myterm.langOut:
                    if lang in myterm.translations_ontolex[resource].keys():
                        for trans_set in myterm.translations_ontolex[resource][lang]:
                            trans_id=trans_set['trans-id']
                            trans_sense_id=trans_id+"-sen"
                            trans_entry_id=trans_id+"-len"
                            trans_form_id=trans_id+"-form"
                            trans_value=trans_set["trans-value"]
                            senserel_id=myterm.lexical_sense_id+'-senrel-'+trans_sense_id 

                            trans_set_id={
                                "@id": trans_sense_id
                                }
                               
                            concept_data["isReferenceOf"].append(trans_set_id)
                        
                               
                            trans_sense_data={
                                        "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                        "@type": "ontolex:LexicalSense",
                                        "@id": trans_sense_id,
                                        "reference":myterm.term_id,
                                        "isSenseOf":trans_entry_id                
                    
                                }
                            trans_entry_data={
                                        "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                        "@type": "ontolex:LexicalEntry",
                                        "@id": trans_entry_id ,
                                        "sense": trans_sense_id,
                                        "form": trans_form_id,
                                        "writtenRep":{
                                            "@language": lang,
                                            "@value":trans_value
                                                    }
                        
                                }
                               
                            vartrans_trans_data={
                                        "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
                                        "@type": "vartrans:senseRelation",
                                        "@id": senserel_id ,
                                        "category": "lexinfo:translation",
                                        "relates": []
                                        
                                   }
                            vartrans_trans_data['relates'].append(source_set_id)
                            vartrans_trans_data['relates'].append(trans_set_id)
                            ontolex_data.append(trans_sense_data) 
                            ontolex_data.append(trans_entry_data) 
                            ontolex_data.append(vartrans_trans_data) 
        
        
        for key in list(concept_data.keys()):
            if concept_data[key] == [] or concept_data[key] == "" or concept_data[key] == {}:
                del concept_data[key]

        for key in list(sense_data.keys()):
            if sense_data[key] == [] or sense_data[key] == "" or sense_data[key] == {}:
                del sense_data[key]

        for key in list(entry_data.keys()):
            if entry_data[key] == [] or entry_data[key] == "" or entry_data[key] == {}:
                del entry_data[key]                

        
        ontolex_data.append(concept_data)
        ontolex_data.append(sense_data)
        ontolex_data.append(entry_data)
        rdf_data=ontolex_data
        # print(myterm.synonyms_ontolex)
        print(rdf_data)
        # print('SYNONYMS')
        # print(myterm.synonyms_eurovoc)
        # print(myterm.synonyms_ontolex)
        # print('TRANSLATIONS')
        # print(myterm.translations_eurovoc)
        # print(myterm.translations_ontolex)
        
    return rdf_data
    
    
    # data_mappings.update(myterm.ids)
    # data_mappings.update(myterm.relations)
    # data_mappings["synonyms"]=myterm.synonyms
    # data_mappings["translations"]=myterm.translations
    # data_mappings["definitions"]=myterm.definitions
    # data_mappings["term_reference"]=myterm.term_ref_iate
    # data_mappings["language_note"]=myterm.note_iate
    # data_mappings["related_iate"]=myterm.related_ids_iate
        
                        
    
# esto genera el json paara mappings
"""
    data_mappings={}
    data={
                "Source Term ID": myterm.term_id,
                "Source Term" : myterm.term,
                "Source Term Context": myterm.context,
                "Source Language": myterm.langIn
            
            }
    data_mappings.update(data)
    data_mappings.update(myterm.ids)
    data_mappings.update(myterm.relations)
    data_mappings["synonyms"]=myterm.synonyms
    data_mappings["translations"]=myterm.translations
    data_mappings["definitions"]=myterm.definitions
    data_mappings["term_reference"]=myterm.term_ref_iate
    data_mappings["language_note"]=myterm.note_iate
    data_mappings["related_iate"]=myterm.related_ids_iate
    """
        
    # data={
    #         "Source Term ID": myterm.term_id,
    #         "Source Term" : myterm.term,
    #         "Source Term Context": myterm.context,
    #         "Source Language": myterm.langIn
        
    #     }
    # iate_data={
    #         "IATE ID": myterm.iate_id,
    #         "IATE Synonyms + Synonym ID": myterm.syn_iate_ids,
    #         "IATE Translations + Translation ID": myterm.trans_iate_ids,
    #         "IATE Definitions": myterm.definitions_iate, 
    #         "IATE Definitions References": myterm.ref_def_iate,
    #         "IATE Term References": myterm.term_ref_iate,
    #         "IATE Language Notes": myterm.note_iate,
    #         "IATE Related Terms IDs": myterm.related_ids_iate
    #     }
    # eurovoc_data={
    #         "EUROVOC ID": myterm.eurovoc_id,
    #         "EUROVOC Synonyms + Synonym ID": myterm.syn_eurovoc_ids,
    #         "EUROVOC Relations": myterm.eurovoc_relations,
    #         "EUROVOC Definitions": myterm.definitions_eurovoc,
    #         "EUROVOC Translations + Translation ID": myterm.trans_eurovoc_ids
    #     }
    # unesco_data={
    #         "UNESCO ID": myterm.unesco_id,
    #         "UNESCO Synonyms + Synonym ID": myterm.syn_unesco_ids,
    #         "UNESCO Translations + Translation ID": myterm.trans_unesco_ids,
    #         "UNESCO Relations": myterm.unesco_relations
    #     }
    # wikidata_data={
    #         "WIKIDATA ID": myterm.wikidata_id,
    #         "WIKIDATA Synonyms + Synonym ID": myterm.syn_wikidata_ids,
    #         "WIKIDATA Translations + Translation ID": myterm.trans_wikidata_ids,
    #         "WIKIDATA Definitions": myterm.definitions_wikidata,
    #         "WIKIDATA Relations": myterm.wikidata_relations
    #     }
    # thesoz_data={
    #         "THESOZ ID": myterm.thesoz_id,
    #         "THESOZ Synonyms + Synonym ID": myterm.syn_thesoz_ids,
    #         "THESOZ Translations + Translation ID": myterm.trans_thesoz_ids,
    #         "THESOZ Definitions": myterm.definitions_thesoz,
    #         "THESOZ Relations": myterm.thesoz_relations
    #     }
    # stw_data={
    #         "STW ID": myterm.stw_id,
    #         "STW Synonyms + Synonym ID": myterm.syn_stw_ids,
    #         "STW Translations + Translation ID": myterm.trans_stw_ids, 
    #         "STW Definitions": myterm.definitions_stw,
    #         "STW Relations": myterm.stw_relations
    #     }
    # ilo_data={
    #         "ILO ID": myterm.ilo_id,
    #         "ILO Synonyms + Synonym ID": myterm.syn_ilo_ids,
    #         "ILO Translations + Translation ID": myterm.trans_ilo_ids,
    #         "ILO Relations": myterm.ilo_relations
    #     }
    
 
    
    # if iate == True:
    #     data.update(iate_data)
    #     print(data)
    # if eurovoc == True:
    #     data.update(eurovoc_data)
    # if unesco == True:
    #     data.update(unesco_data)
    # if wikidata==True:
    #     data.update(wikidata_data)
    # if thesoz == True:
    #     data.update(thesoz_data)
    # if stw == True:
    #     data.update(stw_data)
    # if ilo == True:
    #     data.update(ilo_data)
    
    # data={
    #         "Source Term ID": myterm.term_id,
    #         "Source Term" : myterm.term,
    #         "Source Term Context": myterm.context,
    #         "IATE ID": myterm.iate_id,
    #         "IATE Synonyms": myterm.synonyms_iate,
    #         "IATE Translations": myterm.translations_iate,
    #         "IATE Definitions": myterm.definitions_iate, 
    #         "IATE Definitions References": myterm.ref_def_iate,
    #         "IATE Term References": myterm.term_ref_iate,
    #         "IATE Language Notes": myterm.note_iate,
    #         "IATE Related Terms IDs": myterm.related_ids_iate,
    #         "EUROVOC ID": myterm.eurovoc_id,
    #         "EUROVOC Synonyms": myterm.synonyms_eurovoc,
    #         "EUROVOC Relations": myterm.eurovoc_relations,
    #         "EUROVOC Definitions": myterm.definitions_eurovoc,
    #         "EUROVOC Translations": myterm.translations_eurovoc,
    #         "UNESCO ID": myterm.unesco_id,
    #         "UNESCO Synonyms": myterm.synonyms_unesco,
    #         "UNESCO Translations": myterm.translations_unesco,
    #         "UNESCO Relations": myterm.unesco_relations,
    #         "WIKIDATA ID": myterm.wikidata_id,
    #         "WIKIDATA Synonyms": myterm.synonyms_wikidata,
    #         "WIKIDATA Translations": myterm.translations_wikidata,
    #         "WIKIDATA Definitions": myterm.definitions_wikidata,
    #         "WIKIDATA Relations": myterm.wikidata_relations,
    #         "THESOZ ID": myterm.thesoz_id,
    #         "THESOZ Synonyms": myterm.synonyms_thesoz,
    #         "THESOZ Translations": myterm.translations_thesoz,
    #         "THESOZ Definitions": myterm.definitions_thesoz,
    #         "THESOZ Relations": myterm.thesoz_relations,
    #         "STW ID": myterm.stw_id,
    #         "STW Synonyms": myterm.synonyms_stw,
    #         "STW Translations": myterm.translations_stw, 
    #         "STW Definitions": myterm.definitions_stw,
    #         "STW Relations": myterm.stw_relations,
    #         "ILO ID": myterm.ilo_id,
    #         "ILO Synonyms": myterm.synonyms_ilo,
    #         "ILO Translations": myterm.translations_ilo,
    #         "ILO Relations": myterm.ilo_relations
            
    #         }




@REQUEST_API.route("/relation_validation", methods=["POST"])
def relation_validation():
    myterm=Term.Term()
    
    myterm.term = request.args.get("term")
    myterm.langIn = request.args.get("source_language")
    syns= request.args.get("candidate_terms")
    
    
    
    relvaltest=relvalCode.relation_validation(myterm.term, myterm.langIn, syns)

    
    return Response(json.dumps(relvaltest),  mimetype="application/json")

@REQUEST_API.route("/rdf_conversion", methods=["POST"])
@returns_rdf 
def rdf_conversion():
    json_data = request.json 
    print(json_data)
    rdf_test=rmlCode.rml_converter(json_data)
    
    return Response(rdf_test.serialize(format="ntriples").decode("UTF-8"),  mimetype="text/ntriples")



# json_data = {
#   "terms": "contrato",
#   "resources": "eurovoc",
#   "source_language": "es",
#   "target_languages": "en",
#   "schema_name": "test",
#   "corpus": "El trabajador firmó un contrato con la compañía y ahora cobra dinero", 
#   "output_format": "skos"
# }


# test=enrinching_terminology_internal(json_data)
