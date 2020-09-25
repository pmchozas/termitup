
import iateCode
import wsidCode



def iate_enriching_terms(terms,corpus,  inlang, outlang ):
    outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
    #processedTerms=iate(processedTerms, date, lang_in)
    #processedTerms.sort()
        
        



corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'



terms=['trabajador','puesto de trabajo','horas']
langIn='es'
langOut=['en']


#iate_enriching_terms(terms,corpus, langIn, langOut )

result = iateCode.request_term_to_iate(terms[0], langIn, langOut)
vectors=result[1]

#vectors=['trabajo empresa puesto trabajador', 'otro vector cualquiera']


test = wsidCode.invoke_wsid(terms[0], corpus, vectors)
print(test)