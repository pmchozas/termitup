import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',

def start(corpus):
	c=corpus.split('/')
	name=''.join(c[len(c)-1])
	logging.info('----STARTING TERMIUP WITH CORPUS: '+ name+ '----')

def information(txt, txt2):
	if(txt2=='' ):
		logging.info(txt)
	elif(txt2!='' ):	
		logging.info(txt)
		logging.info(txt2)
	


def error(msg, code):
	logging.error(msg+' '+str(code))

def contFinal():
	file=open('myapp.log', 'r')
	read=file.readlines()
	#print(read)
	cont_euro=0
	cont_lexi=0
	cont_unesco=0
	cont_wiki=0
	cont_iate=0

	alt_euro=0
	alt_euro_es=0
	alt_euro_de=0
	alt_euro_en=0
	alt_euro_nl=0
	
	pref_euro=0
	pref_euro_es=0
	pref_euro_en=0
	pref_euro_de=0
	pref_euro_nl=0

	defi_euro=0
	defi_euro_es=0
	defi_euro_en=0
	defi_euro_de=0
	defi_euro_nl=0


	br_euro=0
	na_euro=0
	re_euro=0

	alt_iate=0
	alt_iate_es=0
	alt_iate_en=0
	alt_iate_de=0
	alt_iate_nl=0

	pref_iate=0
	pref_iate_es=0
	pref_iate_en=0
	pref_iate_de=0
	pref_iate_nl=0

	defi_iate=0
	defi_iate_es=0
	defi_iate_en=0
	defi_iate_de=0
	defi_iate_nl=0

	alt_unesco=0
	alt_unesco_es=0
	alt_unesco_en=0
	alt_unesco_de=0
	alt_unesco_nl=0

	pref_unesco=0
	pref_unesco_es=0
	pref_unesco_en=0
	pref_unesco_de=0
	pref_unesco_nl=0

	defi_unesco=0
	defi_unesco_es=0
	defi_unesco_en=0
	defi_unesco_de=0
	defi_unesco_nl=0

	br_unesco=0
	na_unesco=0
	re_unesco=0

	alt_wiki=0
	alt_wiki_es=0
	alt_wiki_en=0
	alt_wiki_de=0
	alt_wiki_nl=0

	pref_wiki=0
	pref_wiki_es=0
	pref_wiki_en=0
	pref_wiki_de=0
	pref_wiki_nl=0

	defi_wiki=0
	defi_wiki_es=0
	defi_wiki_en=0
	defi_wiki_de=0
	defi_wiki_nl=0

	cont_alt_rel=0
	cont_termlist_rel=0


	for i in read:
		if('Eurovoc' in i):
			cont_euro=cont_euro+1
			if('altLabel' in i):
				alt_euro=alt_euro+1
				lang=i[-3:-1]
				if(lang=='es'):
					alt_euro_es=alt_euro_es+1
				if(lang=='en'):
					alt_euro_en=alt_euro_en+1
				if(lang=='de'):
					alt_euro_de=alt_euro_de+1
				if(lang=='nl'):
					alt_euro_nl=alt_euro_nl+1

			if('prefLabel' in i):
				pref_euro=pref_euro+1
				lang=i[-3:-1]
				if(lang=='es'):
					pref_euro_es=pref_euro_es+1
				if(lang=='en'):
					pref_euro_en=pref_euro_en+1
				if(lang=='de'):
					pref_euro_de=pref_euro_de+1
				if(lang=='nl'):
					pref_euro_nl=pref_euro_nl+1

			if('definition' in i):
				defi_euro=defi_euro+1
				lang=i[-3:-1]
				if(lang=='es'):
					defi_euro_es=defi_euro_es+1
				if(lang=='en'):
					defi_euro_en=defi_euro_en+1
				if(lang=='de'):
					defi_euro_de=defi_euro_de+1
				if(lang=='nl'):
					defi_euro_nl=defi_euro_nl+1
			
			if('broader' in i):
				br_euro=br_euro+1
			if('narrower' in i):
				na_euro=na_euro+1
			if('related' in i):
				re_euro=re_euro+1
		if('Iate' in i):
			cont_iate=cont_iate+1
			if('altLabel' in i):
				alt_iate=alt_iate+1
				lang=i[-3:-1]
				if(lang=='es'):
					alt_iate_es=alt_iate_es+1
				if(lang=='en'):
					alt_iate_en=alt_iate_en+1
				if(lang=='de'):
					alt_iate_de=alt_iate_de+1
				if(lang=='nl'):
					alt_iate_nl=alt_iate_nl+1

			if('prefLabel' in i):
				pref_iate=pref_iate+1
				lang=i[-3:-1]
				if(lang=='es'):
					pref_iate_es=pref_iate_es+1
				if(lang=='en'):
					pref_iate_en=pref_iate_en+1
				if(lang=='de'):
					pref_iate_de=pref_iate_de+1
				if(lang=='nl'):
					pref_iate_nl=pref_iate_nl+1

			if('definition' in i):
				defi_iate=defi_iate+1
				lang=i[-3:-1]
				if(lang=='es'):
					defi_iate_es=defi_iate_es+1
				if(lang=='en'):
					defi_iate_en=defi_iate_en+1
				if(lang=='de'):
					defi_iate_de=defi_iate_de+1
				if(lang=='nl'):
					defi_iate_nl=defi_iate_nl+1
		if('Unesco' in i):
			cont_unesco=cont_unesco+1
			if('altLabel' in i):
				alt_unesco=alt_unesco+1
				lang=i[-3:-1]
				if(lang=='es'):
					alt_unesco_es=alt_unesco_es+1
				if(lang=='en'):
					alt_unesco_en=alt_unesco_en+1
				if(lang=='de'):
					alt_unesco_de=alt_unesco_de+1
				if(lang=='nl'):
					alt_unesco_nl=alt_unesco_nl+1

			if('prefLabel' in i):
				pref_unesco=pref_unesco+1
				lang=i[-3:-1]
				if(lang=='es'):
					pref_unesco_es=pref_unesco_es+1
				if(lang=='en'):
					pref_unesco_en=pref_unesco_en+1
				if(lang=='de'):
					pref_unesco_de=pref_unesco_de+1
				if(lang=='nl'):
					pref_unesco_nl=pref_unesco_nl+1

			if('definition' in i):
				defi_unesco=defi_unesco+1
				lang=i[-3:-1]
				if(lang=='es'):
					defi_unesco_es=defi_unesco_es+1
				if(lang=='en'):
					defi_unesco_en=defi_unesco_en+1
				if(lang=='de'):
					defi_unesco_de=defi_unesco_de+1
				if(lang=='nl'):
					defi_unesco_nl=defi_unesco_nl+1
			
			if('broader' in i):
				br_unesco=br_unesco+1
			if('narrower' in i):
				na_unesco=na_unesco+1
			if('related' in i):
				re_unesco=re_unesco+1
		if('Wikidata' in i):
			cont_wiki=cont_wiki+1
			if('altLabel' in i):
				alt_wiki=alt_wiki+1
				lang=i[-3:-1]
				if(lang=='es'):
					alt_wiki_es=alt_wiki_es+1
				if(lang=='en'):
					alt_wiki_en=alt_wiki_en+1
				if(lang=='de'):
					alt_wiki_de=alt_wiki_de+1
				if(lang=='nl'):
					alt_wiki_nl=alt_wiki_nl+1

			if('prefLabel' in i):
				pref_wiki=pref_wiki+1
				lang=i[-3:-1]
				if(lang=='es'):
					pref_wiki_es=pref_wiki_es+1
				if(lang=='en'):
					pref_wiki_en=pref_wiki_en+1
				if(lang=='de'):
					pref_wiki_de=pref_wiki_de+1
				if(lang=='nl'):
					pref_wiki_nl=pref_wiki_nl+1

			if('definition' in i):
				defi_wiki=defi_wiki+1
				lang=i[-3:-1]
				if(lang=='es'):
					defi_wiki_es=defi_wiki_es+1
				if(lang=='en'):
					defi_wiki_en=defi_wiki_en+1
				if(lang=='de'):
					defi_wiki_de=defi_wiki_de+1
				if(lang=='nl'):
					defi_wiki_nl=defi_wiki_nl+1
		if('altLabel is relation' in i):
			cont_alt_rel=cont_alt_rel+1
		if('term in list is relation' in i):
			cont_termlist_rel=cont_termlist_rel+1
	file.close()
	

	logging.info('----------------------------------------------------------')
	logging.info('Total terms Eurovoc: ('+str(cont_euro)+') Total prefLabel: ('+str(pref_euro)+') Total altLabel: ('+str(alt_euro)+') Total definition: ('+str(defi_euro)+')')
	logging.info('prefLabel es: ('+str(pref_euro_es)+') en: ('+str(pref_euro_en)+') de: ('+str(pref_euro_de)+') nl: ('+str(pref_euro_nl)+')')
	logging.info('altLabel es: ('+str(alt_euro_es)+') en: ('+str(alt_euro_en)+') de: ('+str(alt_euro_de)+') nl: ('+str(alt_euro_nl)+')')
	logging.info('definition es: ('+str(defi_euro_es)+') en: ('+str(defi_euro_en)+') de: ('+str(defi_euro_de)+') nl: ('+str(defi_euro_nl)+')')
	
	logging.info('Total terms Iate: ('+str(cont_iate)+') Total prefLabel: ('+str(pref_iate)+') Total altLabel: ('+str(alt_iate)+') Total definition: ('+str(defi_iate)+')')
	logging.info('prefLabel es: ('+str(pref_iate_es)+') en: ('+str(pref_iate_en)+') de: ('+str(pref_iate_de)+') nl: ('+str(pref_iate_nl)+')')
	logging.info('altLabel es: ('+str(alt_iate_es)+') en: ('+str(alt_iate_en)+') de: ('+str(alt_iate_de)+') nl: ('+str(alt_iate_nl)+')')
	logging.info('definition es: ('+str(defi_iate_es)+') en: ('+str(defi_iate_en)+') de: ('+str(defi_iate_de)+') nl: ('+str(defi_iate_nl)+')')
	
	logging.info('Total terms Unesco: ('+str(cont_unesco)+') Total prefLabel: ('+str(pref_unesco)+') Total altLabel: ('+str(alt_unesco)+') Total definition: ('+str(defi_unesco)+')')
	logging.info('prefLabel es: ('+str(pref_unesco_es)+') en: ('+str(pref_unesco_en)+') de: ('+str(pref_unesco_de)+') nl: ('+str(pref_unesco_nl)+')')
	logging.info('altLabel es: ('+str(alt_unesco_es)+') en: ('+str(alt_unesco_en)+') de: ('+str(alt_unesco_de)+') nl: ('+str(alt_unesco_nl)+')')
	logging.info('definition es: ('+str(defi_unesco_es)+') en: ('+str(defi_unesco_en)+') de: ('+str(defi_unesco_de)+') nl: ('+str(defi_unesco_nl)+')')
	
	logging.info('Total terms Wikidata: ('+str(cont_wiki)+') Total prefLabel: ('+str(pref_wiki)+') Total altLabel: ('+str(alt_wiki)+') Total definition: ('+str(defi_wiki)+')')
	logging.info('prefLabel es: ('+str(pref_wiki_es)+') en: ('+str(pref_wiki_en)+') de: ('+str(pref_wiki_de)+') nl: ('+str(pref_wiki_nl)+')')
	logging.info('altLabel es: ('+str(alt_wiki_es)+') en: ('+str(alt_wiki_en)+') de: ('+str(alt_wiki_de)+') nl: ('+str(alt_wiki_nl)+')')
	logging.info('definition es: ('+str(defi_wiki_es)+') en: ('+str(defi_wiki_en)+') de: ('+str(defi_wiki_de)+') nl: ('+str(defi_wiki_nl)+')')
	

	logging.info('Total terms Relations-Eurovoc: ('+str(br_euro+na_euro+re_euro)+') Total Broader: ('+str(br_euro)+') Total Narrower: ('+str(na_euro)+') Total Related: ('+str(re_euro)+')')
	logging.info('Total terms Relations-Unesco: ('+str(br_unesco+na_unesco+re_unesco)+') Total Broader: ('+str(br_unesco)+') Total Narrower: ('+str(na_unesco)+') Total Related: ('+str(re_unesco)+')')
	
	logging.info('Total relations altLabel: '+ str(cont_alt_rel))
	logging.info('Total relations termlist: '+ str(cont_termlist_rel))

	print('----------------------------------------------------------')
	print('Total terms Eurovoc: ('+str(cont_euro)+') Total prefLabel: ('+str(pref_euro)+') Total altLabel: ('+str(alt_euro)+') Total definition: ('+str(defi_euro)+')')
	print('prefLabel es: ('+str(pref_euro_es)+') en: ('+str(pref_euro_en)+') de: ('+str(pref_euro_de)+') nl: ('+str(pref_euro_nl)+')')
	print('altLabel es: ('+str(alt_euro_es)+') en: ('+str(alt_euro_en)+') de: ('+str(alt_euro_de)+') nl: ('+str(alt_euro_nl)+')')
	print('definition es: ('+str(defi_euro_es)+') en: ('+str(defi_euro_en)+') de: ('+str(defi_euro_de)+') nl: ('+str(defi_euro_nl)+')')
	
	print('Total terms Iate: ('+str(cont_iate)+') Total prefLabel: ('+str(pref_iate)+') Total altLabel: ('+str(alt_iate)+') Total definition: ('+str(defi_iate)+')')
	print('prefLabel es: ('+str(pref_iate_es)+') en: ('+str(pref_iate_en)+') de: ('+str(pref_iate_de)+') nl: ('+str(pref_iate_nl)+')')
	print('altLabel es: ('+str(alt_iate_es)+') en: ('+str(alt_iate_en)+') de: ('+str(alt_iate_de)+') nl: ('+str(alt_iate_nl)+')')
	print('definition es: ('+str(defi_iate_es)+') en: ('+str(defi_iate_en)+') de: ('+str(defi_iate_de)+') nl: ('+str(defi_iate_nl)+')')
	
	print('Total terms Unesco: ('+str(cont_unesco)+') Total prefLabel: ('+str(pref_unesco)+') Total altLabel: ('+str(alt_unesco)+') Total definition: ('+str(defi_unesco)+')')
	print('prefLabel es: ('+str(pref_unesco_es)+') en: ('+str(pref_unesco_en)+') de: ('+str(pref_unesco_de)+') nl: ('+str(pref_unesco_nl)+')')
	print('altLabel es: ('+str(alt_unesco_es)+') en: ('+str(alt_unesco_en)+') de: ('+str(alt_unesco_de)+') nl: ('+str(alt_unesco_nl)+')')
	print('definition es: ('+str(defi_unesco_es)+') en: ('+str(defi_unesco_en)+') de: ('+str(defi_unesco_de)+') nl: ('+str(defi_unesco_nl)+')')
	
	print('Total terms Wikidata: ('+str(cont_wiki)+') Total prefLabel: ('+str(pref_wiki)+') Total altLabel: ('+str(alt_wiki)+') Total definition: ('+str(defi_wiki)+')')
	print('prefLabel es: ('+str(pref_wiki_es)+') en: ('+str(pref_wiki_en)+') de: ('+str(pref_wiki_de)+') nl: ('+str(pref_wiki_nl)+')')
	print('altLabel es: ('+str(alt_wiki_es)+') en: ('+str(alt_wiki_en)+') de: ('+str(alt_wiki_de)+') nl: ('+str(alt_wiki_nl)+')')
	print('definition es: ('+str(defi_wiki_es)+') en: ('+str(defi_wiki_en)+') de: ('+str(defi_wiki_de)+') nl: ('+str(defi_wiki_nl)+')')
	

	print('Total terms Relations-Eurovoc: ('+str(br_euro+na_euro+re_euro)+') Total Broader: ('+str(br_euro)+') Total Narrower: ('+str(na_euro)+') Total Related: ('+str(re_euro)+')')
	print('Total terms Relations-Unesco: ('+str(br_unesco+na_unesco+re_unesco)+') Total Broader: ('+str(br_unesco)+') Total Narrower: ('+str(na_unesco)+') Total Related: ('+str(re_unesco)+')')
	
	print('Total relations altLabel: '+ str(cont_alt_rel))
	print('Total relations termlist: '+ str(cont_termlist_rel))


	




