from modules_api import iateCode
from modules_api import wsidCode
from modules_api import eurovocCode
from modules_api import unescoCode
from modules_api import wikidataCode
from modules_api.Term import Term
from modules_api import thesozCode
from modules_api import stwCode
# def iate_enriching_terms(terms,corpus,  inlang, outlang ):
#     outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
#     #processedTerms=iate(processedTerms, date, lang_in)
#     #processedTerms.sort()


# def iate_enriching_terms(theTerm,corpus ):
#     outFile=iateCode.enrich_term_withTERM(theTerm, 'ficheroquenoentiendo', corpus, True, None)
#     #processedTerms=iate(processedTerms, date, lang_in)
#     #processedTerms.sort()
    
        

#corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'

corpus='a worker has a workplace in a company and gets a salary'

myterm= Term()
myterm.term='worker'

#terms=['trabajador','puesto de trabajo','horas']
myterm.langIn='en'

lang="de"

myterm.langOut=lang.split(', ')



#iate_enriching_terms_withTERM(myterm,corpus)

#result = iateCode.request_term_to_iat(myterm, langIn, langOut)
# iateCode.request_term_to_iate_withTERM(myterm)


#vectors=['trabajo empresa puesto trabajador', 'otro vector cualquiera']


# test = wsidCode.get_vector_weights(myterm, corpus)

# maxw= iateCode.get_best_vector(myterm, corpus)



# iateCode.retrieve_data_from_best_vector(myterm)

# print(myterm.term)
# print(myterm.synonyms_iate)
# print(myterm.translations_iate)
# print(myterm.definitions_iate)


# eurovocCode.get_uri(myterm)
# eurovocCode.get_relations(myterm)
# eurovocCode.get_synonyms(myterm)
# eurovocCode.get_translations(myterm)





# print(myterm.translations_eurovoc)
# print(myterm.definitions_eurovoc)
# print(myterm.eurovoc_relations)

# unescoCode.get_uri(myterm)
# unescoCode.get_synonyms(myterm)
# unescoCode.get_translations(myterm)
# unescoCode.get_relations(myterm)

# print(myterm.unesco_relations)

# print(myterm.unesco_id)
# print(myterm.translations_unesco)


#wikidataCode.create_wikidata_vectors(myterm)
# wikidataCode.get_vector_weights(myterm, corpus)
# wikidataCode.get_best_vector_id(myterm, corpus)
# wikidataCode.get_langIn_data_from_best_vector(myterm, corpus)

# print(myterm.synonyms_wikidata)
# print(myterm.definitions_wikidata)





# wikidataCode.get_langOut_data_from_best_vector(myterm, corpus)
# wikidataCode.get_relations_from_best_vector(myterm, corpus)

# print(myterm.wikidata_relations)


# thesozCode.get_uri(myterm)
# thesozCode.get_definition(myterm)
# thesozCode.get_relations(myterm)
# thesozCode.get_synonyms(myterm)
# thesozCode.get_translations(myterm)


stwCode.get_uri(myterm)
stwCode.get_definition(myterm)
stwCode.get_relations(myterm)
print(myterm.stw_relations)


'''

# corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'
# myterm=Term()
# myterm.term='trabajador'



# #terms=['trabajador','puesto de trabajo','horas']
# myterm.langIn='es'
# print(myterm.langIn)

# myterm.langOut=['en']


# iate_enriching_terms(myterm.term,corpus, myterm.langIn, myterm.langOut )

# result = iateCode.request_term_to_iate(myterm.term, myterm.langIn, myterm.langOut)
# vectors=result[1]
# items=result[0]
# response2=result[2]
# '''
# print(doc)

# f=open('doc.json', 'w+')

# f.write(doc)
# f.close()



# #vectors=['trabajo empresa puesto trabajador', 'otro vector cualquiera']

# '''

# test = wsidCode.get_vector_weights(myterm.term, corpus, vectors)

# maxw= iateCode.get_best_vector(vectors, myterm.term, corpus)

# index_max = maxw[1]

# result_item= iateCode.retrieve_data_from_best_vector(response2, index_max, myterm.langOut, myterm.langIn)

# print(result_item)

