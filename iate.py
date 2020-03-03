import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from os import remove
import collections


#funcion para obtener identificadores
def sctmid_creator():
    numb = randint(1000000, 9999999)
    SCTMID = "LT" + str(numb)
    return SCTMID

#funcion para crear archivo termino-id
def term_id_file(listTerm, termino, nameFile, tipo ):
    ide=''
    listaTerminoId=[]
    if(tipo=='w'):
        fileNew=open(nameFile+'.csv', 'w')
        readerNew=csv.writer(fileNew)
        if(termino):
            ide=sctmid_creator()
            listaTerminoId.append([termino,ide])
            readerNew.writerow([termino,ide])
        
        else:
            file=open(listTerm+'.csv', 'r')
            reader=csv.reader(file)
            for i in reader: 
                termino=i[0]
                ide=sctmid_creator()
                listaTerminoId.append([termino,ide])
                readerNew.writerow([termino,ide])
    else:
        fileNew=open(nameFile+'.csv', 'a')
        readerNew=csv.writer(fileNew)
        if(termino):
            listaTerminoId=comprobarTermino(termino, nameFile,listaTerminoId)
        
        else:
            file=open(listTerm+'.csv', 'r')
            reader=file.readlines()
            for i in reader: 
                split=i.split(',')
                termino=split[0]
                if('\n' in termino):
                    termino=termino[:-1]
                else:
                    termino=termino
                listaTerminoId=comprobarTermino(termino, nameFile,listaTerminoId)
                

    return(listaTerminoId)




#funcion para comprobar si el termino ya existe en la lista
def comprobarTermino(termino, termId, listaTerminoId):
    ide=''
    nuevotermino=''
    listaTermino=[]
    listaIde=[]
    File=open(termId+'.csv', 'r')
    reader=csv.reader(File)
    File2=open(termId+'.csv', 'a')
    reader2=csv.writer(File2)
    for row in reader:
        termFile=row[0]
        ideFile=row[1]
        listaTermino.append(termFile)
        listaIde.append(ideFile)
    #print(listaTermino)

    if(termino in listaTermino):
        pos=listaTermino.index(termino)
        listaTerminoId.append([termino,listaIde[pos]])
    else:
        #print('es nuevo termino')
        ide=sctmid_creator()
        cide=comprobarIDE(ide, termId)
        listaTerminoId.append([termino,ide])
        reader2.writerow([termino,cide])

    return(listaTerminoId)



def comprobarIDE(ide, termId):
    listaIds=[]
    nuevoide=''
    File=open(termId+'.csv', 'r')
    reader=csv.reader(File)
    for row in reader:
        ideFile=row[1]
        if(ide==ideFile):
            ide=sctmid_creator()
            nuevoide=comprobarIDE(ide, termId)
            #print('ya existe ide', cide)
        else:
            nuevoide=ide

    return(nuevoide)

def archivos_eurovoc(lista, fileEurovoc,idioma):
    b=open(fileEurovoc+'_br.csv', 'w')
    broader=csv.writer(b)
    n=open(fileEurovoc+'_na.csv', 'w')
    narrower=csv.writer(n)
    r=open(fileEurovoc+'_re.csv', 'w')
    related=csv.writer(r)


    broader.writerow(['prefLabel@'+idioma, 'term_id','broader_uri', 'broader_id', 'brprefLabel@en', 'brprefLabel@es','brprefLabel@de','brprefLabel@nl'])
    narrower.writerow(['prefLabel@'+idioma, 'term_id','narrower_uri', 'narrower_id', 'naprefLabel@en', 'naprefLabel@es','naprefLabel@de','naprefLabel@nl'])
    related.writerow(['prefLabel@'+idioma, 'term_id','related_uri', 'related_id', 'reprefLabel@en', 'reprefLabel@es','reprefLabel@de','reprefLabel@nl'])
    for i in lista:
        termino=i[0]
        ide=i[1]
        broader.writerow([termino, ide,'','','','','',''])
        narrower.writerow([termino, ide,'','','','','',''])
        related.writerow([termino, ide,'','','','','',''])

#funcion para obtener el baren token (access token)
def obtenerToken(): 
    print('Obteniendo token')
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?username=VictorRodriguezDoncel&password=h4URE7N6fXa56wyK')
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    return(access)



