import os
import json
import csv
import re
import requests
import spacy
import nltk
from nltk.parse import CoreNLPParser
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
from time import time
nlp = spacy.load('es_core_news_sm')
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

# 0 clean punctuation and stopwords
def clean_terms(termlist):
    #print(termlist)
    start_time=time()
    stop=stopwords.words('spanish')
    file=open('data/stop-esp.txt', 'r', encoding='utf-8')
    mystop=file.readlines()

    filew=open('data/stop-esp_all.txt', 'w', encoding='utf-8')
    
    clean_list = []
    cont=0
    for i in mystop:
        #print(i.strip())
        stop.append(i.strip())
    #print(len(termlist))

    for i in stop:
    	filew.write(i+'\n')
    #print('______________________________')
    deletes=[]
    for i in termlist:
        k=i.strip(',.:')
        #print(k)
        if ((k.lower() in stop) or (k in stop)):
        	#print(k.lower(), k)
        	deletes.append(k)
        elif ((k.lower() not in stop) or (k not in stop)):
            #print(k)
            clean_list.append(k.replace(',', '').replace('-', ''))
       


    
    #print(clean_list)	
    #print(len(clean_list))
    cont=len(termlist)-len(clean_list)
    elapsed_time=time()-start_time

    txt='CLEAN_TERMS, DELETE ('+str(cont)+') NEW LIST SIZE: ('+str(len(clean_list))+') TIME: ('+str(elapsed_time)+')'
    logging.info(txt)
    joind=', '.join(deletes)
    logging.info('TERMS REMOVED: '+joind)
    print('CLEAN_TERMS, DELETE', cont, len(clean_list), elapsed_time )
    
    
    return(clean_list)


# 1 añotador
def annotate_timex(text, date, lang):
    start_time=time()
    url = 'http://annotador.oeg-upm.net/annotate'  
    params = {'inputText':text, 'inputDate':date, 'lan': lang}
    #headers = {'content-type': 'application/json'}
    response=requests.post(url, data=params)
    textanotador=response.text
    list_anotador=textanotador.split('|')
    deletes=[]
    cont=0
    for i in list_anotador:
        if('<' in i ):
            cont=cont+1
            deletes.append(i)
            #print(i)
            ind=list_anotador.index(i)
            list_anotador.pop(ind)
    for i in list_anotador:
        if('<' in i ):
            cont=cont+1
            deletes.append(i)
            #print(i)
            ind=list_anotador.index(i)
            list_anotador.pop(ind)
    
    
    anotador=[]
    for i in list_anotador:
        anotador.append(i.strip().replace(',', ''))
    
    for i in deletes:
        ind=i.index('>')
        ind1=i.index('</')
        term=i[ind+1:ind1]
        ind2=deletes.index(i)
        deletes[ind2]=term


    elapsed_time=time()-start_time
    txt='AÑOTADOR, DELETE ('+str(cont)+') NEW LIST SIZE: ('+str(len(anotador))+') TIME: ('+str(elapsed_time)+')'
    logging.info(txt)
    joind=', '.join(deletes)
    logging.info('TERMS REMOVED: '+joind)
    print('AÑOTADOR DELETE', cont, len(anotador), elapsed_time )
    
    return(anotador)





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



# 2 patrones
def delate_pattern(anotador):
	total=0
	deletes=[]
	start_time=time()
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
			about_doc=nlp(joini)
			
			join_tag=''
			for t in about_doc:
				#print(type(t))
				join_tag+=' '+str(i[0])
				join_tag=join_tag.strip()
				
				if(t.pos_ == 'AUX' ):
					lem=t.lemma_
					lemmas_list.append(lem)
					ind=spl.index(str(t))
					list_pos.append('aux--'+str(t.lemma_))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'NOUN'):
					#print(spl,str(t))
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
					deletes.append(joini)
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
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adj+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> aux+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> noun+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+noun: ',term,'|',joini)
					deletes.append(joini)
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
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + verbo: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + nombre:', term, joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + nombre + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + nombre + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + verb + noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + noun + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + aux + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + adv + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='scon' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + sconj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='scon' and pos3[0:4]=='adv-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + sconj + adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + sconj + adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
	elapsed_time=time()-start_time
	txt='PATRONES, DELETE'+' ('+str(cont)+') NEW LIST SIZE: ('+str(len(anotador))+') TIME: ('+str(elapsed_time)+')'
	logging.info(txt)

	joind=', '.join(deletes)
	logging.info('TERMS REMOVED: '+joind)
	print('PATRONES DELETE', cont, len(anotador), elapsed_time)

	return(anotador)

