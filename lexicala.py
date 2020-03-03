import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from os import remove
import collections
#import mysql.connector


def first(read,languageIn, termIn,targets,out): 
	if(termIn):
		access = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+termIn+"", auth=('92938219312', '92938219312'))
		answer=access.json()
		results=answer['n_results']
		if(results>0):
			traduccion(answer,targets,out)
			definitions=definitionGet(answer)
			getsyn=synonymsGet(answer)
			fileout(out, termIn, languageIn, definitions, getsyn)
			print('TERMINO ENTRADA: ',termIn,'LENGUAJE ENTRADA:', languageIn,'SINONIMOS:',getsyn)
			
	else:
		file=open(read, 'r')
		reader=csv.reader(file)
		for i in reader: 
		    termino=i[0]
		    access = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+termino+"", auth=('upm2', '92938219312'))
		    answer=access.json()
		    results=answer['n_results']
		    listaSinonimos=[]
		    if(results>0):
		    	traduccion(answer,targets,out)
		    	definitions=definitionGet(answer)
		    	getsyn=synonymsGet(answer)
		    	fileout(out, termino, languageIn, definitions, getsyn)
		    	print('TERMINO ENTRADA: ',termino,'LENGUAJE ENTRADA:', languageIn,'SINONIMOS:',getsyn)


def synonymsGet(answer):
	listaSinonimos=[]
	sense0=answer['results'][0]
	if('senses' in sense0.keys()):
		sense1=sense0['senses']
		for i in range(len(sense1)):
				sense=sense1[i]['id']
				access = requests.get("https://dictapi.lexicala.com/senses/"+sense+"", auth=('92938219312', '92938219312'))
				answer=access.json()
				#print(termIn, sense)
				if('synonyms' in answer.keys() ):
				 	syn=answer['synonyms']
				 	if(len(syn)>0):
				 		for j in range(len(syn)):
				 			synonym=syn[j]
				 			listaSinonimos.append(synonym)
	return(listaSinonimos)
	
	
		    	
    
def traduccion(answer,targets,out):
	idterm=answer['results'][0]['id']
	#print('IDLEXICALA TERMINO:',idterm)
	trad = requests.get("https://dictapi.lexicala.com/entries/"+idterm+"", auth=('92938219312', '92938219312'))
	jsonTrad=trad.json()
	if('senses' in jsonTrad.keys()):
		traduction=jsonTrad['senses']
		textList=[]
		for i in range(len(traduction)):
			if('translations' in traduction[i].keys()):
				sensescant=traduction[i]['translations']
				for j in targets:
					if(j in sensescant):
						idiomas=sensescant[j]
						#print(idiomas)
						if('text' in idiomas):
							text=idiomas['text']
							textList.append([text, j])
						else:
							for k in range(len(idiomas)):
								text=idiomas[k]['text']
								textList.append([text, j])
	#print(textList)
	synTrac(textList,out)

def synTrac(textList,out):
	for text, leng in textList:
		access = requests.get("https://dictapi.lexicala.com/search?source=global&language="+leng+"&text="+text+"", auth=('92938219312', '92938219312'))
		answer=access.json()
		results=answer['n_results']
		listaSinonimos=[]
		if(results>0):
			definitions=definitionGet(answer)
			getsyn=synonymsGet(answer)
			fileout(out, text, leng, definitions,getsyn)
			print('TERMINO ENTRADA: ',text,'LENGUAJE ENTRADA:', leng,'SINONIMOS:',getsyn)
		    	
def definitionGet(answer):
	listaDefinition=[]
	sense0=answer['results'][0]
	if('senses' in sense0.keys()):
		sense1=sense0['senses']
		for i in range(len(sense1)):
			if('definition' in sense1[i].keys()):
				definitions=sense1[i]['definition']
				listaDefinition.append(definitions)
	print(listaDefinition)
	return(listaDefinition)

def fileout(out, term, lang, definitions, syns):
	synsJoin=','.join(syns)
	for i in definitions:
		defiJoin=','.join(definitions)
		out.writerow([term, lang, synsJoin, i])


				
		


parser=argparse.ArgumentParser()
parser.add_argument("--lista", help="Nombre de archivo con terminos a buscar") #nombre de archivo a leer
parser.add_argument("--termino", help="Termino a buscar") #nombre de archivo a leer
parser.add_argument("languageIn", help="Lenguaje de entrada") #nombre de archivo a leer
parser.add_argument("--targets", help="Array de idiomas de salida")
parser.add_argument("--out", help="Archivo salida")

args=parser.parse_args()
read=args.lista
languageIn=args.languageIn
termIn=args.termino
if(args.targets):
	targets=args.targets.split(' ')
else:
	targets=[]
outname=args.out
csvf=open(outname, 'w')
out=csv.writer(csvf) #se crea el archivo csv
out.writerow(['term (senses)', 'language', 'synonyms', 'definitions'])
first(read,languageIn,termIn,targets,out)




############### Ejecutar para un solo termino
##CON LENGUAJES DE SALIDA:
#python3 lexicala.py --termino casa es --targets "en de" --out lexica10term.csv
##SIN LENGUAJES DE SALIDA
#python3 lexicala.py --termino casa es --out lexica10term.csv


############### Ejecutar para una lista de terminos
#python3 lexicala.py --lista 10term.csv en --targets "en de" --out lexica10term.csv