def haceJson(lista, idioma):
    print('IATE QUERYS-')
    hacejsonList=[]
    auth_token=obtenerToken() #se llama a la funcion que obtiene el token para realizar la consulta posteriormente
    f=open('archivojson.json', 'w')
    hed = {'Authorization': 'Bearer ' +auth_token}
    jsonList=[]
    for i in lista:
        termino=i[0]
        #print(termino) 
        ide=i[1]
        data = {"query": termino,
        "source": idioma,
        "targets": [
        "en",
        "es",
        "de",
        "nl"
        ],
        "search_in_fields": [
            0
        ],
        "search_in_term_types": [
            0,
            1,
            2,
            3,
            4
        ],
         "filter_by_domains": [
    "86817304A07344BC8B544B390129ADDF",
    "5B8AB13A1DA9412F8EE914DD40D469E1",
    "70C8DCD591A145A69CBFAC9405AB90E1",
    "1C9C154AD10E4515B60A5AEEB1A04B7C",
    "7593C35C03034FBA9737E2A7EEADDD6A",
    "78481530C8D346EFBC4CE34FBD730476",
    "698DCDA39DF14751BB4E2449B7274C3D",
    "0460ABF0F73B4799BCD7DC5287D810B0",
    "4FEA3CDDFE3B4DD188D9A6E23004B136",
    "0B52BF975B664CD5997CE4DB99EA67D1",
    "1C2BB68922D84C1AB0B6B362EBA5100A",
    "08A084532207495CB9276FE30188048C",
    "DFFE1B0A73624006888F21D57085832A",
    "D8811DC89580413D8B7B2BD77AD18F10",
    "F93ED12A90064881879E66EEA9987598"

        ],
        "query_operator": 1
    }
        url= 'https://iate.europa.eu/em-api/entries/_search?expand=true&limit=5&offset=0'
        response = requests.get(url, json=data, headers=hed)
        reponse2=response.json()
        js=json.dumps(reponse2)
        jsonList.append(reponse2)
        #print(reponse2)
        json.dump(reponse2,f,indent=4,ensure_ascii=False,)#se guarda todo en un archivo json
    
    #print(jsonList)
    return(jsonList)

def corregirJson():
    print('Creando array de consulta Json')
    file=open('archivojson.json', 'r')
    data=file.readlines()
    file2=open('json_final.json', 'w')
    file2.write('['+'\n')
    for i in data:
        r=i.replace('}{','},{')
        file2.write(r)
    file2.write(']'+'\n')

def obtenerIdioma(idioma2, i, palabra,defi):
    #print('IDOMA: ',idioma2)
    term_val_es=''
    term_val_de=''
    term_val_nl=''
    lenguaje=i['language'][idioma2]
    ambos=[]
    sinonimo=[]
    #print(palabra, idioma2)
    for l in lenguaje:
        if(l=='term_entries' ):
            t_e=i['language'][idioma2]['term_entries']
            defi=''.join(defi)
            if(len(t_e)>0):
                term_val=i['language'][idioma2]['term_entries'][0]['term_value']
                #print('term_value',term_val)
                for t in range(len(t_e)):
                    s=i['language'][idioma2]['term_entries'][t]['term_value']
                    if(palabra is not s ):
                        sinonimo.append(s)
                    
            else:
                term_val=''
                sinonimo.append('')
                sinonimo_en=','.join('')
        elif( l=='definition' ) :
            defi=i['language'][idioma2]['definition']
            sinonimo_j=','.join(sinonimo)
    
    #print(palabra,'sinonimo',sinonimo)
    for i in sinonimo:
        if(i in palabra):
            #print('esta')
            sinonimo.remove(i)
            sinonimo_j=','.join(sinonimo)
        else:
            #print('no esta')
            sinonimo_j=','.join(sinonimo)
    #print('sinonimo 2',sinonimo_j)
    ambos.append(sinonimo_j)
    ambos.append(defi)
    ambos.append(term_val)
    return(ambos)

