import requests

#import spacy
from nltk.corpus import stopwords


from modules_api import iateCode
from modules_api import wsidCode
from modules_api import eurovocCode
from modules_api import unescoCode
from modules_api import wikidataCode
from modules_api.Term import Term
from modules_api import contextCode
from modules_api import thesozCode
from modules_api import stwCode
# from modules_api import relvalCode
from modules_api import iloCode
# def iate_enriching_terms(terms,corpus,  inlang, outlang ):
#     outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
#     #processedTerms=iate(processedTerms, date, lang_in)
#     #processedTerms.sort()


# def iate_enriching_terms(theTerm,corpus ):
#     outFile=iateCode.enrich_term_withTERM(theTerm, 'ficheroquenoentiendo', corpus, True, None)
#     #processedTerms=iate(processedTerms, date, lang_in)
#     #processedTerms.sort()
    


#corpus=' el empresario deberá informar a los trabajadores de la empresa sobre la existencia de puestos de trabajo vacantes'        
# corpus='1.  A estos efectos, la jornada de los trabajadores a tiempo parcial se registrará día a día y se totalizará mensualmente, entregando copia al trabajador, junto con el recibo de salarios, del resumen de todas las horas realizadas en cada mes, tanto las ordinarias como las complementarias a que se refiere el apartado 5.  El empresario deberá conservar los resúmenes mensuales de los registros de jornada durante un periodo mínimo de cuatro años.  En caso de incumplimiento de las referidas obligaciones de registro, el contrato se presumirá celebrado a jornada completa, salvo prueba en contrario que acredite el carácter parcial de los servicios.  d) Las personas trabajadoras a tiempo parcial tendrán los mismos derechos que los trabajadores a tiempo completo. Cuando corresponda en atención a su naturaleza, tales derechos serán reconocidos en las disposiciones legales y reglamentarias y en los convenios colectivos de manera proporcional, en función del tiempo trabajado, debiendo garantizarse en todo caso la ausencia de discriminación, tanto directa como indirecta, entre mujeres y hombres.  e) La conversión de un trabajo a tiempo completo en un trabajo parcial y viceversa tendrá siempre carácter voluntario para el trabajador y no se podrá imponer de forma unilateral o como consecuencia de una modificación sustancial de condiciones de trabajo al amparo de lo dispuesto en el artículo 41.1.a). El trabajador no podrá ser despedido ni sufrir ningún otro tipo de sanción o efecto perjudicial por el hecho de rechazar esta conversión, sin perjuicio de las medidas que, de conformidad con lo dispuesto en los artículos 51 y 52.c), puedan adoptarse por causas económicas, técnicas, organizativas o de producción.  A fin de posibilitar la movilidad voluntaria en el trabajo a tiempo parcial, el empresario deberá informar a los trabajadores de la empresa sobre la existencia de puestos de trabajo vacantes, de manera que aquellos puedan formular solicitudes de conversión voluntaria de un trabajo a tiempo completo en un trabajo a tiempo parcial y viceversa, o para el incremento del tiempo de trabajo de los trabajadores a tiempo parcial, todo ello de conformidad con los procedimientos que se establezcan en convenio colectivo.  Con carácter general, las solicitudes a que se refiere el párrafo anterior deberán ser tomadas en consideración, en la medida de lo posible, por el empresario. La denegación de la solicitud deberá ser notificada por el empresario al trabajador por escrito y de manera motivada.  f) Los convenios colectivos establecerán medidas para facilitar el acceso efectivo de los trabajadores a tiempo parcial a la formación profesional continua, a fin de favorecer su progresión y movilidad profesionales.  5. Se consideran horas complementarias las realizadas como adición a las horas ordinarias pactadas en el contrato a tiempo parcial, conforme a las siguientes reglas:  a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo, pero constituirá, en todo caso, un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.  b) Solo se podrá formalizar un pacto de horas complementarias en el caso de contratos a tiempo parcial con una jornada de trabajo no inferior a diez horas semanales en cómputo anual. '
#corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca, tiene un jefe y un salario.'

# corpus='a service worker takes care of social matters and work with people. Earns a salary.'

myterm= Term()
myterm.term= 'worker'
# myterm.context='el empresario de la empresa le bajó el salario al trabajador, firmó un acuerdo de trabajo, el contratista del proyecto mandó al empleador a casa'
myterm.context="the worker signed an employment agreement and now works in a company with a salary and team work is important and labour law is more important"
#myterm.synonyms_iate=['trabajador', 'asistente social', 'manzana']
#terms=['trabajador','puesto de trabajo','horas']
myterm.langIn='en'

lang="es, de"

myterm.langOut=lang.split(', ')
myterm.schema='test'
test= wikidataCode.enrich_term_wikidata(myterm)
# test2= stwCode.enrich_term_stw(myterm)
test3= eurovocCode.enrich_term_eurovoc(myterm)


# myterm.ids['ids']={}
# myterm.ids['ids']['iate']=myterm.iate_id
# myterm.ids['ids']['wikidata']=myterm.wikidata_id
# myterm.ids['ids']['eurovoc']=myterm.eurovoc_id
# myterm.ids['ids']['ilo']=myterm.ilo_id
# myterm.ids['ids']['stw']=myterm.stw_id
# myterm.ids['ids']['thesoz']=myterm.thesoz_id
# myterm.ids['ids']['unesco']=myterm.unesco_id
# myterm.relations['relations']={}
# myterm.relations['relations']['wikidata']=myterm.wikidata_relations
# myterm.relations['relations']['eurovoc']=myterm.eurovoc_relations
# myterm.relations['relations']['ilo']=myterm.ilo_relations
# myterm.relations['relations']['stw']=myterm.stw_relations
# myterm.relations['relations']['thesoz']=myterm.thesoz_relations
# myterm.relations['relations']['unesco']=myterm.unesco_relations
# data_mappings={}
# data={
#             'Source Term ID': myterm.term_id,
#             'Source Term' : myterm.term,
#             'Source Term Context': myterm.context,
#             'Source Language': myterm.langIn
        
#         }
# data_mappings.update(data)
# data_mappings.update(myterm.ids)
# data_mappings['synonyms']=myterm.synonyms
# data_mappings['translations']=myterm.translations
# data_mappings['definitions']=myterm.definitions
# data_mappings.update(myterm.relations)
# data_mappings['term_reference']=myterm.term_ref_iate
# data_mappings['language_note']=myterm.note_iate
# data_mappings['related_iate']=myterm.related_ids_iate
    # ids={}
    # translations={}
    # synonyms={}
    # definitions={}
    # relations={}
    # term_ref={}
    # lang_note={}
    # related_term={}
    
print(data_mappings)

'''

iloCode.get_uri(myterm)

iloCode.get_synonyms(myterm)

iloCode.get_translations(myterm)

iloCode.get_relations(myterm)
print(myterm.ilo_id)
print(myterm.synonyms_ilo)
print(myterm.translations_ilo)
print(myterm.ilo_relations)



term_in = myterm.term
lang_in = myterm.langIn
synonyms = "trabajador, asistente social, manzana"


relvaltest=relvalCode.main(term_in, lang_in, synonyms)

print(relvaltest)
'''


# test=relvalCode.get_conceptNet_synonyms(myterm)

# print(test)


# iate_enriching_terms_withTERM(myterm,corpus)

#result = iateCode.request_term_to_iate(myterm, langIn, langOut)
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


# stwCode.get_uri(myterm)
# stwCode.get_definition(myterm)
# stwCode.get_relations(myterm)
# stwCode.get_synonyms(myterm)
# stwCode.get_translations(myterm)


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

