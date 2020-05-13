
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
import os
from os import remove
import collections
from os import listdir
from os.path import isfile, isdir
from unicodedata import normalize
import globales
# check
name_file=globales.name_file
targets=globales.targets
def checkTerm(lang,  termSearch, relation, targets):
    listt_arq=path(targets, relation,name_file)
    ide=sctmid_creator()
    termSearch=termSearch.replace('\ufeff', '')
    termSearch=termSearch.replace('_', ' ')
    termSearch=termSearch.lower()
    n=termSearch
    n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", n), 0, re.I
            )
    n = normalize( 'NFC', n)
    for carps in listt_arq:
        for j in carps:
            if('.DS_Store' not in j):
                slp=j.split('_')
                
                if(len(slp)>2):
                    termfile=slp[:len(slp)-1]
                    termfile=' '.join(termfile)
                    slp2=slp[len(slp)-1].split('.')
                    idefile=slp2[0]
                else:

                    termfile=slp[0]
                    if(len(slp)>1):
                        slp2=slp[1].split('.')
                    idefile=slp2[0]

                

                if(n == termfile):
                    termSearch='1'
                    ide=idefile
                else:
                    termSearch=termSearch
                    if(ide in idefile):
                        ide=sctmid_creator()
                        checkTerm(lang, termSearch, relation, targets)
                    else:
                        ide=ide
    return(ide, termSearch)



# files
def path(targets, relation,name_file):
    listt_arq=[]
    #targets=['terminosjson']
    for i in targets:
        if(relation!=''):
            path=name_file+i+'/'+relation+'/'
        else:
            path=name_file+i+'/'
        listt = [obj for obj in listdir(path) if isfile(path + obj)]
        listt_arq.append(listt)
    return(listt_arq)

# id creation
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID