#RECIBE CONTEXTO COMO ARCHIVO DE ENTRADA

import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from os import remove
import collections
#import mysql.connector

def lexicalaSearch(languageIn, term):
	search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+languageIn+"&text="+term+"", auth=('987123456', '987123456'))
	answerSearch=search.json()
	return(answerSearch)

def lexicalaSense(maximo):
	sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('987123456', '987123456'))
	answerSense=sense.json()
	return(answerSense)

def first(read,languageIn, termIn,targets,out,context, contextFile): 
	if(termIn):
		answer=lexicalaSearch(languageIn, termIn)
		results=answer['n_results']
		if(results>0):
			definitions=definitionGet(answer)
			maximo=wsid(termIn,context,contextFile, definitions)
			tradMax=traductionGet(maximo, targets)
			synsTrad=justSyn(tradMax)
			getsyn=synonymsGet(maximo)
			fileout(termIn, maximo, getsyn, tradMax, synsTrad)

			
	else:
		file=open(read, 'r')
		reader=csv.reader(file)
		for i in reader: 
		    termino=i[0]
		    print(termino)
		    answer=lexicalaSearch(languageIn, termino)
		    results=answer['n_results']
		    listaSinonimos=[]
		    if(results>0):
		    	definitions=definitionGet(answer)
		    	maximo=wsid(termino,context,contextFile, definitions)
		    	tradMax=traductionGet(maximo, targets)
		    	synsTrad=justSyn(tradMax)
		    	getsyn=synonymsGet(maximo)
		    	fileout(termIn, maximo, getsyn)

def justSyn(tradMax):
	slp=tradMax[0].split(',')
	listaSinonimos=[]
	answer=lexicalaSearch(slp[1], slp[0])
	results=answer['n_results']
	if(results>0):
		if('synonyms' in answer.keys() ):
			syn=answer['synonyms']
			if(len(syn)>0):
				for j in range(len(syn)):
				 	synonym=syn[j]
				 	listaSinonimos.append(synonym)
	joinSyns=','.join(listaSinonimos)
	return(joinSyns)



def synonymsGet(maximo):
	listaSinonimos=[]
	answer=lexicalaSense(maximo[1])
	if('synonyms' in answer.keys() ):
		syn=answer['synonyms']
		if(len(syn)>0):
			for j in range(len(syn)):
				 synonym=syn[j]
				 listaSinonimos.append(synonym)
	joinSyns=','.join(listaSinonimos)
	return(joinSyns)
	

		    	
def definitionGet(answer):
	listaDefinition=[]
	listaId=[]
	sense0=answer['results'][0]
	if('senses' in sense0.keys()):
		sense1=sense0['senses']
		for i in range(len(sense1)):
			if('definition' in sense1[i].keys()):
				id_definitions=sense1[i]['id']
				definitions=sense1[i]['definition']
				listaDefinition.append(definitions.replace(',', ''))
				listaId.append(id_definitions)
	return(listaDefinition, listaId)

def wsid(termIn, context, contextFile, definitions):
	if(contextFile):
		file=open(contextFile, 'r')
		reader=csv.reader(file)
		pesos=[]
		for contexto in reader:
			termino=contexto[0]
			contex=contexto[1]
			start=contexto[2]
			end=contexto[3]
			if(termIn in termino):
				listdef=definitions[0]
				listIde=definitions[1]
				definitionsJoin=', '.join(listdef)
				response = requests.post(
					    'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
					    params={'context': contex, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
					    headers ={'accept': 'application/json',
								'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
								}
						)
				if(response.json()):
					pesos=response.json()
				else:
					pesos=[]


		if(len(pesos)>0):
			max_item = max(pesos, key=int)
			posMax=pesos.index(max_item)
			defiMax=listdef[posMax]
			idMax=listIde[posMax]
		else:
			defiMax=''
			idMax=''
	else:
		pesos=[]
		start=context.index(termIn)
		longTerm=len(termIn)
		end=context.index(termIn)+longTerm
		listdef=definitions[0]
		listIde=definitions[1]
		definitionsJoin=', '.join(listdef)
		response = requests.post(
					    'http://wsid-88-staging.cloud.itandtel.at/wsd/api/lm/disambiguate_demo/',
					    params={'context': context, 'start_ind': start, 'end_ind': end,  'senses': definitionsJoin}, 
					    headers ={'accept': 'application/json',
								'X-CSRFToken': 'WCrrUzvdvbA4uahbunqIJGxTpyAwFuIGgIm9O91EfeiQwH3TnUUsnF2cdXkHXi94'
								}
						)
		if(response.json()):
			pesos=response.json()
		else:
			pesos=[]

		if(len(pesos)>0):
			max_item = max(pesos, key=int)
			posMax=pesos.index(max_item)
			defiMax=listdef[posMax]
			idMax=listIde[posMax]
		else:
			defiMax=''
			idMax=''


	return(defiMax, idMax)


def traductionGet(maximo, targets):
	textList=[]
	jsonTrad=lexicalaSense(maximo[1])
	if('translations' in jsonTrad.keys()):
		translations=jsonTrad['translations']
		for j in targets:
			if(j in translations):
				idiomas=translations[j]
				if('text' in idiomas):
					text=idiomas['text']
					textList.append(text+','+ j)
				else:
					for k in range(len(idiomas)):
						text=idiomas[k]['text']
						textList.append(text+','+ j)
	return(textList)


def fileout(termIn,maximo, getsyn, tradMax, synsTrad):
	defMax=maximo[0]
	joinT='-'.join(tradMax)
	out.writerow([termIn, defMax, maximo[1], getsyn, joinT, synsTrad])





				
		


parser=argparse.ArgumentParser()
parser.add_argument("--lista", help="Nombre de archivo con terminos a buscar") #nombre de archivo a leer
parser.add_argument("--termino", help="Termino a buscar") #nombre de archivo a leer
parser.add_argument("languageIn", help="Lenguaje de entrada") #nombre de archivo a leer
parser.add_argument("--targets", help="Array de idiomas de salida")
parser.add_argument("--context", help="Contexto")
parser.add_argument("--contextFile", help="Archivo de contextos")
parser.add_argument("--out", help="Archivo salida sin extension (sin .csv)")

args=parser.parse_args()
read=args.lista
languageIn=args.languageIn
termIn=args.termino
context=args.context
contextFile=args.contextFile

if(args.targets):
	targets=args.targets.split(' ')
else:
	targets=[]
outname=args.out

csvf=open(outname+'.csv', 'w')
out=csv.writer(csvf) #se crea el archivo csv
out.writerow(['term In', 'desambiguation','ID', 'synonyms', 'term-target', 'synonyms-target'])

first(read,languageIn,termIn,targets,out,context, contextFile)






##EJECUTAR con lista de contextos, para un solo termino y lenguajes de salida
#MacBook-Pro-de-Karen:termitup karenvazquez$ python3 desambiguacion.py --termino término es --targets "en de" --contextFile contextos_salida.csv 
##EJECUTAR con un contexto, para un solo termino y lenguaje de salida
#MacBook-Pro-de-Karen:termitup karenvazquez$ python3 desambiguacion.py --termino término es --targets "en de" --context "f Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antigüedad en la empresa." 


