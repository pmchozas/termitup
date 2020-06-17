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

### searchTerm_all.py
### Querying terms to expand with definitions, synonyms and synonyms disambiguation according to a context
This code requires:
python3 with the following libraries: argparse, csv, requests, json, random, re, os, collections

Arguments:
- "--sourceTerm", help="Source term to search"
- "lang", help="Source language"
- "--targets", help="Source language out"
- "--context", help="Context to disambiguate"

For example: python3 searchTerm_all.py "maternity leave" en --targets "en es de nl" iate
input: term, language in, language out, api name
output: Definition and synonyms in languague out

For example: python3 searchTerm_all.py "maternity leave" en eurovoc
input: term, language in, api name
output: Broader term, Narrower term, Related term

For example: python3 searchTerm_all.py "maternity leave" en --targets "en es de nl" --context "period in which a woman is legally allowed to be absent from work in the weeks before and after she gives birth" syns
For example: python3 searchTerm_all.py "descanso" es --targets "en de nl es" --context "Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella." syns
input: term, language in, language out, context, api name
output: Definition disambiaguate with synonym, and synonyms in language out


For example: python3 searchTerm_all.py descanso es --targets "en de nl es" all
input: term, language in, language out, all
out put:
-Definition and synonyms in languague out
-Broader term, Narrower term, Related term
-Definition disambiaguate with synonym, and synonyms in language out



### Querying IATE: iate.py
From IATE, we retrieve:
- Translations 
- Synonyms
- Definitions

This code requires:

python3 with the following libraries: argparse, csv, requests, json, random, re, os, collections

Arguments:

- "--sourceFile", help="Name of the source csv file (term list)"
- "--sourceTerm", help="Source term to search"
- "--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms"
- "--termId", help="Name of the termino_id file, to save terms and ids"
- "--targetFile", help="Name of the target file"
- "--euroSource", help="Name of the eurovoc source file without extension"
- "lang", help="Source language"
- "apiName", help="Name of the api: 'iate' or 'eurovoc'"

Example: `python3 iate.py --sourceFile sources/contracts_v2.csv --type a  --termId termino_id.csv --targetFile contracts_v2_out.csv --euroSource contracts2_eurosource en iate`  

INPUT: plain list of terms in CSV format
OUTPUT:
- CSV file with the info retrieved from IATE. The code generates a repetitive csv file, ugly for human eye, but necessary to convert the files into RDF with RMLmapper.
- Eurovoc source files: one CSV file per each terminological relation: broader, narrower, related. These are necessary to execute eurovoc queries. 

Note: iate.py results are filtered by domain, specifically, the legal domain. To query the whole iate, please delete the filters by domain in "haceJson" function. To generate human readable results, please use iage_comas.py

### Querying EuroVoc: eurovoc.py
From EuroVoc, we retrieve:
- Broader terms 
- Narrower terms
- Related terms

This code requires:

python3 with the following libraries: argparse, csv, SPARQLWrapper, multiprocessing, time

Arguments:

- "--sourceFile", help="Name of the source csv file (term list)"
- "--sourceTerm", help="Source term to search"
- "--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms"
- "--targetFile", help="Name of the target file"
- "query", help="Broader, narrower or related" 
- "lang", help="Source language"  (Write `todos` to retrieve results in en, es, de and nl.)

Example: `python3 eurovoc.py --sourceFile contract2_eurosource_br.csv --type w --targetFile contract2_eurosource_br_out.csv broader todos` 

INPUT: Eurovoc sources generated from iate.py (CSV files)
OUTPUT: Eurovoc output (CSV files)

### api-all

Api Flask-Swagger

execute
-python app.py



