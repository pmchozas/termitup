# TermitUp


TermitUp is a tool for terminology enrichment: given a domain specific corpus, TermitUp performs statistical terminology extraction and post-process the resulting term list with a series of linguistic processes and external tools such as the Añotador (https://annotador.oeg.fi.upm.es/), to clean temporal expressions. Then, it queries several language resources (some part of the Linguistic Linked Open Data cloud) for candidate terms matching those in the term list. 

TermitUp builds sense indicators for both the source and the candidate terms, and performs a Word Sense Disambiguation process (with Semantic Web Company's service), matching those concepts with the closest domain. From the concepts matched in the external resources, TermitUp retrieves every piece of information available (translations, synonyms, definitions, usage notes and terminological relations), already disambiguated, and enriches the source term lists, creating links amongst the resources in the LLOD. 

See TermitUp Architecture: 

<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/termitup_architecture.png" width="70%" />


Afterwards, TermitUp offers the possibility of creating hierarchical relations amongst the terms in the source list and also of validating the synonymy relations retrieved from the external resources, by applying linguistic patterns and additional language resources. Finally, the results are published in separate json-ld files, modeled in SKOS and Ontolex (users' choice). Finally, TermitUp API publishes the enriched terminologies generated in a Virtuoso Enpoint, where they can be freely queried.

Examples of the SKOS and Ontolex models followed are shown below: 

### SKOS

<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/skos_model.png" width="30%" /> 

### Ontolex

<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/ontolex_model.png" width="40%" />


These models, however, are not able to model certain pieces of data that are very relevant when building enriched terminologies from heterogeneous data sources. Those limitations are discussed in the Wiki of the W3C Ontology-Lexicon Community Group, as a proposal for good practices to model enriched terminologies: https://www.w3.org/community/ontolex/wiki/Terminology

## TermitUp in R&D Projects

TermitUp has been developed within the European H2020 project Prêt-à-LLOD (https://pret-a-llod.github.io/), whose objective is to promote the generation and adoption of linguistic technologies that reuse Linked Data, in order to reduce the management and cleaning time that users currently spend when using linguistic data. The set of tools developed in this project, which includes TermitUp, will be applied in international pilots with different domains, including the pharmaceutical and government areas. Therefore, we expect that the impact of TermitUp in this case will be multilingual and cross-domain, since Prêt-à-LLOD consortium is composed of five research centers and universities and four industry partners, including Oxford University Press and Semantic Web Company. 

Additionally, TermitUp has been employed within the European Lynx project (https://lynx-project.eu/), aimed at building a multilingual and multi-jurisdictional knowledge graph to help both SMEs and large companies comply with the regulations in force in each country. Lynx contributions include Multilingual Search and Query Expansion systems, where language resources and, specifically, domain terminologies play a very important role. TermitUp has generated multilingual enriched terminologies (Dutch, English, German and Spanish) for each of the Lynx pilots, that are focused on three legal subdomains: labour law, contract law and industrial standards. The resulting terminologies are published in SKOS format and can be accessed through the Lynx Terminology platform (http://lkg.lynx-project.eu/kos) and are also available in Zenodo (https://zenodo.org/communities/lynx/?page=1\&size=20). 

TermitUp is also envisaged to be used in two ongoing projects: a national project supported by Grupo CPOnet (https://www.grupocponet.com/), focused on creating a service that, given a text, identifies and relates industry names with tax crimes, in order to evaluate the confidence level of a given company; and SmarTerp, whose aim is to develop a service that helps interpreting professionals by providing them extra information on the discourse at real time. 

## Authors

TermitUp has been developed by researchers from the Ontology Engineering Group (https://oeg.fi.upm.es/) of Universidad Politécnica de Madrid (https://www.upm.es/):
* Patricia Martín-Chozas (pmchozas@fi.upm.es)
* Karen Leticia Vázquez-Flores (kvazquez@delicias.dia.fi.upm.es)
* Pablo Caalleja (pcalleja@fi.upm.es)
* Elena Montiel-Ponsoda (emontiel@fi.upm.es)
* Víctor Rodríguez-Doncel (vrodriguez@fi.upm.es)

Visit TermitUp home: https://termitup.oeg.fi.upm.es/

Try TermitUp API: https://termitup.oeg.fi.upm.es/swagger/

Access TerrmitUp SPARQL Endpoint: https://termitup.oeg.fi.upm.es/sparql

Feedback is very welcome!



