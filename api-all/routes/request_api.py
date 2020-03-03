"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from flask import Flask
import requests
from flask_restplus import Resource, Api, fields, reqparse
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint

import argparse
import csv #libreria para exportar a excel o csv 
import requests #libreria para querys en api
import json #libreria para utulizar json en python
from random import randint #libreria para random
import re
from os import remove
import collections
import json

REQUEST_API = Blueprint('term_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/term/<string:termIn>,<string:languageIn>,<string:context>,<string:targets>', methods=['GET'])
def get_syms(languageIn,termIn,context,targets):
    listaDefinition=[]
    listaId=[]
    pesos=[]
    listaSinonimos=[]
    access = requests.get('https://dictapi.lexicala.com/search?', params= {'source': 'global', 'language':languageIn, 'text':termIn}, auth=('upm2','XvrPwS4y'))
    answer=access.json()
    results=answer['n_results']
    if(results>0):
        #definitions=definitionGet(answer)
        sense0=answer['results'][0]
        if('senses' in sense0.keys()):
            sense1=sense0['senses']
            for i in range(len(sense1)):
                if('definition' in sense1[i].keys()):
                    id_definitions=sense1[i]['id']
                    definitions=sense1[i]['definition']
                    listaDefinition.append(definitions.replace(',', ''))
                    listaId.append(id_definitions)





        start=context.index(termIn)
        longTerm=len(termIn)
        end=context.index(termIn)+longTerm
        listdef=listaDefinition
        listIde=listaId
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




                #def traductionGet(maximo, targets):
        targets=targets.split(' ')

        textList=[]
        trad = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('upm2', 'XvrPwS4y'))
        jsonTrad=trad.json()
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
        #print(textList)
            #return(textList)

            #def justSyn(tradMax):
        slp=textList[0].split(',')
        listaSinonimos=[]
        access = requests.get("https://dictapi.lexicala.com/search?source=global&language="+slp[1]+"&text="+slp[0]+"", auth=('upm2', 'XvrPwS4y'))
        answer=access.json()
        results=answer['n_results']
        if(results>0):
            if('synonyms' in answer.keys() ):
                syn=answer['synonyms']
                if(len(syn)>0):
                    for j in range(len(syn)):
                        synonym=syn[j]
                        listaSinonimos.append(synonym)
        print(listaSinonimos)
        joinSyns=','.join(listaSinonimos)
        #print(joinSyns)
        #return(joinSyns)

        #getsyn=synonymsGet(maximo)
        access = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('upm2', 'XvrPwS4y'))
        answer=access.json()
        #print(termIn, sense)
        if('synonyms' in answer.keys() ):
            syn=answer['synonyms']
            if(len(syn)>0):
                for j in range(len(syn)):
                    synonym=syn[j]
                    listaSinonimos.append(synonym)
        #print(listaSinonimos)
        joinSyns=','.join(listaSinonimos)
        #print(termIn, defiMax, joinSyns)
        #return(joinSyns)
        jointrad=','.join(textList)
        todo='SENTIDO MAXIMO: '+defiMax+', SINONIMOS: '+joinSyns+' TARGETS: '+jointrad

        

        x={}
        x={'term': termIn,'disambiguation': defiMax, 'language': languageIn}
        x['synonyms']=[]
        x['Targets']=[]
        for j in listaSinonimos:
            x['synonyms'].append({'value': j, 'lenguaje': languageIn})
        for k in textList:
            spl=k.split(',')
            x['Targets'].append({'language':slp[1],'value': slp[0]})
        return jsonify(x),200  
            

