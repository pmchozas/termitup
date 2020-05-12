import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
import os
from os import remove
import collections
from os import listdir
from os.path import isfile, isdir
import time

def leerContextos(fileTerms, fileContexts):
	fileT=open(fileTerms, 'r')
	readTerms=csv.reader(fileT)

	fileC=open(fileContexts, 'r')
	readContexts=fileC.readlines()

	fileNew=open('estatutoContexts.csv', 'w')
	fn = csv.writer(fileNew)

	lista=[]
	for termino in readTerms:
		for contexts in readContexts:
			if(termino[0] in contexts):
				while(termino[0] not in lista):
					start=contexts.index(termino[0])
					tam=len(termino[0])
					end=contexts.index(termino[0])+tam
					fn.writerow([termino[0],contexts, start, end])
					lista.append(termino[0])


		



leerContextos('estatuto.csv', 'estatuto.txt')