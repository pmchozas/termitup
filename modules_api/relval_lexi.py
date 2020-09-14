import json
import requests
import time
import check_term
import eurovocCode
import spacy
from nltk.corpus import stopwords
from time import time
import trans_id
import re
from unicodedata import normalize
import jsonFile
import wsidCode
import nltk
from nltk import SnowballStemmer
from nltk.parse import CoreNLPParser
from nltk.stem import PorterStemmer
stemmerporter = PorterStemmer()
stemmersnow=SnowballStemmer('spanish')
import conts_log

nlp = spacy.load('es_core_news_sm')
# =========================================
# 
# =========================================
def get_conceptNet_synonyms(term, lang):
    # Given a term, get the synonyms from ConcetpNet of the same language
    # Note that all words are in lower case on ConceptNet, unlike Wikidata
    # Start and end edges should be taken into account
    synonyms = list()
    query_url_pattern = "http://api.conceptnet.io/query?EDGEDIRECTION=/c/LANG/TERM&rel=/r/Synonym&limit=1000"
    
    edge_directions = {"start":"end", "end":"start"}
    for direction in edge_directions.keys():
        query_url = query_url_pattern.replace("EDGEDIRECTION", direction).replace("LANG", lang).replace("TERM", term)
        obj = requests.get(query_url).json()
        for edge_index in range(len(obj['edges'])):
            syn_lang = obj['edges'][edge_index][edge_directions[direction]]["language"]
            if syn_lang == lang:
                synonyms.append(obj['edges'][edge_index][edge_directions[direction]]["label"])
    together=lexicala(lang, term,list(set(synonyms)))
                    
    return (together)

def lexicala_term(lang, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+lang+"&text="+term+"", auth=('upm2', 'XvrPwS4y'))
    answerSearch=search.json()
    return(answerSearch)

def lexicala_sense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('upm2', 'XvrPwS4y'))
    answerSense=sense.json()
    return(answerSense)

def altLabel_lexicala(maximo, target):
    traductions=[]
    jsonTrad=lexicala_sense(maximo)
    if('synonyms' in jsonTrad.keys()):
        for i in range(len(jsonTrad['synonyms'])):
            syn=jsonTrad['synonyms'][i]
            traductions.append(syn)

    
    return(traductions)

def definition_lexicala(answer,lang):
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
            else:
                pref_lex=altLabel_lexicala(sense1[i]['id'], lang)
                if(len(pref_lex)):
                    for j in pref_lex:
                        listaDefinition.append(j[0])
                        listaId.append(sense1[i]['id'])

            

    return(listaDefinition, listaId)

def lexicala(lang, term, cn):
    synm=[]
    try:
        answer=lexicala_term(lang, term)
        if('n_results' in answer):
            results=answer['n_results']
            if(results>0):
                list_senses=answer['results'][0]['senses']
                for s in range(len(list_senses)):
                    sense=list_senses[s]['id']
                    alt_lex=altLabel_lexicala(sense, lang)
                    if(len(alt_lex)):
                        join_alt=', '.join(alt_lex)
                        if(join_alt not in cn):
                            cn.append(join_alt)
                        synm.append(join_alt)
           
    except json.decoder.JSONDecodeError:
        pass

    return(cn)


