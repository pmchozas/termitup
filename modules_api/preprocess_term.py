import csv #libreria para exportar a excel o csv 
import nltk 
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import random

def preProcessingTerm(term, corpus, lang):
    context=corpus
    list_contx_rd=list()
    if(context):
        context=context
    elif(contextFile):
        file=open(contextFile, 'r', encoding='utf-8')
        contextFile=file.readlines()
        list_contx=[]
        list_len=[]
        for i in contextFile:
            text=i.replace('\n', '')
            if(term in text):
                ind=text.index(term)
                #print(ind)
                start=text[0:ind]
                end=text[ind:]
                list_start=start.split(' ')
                list_end=end.split(' ')
                context1=list_start[len(list_start)-48:]
                context2=list_end[:48]
                join1=' '.join(context1)
                join2=' '.join(context2)
                context=join1+' '+join2
                #print(context)
                list_contx.append(context)

    else:
        contextFile=leerContextos(lang, term)
        for j in contextFile:
            if(term.lower() == j[0].lower()):
                context=j[1].lower()
                context=reduction_wsid(context)

    #print(term, len(list_contx), list_contx)
    if(len(list_contx)):
        list_contx_rd=list()
        for i in range(5):
            aleatorio = random.choice(list_contx)
            if aleatorio not in list_contx_rd:
                list_contx_rd.append(aleatorio)
    #print(len(aleatorio), len(list_contx_rd), list_contx_rd)

    return(term,  context, list_contx_rd)




def leerContextos(lang, termIn):
    configuration= {
        "es": "contexts/Spain-judgements-ES.ttl",
        "en": "contexts/UK-judgements-EN.ttl",
        "nl": "contexts/DNVGL-NL.ttl",
        "de": "contexts/contracts_de.ttl",
    }

    configuration2= {
        "es": "contexts/Spain-legislation-ES.ttl",
        "en": "contexts/Ireland-legislation-EN.ttl",
        "nl": "contexts/DNVGL-NL.d ttl",
        "de": "contexts/Austria-collectiveagreements-DE.ttl",
    }

    configuration3= {
        "es": "contexts/Spain-collectiveagreements-ES.ttl",
        "en": "contexts/DNVGL-EN.ttl",
        "nl": "contexts/DNVGL-NL.ttl",
        "de": "contexts/Austria-legislation-DE.ttl"
    }
    
    es = '%s'%configuration["es"]
    en = '%s'%configuration["en"]
    nl = '%s'%configuration["nl"]
    de = '%s'%configuration["de"]
    encoding = 'utf-8'
    if(lang=='es'):
        file = open(es, "r")
    elif(lang=='en'):
        file = open(en, "r")
    elif(lang=='de'):
        file = open(de, "r")
    elif(lang=='nl'):
        file = open(nl, "r")

    content = file.readlines()
    
    listt=[]
    listt1=[]
    matrix=[]
    contextlist=[]
    find=[]
    cont=0
    for i in content:
        findword=i.find('skos:Concept')
        if(findword!=-1):
            cont=cont+1
        
    for i in content:     
        findword1=i.find('skos:prefLabel')
        if(findword1!=-1):
            text = i.split('"')
            pref=text[1]    
            listt1.append(pref)
    cont1=0     
    for i in content:     
        findword=i.find('skos:Concept')
        findword2=i.find('lynxlang:hasExample')
        if(findword!=-1):
            matrix.insert(cont,[])
            cont1=cont1+1

        if(findword2!=-1):
            text1 = i.split('"',1)
            pref1=text1[1]
            listt.append(str(pref1)+'|'+str(cont1-1))   

    for i in range(cont):
        matrix[i].insert(0, listt1[i])
        slp=listt[i].split('|')
        matrix[i].insert(1, slp[0])

    limpiar=re.compile("<'\'.*?>")
    for i in matrix:
        r=''.join(i[0])
        r2=''.join(i[1])
        row1 = re.sub(r'<[^>]*?>','', r)
        row1 = row1.replace('@es;','')
        row2 = re.sub(r'<[^>]*?>','', r2)
        row2 = row2.replace('@es;','').replace('\\','').replace('"','')
        if(row1 in row2):
            contextlist.append([row1,row2[:-1]])
        
    for i in contextlist:
        if(termIn in i[0] and len(find)==0):
            start=i[1].index(termIn)
            tam=len(termIn)
            end=i[1].index(termIn)+tam
            find.append([termIn,i[1], start, end])
    return(find)

#preProcessingTerm('abonar', None, '../data/corpus/estatuto_es.txt', 'es')


