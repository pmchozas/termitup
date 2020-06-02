import os
import json
import csv
import nltk 
from nltk import pos_tag
from nltk.parse import CoreNLPParser
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer 
from nltk.stem import SnowballStemmer
from nltk.tag import StanfordPOSTagger
import re
import requests
import spacy

nlp = spacy.load('es_core_news_sm')


java_path = "../Java/jdk1.8.0_131/bin/java.exe"
os.environ['JAVAHOME'] = java_path
tagger='/Users/karenvazquez/Downloads/stanford-postagger-full-2018-10-16/spanish.tagger'
jar1='/Users/karenvazquez/Downloads/stanford-postagger-full-2018-10-16/models/standford-postagger.jar'
es_stemmer = SnowballStemmer('spanish')

# 0 clean punctuation and stopwords
def clean_terms(termlist):
    stop=stopwords.words('spanish')
    file=open('stop-esp.txt', 'r', encoding='utf-8')
    mystop=file.readlines()
    clean_list = []
    for i in mystop:
        stop.append(i.strip())
    
    for i in termlist:
        k=i.strip(',.:')
        if k not in stop:
            clean_list.append(k)
    return(clean_list)


# 1 añotador
def annotate_timex(text, date, lang):
    url = 'http://annotador.oeg-upm.net/annotate'  
    params = {'inputText':text, 'inputDate':date, 'lan': lang}
    #headers = {'content-type': 'application/json'}
    response=requests.post(url, data=params)
    return(response.text)

# 2 patrones
def delate_pattern(anotador):
	#string_anotador='| '.join(anotador)
	print(len(anotador))
	total=0
	for i in anotador:
		total=total+1
		joini=''.join(i.strip().replace('-', ''))

		if(joini[-1:]==' '):
			joini=joini[:-1]
		list_pos=[]
		if(joini!=''):
			pos_tagger = CoreNLPParser('http://localhost:9003', tagtype='pos')
			tag=pos_tagger.tag(joini.split(' '))
			about_doc=nlp(joini)
			#for token in about_doc:
			#	print (token, token.tag_)
		
			join_tag=''
			for t in about_doc:
				#print(t, t.pos_)
				join_tag+=' '+str(t)
				join_tag=join_tag.strip()
				spl=joini.split(' ')
				
				if(t.pos_ == 'AUX' ):
					ind=spl.index(str(t))
					list_pos.append('aux--'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'NOUN'):
					ind=spl.index(str(t))
					list_pos.append('noun-'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'VERB'):
					ind=spl.index(str(t))
					list_pos.append('verb-'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'ADV'):
					ind=spl.index(str(t))
					list_pos.append('adv--'+str(t))
					#print(t,'-',i,'-',ind)
				if(t.pos_ ==  'ADJ'):
					ind=spl.index(str(t))
					list_pos.append('adj--'+str(t))
					#print(t,'-',i,'-',ind)
			spl_i=joini.split(' ')
			if(len(list_pos)==2 and len(spl_i)==2):
				
				#print(list_pos, total, spl_i, len(spl_i))
				pos1=list_pos[0]
				pos2=list_pos[1]
				term=''
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					print('aux+ver: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					print('verb+aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='verb' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					print('verb+verb: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					print('nombre+verb: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					print('nombre+aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='adv-' and pos2[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]
					print('adv+adj: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='adj-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					print('adj+adv: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='adv-' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					print('adv+aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='aux-' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					print('aux+adv: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='adv-' and pos2[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]
					print('adv+verb: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='verb' and pos2[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]
					print('verb+aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='adv-'):
					term=pos1[5:]+' '+pos2[5:]
					print('noun+adv: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='adv-' and pos2[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]
					print('adv+noun: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)

			if(len(list_pos)==3 and len(spl_i)==3):
				##print(list_pos, total)
				pos1=list_pos[0]
				pos2=list_pos[1]
				pos3=list_pos[2]
				term=''
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + verbo + verbo: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + aux + verbo: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + aux + aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + verb + aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + verb + nombre:', term, joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='aux-' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + aux + nombre: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='verb' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('verb + nombre + nombre: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='verb'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + nombre + verb: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='aux-' and pos2[0:4]=='noun' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('aux + nombre + nombre: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='noun' and pos3[0:4]=='aux-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('nombre + nombre + aux: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='aux-' and pos2[0:4]=='verb' and pos3[0:4]=='noun'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('aux + verb + noun: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='adj-'):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('noun + verb + adj: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
				if(pos1[0:4]=='noun' and pos2[0:4]=='verb' and pos3[0:4]=='noun' and joini in anotador):
					term=pos1[5:]+' '+pos2[5:]+' '+pos3[5:]
					print('noun + verb + noun: ',term,joini)
					ind=anotador.index(joini)
					anotador.pop(ind)
	
	#print(len(anotador))
	#delete_numbers(anotador)
	#quit_plural(anotador)
	return(anotador)

# 3 plurales
def quit_plural(valuelist):
	plural=[]
	for i in valuelist:
		term=i
		plu=''
		if('es' in term[-2:] or 's'  in term[-1:]):
			slp=term.split(' ')
			for j in slp:
				if( ('es' in j[-2:] ) and 't' not in j[-3:-2] ):
					plu+=' '+j[:-2]
				elif(('s' in j[-1:]) ):
					plu+=' '+j[:-1]
				else:
					plu+=' '+j
			#print(term,'|',plu)	
			ind=valuelist.index(term)
			valuelist[ind]=plu.strip()
					
	
	quit_plu=[]
	nuevalista=set(valuelist)
	for i in nuevalista:
		quit_plu.append(i)	
		

	return(quit_plu)

# 4 numeros
def delete_numbers(list_):
	file=open('numberlist_es', 'r', encoding='utf-8')
	read=file.readlines()

	for i in read:
		if(i[-1:]=='\n'):
			i=i[:-1]
			for j in list_:
				#print(i,'|', j)
				if(' '+i+' ' == ' '+j+' ' ):
					print(i, '|', j)
					ind=list_.index(j)
					list_.pop(ind)
	return(list_)


# 5 leer archivo 
def readFile(read):
	text=''
	for i in read:
		spl=i[:-1].split('\t')
		term=spl[1]
		spl2=term.split(' ')
		text+='| '+spl[1]

	return text





#-------MAIN-------#

file=open('estatutoterms_minfreq4.txt', 'r', encoding='utf-8')
read=file.readlines()
text=readFile(read)
date='2020-05-26'
lang='ES'
#print(text)
termlist=text.split('| ')
clean_text=clean_terms(termlist)
#la función clean_terms devuelve una lista limpia de términos
#qué se le pasa a la función anotador?
textanotador=annotate_timex(text, date, lang)
list_anotador=textanotador.split('|')
for i in list_anotador:
	if('<' in i ):
		ind=list_anotador.index(i)
		list_anotador.pop(ind)
for i in list_anotador:
	if('<' in i ):
		ind=list_anotador.index(i)
		list_anotador.pop(ind)

anotador=[]
for i in list_anotador:
	anotador.append(i.strip())

pattern=delate_pattern(anotador)
plural=quit_plural(pattern)
numbers=delete_numbers(plural)
new=open('salida_preproceso.txt', 'w')
for i in numbers:
	new.write(i+'\n')




