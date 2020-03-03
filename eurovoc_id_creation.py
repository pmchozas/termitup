import json #libreria para utulizar json en python
import pprint #libreria que permite observar mejor un json
import csv #libreria para exportar a excel o csv 
from random import randint #libreria para random
import re
from os import remove
import collections
import argparse
#funcion para obtener identificadores
def sctmid_creator():
    numb = randint(1000000, 9999999)

    SCTMID = "LT" + str(numb)
    return SCTMID

#funcion para crear archivo termino-id
def archivoT_ID(palabra, ex2):
    ide=sctmid_creator()
    ex2.writerow([palabra,ide,'','','','','','','','','','','',''])
    return(ide)

def agregar(nuevosTerminos):
    nuevos=[]
    with open(nuevosTerminos) as File:
        reader=csv.reader(File)
        for row in reader:
            term=row[0]
           # print(term)
    
#funcion para comprobar si el termino ya existe en la lista
def comprobarTermino(nuevo):
    e=open('comprobacion.csv', 'w')
    ex=csv.writer(e) #se crea el archivo csv 
    lista=[]
    n=open('termino_id.csv', 'r')
    lineas=n.readlines()
    with open(nuevo) as File:
        reader=csv.reader(File)
        for row in reader:
            term=row[0]
            lista.append(term)
            for i in lineas:
                s=i.split(',')
                t=s[0]
                idd=s[1]
                if(term==t):
                    lista.remove(term)
                    #agregar(i[:-1])
                    #print('iguales', term)
               
                    
    #print(lista)
    #ex.writerow(['prefLabel@en'])
    for i in lista:
        ex.writerow([i])
    e.close()
    lista=open("comprobacion.csv", newline='')
    tipo='a'
    haceJson(lista,tipo)
    #agregar(ex)

def comprobarIDE(ide):
    listaIds=[]
    nuevoide=''
    #print('comprobar ide', ide)
    with open('termino_id.csv', newline='') as File:
        reader=csv.reader(File)
        for row in reader:
            identificador=row[0]
            #print(identificador)
            listaIds.append(identificador)
            if(ide==identificador):
                nuevoide=sctmid_creator()
                #print('repetido', nuevoide)
            else:
                nuevoide=ide
                #print('no es repetido',nuevoide)
    #print(nuevoide)
    return(nuevoide)

#crear nuevas ids para broaders y narrowers
#hay que añadir el narrower.csv

def eurovocuris():
    # listaeuroterm=[]

    File2=open('euroterm.csv', 'w', newline='\n')
    writer = csv.writer(File2)

    with open('salida_broader.csv', 'r') as File1:
        reader = csv.reader(File1)
        for row in reader:
            print(row)
            a=row[2]
            writer.writerow([row[2]])
                # euroterm=row[2]
                # listaeuroterm.append(euroterm)
            # return(listaeuroterm)
        # return(euroterm)

#hay que añadir que compruebe los términos de euroterm etc
def asignID(termIdFile, inFile, outFile):
    nuevoid=''
    File1=open(termIdFile, 'a')
    #writer1 = csv.writer(File1)
    listwriter1=[]
    File2=open(outFile, 'w')
    #writer2 = csv.writer(File2)
    listwriter2=[]
    listwriter2.append(['prefLabel@en', 'term_id', 'broader_uri', 'broader_id', 'prefLabel@en', 'prefLabel@es', 'prefLabel@de', 'prefLabel@nl'])
    nuevosids=[]
    listUris=[]
    idebueno=''
    lines=[]
    File= open(inFile, 'r')
    reader=csv.reader(File)
    for row in reader:
        #print(row)
        if(len(row)>1):
            uri=row[2]
            if(uri!="-"):
                listUris.append(uri)


    repetido = []
    unico = []
     
    for x in listUris:
        if x not in unico:
            ide=sctmid_creator()
            #print(x,'ide generado', ide)
            nuevoid=comprobarIDE(ide)
            nuevosids.append(nuevoid)
            unico.append([x,nuevoid])
        else:
            if x not in repetido:
                repetido.append(x)
    #print(len(listUris))
    c=0
    Files=open(inFile, newline='\n')
    reader2=csv.reader(Files)
    for row in reader2:
        if(len(row)>1):
            listwriter1.insert(c, [])
            listwriter2.insert(c, [])
            pref=row[0]
            termid=row[1]
            broaderuri=row[2]
            broaderid=row[3]
            prefen=row[4]
            prefes=row[5]
            prefde=row[6]
            prefnl=row[7]
            for t in unico:
                #print(broaderuri,'-',t[0])
                if(broaderuri==t[0]):
                    idebueno=t[1]
                
            #print(pref,termid,broaderuri,idebueno,broaderid, prefen, prefes, prefde, prefnl)
            if(idebueno!='-' or len(row)<1):
                listwriter1[c].insert(0, prefen)
                listwriter1[c].insert(1, idebueno)
            listwriter2.append([pref,termid,broaderuri,idebueno, prefen, prefes, prefde, prefnl])
            
            idebueno='-'
            c=c+1

    for r in listwriter1[1:]:
        if(len(r)>1):
            joinr=','.join(r)
            File1.write(joinr+'\n')
    for r in listwriter2[2:]:
        if(len(r)>1 or r==''):
            joinr=','.join(r)
            File2.write(joinr+'\n')

    

parser=argparse.ArgumentParser()
parser.add_argument("inFile", help="Nombre de archivo con terminos")
parser.add_argument("termIdFile", help="Nombre de archivo con terminos")
parser.add_argument("outFile", help="Nombre de archivo nuevo generado")
args=parser.parse_args()

inFile=args.inFile
termIdFile=args.termIdFile
outFile=args.outFile


asignID(termIdFile, inFile, outFile)