#funcion que introduce todo en un csv 
def parserExcel(lista, jsonlist,  csvFILE,tipo,idioma):
    print('Parseando a Excel')
    nuevost=0
    #data=json
    file=open('json_final.json', 'r')
    data=json.load(file)

    csvf=open(csvFILE+'.csv', 'w')
    csvwriter=csv.writer(csvf) #se crea el archivo csv

    
    if(idioma=='es'):
        csvwriter.writerow(['term_id','prefLabel@'+idioma,'altLabel@'+idioma, 'definition@'+idioma, 'prefLabel@en','altLabel@en', 'definition@en','prefLabel@de','altLabel@de', 'definition@de','prefLabel@nl','altLabel@nl', 'definition@nl', 'iate_id'])
    elif(idioma=='en'):
        csvwriter.writerow(['term_id','prefLabel@'+idioma,'altLabel@'+idioma, 'definition@'+idioma, 'prefLabel@es','altLabel@es', 'definition@es','prefLabel@de','altLabel@de', 'definition@de','prefLabel@nl','altLabel@nl', 'definition@nl', 'iate_id'])
    elif(idioma=='de'):
        csvwriter.writerow(['term_id','prefLabel@'+idioma,'altLabel@'+idioma, 'definition@'+idioma, 'prefLabel@en','altLabel@en', 'definition@en','prefLabel@es','altLabel@es', 'definition@es','prefLabel@nl','altLabel@nl', 'definition@nl', 'iate_id'])
    elif(idioma=='nl'):
        csvwriter.writerow(['term_id','prefLabel@'+idioma,'altLabel@'+idioma, 'definition@'+idioma, 'prefLabel@en','altLabel@en', 'definition@en','prefLabel@de','altLabel@de', 'definition@de','prefLabel@es','altLabel@es', 'definition@es', 'iate_id'])
    
    j=0
    for i in lista[1:]:
        palabra=i[0] 
        ide=i[1] 
        #print(palabra)
         
        defi=''
        dat=data[j]
        term=''
        listafinal=[]
        resultado_es=[]
        resultado_en=[]
        resultado_de=[]
        resultado_nl=[]
        if('items' in dat.keys()):
            termino=data[j]['items']
            for i in termino:#en cada de los siguientes ciclos se va interactuando en el json para obtener lo necesario
                uri2=i['id']
                leng=i['language']
                for k in leng:
                    if(k=='es'):
                        listaFinal_es=obtenerIdioma('es', i,palabra,defi)
                        listaSinonimo_es=listaFinal_es[0]
                        definicionCompleta_es=listaFinal_es[1]
                        term_val_es=listaFinal_es[2]
                        resultado_es.append(listaSinonimo_es)
                        
                    elif(k=='en'):
                        listaFinal_en=obtenerIdioma('en', i,palabra,defi)
                        listaSinonimo_en=listaFinal_en[0]
                        definicionCompleta_en=listaFinal_en[1]
                        term_val_en=listaFinal_en[2]
                        resultado_en.append(listaSinonimo_en)
                            
                    elif(k=='de'):
                        listaFinal_de=obtenerIdioma('de', i,palabra,defi)
                        listaSinonimo_de=listaFinal_de[0]
                        definicionCompleta_de=listaFinal_de[1]
                        term_val_de=listaFinal_de[2]
                        resultado_de.append(listaSinonimo_de)
                            
                    elif(k=='nl'):
                        listaFinal_nl=obtenerIdioma('nl', i,palabra,defi)
                        listaSinonimo_nl=listaFinal_nl[0]
                        definicionCompleta_nl=listaFinal_nl[1]
                        term_val_nl=listaFinal_nl[2]
                        resultado_nl.append(listaSinonimo_nl)
                            

                    else:
                        term_val_es=''
                        term_val_de=''
                        term_val_en=''
                        term_val_nl=''   
                
                '''
                limpiar=re.compile('<.*?>')
                r_es=','.join(resultado_es)
                r_en=','.join(resultado_en)
                r_de=','.join(resultado_de)
                r_nl=','.join(resultado_nl)
                sinonimoEN=re.sub(limpiar,'', r_en).encode();
                definicionEN=re.sub(limpiar,'', definicionCompleta_en).encode();
                sinonimoES=re.sub(limpiar,'', r_es).encode();
                definicionES=re.sub(limpiar,'', definicionCompleta_es).encode();
                sinonimoDE=re.sub(limpiar,'', r_de).encode();
                definicionDE=re.sub(limpiar,'', definicionCompleta_de).encode();
                sinonimoNL=re.sub(limpiar,'', r_nl).encode();
                definicionNL=re.sub(limpiar,'', definicionCompleta_nl).encode();

                csvwriter.writerow([ide,palabra, sinonimoEN.decode(),definicionEN.decode(),term_val_es, sinonimoES.decode(),definicionES.decode(),term_val_de, sinonimoDE.decode(),definicionDE.decode(),term_val_nl, sinonimoNL.decode(),definicionNL.decode(),uri2])
                ''' 
                
                
                r_es=','.join(resultado_es)
                r_en=','.join(resultado_en)
                r_de=','.join(resultado_de)
                r_nl=','.join(resultado_nl)
                limpiar=re.compile('<.*?>')
                listaSinonimo_en=r_en.split(',')
                listaSinonimo_nl=r_nl.split(',')
                listaSinonimo_es=r_es.split(',')
                listaSinonimo_de=r_de.split(',')   
                '''for singles in listaSinonimo_en:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', singles),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                        
                for sspanish in listaSinonimo_es:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', sspanish),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                        
                for sgerman in listaSinonimo_de:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', sgerman),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])

                for sdutch in listaSinonimo_nl:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', sdutch),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                '''
            if(idioma=='en'):  
                for singles in listaSinonimo_en:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', singles),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sspanish in listaSinonimo_es:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', sspanish),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sgerman in listaSinonimo_de:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', sgerman),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sdutch in listaSinonimo_nl:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', sdutch),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                
            elif(idioma=='es'):      
                for singles in listaSinonimo_en:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_en, re.sub(limpiar,'', singles),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sspanish in listaSinonimo_es:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', sspanish),re.sub(limpiar,'', definicionCompleta_es),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sgerman in listaSinonimo_de:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', sgerman),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sdutch in listaSinonimo_nl:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', sdutch),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                
            elif(idioma=='de'):      
                for singles in listaSinonimo_en:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sspanish in listaSinonimo_es:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_en,  re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sgerman in listaSinonimo_de:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', sgerman),re.sub(limpiar,'', definicionCompleta_de),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sdutch in listaSinonimo_nl:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_nl, re.sub(limpiar,'', sdutch),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                
            elif(idioma=='nl'):
                for singles in listaSinonimo_en:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sspanish in listaSinonimo_es:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sgerman in listaSinonimo_de:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_es, re.sub(limpiar,'', listaSinonimo_es[0]),re.sub(limpiar,'', definicionCompleta_es),term_val_nl, re.sub(limpiar,'', listaSinonimo_nl[0]),re.sub(limpiar,'', definicionCompleta_nl),uri2])
                for sdutch in listaSinonimo_nl:
                    csvwriter.writerow([ide,palabra, re.sub(limpiar,'', sdutch),re.sub(limpiar,'', definicionCompleta_nl),term_val_en, re.sub(limpiar,'', listaSinonimo_en[0]),re.sub(limpiar,'', definicionCompleta_en),term_val_de, re.sub(limpiar,'', listaSinonimo_de[0]),re.sub(limpiar,'', definicionCompleta_de),term_val_e, re.sub(limpiar,'', listaSinonimo_e),re.sub(limpiar,'', definicionCompleta_e),uri2])
                
           
        else:
            csvwriter.writerow([ide,palabra,'','','','','','','','','','','',''])
        j=j+1
        term_val_es=''
        term_val_de=''
        term_val_en=''
        term_val_nl='' 
        listaSinonimo_es=''
        listaSinonimo_de=''
        listaSinonimo_en=''
        listaSinonimo_nl='' 
        definicionCompleta_es=''
        definicionCompleta_de=''
        definicionCompleta_en=''
        definicionCompleta_nl=''

        
            

    print('___________PROCESS FIHISHED_____________')


   
    




