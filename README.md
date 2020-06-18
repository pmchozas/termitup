# TermitUp


TermitUp is a tool for terminology enrichment: given a domain specific corpus, TermitUp performs statistical terminology extraction (with TBXTools) and cleans the resulting term list with a series of liguistic processes. Then, it queries several language resources (some part of the Linguistic Linked Open Data cloud) for candidate terms matching those in the term list. 

TermitUp builds sense indicators for both the source and the candidate terms, and performs a Word Sense Disambiguation process (with Semantic Web Company's service), matching those concepts with the closest domain. From the concepts matched in the external resources, TermitUp retrieves every piece of information available (translations, synonyms, definitions and terminological relations), already disambiguated, and enriches the source term lists, creating links amongst the resources in the LLOD. 

Afterwards, TermitUp offers the possibility of creating hierarchical relations amongst the terms in the source list and also of validating the synonymy relations retrieved from the external resources. Finally, the results are published in separate json-ld files, modeled in SKOS-XL, that permits keeping the provenance of specific pieces of the data retrieved. 

## Execution from bash

### postprocess.py
Requirements
JAVA 1.8 and environment variable JAVA_HOME

Before executing preprocess.py, you must install and execute Stanford CoreNLP in NLTK

- pip3 install -U nltk
- wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
- unzip stanford-corenlp-full-2018-02-27.zip
- cd stanford-corenlp-full-2018-02-27
- wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2018-02-27-models.jar
- wget https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-spanish.properties 
- cd stanford-corenlp-full-2018-02-27

- java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-serverProperties StanfordCoreNLP-spanish.properties \
-preload tokenize,ssplit,pos,ner,parse \
-status_port 9003  -port 9003 -timeout 15000

### main.py
### Statistical Terminology Extraction from corpus. Linguistic Postprocessing of the extracted terms. Terminology Enrichment from Language Resources (part of them in the LLOD) with definitions, translations, synonyms and terminological relations. 

This code requires:

python3 with the following libraries: argparse, csv, requests, json, random, re, os, collections

Arguments:

- "--sourceFile", help="Name of the source csv file (term list)"
- "lang", help="Source language of the corpus"
- "targets", help="Target languages for the info retrieved"
- "--contextFile", help="Path to the file to extract the context"
- "--wsid", help="Type yes or no for word sense disambiguation"
- "--type", help="Type the name of the schema (domain) without blank spaces"
- "--corpus", help="Path to the file to extract the terms"

Example: python3 main.py --lang es --targets "es de nl en" --contextFile data/corpus/estatuto_es.txt --wsid yes --schema "labourlaw" --corpus data/corpus/estatuto_es.txt   

INPUT: corpus.txt  
OUTPUT: enriched and linked jsonld files (one file per term)


### api-all

Api Flask-Swagger

execute
-python3 app.py



