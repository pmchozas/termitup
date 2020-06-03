# Termitup

This service converts a plain monolingual term list into a multilingual linked terminology by querying external resources that are part of the Linguistic Linked Open Data cloud (such as IATE and EuroVoc). 

## Execution from bash

### preprocess.py
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

### Creating IDs for new concepts: eurovoc_id_creation.py
This script creates new IDs for the terms retrieved from EuroVoc. This step is necessary to model them as skos:Concept and create the final RDF.

INPUT: EuroVoc target files (CSV)
OUTPUT: EuroVoc target files with ID assigned (CSV)

Example: `python3 eurovoc_id_creation.py contract2_eurosource_br_out.csv termino_id.csv contract2_eurosource_br_out_ID.csv` 


### Conversion into RDF
- Java version 1.8+
- Rmlmapper https://github.com/RMLio/rmlmapper-java/releases

To convert yaml file into ttl from bash: `yarrrml-parser -i mapping.yaml -o mapping.rml.ttl`

To run rmlmapper from bash: `java -jar rmlmapper.jar -m mapping.rml.ttl -o outputfileName.nt -d`

To remove empty strings from bash: `sed -i '' -e 's/<.*>.*<.*>.*""@.*//g' output.nt`

### api-all

Api Flask-Swagger

execute
-python app.py



