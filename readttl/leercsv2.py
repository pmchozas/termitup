# -*- coding: utf-8 -*-
import csv
import sys
from csv import *
import codecs
import re
import argparse 

#como ejecutar desde linea de comandos: python3 leercsv2.py nombredelarchivodeentrada.ttl nombredelarchivodesalida 
#(no se pone la extension del archivo automaticamente lo va a crear en csv)
#lee un ttl en skos y saca los términos a un csv

def cleanttl(infile, outfile):
	encoding = 'utf-8'
	archivo = open(infile, "r")
	contenido = archivo.readlines()

	e=open(outfile+'.csv','w',newline='', encoding='utf-8') 
	ex=csv.writer(e) #se crea el archivo csv   
	ex.writerow(['Termino', 'Contexto', 'Inicio', 'Fin'])
	lista=[]
	lista1=[]
	matriz=[]
	cont=0
	for i in contenido:
		encuentra=i.find('skos:Concept')
		if(encuentra!=-1):
			cont=cont+1
		
	for i in contenido:		
		encuentra1=i.find('skos:prefLabel')
		if(encuentra1!=-1):
			text = i.split('"')
			pref=text[1]	
			lista1.append(pref)
	cont1=0		
	for i in contenido:		
		encuentra=i.find('skos:Concept')
		encuentra2=i.find('lynxlang:hasExample')
		if(encuentra!=-1):
			matriz.insert(cont,[])
			cont1=cont1+1

		if(encuentra2!=-1):
			text1 = i.split('"',1)
			pref1=text1[1]
			lista.append(str(pref1)+'|'+str(cont1-1))	

	for i in range(cont):
		matriz[i].insert(0, lista1[i])
		slp=lista[i].split('|')
		matriz[i].insert(1, slp[0])

	limpiar=re.compile("<'\'.*?>")
	for i in matriz:

		r=''.join(i[0])
		r2=''.join(i[1])

		row1 = re.sub(r'<[^>]*?>','', r)
		row1 = row1.replace('@es;','')

		row2 = re.sub(r'<[^>]*?>','', r2)
		row2 = row2.replace('@es;','').replace('\\','').replace('"','')
		if(row1 in row2):
			start=row2.index(row1)
			tam=len(row1)
			end=row2.index(row1)+tam

		

		ex.writerow([row1,row2, start, end])

print("archivo listo")


parser=argparse.ArgumentParser()
parser.add_argument("sourceFile", help="Name file input") #nombre de archivo a leer
parser.add_argument("fileOut", help="Name file out") #nombre de archivo a leer
args=parser.parse_args()

infile=args.sourceFile
outfile=args.fileOut
cleanttl(infile, outfile)





	

	
