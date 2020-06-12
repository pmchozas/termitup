from TBXTools import *

def main(corpus):
	extractor=TBXTools()
	extractor.create_project("statistical8.sqlite","esp",overwrite=True)
	extractor.load_sl_corpus(corpus)
	extractor.ngram_calculation(nmin=1,nmax=3,minfreq=3)
	extractor.load_sl_stopwords("stop-esp.txt")
	extractor.load_sl_inner_stopwords("inner-stop-esp.txt")
	extractor.statistical_term_extraction(minfreq=3)
	# aquí junta los términos que son iguales pero están en mayus y en minus
	extractor.case_normalization(verbose=True)
	# esto no sé muy bien lo que hace pero saca menos términos que si no se pone, lo cual es mejor, creo que quita basurilla
	extractor.nest_normalization(verbose=True)
	extractor.regexp_exclusion(verbose=True)
	extractor.load_sl_exclusion_regexps("exclusion-regexps.txt")
	extractor.regexp_exclusion(verbose=True)
	#para extraer unigramas, descomenta esto
	#extractor.select_unigrams("unigrams.txt",position=-1)
	out=extractor.save_term_candidates("estatutoterms_mx.txt")

	return(out)
