
import iateCode
import wsidCode
import Term


def iate_enriching_terms(terms,corpus,  inlang, outlang ):
    outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
    #processedTerms=iate(processedTerms, date, lang_in)
    #processedTerms.sort()
        
        



corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'



terms=['trabajador','puesto de trabajo','horas']
langIn='es'
langOut=['en']


iate_enriching_terms(terms,corpus, langIn, langOut )

result = iateCode.request_term_to_iate(terms[0], langIn, langOut)
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

test = wsidCode.get_vector_weights(terms[0], corpus, vectors)

maxw= iateCode.get_best_vector(vectors, terms[0], corpus)

index_max = maxw[1]

result_item= iateCode.retrieve_data_from_best_vector(response2, index_max, langOut, langIn)

print(result_item)