def inducer(T, A, S):
    # Gets T, the list of preferred labels and A, the list of alternative labels
    # Using synonyms of T, S, it induces the semantic relationship that exists between T and A. 
    # S is a dictionary of word as term and dictionary {lang: synonyms} as values.
    semantic_relationship = None
    pos_tagger = CoreNLPParser('http://localhost:9003', tagtype='pos')
                        
    if len(A) and len(T):
        invalid = False


        if " ".join(A).lower() == " ".join(T).lower():
            # They are identical. No semantic relationship should be induced. 
            pass
        
        elif len(T) == len(A) :
            case_check = list()
            stop=stopwords.words('spanish')
            list_pos=list()
            for t in T:
                if t not in stop:
                    stem_t=stemmersnow.stem(t)
                    stem_a=[stemmersnow.stem(token) for token in A]
                        
                    if t in A :
                        case_check.append(True)
                    elif(stem_t in stem_a):
                        tag_t=pos_tagger.tag(t.split(' '))
                        tag_a=[pos_tagger.tag(a.split(' ')) for a in A]
                            
                        list_pos.append(tag_t[0][1])
                        list_pos.append(tag_a[0][0][1])
                        if(('NOUN' in list_pos and 'VERB' in list_pos) or('AUX' in list_pos and 'VERB' in list_pos)):
                                semantic_relationship = "related"
                        elif(list_pos.count('NOUN') >=2  ):
                            #print(T,A,'noun+noun',list_pos)
                            semantic_relationship = "related"
                        elif('NOUN' in list_pos and 'ADJ' in list_pos):
                            #print(T,A,'noun+adj', list_pos)
                            semantic_relationship='related'
                        elif(list_pos.count('ADJ') >=2  ):
                            #print(T,A,'adj+adj',list_pos)
                            semantic_relationship = "related"
                        elif('VERB' in list_pos and 'ADJ' in list_pos):
                            #print(T,A,'noun+adj', list_pos)
                            semantic_relationship='related'


                        else:
                            # check if the language exists
                            if len(S[t]):
                                
                                if True in [True for s_t in S[t] if s_t in A]:
                                    case_check.append(True)
                                else:
                                    case_check.append(False)
                            else:
                                invalid = True
                
                if semantic_relationship != None:
                    semantic_relationship=semantic_relationship
                elif case_check.count(True) < len(T) and case_check.count(True)>0:
                    semantic_relationship = "related"
                elif not invalid and False not in case_check: 
                    semantic_relationship = "synonymy"
                elif(case_check.count(False) >case_check.count(True) ):
                    semantic_relationship = None


        elif len(T) < len(A):
            case_check = list()
            for t in T:
                if t in A:
                    case_check.append(True)
                else:
                    # check if the language exists
                    if len(S[t]):
                        if True in [True for s_t in S[t] if s_t in A]:
                            case_check.append(True)
                        else:
                            case_check.append(False)
                    else:
                        case_check.append(False)

            # print(case_check)
            if False not in case_check:
                semantic_relationship = "narrower"

        elif len(T) > len(A):
            case_check = True
            for a in A:
                # Find all the synonyms of the existing terms
                syns = list()
                for term_syn in S.values():
                    if len(term_syn):
                        syns = syns + term_syn
                    else:
                        pass

                syns = list(set(syns))
                #print('sysn set', syns)

                if len(syns):
                    #if([True for s_t in syns if a in s_t])
                    if not (a in T ):
                        case_check = False
                    #if not (a in T or True in [True for s_t in syns if a in s_t]):
                    #    case_check = False
                else:
                    invalid = True
            #print(case_check, invalid)
            #if case_check is True and invalid is False:
            #   pass
            if not invalid and case_check:
                semantic_relationship = "broader"

        else:
            pass
    #print(semantic_relationship)
    return semantic_relationship
