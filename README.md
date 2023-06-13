# TermitUp

TermitUp is a tool for terminology enrichment: given a domain specific corpus, TermitUp performs statistical terminology extraction and post-process the resulting term list with a series of linguistic processes and external tools such as the Añotador (https://annotador.oeg.fi.upm.es/), to clean temporal expressions. Then, it queries several language resources (some part of the Linguistic Linked Open Data cloud) for candidate terms matching those in the term list. 

TermitUp builds sense indicators for both the source and the candidate terms, and performs a Word Sense Disambiguation process (with Semantic Web Company's service), matching those concepts with the closest domain. From the concepts matched in the external resources, TermitUp retrieves every piece of information available (translations, synonyms, definitions, usage notes and terminological relations), already disambiguated, and enriches the source term lists, creating links amongst the resources in the LLOD. 

See TermitUp Architecture: 
<p align="center">
<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/termitup_arch.png" width="60%" />
</p>

Afterwards, TermitUp offers the possibility of creating hierarchical relations amongst the terms in the source list and also of validating the synonymy relations retrieved from the external resources, by applying linguistic patterns and additional language resources. Finally, the results are published in separate json-ld files, modeled in SKOS and Ontolex (users' choice). Finally, TermitUp API publishes the enriched terminologies generated in a Virtuoso Enpoint, where they can be freely queried.

Examples of the SKOS and Ontolex models followed are shown below: 

### SKOS
<p align="center">
<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/skos_model.png" width="30%" /> 
</p>

### Ontolex
<p align="center">
<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/ontolex_model.png" width="40%" />
</p>

These models, however, are not able to model certain pieces of data that are very relevant when building enriched terminologies from heterogeneous data sources. Those limitations are discussed in the Wiki of the W3C Ontology-Lexicon Community Group, as a proposal for good practices to model enriched terminologies: https://www.w3.org/community/ontolex/wiki/Terminology

## Useful links 

Visit TermitUp home: https://termitup.oeg.fi.upm.es/

Try TermitUp API: https://termitup.oeg.fi.upm.es/swagger/

Access TerrmitUp SPARQL Endpoint: https://termitup.oeg.fi.upm.es/sparql

DOI: https://doi.org/10.5281/zenodo.4461806


## TermitUp in R&D Projects

TermitUp has been developed within the European H2020 project Prêt-à-LLOD (https://pret-a-llod.github.io/), whose objective is to promote the generation and adoption of linguistic technologies that reuse Linked Data, in order to reduce the management and cleaning time that users currently spend when using linguistic data. The set of tools developed in this project, which includes TermitUp, will be applied in international pilots with different domains, including the pharmaceutical and government areas. Therefore, we expect that the impact of TermitUp in this case will be multilingual and cross-domain, since Prêt-à-LLOD consortium is composed of five research centers and universities and four industry partners, including Oxford University Press and Semantic Web Company. 

Additionally, TermitUp has been employed within the European Lynx project (https://lynx-project.eu/), aimed at building a multilingual and multi-jurisdictional knowledge graph to help both SMEs and large companies comply with the regulations in force in each country. Lynx contributions include Multilingual Search and Query Expansion systems, where language resources and, specifically, domain terminologies play a very important role. TermitUp has generated multilingual enriched terminologies (Dutch, English, German and Spanish) for each of the Lynx pilots, that are focused on three legal subdomains: labour law, contract law and industrial standards. The resulting terminologies are published in SKOS format and can be accessed through the Lynx Terminology platform (http://lkg.lynx-project.eu/kos) and are also available in Zenodo (https://zenodo.org/communities/lynx/?page=1\&size=20). 

TermitUp is also envisaged to be used in two ongoing projects: a national project supported by Grupo CPOnet (https://www.grupocponet.com/), focused on creating a service that, given a text, identifies and relates industry names with tax crimes, in order to evaluate the confidence level of a given company; and SmarTerp, whose aim is to develop a service that helps interpreting professionals by providing them extra information on the discourse at real time. 

## TermitUp API

TermitUp can be easily used through the swagger rest service: https://termitup.oeg.fi.upm.es/swagger/

The swagger is composed of four methods: 

#### Terminology Extraction
Parameters:
- Language of the source terms: es/en 
- Corpus containing the terms (raw text)

Output: List of automatically extracted terms

#### Terminology Post-processing

Parameters: 
- Terms to postprocess, separated by commas.
- Tasks: Write timeEx to remove temporal expressions; write patterns to remove non terminological structures in Spanish; write plurals to remove plurals in Spanish; write accents to remove accents in Spanish. To perform several tasks, write them separated by commas: "tasks": "timeEx, patterns, numbers"
- Language of the source terms: es/en 

Output: List of automatically post-processed (clean) terms

#### Terminology Enriching

Parameters: 
- Terms: terms to enrich, separated by commas.
- Resources: External resources to enrich the terms, separated by commas: eurovoc, iate, wikidata, unesco, thesoz, stw, ilo.
- Source_language: language of the source terms.
- Target_languages: language or languages of the desired information to retrieve.
- Schema_name: name of the domain to which the terms belong (preferably one word).
- Corpus: text from which the terms have been extracted.
- Relval: write "yes" or "no" to invoke validate_relations module.
- Output_format: write "skos" or "ontolex" to structure the output terminologies accordingly.
- Sparql_publishing: write "yes" or "no" to publish the output terminologies in TermitUp SPARQL Endpoint

Output: enriched terminologies with translations, synonyms, definitions, conceptual relations and additional linguistic information (usage notes, references, etc.), linked with resources in the LLOD, structured in SKOS/Ontolex. 

#### Relation Validation

Parameters: 
- Source term: the original term, for instance, worker
- Source language: the language of the original term
- Candidate terms: candidate terms to validate relations, separated by commas, in the same language as the source term: domestic worker, civil worker

Output: the type of relation amongst the original term and the candidate terms, supported by linguistic patterns and ConceptNet

#### TermitUp SPARQL Endpoint
Activating the sparql_publishing parameter in the Terminology Enriching module allows the publication of the terminologies in TermitUp SPARQL Endpoint: https://termitup.oeg.fi.upm.es/sparql

## Authors

TermitUp has been developed by researchers from the Ontology Engineering Group (https://oeg.fi.upm.es/) of Universidad Politécnica de Madrid (https://www.upm.es/):
* Patricia Martín-Chozas (pmchozas@fi.upm.es)
* Karen Leticia Vázquez-Flores (kvazquez@delicias.dia.fi.upm.es)
* Pablo Calleja (pcalleja@fi.upm.es)
* Elena Montiel-Ponsoda (emontiel@fi.upm.es)
* Víctor Rodríguez-Doncel (vrodriguez@fi.upm.es)


Feedback is very welcome!



<p align="center">
            <img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/logopal.png" width="12%">
            <img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/Logo_OEG.gif" width="10%">
            <img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/fi.jpg" width="8%">
            <img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/upm.jpg" width="10%">
            
</p>

## Citation
Martín-Chozas, P., Vázquez-Flores, K., Calleja, P., Montiel-Ponsoda, E., and Rodríguez-Doncel, V. (2022). TermitUp: Generation and Enrichment of Linked Terminologies. Semantic Web, 13, 967–986. 36.

