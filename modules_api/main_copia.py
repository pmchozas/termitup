
import iateCode





def iate_enriching_terms(terms,corpus,  inlang, outlang ):
    outFile=iateCode.enrich_term(terms[0], inlang, outlang, 'ficheroquenoentiendo', corpus, True, None)
    #processedTerms=iate(processedTerms, date, lang_in)
    #processedTerms.sort()
        
        



corpus= 'el trabajador estará en su puesto de trabajo durante 24 horas hasta que desfallezca'



terms=['trabajador','puesto de trabajo','horas']
langIn='es'
langOut=['en']


iate_enriching_terms(terms,corpus,  langIn, langOut )