@REQUEST_API.route('/term/<string:termino>,<string:idioma>,<string:targets>', methods=['GET'])
def get_all(idioma,termino,targets):
    targets=targets.split(' ')
    relation=['broader', 'narrower', 'related']
    context=[['pactada','1. La duración de la jornada de trabajo será la pactada en los convenios colectivos o contratos de trabajo.','48','55'],
    ['duración','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','3','11'],
    ['descanso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','72','80'],
    ['preaviso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','156','164'],
    ['acuerdo','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','53','60'],
    ['semanales','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','77','86'],
    ['límite','cuál es el límite de la jornada laboral','11','17'],
    ['trabajador','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','123','133'],
    ['convenio','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','12','20'],
    ['manera','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','252','258'],
    ['jornada','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','172','179'],
    ['hora','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','198','202'],
    ['prestación','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','209','219'],
    ['defecto','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','40','47'],
    ['trabajo','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','223','230'],
    ['ley','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','114','117'],
    ['empresa','2. Mediante convenio colectivo o en su defecto por acuerdo entre la empresa y los representantes de los trabajadores se podrá establecer la distribución irregular de la jornada a lo largo del año. En defecto de pacto la empresa podrá distribuir de manera irregular a lo largo del año el diez por ciento de la jornada de trabajo.','70','77'],
    ['caso','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','43','47'],
    ['promedio','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','110','118'],
    ['días','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','181','185'],
    ['cómputo','La duración máxima de la jornada ordinaria de trabajo será de cuarenta horas semanales de trabajo efectivo de promedio en cómputo anual.','122','129'],
    ['Sección','Sección 5. Tiempo de trabajo','0','7'],
    ['semanal','Dicha distribución deberá respetar en todo caso los periodos mínimos de descanso diario y semanal previstos en la ley y el trabajador deberá conocer con un preaviso mínimo de cinco días el día y la hora de la prestación de trabajo resultante de aquella.','90','97'],
    ['conjunto','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','142','150'],
    ['cuantía','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','84','91'],
    ['Salario','Artículo 27. Salario mínimo interprofesional.','13','20'],
    ['productividad','b) La productividad media nacional alcanzada.','6','19'],
    ['participación','c) El incremento de la participación del trabajo en la renta nacional.','23','36'],
    ['renta','c) El incremento de la participación del trabajo en la renta nacional.','55','60'],
    ['salario','2. El salario mínimo interprofesional en su cuantía es inembargable.','6','13'],
    ['incremento','c) El incremento de la participación del trabajo en la renta nacional.','6','16'],
    ['coyuntura','d) La coyuntura económica general.','6','15'],
    ['Gobierno','1. El Gobierno fijará previa consulta con las organizaciones sindicales y asociaciones empresariales más representativas anualmente el salario mínimo interprofesional teniendo en cuenta:','6','14'],
    ['estructura','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','65','75'],
    ['trabajo','c) El incremento de la participación del trabajo en la renta nacional.','41','48'],
    ['caso','Igualmente se fijará una revisión semestral para el caso de que no se cumplan las previsiones sobre el índice de precios citado.','52','56'],
    ['revisión','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','3','11'],
    ['cómputo','La revisión del salario mínimo interprofesional no afectará a la estructura ni a la cuantía de los salarios profesionales cuando estos en su conjunto y cómputo anual fueran superiores a aquel.','153','160'],
    ['Sección','Sección 4. Salarios y garantías salariales','0','7'],
    ['cuantía','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','322','329'],
    ['duración','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','159','167'],
    ['descanso','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','133','141'],
    ['modalidad','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','147','156'],
    ['contrato','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','174','182'],
    ['acuerdo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','166','173'],
    ['superior','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','51','59'],
    ['pago','Qué requisitos de pago de horas extras existen','18','22'],
    ['carácter','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','107','115'],
    ['carácter','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','107','115'],
    ['apartado','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','102','110'],
    ['apartado','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','102','110'],
    ['valor','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','384','389'],
    ['convenio','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','209','217'],
    ['actividad','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','148','157'],
    ['jornada','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','198','205'],
    ['hora','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','31','35'],
    ['colocación','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','221','231'],
    ['pacto','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','491','496'],
    ['Gobierno','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','3','11'],
    ['ramas','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','139','144'],
    ['meses','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','163','168'],
    ['trabajo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','71','78'],
    ['anual','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','217','222'],
    ['caso','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','357','361'],
    ['cómputo','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','209','216'],
    ['realizadas','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','553','563'],
    ['párrafo','A los efectos de lo dispuesto en el párrafo anterior no se computarán las horas extraordinarias que hayan sido compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','36','43'],
    ['consideración','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','14','27'],
    ['Sección','Sección 5. Tiempo de trabajo','0','7'],
    ['artículo','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','181','189'],
    ['situación','El Gobierno podrá suprimir o reducir el n√∫mero máximo de horas extraordinarias por tiempo determinado con carácter general o para ciertas ramas de actividad o ámbitos territoriales para incrementar las oportunidades de colocación de los trabajadores en situación de desempleo.','255','264'],
    ['ausencia','1. Tendrán la consideración de horas extraordinarias aquellas horas de trabajo que se realicen sobre la duración máxima de la jornada ordinaria de trabajo fijada de acuerdo con el artículo anterior. Mediante convenio colectivo o en su defecto contrato individual se optará entre abonar las horas extraordinarias en la cuantía que se fije que en ning√∫n caso podrá ser inferior al valor de la hora ordinaria o compensarlas por tiempos equivalentes de descanso retribuido. En ausencia de pacto al respecto se entenderá que las horas extraordinarias realizadas deberán ser compensadas mediante descanso dentro de los cuatro meses siguientes a su realización.','479','487'],
    ['proporción','2. El n√∫mero de horas extraordinarias no podrá ser superior a ochenta al año salvo lo previsto en el apartado 3. Para los trabajadores que por la modalidad o duración de su contrato realizasen una jornada en cómputo anual inferior a la jornada general en la empresa el n√∫mero máximo anual de horas extraordinarias se reducirá en la misma proporción que exista entre tales jornadas.','340','350'],
    ['contrato','Sección 3. Elementos y eficacia del contrato de trabajo','37','45'],
    ['admisión','Se prohíbe la admisión al trabajo a los menores de dieciséis años.','14','22'],
    ['eficacia','Sección 3. Elementos y eficacia del contrato de trabajo','24','32'],
    ['Trabajo','Artículo 6. Trabajo de los menores.','12','19'],
    ['trabajo','Se prohíbe la admisión al trabajo a los menores de dieciséis años.','26','33'],
    ['edad','Cuál es la edad mínima para trabajar','11','15'],
    ['Sección','Sección 3. Elementos y eficacia del contrato de trabajo','0','7'],
    ['cuyos','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','97','102'],
    ['lactancia','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','152','161'],
    ['ámbito','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','139','145'],
    ['sector','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','146','152'],
    ['posesión','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','170','178'],
    ['duración','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','134','142'],
    ['periodo','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','99','106'],
    ['contrato','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','21','29'],
    ['incapacidad','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','19','30'],
    ['superior','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','79','87'],
    ['mes','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','93','96'],
    ['título','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','182','188'],
    ['práctica','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','59','67'],
    ['efecto','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','162','168'],
    ['efecto','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','162','168'],
    ['máster','A los efectos de este artículo los títulos de grado máster y en su caso doctorado correspondientes a los estudios universitarios no se considerarán la misma titulación salvo que al ser contratado por primera vez mediante un contrato en prácticas el trabajador estuviera ya en posesión del título superior de que se trate.','54','60'],
    ['trabajador','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','33','43'],
    ['convenio','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','51','59'],
    ['salario','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','275','282'],
    ['antig√ºedad','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','172','182'],
    ['vigencia','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','231','239'],
    ['equivalente','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','346','357'],
    ['sesenta','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','152','159'],
    ['grado','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','192','197'],
    ['nivel','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','243','248'],
    ['virtud','c) Ning√∫n trabajador podrá estar contratado en prácticas en la misma o distinta empresa por tiempo superior a dos años en virtud de la misma titulación o certificado de profesionalidad.','122','128'],
    ['retribución','e) La retribución del trabajador será la fijada en convenio colectivo para los trabajadores en prácticas sin que en su defecto pueda ser inferior al sesenta o al setenta y cinco por ciento durante el primero o el segundo año de vigencia del contrato respectivamente del salario fijado en convenio para un trabajador que desempeñe el mismo o equivalente puesto de trabajo.','6','17'],
    ['término','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','9','16'],
    ['meses','d) Salvo lo dispuesto en convenio colectivo el periodo de prueba no podrá ser superior a un mes para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado medio o de certificado de profesionalidad de nivel 1 o 2 ni a dos meses para los contratos en prácticas celebrados con trabajadores que estén en posesión de título de grado superior o de certificado de profesionalidad de nivel 3.','265','270'],
    ['trabajo','Tampoco se podrá estar contratado en prácticas en la misma empresa para el mismo puesto de trabajo por tiempo superior a dos años aunque se trate de distinta titulación o distinto certificado de profesionalidad.','91','98'],
    ['paternidad','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','164','174'],
    ['empresa','f) Si al término del contrato el trabajador continuase en la empresa no podrá concertarse un nuevo periodo de prueba computándose la duración de las prácticas a efecto de antig√ºedad en la empresa.','61','68'],
    ['formación','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','115','124'],
    ['fines','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','102','107'],
    ['cómputo','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','192','199'],
    ['obtención','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','43','52'],
    ['Sección','Sección 4. Modalidades del contrato de trabajo','0','7'],
    ['objeto','a) El puesto de trabajo deberá permitir la obtención de la práctica profesional adecuada al nivel de estudios o de formación cursados. Mediante convenio colectivo de ámbito sectorial estatal o en su defecto en los convenios colectivos sectoriales de ámbito inferior se podrán determinar los puestos de trabajo o grupos profesionales objeto de este contrato.','336','342'],
    ['titulación','Tampoco se podrá estar contratado en prácticas en la misma empresa para el mismo puesto de trabajo por tiempo superior a dos años aunque se trate de distinta titulación o distinto certificado de profesionalidad.','159','169'],
    ['exceder','b) La duración del contrato no podrá ser inferior a seis meses ni exceder de dos años dentro de cuyos límites los convenios colectivos de ámbito sectorial estatal o en su defecto los convenios colectivos sectoriales de ámbito inferior podrán determinar la duración del contrato atendiendo a las características del sector y de las prácticas a realizar.','66','73'],
    ['riesgo','Las situaciones de incapacidad temporal riesgo durante el embarazo maternidad adopción guarda con fines de adopción acogimiento riesgo durante la lactancia y paternidad interrumpirán el cómputo de la duración del contrato.','41','47'],
    ['establecidos','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','401','413'],
    ['empleo','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','280','286'],
    ['marco','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','229','234'],
    ['programas','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','515','524'],
    ['sistema','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','239','246'],
    ['sistema','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','239','246'],
    ['duración','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','338','346'],
    ['contrato','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','3','11'],
    ['texto','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','575','580'],
    ['límite','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','318','324'],
    ['alternancia','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','131','142'],
    ['actividad','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','146','155'],
    ['letras','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','421','427'],
    ['Ley','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','597','600'],
    ['régimen','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','120','127'],
    ['cualificación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','68','81'],
    ['edad','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','328','332'],
    ['empresa','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','182','189'],
    ['aplicación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','465','475'],
    ['formación','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','20','29'],
    ['Sección','Sección 4. Modalidades del contrato de trabajo','0','7'],
    ['objeto','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','58','64'],
    ['artículo','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','440','448'],
    ['aprendizaje','El contrato para la formación y el aprendizaje tendrá por objeto la cualificación profesional de los trabajadores en un régimen de alternancia de actividad laboral retribuida en una empresa con actividad formativa recibida en el marco del sistema de formación profesional para el empleo o del sistema educativo. 1. El límite de edad y de duración para los contratos para la formación y el aprendizaje establecidos en las letras a) y b) del artículo 11.2 no será de aplicación cuando se suscriban en el marco de los programas p√∫blicos de empleo y formación contemplados en el texto refundido de la Ley de Empleo.','35','46'],
    ['establecidos','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','122','134'],
    ['atención','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','7','15'],
    ['aceptación','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','298','308'],
    ['renuncia','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','65','73'],
    ['duración','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','90','98'],
    ['ordinarias','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','442','452'],
    ['respecto','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','334','342'],
    ['incompatibilidad','2. Necesidades formativas siempre que se acredite la incompatibilidad horaria.','55','71'],
    ['contrato','3. Incompatibilidad con otro contrato a tiempo parcial.','30','38'],
    ['adición','5. Se consideran horas complementarias las realizadas como adición a las horas ordinarias pactadas en el contrato a tiempo parcial conforme a las siguientes reglas:','59','66'],
    ['preaviso','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','102','110'],
    ['recibo','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','320','326'],
    ['pactadas','Estas horas complementarias no se computarán a efectos de los porcentajes de horas complementarias pactadas que se establecen en la letra c).','99','107'],
    ['semanales','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','162','171'],
    ['relevo','Artículo 12. Contrato a tiempo parcial y contrato de relevo','53','59'],
    ['efecto','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','54','60'],
    ['efecto','e) El pacto de horas complementarias podrá quedar sin efecto por renuncia del trabajador mediante un preaviso de quince días una vez cumplido un año desde su celebración cuando concurra alguna de las siguientes circunstancias:','54','60'],
    ['trabajador','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','244','254'],
    ['convenio','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','409','417'],
    ['materia','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','91','98'],
    ['empresario','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','193','203'],
    ['condiciones','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','43','54'],
    ['jornada','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','102','109'],
    ['conducta','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','548','556'],
    ['cotización','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','121','131'],
    ['sesenta','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','291','298'],
    ['hora','d) El trabajador deberá conocer el día y la hora de realización de las horas complementarias pactadas con un preaviso mínimo de tres días salvo que el convenio establezca un plazo de preaviso inferior.','44','48'],
    ['letras','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','130','136'],
    ['porcentaje','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','188','198'],
    ['pacto','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','21','26'],
    ['realización','h) La realización de horas complementarias habrá de respetar en todo caso los límites en materia de jornada y descansos establecidos en los artículos 34.3 y 4; 36.1 y 37.1.','6','17'],
    ['carencia','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','168','176'],
    ['incumplimiento','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','160','174'],
    ['retribución','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','244','255'],
    ['bases','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','112','117'],
    ['enunciadas','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','52','62'],
    ['trabajo','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','129','136'],
    ['celebración','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','210','221'],
    ['momento','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','196','203'],
    ['caso','f) El pacto de horas complementarias y las condiciones de realización de las mismas estarán sujetos a las reglas previstas en las letras anteriores. En caso de incumplimiento de tales reglas la negativa del trabajador a la realización de las horas complementarias pese a haber sido pactadas no constituirá conducta laboral sancionable.','152','156'],
    ['cómputo','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','175','182'],
    ['realizadas','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','43','53'],
    ['citado','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','250','256'],
    ['Seguridad','i) Las horas complementarias efectivamente realizadas se retribuirán como ordinarias computándose a efectos de bases de cotización a la Seguridad Social y periodos de carencia y bases reguladoras de las prestaciones. A tal efecto el n√∫mero y retribución de las horas complementarias realizadas se deberá recoger en el recibo individual de salarios y en los documentos de cotización a la Seguridad Social.','137','146'],
    ['posterioridad','a) El empresario solo podrá exigir la realización de horas complementarias cuando así lo hubiera pactado expresamente con el trabajador. El pacto sobre horas complementarias podrá acordarse en el momento de la celebración del contrato a tiempo parcial o con posterioridad al mismo pero constituirá en todo caso un pacto específico respecto al contrato. El pacto se formalizará necesariamente por escrito.','258','271'],
    ['Sección','Sección 4. Modalidades del contrato de trabajo','0','7'],
    ['letra','Estas horas complementarias no se computarán a efectos de los porcentajes de horas complementarias pactadas que se establecen en la letra c).','132','137'],
    ['objeto','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','453','459'],
    ['plazo','d) El trabajador deberá conocer el día y la hora de realización de las horas complementarias pactadas con un preaviso mínimo de tres días salvo que el convenio establezca un plazo de preaviso inferior.','175','180'],
    ['artículo','1. La atención de las responsabilidades familiares enunciadas en el artículo 37.6.','69','77'],
    ['exceder','El n√∫mero de horas complementarias pactadas no podrá exceder del treinta por ciento de las horas ordinarias de trabajo objeto del contrato. Los convenios colectivos podrán establecer otro porcentaje máximo que en ning√∫n caso podrá ser inferior al citado treinta por ciento ni exceder del sesenta por ciento de las horas ordinarias contratadas.','53','60'],
    ['perjuicio','g) Sin perjuicio del pacto de horas complementarias en los contratos a tiempo parcial de duración indefinida con una jornada de trabajo no inferior a diez horas semanales en cómputo anual el empresario podrá en cualquier momento ofrecer al trabajador la realización de horas complementarias de aceptación voluntaria cuyo n√∫mero no podrá superar el quince por ciento ampliables al treinta por ciento por convenio colectivo de las horas ordinarias objeto del contrato. La negativa del trabajador a la realización de estas horas no constituirá conducta laboral sancionable.','7','16'],
    ['nocturno','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','21','29'],
    ['noche','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','64','69'],
    ['Trabajo','Artículo 36. Trabajo nocturno trabajo a turnos y ritmo de trabajo','13','20'],
    ['trabajo','Se considera trabajo nocturno el realizado entre las diez de la noche y las seis de la mañana.','13','20'],
    ['ritmo','Artículo 36. Trabajo nocturno trabajo a turnos y ritmo de trabajo','50','55'],
    ['Sección','Sección 5. Tiempo de trabajo','0','7'],
    ['ampliaciones','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','89','101'],
    ['regla','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','150','155'],
    ['duración','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','266','274'],
    ['periodo','Cuánto es el periodo mínimo de descanso semanal','13','20'],
    ['descanso','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','27','35'],
    ['mañana','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','215','221'],
    ['regímenes','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','146','155'],
    ['fijación','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','134','142'],
    ['régimen','Cuál es el régimen del descanso semanal','11','18'],
    ['trabajo','cuál es el máximo de días de trabajo ininterrumplido','29','36'],
    ['aplicación','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','13','23'],
    ['días','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','104','108'],
    ['derecho','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','25','32'],
    ['Sección','Sección 5. Tiempo de trabajo','0','7'],
    ['artículo','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','63','71'],
    ['semanal','Resultará de aplicación al descanso semanal lo dispuesto en el artículo 34.7 en cuanto a ampliaciones y reducciones así como para la fijación de regímenes de descanso alternativos para actividades concretas.','36','43'],
    ['tarde','Los trabajadores tendrán derecho a un descanso mínimo semanal acumulable por periodos de hasta catorce días de día y medio ininterrumpido que como regla general comprenderá la tarde del sábado o en su caso la mañana del lunes y el día completo del domingo. La duración del descanso semanal de los menores de dieciocho años será como mínimo de dos días ininterrumpidos.','180','185'],
    ['establecidos','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','571','583'],
    ['fecha','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','165','170'],
    ['productividad','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','421','434'],
    ['técnica','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','289','296'],
    ['trabajador','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','39','49'],
    ['residencia','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','231','241'],
    ['salario','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','212','219'],
    ['decisión','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','14','22'],
    ['indemnización','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','180','193'],
    ['existencia','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','255','265'],
    ['empresario','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','53','63'],
    ['organización','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','437','449'],
    ['actividad','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','530','539'],
    ['traslado','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','15','23'],
    ['compensación','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','108','120'],
    ['centro','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','117','123'],
    ['antelación','La decisión de traslado deberá ser notificada por el empresario al trabajador así como a sus representantes legales con una antelación mínima de treinta días a la fecha de su efectividad.','126','136'],
    ['meses','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','260','265'],
    ['trabajo','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','128','135'],
    ['extinción','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','138','147'],
    ['empresa','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','104','111'],
    ['razones','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','269','276'],
    ['caso','Cuáles son los derechos del trabajador en caso de que la empresa decida trasladar su centro de trabajo','42','46'],
    ['producción','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','318','328'],
    ['días','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','204','208'],
    ['derecho','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','57','64'],
    ['Movilidad','Artículo 40. Movilidad geográfica','13','22'],
    ['Sección','Sección 1. Movilidad funcional y geográfica','0','7'],
    ['supuesto','Notificada la decisión de traslado el trabajador tendrá derecho a optar entre el traslado percibiendo una compensación por gastos o la extinción de su contrato percibiendo una indemnización de veinte días de salario por año de servicio prorrateándose por meses los periodos de tiempo inferiores a un año y con un máximo de doce mensualidades. La compensación a que se refiere el primer supuesto comprenderá tanto los gastos propios como los de los familiares a su cargo en los términos que se convengan entre las partes y nunca será inferior a los límites mínimos establecidos en los convenios colectivos.','391','399'],
    ['itinerantes','El traslado de trabajadores que no hayan sido contratados específicamente para prestar sus servicios en empresas con centros de trabajo móviles o itinerantes a un centro de trabajo distinto de la misma empresa que exija cambios de residencia requerirá la existencia de razones económicas técnicas organizativas o de producción que lo justifiquen. Se consideraran tales las que estén relacionadas con la competitividad productividad u organización técnica o del trabajo en la empresa así como las contrataciones referidas a la actividad empresarial.','146','157']]
    
    response=requests.get('https://iate.europa.eu/uac-api/auth/token?', params={'username':'VictorRodriguezDoncel','password':'h4URE7N6fXa56wyK'})
    reponse2=response.json()
    access=reponse2['tokens'][0]['access_token']
    hacejsonList=[]
    hed = {'Authorization': 'Bearer ' +access}
    jsonList=[]
    data = {"query": termino,
    "source": idioma,
    "targets": targets,
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
    jsondump=json.dumps(reponse2)

    defi=''
    term_val=''
    syn=''
    data=json.loads(jsondump)
    result=[]
    end=[]
    if('items' in data.keys()):
        term=data['items']
        for item in range(len(term)):
            ide_iate=data['items'][item]['id']
            leng=data['items'][item]['language']
            for target in targets:
                if(target in leng):
                    language=leng[target]
                    if('term_entries' in language.keys()):
                        term_entries=language['term_entries']
                        if(len(term_entries)>0):
                            term_val=language['term_entries'][0]['term_value']
                            for t in range(len(term_entries)):
                                syn=language['term_entries'][t]['term_value']
                    if('definition' in language.keys()):
                        defi=language['definition']
                        result.append([defi, syn,target])
    for i in result:
        if(i[0]!='' and i[1]!=''):
            definition=i[0]
            syns=i[1]
            end.append(definition+'-'+syns)
        
    for e in end:
        print(e)
    joinEnd=','.join(end)
    #return end

        
    results=[]
    resultsEurovoc=[]
    for rel in relation:
        termino2='"'+termino+'"'
        lenguaje2='"'+idioma+'"'
        resultado=''
        resultadouri=''
        url = ("http://publications.europa.eu/webapi/rdf/sparql")
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        select ?c ?label
        from <http://eurovoc.europa.eu/100141>
        where
        {
        VALUES ?searchTerm { """+termino2+""" }
        VALUES ?searchLang { """+lenguaje2+""" }
        VALUES ?relation {skos:prefLabel}
        ?c a skos:Concept .
        ?c ?relation ?label .
        filter (regex(?label, "(^)"""+termino+"""($)"))
        }
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)

        if (len(results["results"]["bindings"])==0):
            resultadouri='-'
        else:
            for result in results["results"]["bindings"]:
                resultadouri=result["c"]["value"]
                resultadol=result["label"]["value"]
        resultado=''
        url=("http://publications.europa.eu/webapi/rdf/sparql")
        query="""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
            select ?c ?label         
            from <http://eurovoc.europa.eu/100141>        
            where       
            {      
            VALUES ?c {<"""+resultadouri+"""> }
            VALUES ?relation { skos:"""+rel+""" } # skos:broader
            ?c a skos:Concept .
            ?c ?relation ?label .
            }
         
         
        """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                resultado='-'
        else:
            for result in results["results"]["bindings"]:
                resultado=result["label"]["value"]
                
        resultado=''
        lenguaje2='"'+idioma+'"'
        url=("http://publications.europa.eu/webapi/rdf/sparql")
        query="""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
            select ?c ?label 
            from <http://eurovoc.europa.eu/100141> 
            where 
            {
            VALUES ?c { <"""+resultado+"""> }
            VALUES ?searchLang { """+lenguaje2+""" undef } 
            VALUES ?relation { skos:prefLabel  } 
            ?c a skos:Concept . 
            ?c ?relation ?label . 
            filter ( lang(?label)=?searchLang )
            }
            """
        r=requests.get(url, params={'format': 'json', 'query': query})
        results=json.loads(r.text)
        if (len(results["results"]["bindings"])==0):
                resultado='-'
        else:
            for result in results["results"]["bindings"]:
                resultado=result["label"]["value"]
        resultsEurovoc.append('Relación: '+rel+'Respuesta: '+resultado)
                   
        #print(' Relación: ',rel, ' Respuesta: ', resultado)

    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+idioma+"&text="+termino+"", auth=('upm2','XvrPwS4y'))
    answerSearch=search.json()
    if(termino):
        answer=answerSearch
        results=answer['n_results']
        if(results>0):
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
            pesos=[]
            for contexto in context:
                terminoC=contexto[0]
                contex=contexto[1]
                start=contexto[2]
                end=contexto[3]
                if(termino in terminoC):
                    listdef=listaDefinition
                    listIde=listaId
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
            textList=[]
            sense = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('upm2','XvrPwS4y'))
            answerSense=sense.json()
            if('translations' in answerSense.keys()):
                translations=answerSense['translations']
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
            slp=textList[0].split(',')
            listaSinonimos=[]
            search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+slp[1]+"&text="+slp[0]+"", auth=('upm2','XvrPwS4y'))
            answerSearch=search.json()
            results=answer['n_results']
            if(results>0):
                if('synonyms' in answer.keys() ):
                    syn=answer['synonyms']
                    if(len(syn)>0):
                        for j in range(len(syn)):
                            synonym=syn[j]
                            listaSinonimos.append(synonym)
            joinSyns=','.join(listaSinonimos)
            listaSinonimos=[]
            sense = requests.get("https://dictapi.lexicala.com/senses/"+idMax+"", auth=('upm2','XvrPwS4y'))
            answerSense=sense.json()
            if('synonyms' in answerSense.keys() ):
                syn=answerSense['synonyms']
                if(len(syn)>0):
                    for j in range(len(syn)):
                        synonym=syn[j]
                        listaSinonimos.append(synonym)
            joinSyns=','.join(listaSinonimos)
            #print(termino,' Desambiguación: ',defiMax)
            #print('Sinonimos del termino: ',joinSyns)
            #print('Sinonimos lenguajes de salida: ',textList)
            jointlist=','.join(textList)
            joinEuro=','.join(resultsEurovoc)
            todo=joinEnd+','+joinEuro+','+termino+'Desambiguación:'+defiMax+'Sinonimos del termino:'+joinSyns+'Sinonimos lenguajes de salida:'+jointlist
                

            w={}
            w={'Term': termino,'disambiguation': defiMax, 'language': idioma}
            w['synonyms']=[]
            w['Targets']=[]
            w['IATE']=[]
            for j in listaSinonimos:
                w['synonyms'].append({'Value': j, 'language': idioma})
            for k in textList:
                spl=k.split(',')
                w['Targets'].append({'language':slp[1],'Value': slp[0]})
                

            for i in result:
                if(i[0]!='' and i[1]!=''):
                    w['IATE'].append({'PrefLabel': i[1],'definition': i[0], 'language': i[2]})

                        
                        
            #z=json.dumps(w)
            #print(w)
            return jsonify(w),200  















  


