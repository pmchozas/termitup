
import iateCode
import wsidCode
from Term import Term


def iate_enriching_terms(terms,corpus,  inlang, outlang ):
    outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
    #processedTerms=iate(processedTerms, date, lang_in)
    #processedTerms.sort()
        
        

corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'


myterm=Term.term='trabajador'

#terms=['trabajador','puesto de trabajo','horas']
langIn=Term.langIn='es'
langOut=Term.langOut=['en']


iate_enriching_terms(myterm,corpus, langIn, langOut )

result = iateCode.request_term_to_iate(myterm, langIn, langOut)
vectors=result[1]
items=result[0]
response2=result[2]
'''
print(doc)
f=open('doc.json', 'w+')
f.write(doc)
f.close()
#vectors=['trabajo empresa puesto trabajador', 'otro vector cualquiera']
'''

test = wsidCode.get_vector_weights(myterm, corpus, vectors)

maxw= iateCode.get_best_vector(vectors, myterm, corpus)

index_max = maxw[1]

result_item= iateCode.retrieve_data_from_best_vector(response2, index_max, langOut, langIn)

print(result_item)


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

