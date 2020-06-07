import os
import json
import csv
import re
import requests
import spacy
from nltk.corpus import stopwords
nlp = spacy.load('es_core_news_sm')


# 0 clean punctuation and stopwords
def clean_terms(termlist):
    stop=stopwords.words('spanish')
    file=open('data/stop-esp.txt', 'r', encoding='utf-8')
    mystop=file.readlines()
    clean_list = []
    cont=0
    for i in mystop:
        stop.append(i.strip())
    print(len(termlist))
    for i in termlist:
        k=i.strip(',.:')
        if k not in stop:
            clean_list.append(k)
    print(len(clean_list))
    cont=len(termlist)-len(clean_list)
    print('CLEAN_TERMS DELETE', cont, len(clean_list) )
    return(clean_list)


# 1 añotador
def annotate_timex(text, date, lang):
    url = 'http://annotador.oeg-upm.net/annotate'  
    params = {'inputText':text, 'inputDate':date, 'lan': lang}
    #headers = {'content-type': 'application/json'}
    response=requests.post(url, data=params)
    return(response.text)


def infinitive(verb):
	
	if(verb[-2:]=='ar' or verb[-2:]=='er' or verb[-2:]=='ir'):
		#print('')
		verb=verb
	else:
		#print(verb,'-',verb[-2:])
		if(verb[-2:]=='rá' ):
			print('---',verb,'-',verb[:-1])
			verb=verb[:-1]
		if(verb[-2:]=='án'):
			print('---',verb,'-',verb[:-2])
			verb=verb[:-2]
		if(verb[-2:]=='ré'):
			print('---',verb,'-',verb[:-1])
			verb=verb[:-1]
	return (verb)

def annotate_infinitive(verb):
    url = 'https://gramatica.usc.es/~gamallo/php/ProlnatTagger/index.php'  
    params = {'texto':verb, 'lingua':'es'}
    #headers = {'content-type': 'application/json'}
    response=requests.post(url, data=params)
    print(response.text)
    return(response.text)



# 2 patrones
def delate_pattern(anotador):
	#string_anotador='| '.join(anotador)
	#print(len(anotador))
	total=0


	lemmas_list=[]
	cont=0
	for i in anotador:
		total=total+1
		joini=i
		
		if(joini[-1:]==' '):
			joini=joini[:-1]
		list_pos=[]
		spl=joini.split(' ')
		if(joini!=''):
		#if(len(spl)>1):
			about_doc=nlp(joini)
			#print('----',  i)
			join_tag=''
			for t in about_doc:
				#print(t,'|', t.pos_)
				join_tag+=' '+str(t)
				join_tag=join_tag.strip()
				
				#print(spl)
				if(t.pos_ == 'AUX' ):
					lem=t.lemma_
					lemmas_list.append(lem)
					#print('LEMAS AUX', t,'|',t.lemma_)
					ind=spl.index(str(t))
					list_pos.append('aux--'+str(t.lemma_))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'NOUN'):
					#print(str(t))
					ind=spl.index(str(t))
					list_pos.append('noun-'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'VERB'):
					lem=t.lemma_
					lemmas_list.append(lem)
					#print('LEMAS VERB', t,'|',t.lemma_,'|', len(spl)  )
					ind=spl.index(str(t))
					list_pos.append('verb-'+str(t.lemma_))
					#print(t,'-',i,'-',ind)
					if(len(spl)==1):
						ind=anotador.index(str(t))
						#print(anotador[ind])
						anotador[ind]=str(t.lemma_)
						#print(anotador[ind])
				if(t.pos_ ==  'ADV'):
					ind=spl.index(str(t))
					list_pos.append('adv--'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'ADJ'):
					ind=spl.index(str(t))
					list_pos.append('adj--'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'SCONJ'):
					ind=spl.index(str(t))
					list_pos.append('sconj'+str(t))
					#print(t,'-',i,'-',ind)
			spl_i=joini.split(' ')
			#print('------------', list_pos)
			if(len(list_pos)==1):
				pos1=list_pos[0]
				if(pos1[0:4]=='adv-' ):
					term=pos1[5:]
					#print('--> adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1

			if(len(list_pos)==2 and len(spl_i)==2):
				
				#print(list_pos, total, spl_i, len(spl_i))
				pos1=list_pos[0]
				pos2=list_pos[1]
				term=''
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> aux+ver: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+verb: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+verb: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adj+adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> aux+adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+verb: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> noun+adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+noun: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+noun: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1

			if(len(list_pos)==3 and len(spl_i)==3):
				##print(list_pos, total)
				pos1=list_pos[0]
				pos2=list_pos[1]
				pos3=list_pos[2]
				term=''
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verbo + verbo: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + verbo: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + nombre:', term, joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + nombre: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + nombre + nombre: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + verb: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + nombre + nombre: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + aux: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + verb + noun: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + noun: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + noun + adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + aux + adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + adv + adj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='scon' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + sconj: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='scon' and pos3[0:4]=='adv-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + sconj + adv: ',term,'|',joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
	print('PATRONES DELETE', cont, len(anotador))
	#print(len(anotador))
	#delete_numbers(anotador)
	#quit_plural(anotador)
	return(anotador)

