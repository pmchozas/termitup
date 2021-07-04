#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 17:25:00 2021

@author: pmchozas
"""

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

sw_spanish="./data/stop-esp.txt"
sw_english="./data/stop-eng.txt"
inner_spanish="./data/inner-stop-esp.txt"
inner_english="./data/inner-stop-eng.txt"
from flair.data import Sentence
from flair.models import SequenceTagger
import stanza
def delete_pattern_en(term_list):
	total=0
	deletes=[]

	lemmas_list=[]
	cont=0
	cont_inf=0
	cont_post=0
	for i in term_list:
		if(len(i)>1):
			#print( i, i.split(' ') )
            
			pos_tagger = SequenceTagger.load("flair/pos-english")
			i=Sentence(i)
            #si se cae el de lynx, probar con este https://corenlp.run/
			print('esto es i')
			print(i)
			#tag=pos_tagger.tag(i.split(' '))
			tag=i.get_spans('pos')
			print(tag)
			total=total+1
			joini=i
			list_pos=[]
			#spl=joini.split(' ')
			if(joini!=''):
				join_tag=''
				for t in tag:
					if(t[1] == 'AUX' ):
						doc=nlp(t[0])
						lemlist=[tok.lemma_ for tok in doc]
						lem=''.join(lemlist)
						lemmas_list.append(lem)
						if(lem==i):
							lem=t[0]
						list_pos.append('aux--'+str(lem))
						if(len(spl)==1):
							ind=term_list.index(str(i))
							term_list[ind]=str(lem)
					if(t[1] ==  'NOUN'):
						list_pos.append('noun-'+str(t[0]))
					if(t[1] ==  'VERB'):
						cont_inf=cont_inf+1
						doc=nlp(t[0])
						for tok in doc:
							l=tok.lemma_
							if(l!=t[0]):
								cont_post=cont_post+1
						lemlist=[tok.lemma_ for tok in doc]
						lem=''.join(lemlist)
						lemmas_list.append(lem)
						if(lem==i):
							lem=t[0]
						list_pos.append('verb-'+str(lem))
						if(len(spl)==1):
							ind=term_list.index(str(i))
							term_list[ind]=str(lem)
					if(t[1] ==  'ADV'):
						list_pos.append('adv--'+str(t[0]))
					if(t[1] ==  'ADJ'):
						list_pos.append('adj--'+str(t[0]))
					if(t[1] ==  'SCONJ'):
						list_pos.append('sconj'+str(t[0]))
				
				spl_i=joini.split(' ')
				
				if(len(list_pos)==1):
					pos1=list_pos[0]
					if(pos1[0:4]=='adv-' ):
						term=pos1[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1

				elif(len(list_pos)==2 and len(spl_i)==2):
					pos1=list_pos[0]
					pos2=list_pos[1]
					term=''
					if(pos1[0:4]=='aux-' and pos2[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adv-' and pos2[0:4]=='adj-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adv-' and pos2[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='aux-' and pos2[0:4]=='adv-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adv-' and pos2[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='adv-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adv-' and pos2[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='adv-'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='aux-' and pos2[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adj-' and pos2[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1

				elif(len(list_pos)==3 and len(spl_i)==3):
					#print(list_pos, spl_i,'-', len(list_pos), len(spl_i))
					pos1=list_pos[0]
					pos2=list_pos[1]
					pos3=list_pos[2]
					term=''
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='verb'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='aux-'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='aux-' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='adj-'):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='noun' and pos2[0:4]=='adv-' and pos3[0:4]=='scon' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adj-' and pos2[0:4]=='scon' and pos3[0:4]=='adv-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='verb' and pos2[0:4]=='verb' and pos3[0:4]=='verb' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1
					if(pos1[0:4]=='adj-' and pos2[0:4]=='noun' and pos3[0:4]=='adj-' and joini in term_list):
						term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
						deletes.append(joini)
						ind=term_list.index(joini)
						#term_list.pop(ind)
						cont=cont+1

	for i in deletes:
		if(i in term_list):
			ind=term_list.index(i)
			term_list.pop(ind)
			
	
	#elapsed_time=time()-start_time
	#txt='PATRONES, DELETE'+' ('+str(cont)+') NEW LIST SIZE: ('+str(len(term_list))+') TIME: ('+str(elapsed_time)+')'
	joind=', '.join(deletes)
	#print('PATRONES DELETE', cont, len(term_list), elapsed_time)
	#conts_log.information(txt, 'TERMS REMOVED: '+joind)
	return(term_list)

'____MAIN____'
#stanza.download('en')
#nlp = stanza.Pipeline('en')
stanza.download('es')
nlp_es = stanza.Pipeline('es')
termlist=['horse', 'must', 'drinking', 'for', 'red', 'cat']
term_list=['caballo', 'hacer pis', 'he hecho', 'rojo']

#delete_pattern_en(term_list)

#tagger= SequenceTagger.load("flair/pos-english")
#pos_tagger = CoreNLPParser('https://corenlp.run/', tagtype='pos')

t="caballo rojo"

doc=nlp_es(t)
print(doc)
sent=doc.sentences[0]
word=sent.words

for info in word:
    pos=info.upos
    print(info.text)
    print(info.upos)
    tupla=(info.text, info.pos)
    print(tupla)


# for term in term_list:
#     doc=nlp_es(term)
#     sent=doc.sentences[0]
#     word=sent.words
#     info=word[0]
#     pos=info.upos
    
#     print(info.text)
#     print(pos)