# 2 patrones
def delate_pattern_2(anotador):
	total=0
	deletes=[]
	start_time=time()
	lemmas_list=[]
	cont=0
	
	for i in anotador:
		pos_tagger = CoreNLPParser('http://localhost:9003', tagtype='pos')
		tag=pos_tagger.tag(i.split(' '))

		total=total+1
		joini=i
		
		if(joini[-1:]==' '):
			joini=joini[:-1]
		list_pos=[]
		spl=joini.split(' ')
		if(joini!=''):
			join_tag=''
			for t in tag:
				if(t[1] == 'AUX' ):
					#print(joini, t)
					doc=nlp(t[0])
					lemlist=[tok.lemma_ for tok in doc]
					lem=''.join(lemlist)
					lemmas_list.append(lem)
					if(lem==i):
						lem=t[0]
					list_pos.append('aux--'+str(lem))
					if(len(spl)==1):
						ind=anotador.index(str(i))
						anotador[ind]=str(lem)
				if(t[1] ==  'NOUN'):
					#print(joini, t)
					list_pos.append('noun-'+str(t[0]))
				if(t[1] ==  'VERB'):
					#print(joini, t)
					doc=nlp(t[0])
					lemlist=[tok.lemma_ for tok in doc]
					lem=''.join(lemlist)
					lemmas_list.append(lem)
					if(lem==i):
						lem=t[0]
					list_pos.append('verb-'+str(lem))
					if(len(spl)==1):
						ind=anotador.index(str(i))
						anotador[ind]=str(lem)
				if(t[1] ==  'ADV'):
					#print(joini, t)
					list_pos.append('adv--'+str(t[0]))
				if(t[1] ==  'ADJ'):
					#print(joini, t)
					list_pos.append('adj--'+str(t[0]))
				if(t[1] ==  'SCONJ'):
					#print(joini, t)
					list_pos.append('sconj'+str(t[0]))
			#print('------------', list_pos)
			spl_i=joini.split(' ')
			
			if(len(list_pos)==1):
				pos1=list_pos[0]
				if(pos1[0:4]=='adv-' ):
					term=pos1[5:]
					#print('--> adv: ',term,'|',joini)
					deletes.append(joini)
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
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> nombre+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adj+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> aux+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> noun+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adv-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> adv+noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					#print('--> verb+noun: ',term,'|',joini)
					deletes.append(joini)
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
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + verbo: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + verb + nombre:', term, joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + aux + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + nombre + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + verb: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + nombre + nombre: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> nombre + nombre + aux: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> aux + verb + noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + verb + noun: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> verb + noun + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + aux + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + adv + adj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='scon' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> noun + adv + sconj: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='adj-' and pos2[0:4]=='scon' and pos3[0:4]=='adv-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + sconj + adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					#print('--> adj + sconj + adv: ',term,'|',joini)
					deletes.append(joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
					cont=cont+1
	elapsed_time=time()-start_time
	txt='PATRONES, DELETE'+' ('+str(cont)+') NEW LIST SIZE: ('+str(len(anotador))+') TIME: ('+str(elapsed_time)+')'
	logging.info(txt)

	joind=', '.join(deletes)
	logging.info('TERMS REMOVED: '+joind)
	print('PATRONES DELETE', cont, len(anotador), elapsed_time)

	return(anotador)


# 3 plurales
def quit_plural(valuelist):
	start_time=time()
	file=open('data/numberlist_es', 'r', encoding='utf-8')
	read=file.readlines()
	plural=[]
	cont=0
	for i in valuelist:
		ind=valuelist.index(i)
		term=i.replace(',', '').replace('-', ' ')
		valuelist[ind]=term
		plu=''
		if('es' in term[-2:] or 's'  in term[-1:]):
			slp=term.split(' ')
			#print(term)

			for n in read:
				if(n[:-1] in slp):
					plu=i
					#print(i, '-', n[:-1], '-', plu)

			if not len(plu):
				for j in slp:
					if( ('es' in j[-2:] ) and 't' not in j[-3:-2] and 'l' not in j[-3:-2] or  ('les' in j[-3:] )   ):
						#print(j[-4:-2])
						plu+=' '+j[:-2]
						
						if('on' in plu[-2:]):
							plu=' '+plu[:-2]+'ón'
						if('v' in plu[-1:]):
							plu=' '+plu+'e'
						if('bl' in plu[-2:]):
							plu=' '+plu+'e'
						if('br' in plu[-2:]):
							plu=' '+plu+'e'

							#print(plu)
					elif(('s' in j[-1:]) ):
						plu+=' '+j[:-1]
						pos=slp.index(j)
						
						if(pos>0):
							bef=slp[0]
							#print(bef)
							if('n' in bef[-1:] and 'ón' not in bef[-2:]):
								
								splb=plu.split(' ')
								
								firts=splb[1]
								
								if('n' not in firts[-1:]):
									pass
								else:
									plu0=firts[:-1]
									join1=' '.join(splb[2:])
									
									plu=plu0+' '+join1
								
							

					else:
						plu+=' '+j



			#print(term, '|',plu.strip())
			ind=valuelist.index(term)
			valuelist[ind]=plu.strip()			
			cont=cont+1
	quit_plu=[]
	nuevalista=set(valuelist)
	for i in nuevalista:
		quit_plu.append(i)	

	deletes = []
	new=[]
	for i in valuelist:
	    if i not in new:
	        new.append(i)
	    else:
	    	deletes.append(i)

	elapsed_time=time()-start_time
	txt='PLURAL, DELETE'+' ('+str(len(valuelist)-len(quit_plu))+') NEW LIST SIZE: ('+str(len(quit_plu))+') TIME: ('+str(elapsed_time)+')'
	logging.info(txt)
	joind=', '.join(deletes)
	logging.info('TERMS REMOVED: '+joind)
	print('PLURALES DELETE', len(valuelist)-len(quit_plu), len(quit_plu), elapsed_time)
	return(quit_plu)

# 4 numeros
def delete_numbers(list_):
	print(list_)
	start_time=time()
	file=open('data/numberlist_es', 'r', encoding='utf-8')
	read=file.readlines()
	cont=0
	deletes=[]
	for i in read:
		if(i[-1:]=='\n'):
			i=i[:-1]
			for j in list_:
				#print(i,'|', j)
				if(' '+i+' ' in ' '+j+' ' ):
					print(i, '|', j)
					deletes.append(j)
					ind=list_.index(j)
					cont=cont+1
					list_.pop(ind)
	list_.sort()
	elapsed_time=time()-start_time
	txt='NUMBERS, DELETE'+' ('+str(cont)+') NEW LIST SIZE: ('+str(len(list_))+') TIME: ('+str(elapsed_time)+')'
	logging.info(txt)
	joind=', '.join(deletes)
	logging.info('TERMS REMOVED: '+joind)
	print('NUMEROS DELETE', cont, len(list_), elapsed_time)
	return(list_)


# 5 leer archivo 
def readFile(read):
	start_time=time()
	text=''
	for i in read:
		if(i[-1:]=='\n'):
			spl=i[:-1].split('\t')
		else:
			spl=i.split('\t')
		term=spl[1].replace('-', '').replace(',', '').replace(';', '')
		spl2=term.split(' ')
		text+='| '+spl[1]
	elapsed_time=time()-start_time
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
	start_time=time()
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
	last.sort()
	elapsed_time=time()-start_time
	#txt='ACENTOS'+' '+str(len(last))+' '+str(elapsed_time)
	#logging.info(txt)
	#print('ACENTOS',len(last), elapsed_time)
	
	return(last)


#-------MAIN-------#
def main(read):
	#file=open('../data/estatutoterms_minfreq4.txt', 'r', encoding='utf-8')
	#read=file.readlines()
	#file.close()
	start_time=time()
	text=readFile(read)
	date='2020-06-03'
	lang='ES'
	#print(text)
	termlist=text.split('| ')
	clean_text=clean_terms(termlist)
	
	join_clean_text='| '.join(clean_text).replace('-', '').replace(',', '').replace(';', '')
	#anotador=annotate_timex2(clean_text)
	anotador=annotate_timex(join_clean_text, date, lang)
	anotador.sort()
	pattern=delate_pattern_2(anotador)
	plural=quit_plural(pattern)
	numbers=delete_numbers(plural)
	tildes=acentos(numbers)
	#tildes.sort()
	stop2=clean_terms(tildes)
	new=open('data/clean_terms_freq4.txt', 'w')#se imprime lo que se queda

	for i in stop2:
	    new.write(i+'\n')
	new.close()
	elapsed_time=time()-start_time
	print('Main', elapsed_time)
	return(stop2)


#file=open('data/estatuto_es.txt', 'r', encoding='utf-8')
#read=file.readlines()
#main(read)