# 3 plurales
def quit_plural(valuelist):
	plural=[]
	cont=0
	for i in valuelist:
		term=i
		plu=''
		if('es' in term[-2:] or 's'  in term[-1:]):
			slp=term.split(' ')
			for j in slp:
				if( ('es' in j[-2:] ) and 't' not in j[-3:-2] and 'l' not in j[-3:-2]  ):
					
					plu+=' '+j[:-2]
					
					if('on' in plu[-2:]):
						plu=' '+plu[:-2]+'ón'
						#print(plu)
				elif(('s' in j[-1:]) ):
					plu+=' '+j[:-1]
				else:
					plu+=' '+j
			#print(plu)
			ind=valuelist.index(term)
			valuelist[ind]=plu.strip()
			
			cont=cont+1
					
	
	quit_plu=[]
	nuevalista=set(valuelist)
	for i in nuevalista:
		quit_plu.append(i)	
	
	print('PLURALES DELETE', len(valuelist)-len(quit_plu), len(quit_plu))
	
	return(quit_plu)

# 4 numeros
def delete_numbers(list_):
	file=open('data/numberlist_es', 'r', encoding='utf-8')
	read=file.readlines()
	cont=0
	for i in read:
		if(i[-1:]=='\n'):
			i=i[:-1]
			for j in list_:
				#print(i,'|', j)
				if(' '+i+' ' == ' '+j+' ' ):
					#print(i, '|', j)
					ind=list_.index(j)
					cont=cont+1
					list_.pop(ind)
	print('NUMEROS DELETE', cont, len(list_))
	return(list_)


# 5 leer archivo 
def readFile(read):
	text=''
	for i in read:
		if(i[-1:]=='\n'):
			spl=i[:-1].split('\t')
		else:
			spl=i.split('\t')
		term=spl[1]
		spl2=term.split(' ')
		text+='| '+spl[1]

	return text

#elimina tildes
def quit_tilds(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s

def acentos(last):
	til=[]
	list_acentos=[]
	for i in last:
		acento=re.search("[áéíóúÁÉÍÓÚ]+", i)
		if(acento!=None):
			sin=quit_tilds(i)
			list_acentos.append(i)
			til.append(sin)
		else:
			til.append(i)

	til2 = []
	delete=[]
	for i in til:
		if i not in til2:
			til2.append(i)
		else:
			delete.append(i)


	#print(list_acentos)

	#print(delete)
	indices=[]
	delete2=[]
	for i in last:
		if(i in delete and i not in indices):
			indices.append(i)
			delete2.append(i)
	for i in delete2:
		ind=last.index(i)
		last.pop(ind)

	#print(last)

	return(last)


#-------MAIN-------#
def main(read):
	#file=open('../data/estatutoterms_minfreq4.txt', 'r', encoding='utf-8')
	#read=file.readlines()
	#file.close()
	text=readFile(read)
	date='2020-06-03'
	lang='ES'
	#print(text)
	termlist=text.split('| ')
	clean_text=clean_terms(termlist)
	join_clean_text='| '.join(clean_text).replace('-', '').replace(',', '').replace(';', '')
	textanotador=annotate_timex(join_clean_text, date, lang)
	list_anotador=textanotador.split('|')
	#print('ANOTADOR---')
	cont=0
	for i in list_anotador:
		if('<' in i ):
			#print(i)
			cont=cont+1
			ind=list_anotador.index(i)
			list_anotador.pop(ind)
	for i in list_anotador:
		if('<' in i ):
			#print(i)
			cont=cont+1
			ind=list_anotador.index(i)
			list_anotador.pop(ind)
	
	
	anotador=[]
	for i in list_anotador:
		anotador.append(i.strip().replace(',', ''))
	print('AÑOTADOR DELETE', cont, len(anotador) )
	pattern=delate_pattern(anotador)
	plural=quit_plural(pattern)
	numbers=delete_numbers(plural)
	numbers.sort()
	tildes=acentos(numbers)
	tildes.sort()
	new=open('data/clean_terms_freq4.txt', 'w')#se imprime lo que se queda

	for i in tildes:
	    new.write(i+'\n')
	new.close()
	return(tildes)


file=open('data/estatutoterms_minfreq4.txt', 'r', encoding='utf-8')
read=file.readlines()
main(read)

