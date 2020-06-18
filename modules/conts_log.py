
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
def main():
	file=open('myapp.log', 'r')
	read=file.readlines()
	#print(read)
	cont_euro=0
	cont_lexi=0
	cont_unesco=0
	cont_wiki=0
	cont_iate=0

	alt_euro=0
	pref_euro=0
	defi_euro=0
	br_euro=0
	na_euro=0
	re_euro=0

	alt_iate=0
	pref_iate=0
	defi_iate=0

	alt_unesco=0
	pref_unesco=0
	defi_unesco=0
	br_unesco=0
	na_unesco=0
	re_unesco=0

	alt_lexi=0
	pref_lexi=0
	defi_lexi=0

	alt_wiki=0
	pref_wiki=0
	defi_wiki=0



	for i in read:
		if('Eurovoc' in i):
			cont_euro=cont_euro+1
			if('altLabel' in i):
				alt_euro=alt_euro+1
			if('prefLabel' in i):
				pref_euro=pref_euro+1
			if('definition' in i):
				defi_euro=defi_euro+1
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
			if('prefLabel' in i):
				pref_iate=pref_iate+1
			if('definition' in i):
				defi_iate=defi_iate+1
		if('Unesco' in i):
			cont_unesco=cont_unesco+1
			if('altLabel' in i):
				alt_unesco=alt_unesco+1
			if('prefLabel' in i):
				pref_unesco=pref_unesco+1
			if('definition' in i):
				defi_unesco=defi_unesco+1
			if('broader' in i):
				br_unesco=br_unesco+1
			if('narrower' in i):
				na_unesco=na_unesco+1
			if('related' in i):
				re_unesco=re_unesco+1
		if('Lexicala' in i):
			cont_lexi=cont_lexi+1
			if('altLabel' in i):
				alt_lexi=alt_lexi+1
			if('prefLabel' in i):
				pref_lexi=pref_lexi+1
			if('definition' in i):
				defi_lexi=defi_lexi+1
		if('Wikidata' in i):
			cont_wiki=cont_wiki+1
			if('altLabel' in i):
				alt_wiki=alt_wiki+1
			if('prefLabel' in i):
				pref_wiki=pref_wiki+1
			if('definition' in i):
				defi_wiki=defi_wiki+1

	


	logging.info('Total terms Eurovoc: ('+str(cont_euro)+') Total prefLabel: ('+str(pref_euro)+') Total altLabel: ('+str(alt_euro)+') Total definition: ('+str(defi_euro)+')')
	logging.info('Total terms Iate: ('+str(cont_iate)+') Total prefLabel: ('+str(pref_iate)+') Total altLabel: ('+str(alt_iate)+') Total definition: ('+str(defi_iate)+')')
	logging.info('Total terms Unesco: ('+str(cont_unesco)+') Total prefLabel: ('+str(pref_unesco)+') Total altLabel: ('+str(alt_unesco)+') Total definition: ('+str(defi_unesco)+')')
	logging.info('Total terms Wikidata: ('+str(cont_wiki)+') Total prefLabel: ('+str(pref_wiki)+') Total altLabel: ('+str(alt_wiki)+') Total definition: ('+str(defi_wiki)+')')
	logging.info('Total terms Lexicala: ('+str(cont_lexi)+') Total prefLabel: ('+str(pref_lexi)+') Total altLabel: ('+str(alt_lexi)+') Total definition: ('+str(defi_lexi)+')')
	logging.info('Total terms Relations-Eurovoc: ('+str(br_euro+na_euro+re_euro)+') Total Broader: ('+str(br_euro)+') Total Narrower: ('+str(na_euro)+') Total Related: ('+str(re_euro)+')')
	logging.info('Total terms Relations-Unesco: ('+str(br_unesco+na_unesco+re_unesco)+') Total Broader: ('+str(br_unesco)+') Total Narrower: ('+str(na_unesco)+') Total Related: ('+str(re_unesco)+')')
	