# =========================================
# main
# =========================================
# Read the configuration file
def main(outFile, file_schema, targets, clean, lang_in, context):
    conts_log.information('-----RelVal----','')
    #clean=['artículo', 'empresa', 'trabajador', 'contrato', 'periodo', 'derecho', 'empresario', 'duración', 'convenio', 'ámbito', 'ley', 'caso', 'laboral', 'aplicación', 'plazo', 'colectivo', 'comisión', 'autoridad', 'disposición', 'número', 'apartado', 'procedimiento', 'formación', 'perjuicio', 'seguridad', 'centro', 'decisión', 'convenio colectivo', 'representación', 'suspensión', 'máximo', 'fecha', 'despido', 'salario', 'profesional', 'actividad', 'autoridad laboral', 'comité', 'superior', 'carácter', 'extinción', 'previsto', 'puesto', 'negociación', 'adopción', 'ciento', 'social', 'legal', 'persona', 'párrafo', 'ejercicio', 'inferior', 'personal', 'dirección', 'relación', 'comunicación', 'servicio', 'realización', 'parcial', 'disposición adicional', 'oficina', 'prestación', 'mínimo', 'comité de empresa', 'objeto', 'fines de adopción', 'constitución', 'pública', 'correspondiente', 'materia', 'situación', 'jurisdicción', 'texto', 'desarrollo', 'indemnización', 'resolución', 'consulta', 'información', 'colectiva', 'garantía', 'fondo', 'oficina pública', 'inicio', 'disfrute', 'copia', 'representativa', 'mesa', 'reducción', 'sección', 'empresarial', 'trabajadora', 'cumplimiento', 'conformidad', 'texto refundido', 'electoral', 'establecer', 'grupo', 'igualdad', 'protección', 'riesgo', 'condición', 'traslado', 'promoción', 'orden', 'máxima', 'oficina pública dependiente', 'proceso', 'sistema', 'régimen', 'seguridad social', 'cómputo', 'negociación colectiva', 'pacto', 'real', 'negociar', 'previo', 'mayoría', 'incapacidad', 'excedencia', 'título', 'disposición transitoria', 'edad', 'comisión representativa', 'registro', 'persona trabajadora', 'público', 'judicial', 'determinada', 'estatal', 'descanso', 'económica', 'falta', 'comunicar', 'razón', 'cargo', 'fondo de garantía', 'movilidad', 'nivel', 'consideración', 'salarial', 'periodo de suspensión', 'capacidad', 'modificación', 'progenitor', 'nacional', 'jubilación', 'exceder', 'cualquiera', 'comunidad', 'tramitación', 'pago', 'existencia', 'igualmente', 'suspensión del contrato', 'acta', 'sector', 'intervención', 'compensación', 'comisión negociadora', 'causa', 'preaviso', 'contenido', 'formación profesional', 'individual', 'cuantía', 'antigüedad', 'duración determinada', 'madre', 'abono', 'retribución', 'salud', 'vigor', 'lactancia', 'función', 'miembros del comité', 'normativa', 'autónoma', 'previa', 'temporal', 'base', 'permiso', 'órgano', 'modalidad', 'regulación', 'asistencia', 'mínima', 'delegados de personal', 'finalización', 'acción', 'vigencia', 'normal', 'efectiva', 'concurren', 'gobierno', 'organización', 'ejecución', 'aprendizaje', 'arbitral', 'antelación', 'disminución', 'discapacidad', 'inmediatamente', 'apertura', 'ordinaria', 'ausencia', 'prevención', 'obligado', 'efectivo', 'votación', 'cedente', 'funcional', 'reclamar', 'comunidad autónoma', 'deber', 'naturaleza', 'duración máxima', 'representante', 'solución', 'salario mínimo', 'lista', 'relevo', 'ley orgánica', 'obligación', 'celebrado', 'efecto', 'favorecer', 'virtud', 'ámbito estatal', 'adaptación', 'fuerza', 'capítulo', 'cabo', 'jurisdicción social', 'consecuencia', 'posterioridad', 'producción', 'decisión extintiva', 'proporcional', 'contratación', 'obra', 'facilitar', 'importe', 'completo', 'grupo profesional', 'proporción', 'informar', 'violencia', 'clasificación', 'distribución', 'embarazo', 'límite', 'afectado', 'presente', 'extinción del contrato', 'anterioridad', 'conflicto', 'reunión', 'totalidad', 'menor', 'mesa electoral', 'suficiente', 'cambio', 'despido colectivo', 'libertad', 'resultado', 'comités de empresa', 'letra', 'entrada', 'nocturno', 'equivalente', 'real decreto', 'celebrar', 'conocimiento', 'incumplimiento', 'conciliación', 'grado', 'legislación', 'aplicable', 'entidad', 'disfrutar', 'copia básica', 'ministerio', 'permanencia', 'laudo', 'solicitud', 'persistente', 'preferencia', 'desempleo', 'voto', 'prioridad', 'reclamación', 'administrativa', 'acordar', 'alta', 'sectorial', 'garantía salarial', 'reserva', 'finalice', 'conjunto', 'defecto', 'president']
    # ================
    if('skos-xl:prefLabel' in outFile.keys()):
        pref=outFile['skos-xl:prefLabel']
        #pref=['artículo', 'empresa', 'trabajador', 'contrato', 'periodo', 'derecho', 'empresario', 'duración', 'convenio', 'ámbito', 'ley', 'caso', 'laboral', 'aplicación', 'plazo', 'colectivo', 'comisión', 'autoridad', 'disposición', 'número', 'apartado', 'procedimiento', 'formación', 'perjuicio', 'seguridad', 'centro', 'decisión', 'convenio colectivo', 'representación', 'suspensión', 'máximo', 'fecha', 'despido', 'salario', 'profesional', 'actividad', 'autoridad laboral', 'comité', 'superior', 'carácter', 'extinción', 'previsto', 'puesto', 'negociación', 'adopción', 'ciento', 'social', 'legal', 'persona', 'párrafo', 'ejercicio', 'inferior', 'personal', 'dirección', 'relación', 'comunicación', 'servicio', 'realización', 'parcial', 'disposición adicional', 'oficina', 'prestación', 'mínimo', 'comité de empresa', 'objeto', 'fines de adopción', 'constitución', 'pública', 'correspondiente', 'materia', 'situación', 'jurisdicción', 'texto', 'desarrollo', 'indemnización', 'resolución', 'consulta', 'información', 'colectiva', 'garantía', 'fondo', 'oficina pública', 'inicio', 'disfrute', 'copia', 'representativa', 'mesa', 'reducción', 'sección', 'empresarial', 'trabajadora', 'cumplimiento', 'conformidad', 'texto refundido', 'electoral', 'establecer', 'grupo', 'igualdad', 'protección', 'riesgo', 'condición', 'traslado', 'promoción', 'orden', 'máxima', 'oficina pública dependiente', 'proceso', 'sistema', 'régimen', 'seguridad social', 'cómputo', 'negociación colectiva', 'pacto', 'real', 'negociar', 'previo', 'mayoría', 'incapacidad', 'excedencia', 'título', 'disposición transitoria', 'edad', 'comisión representativa', 'registro', 'persona trabajadora', 'público', 'judicial', 'determinada', 'estatal', 'descanso', 'económica', 'falta', 'comunicar', 'razón', 'cargo', 'fondo de garantía', 'movilidad', 'nivel', 'consideración', 'salarial', 'periodo de suspensión', 'capacidad', 'modificación', 'progenitor', 'nacional', 'jubilación', 'exceder', 'cualquiera', 'comunidad', 'tramitación', 'pago', 'existencia', 'igualmente', 'suspensión del contrato', 'acta', 'sector', 'intervención', 'compensación', 'comisión negociadora', 'causa', 'preaviso', 'contenido', 'formación profesional', 'individual', 'cuantía', 'antigüedad', 'duración determinada', 'madre', 'abono', 'retribución', 'salud', 'vigor', 'lactancia', 'función', 'miembros del comité', 'normativa', 'autónoma', 'previa', 'temporal', 'base', 'permiso', 'órgano', 'modalidad', 'regulación', 'asistencia', 'mínima', 'delegados de personal', 'finalización', 'acción', 'vigencia', 'normal', 'efectiva', 'concurren', 'gobierno', 'organización', 'ejecución', 'aprendizaje', 'arbitral', 'antelación', 'disminución', 'discapacidad', 'inmediatamente', 'apertura', 'ordinaria', 'ausencia', 'prevención', 'obligado', 'efectivo', 'votación', 'cedente', 'funcional', 'reclamar', 'comunidad autónoma', 'deber', 'naturaleza', 'duración máxima', 'representante', 'solución', 'salario mínimo', 'lista', 'relevo', 'ley orgánica', 'obligación', 'celebrado', 'efecto', 'favorecer', 'virtud', 'ámbito estatal', 'adaptación', 'fuerza', 'capítulo', 'cabo', 'jurisdicción social', 'consecuencia', 'posterioridad', 'producción', 'decisión extintiva', 'proporcional', 'contratación', 'obra', 'facilitar', 'importe', 'completo', 'grupo profesional', 'proporción', 'informar', 'violencia', 'clasificación', 'distribución', 'embarazo', 'límite', 'afectado', 'presente', 'extinción del contrato', 'anterioridad', 'conflicto', 'reunión', 'totalidad', 'menor', 'mesa electoral', 'suficiente', 'cambio', 'despido colectivo', 'libertad', 'resultado', 'comités de empresa', 'letra', 'entrada', 'nocturno', 'equivalente', 'real decreto', 'celebrar', 'conocimiento', 'incumplimiento', 'conciliación', 'grado', 'legislación', 'aplicable', 'entidad', 'disfrutar', 'copia básica', 'ministerio', 'permanencia', 'laudo', 'solicitud', 'persistente', 'preferencia', 'desempleo', 'voto', 'prioridad', 'reclamación', 'administrativa', 'acordar', 'alta', 'sectorial', 'garantía salarial', 'reserva', 'finalice', 'conjunto', 'defecto', 'president']
        
        for i in range(len(pref)):
            altLabel_induction = dict()
            lang=pref[i]['literalForm']['@language']
            value1=pref[i]['literalForm']['@value'].lower()
            T=pref[i]['literalForm']['@value'].lower().split()
            if(lang=='es'):
                S = dict()
                for t in T:
                    if t not in S:
                        S[t] = get_conceptNet_synonyms(t, lang)
                # S = get_conceptNet_synonyms(T.replace(" ", "_"), lang)
                #print("T:", T, "lang:", lang, "S:", S)
            
            if len(S):
                if ('skos-xl:altLabel' in outFile.keys()):
                    alt=outFile['skos-xl:altLabel']
                    for j in alt:
                        item1=j
                        value2=j['literalForm']['@value']
                        A=j['literalForm']['@value'].lower().split()
                        language=j['literalForm']['@language']
                        if(lang=='es'):
                            if len(A):
                                # Go for axiom induction    
                                T_A_relationship = inducer(T, A, S)
                                altLabel_induction[" ".join(A)] = T_A_relationship
                                #print('T: ', T, 'A: ',A, 'S: ', S)
                                #print("A:", A, "SR:", T_A_relationship)
                                #print('--------------------------')
                                       
                                if(T_A_relationship!=None):
                                    
                                    if(T_A_relationship!='synonymy'):
                                        conts_log.information('----------','altLabel is relation')
                                        conts_log.information('Relation Validation, Term: '+ value1,'')
                                        conts_log.information('Found relation: '+T_A_relationship+ ' -'+value2,'')
                                 
                                        ##print('T: ', T, 'A: ',A, 'S: ', S)
                                        ##print("A:", A, "SR:", T_A_relationship)
                                        ##print('--------------------------')
                                        ind=alt.index(item1)
                                        del outFile["skos-xl:altLabel"][ind]
                                        check=check_term.checkTerm(lang,value2, '', [language], '')
                                        ide=check[0]
                                        ide_file=ide
                                        termSearch=check[1]
                                        if(termSearch!='1'):
                                            eurovocCode.eurovoc_file(termSearch, ide, T_A_relationship, None, language, 'labourlaw',  outFile["@id"], file_schema, outFile,targets)
                                        full=jsonFile.full_rels(outFile, T_A_relationship)
                                        cadena = re.sub('[/,+.;:/)([]]*', '',  value2)
                                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                                                            normalize( "NFD", cadena), 0, re.I
                                            )
                                        n = normalize( 'NFC', n)
                                        uri=n.replace(' ','-')+'-'+lang
                                        if(uri not in full):
                                            if(T_A_relationship not in outFile.keys()):
                                                outFile[T_A_relationship]=[]
                                                outFile[T_A_relationship].append(uri)
                                            else:
                                                outFile[T_A_relationship].append(uri)
                                        
                if (len(clean)):
                   
                    for j in clean:
                        item1=j
                        value2=j
                        A=j.lower().split()
                        language=lang_in
                        #print(T, 'A: ', A, language)
                        if(language=='es' and lang=='es'):
                            if len(A):
                                # Go for axiom induction 
                                T_A_relationship = inducer(T, A, S)
                                altLabel_induction[" ".join(A)] = T_A_relationship
                                if(T_A_relationship!=None):
                                    if(T_A_relationship!='synonymy'):
                                        #print('T: ', T, 'A: ',A, 'S: ', S)
                                        #print("A:", A, "SR:", T_A_relationship)
                                        #print('--------------------------')
                                        conts_log.information('----------','term in list is relation')
                                        conts_log.information('Relation Validation, Term: '+ value1+'','')
                                        conts_log.information('Found relation: '+T_A_relationship+ ' -'+value2+'','')
                                        
                                        full=jsonFile.full_rels(outFile, T_A_relationship)
                                        
                                        cadena = re.sub('[/,+.;:/)([]]*', '',  value2)
                                        n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                                                            normalize( "NFD", cadena), 0, re.I
                                            )
                                        n = normalize( 'NFC', n)
                                        uri=n.replace(' ','-')+'-'+lang
                                        if(uri not in full):
                                            if(T_A_relationship not in outFile.keys()):
                                                outFile[T_A_relationship]=[]
                                                outFile[T_A_relationship].append(uri)
                                            else:
                                                outFile[T_A_relationship].append(uri)
                                
            else:
                # No synonyms found on ConceptNet"
                altLabel_induction = {}
    #print(outFile)
    return (outFile)
                



