import csv
import sys

#lee un ttl en skos y saca los términos a un csv

def cleanttl(file):
	archivo = open(file, "r")
	contenido = archivo.readlines()

	e=open('termsclean.csv','w')
	ex=csv.writer(e) #se crea el archivo csv    

	lista=[]
	for i in contenido:
		encuentra=i.find('skos:prefLabel')
		if(encuentra!=-1):
			text = i.split('"')
			pref=text[1]		
			lista.append(pref)

	for x in lista: 	
		term = x.split(", ")
		lista2=ex.writerow(term)

	print("Archivo csv listo")

file="spain-labourlaw-ES.ttl"
cleanttl(file)





	

	