parser=argparse.ArgumentParser()
parser.add_argument("--sourceFile", help="Name of the source csv file (term list)") #nombre de archivo a leer
parser.add_argument("--sourceTerm", help="Source term to search") #nombre de archivo a leer
parser.add_argument("--type", help="Type of file read of termino_id.csv: 'w' to create file or 'a' to read and add new terms") #tipo de archivo lectura o escritura (w/a)
parser.add_argument("--termId", help="Name of the termino_id file, to save terms and ids") #nombre de archivo termino-id
parser.add_argument("--targetFile", help="Name of the target file")
parser.add_argument("--euroSource", help="Name of the eurovoc source file without extension")
parser.add_argument("lang", help="Source language")
parser.add_argument("apiName", help="Name of the api: 'iate' or 'eurovoc'") 
args=parser.parse_args()

nameapi=args.apiName




if(nameapi=='iate'):
    listTerm=args.sourceFile
    termino=args.sourceTerm
    typeFile=args.type
    termId=args.termId
    idioma=args.lang
    csvFILE=args.targetFile
    fileEurovoc=args.euroSource

    #print(typeFile, termino)
    if(typeFile=='new'):
        tipo='w'
        lista=term_id_file(listTerm, termino, termId, tipo)
        #print(lista)
        archivos_eurovoc(lista, fileEurovoc,idioma)
        jsonlist=haceJson(lista, idioma)
        corregirJson()
        parserExcel(lista, jsonlist,  csvFILE,tipo,idioma)
    else:
        tipo='a'
        lista=term_id_file(listTerm, termino, termId, tipo)
        #print(lista)
        archivos_eurovoc(lista, fileEurovoc,idioma)
        jsonlist=haceJson(lista, idioma)
        corregirJson()
        parserExcel(lista, jsonlist, csvFILE,tipo,idioma)


####
#karenvazquez$ python3 iate.py --sourceFile 10term --type new --termId terminosId_k --targetFile salida_k --euroSource out_eurovoc en iate
