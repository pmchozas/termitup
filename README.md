# TermitUp


TermitUp is a tool for terminology enrichment: given a domain specific corpus, TermitUp performs statistical terminology extraction and post-process the resulting term list with a series of liguistic processes and external tools such as the Añotador (https://annotador.oeg.fi.upm.es/), to clean temporal expressions. Then, it queries several language resources (some part of the Linguistic Linked Open Data cloud) for candidate terms matching those in the term list. 

TermitUp builds sense indicators for both the source and the candidate terms, and performs a Word Sense Disambiguation process (with Semantic Web Company's service), matching those concepts with the closest domain. From the concepts matched in the external resources, TermitUp retrieves every piece of information available (translations, synonyms, definitions, usage notes and terminological relations), already disambiguated, and enriches the source term lists, creating links amongst the resources in the LLOD. 

Afterwards, TermitUp offers the possibility of creating hierarchical relations amongst the terms in the source list and also of validating the synonymy relations retrieved from the external resources, by applying linguistic patterns and additional language resources. Finally, the results are published in separate json-ld files, modeled in SKOS and Ontolex (users' choice).

Finally, TermitUp API offers a publication module that relies on Terminoteca RDF, where the previously generated JSON-LD files can be stored and freely queried.


Visit TermitUp home: https://termitup.oeg.fi.upm.es/
and try TermitUp API: https://termitup.oeg.fi.upm.es/swagger/

Feedback is very welcome!



