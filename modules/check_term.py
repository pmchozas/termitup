
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
import os
from os import remove
import collections
from os import listdir
from os.path import isfile, isdir
from unicodedata import normalize
import csv
import trans_id

# check if the term already exists
def checkTerm(lang,  termSearch, relation, targets, ide1):
    listt_arq=path(targets, relation)
    ide=trans_id.trans_ID(termSearch, lang)
    n=termSearch
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
    n = normalize( 'NFC', n)
    for carps in listt_arq:
        for j in carps:
            #print(j)
            if('.DS_Store' not in j):
                slp=j.split('-')
                termfile=''
                if(len(slp)>2):
                    termfile=slp[:len(slp)-1]
                    termfile=' '.join(termfile)
                    slp2=slp[len(slp)-1].split('.')
                    #idefile=slp2[0]
                    
                elif(len(slp)>1):
                    termfile=slp[0]
                    if(len(slp)>1):
                        slp2=slp[1].split('.')
                        #idefile=slp2[0]
                
                
                #print(termfile, n)
                if(n == termfile):
                    termSearch='1'
                    #ide=idefile
                else:
                    termSearch=termSearch
                    '''if(ide in idefile):
                        ide=sctmid_creator()
                        checkTerm(lang, termSearch, relation, targets, ide)
                    else:
                        ide=ide'''
    #print('FOLDER: ', ide, termSearch)
    check2=check_term_in_Terminology(ide, termSearch)
    return(check2[0], check2[1])

def check_term_in_Terminology(ide, termSearch):
    file=open('terms_terminology.csv', 'r', encoding='utf-8')
    read=csv.reader(file)
    for i in read:
        if(termSearch ==i[0] ):
            termSearch='1'
            if(ide in i ):
                ide=sctmid_creator()
                #checkTerm(lang, termSearch, relation, targets, ide)
            else:
                ide=ide
        else:
            termSearch=termSearch

    return(ide, termSearch)

# files
def path(targets, relation):
    listt_arq=[]
    '''for i in targets:
        if(relation!=''):
            path=i+'/'+relation+'/'
        else:
            path=i+'/'
        listt = [obj for obj in listdir(path) if isfile(path + obj)]
        listt_arq.append(listt)'''

    path='data/output/'
    listt = [obj for obj in listdir(path) if isfile(path + obj)]
    listt_arq.append(listt)
    return(listt_arq)

# id creation
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID