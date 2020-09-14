import json
import requests
import wsidCode
import extrafunctions


def lexicala(lang, term, targets, context,  outFile, wsid, rels):
    try:
        answer=lexicala_term(lang, term)
        if('n_results' in answer):
            results=answer['n_results']
            if(results>0):
                #print('-se encontro lexicala-')
                definitions=definition_lexicala(answer, lang)
                if(context==None):
                    context=term
                    wsid='yes'

                if(wsid=='yes'):
                    maximo=wsidCode.wsidFunction(term,context,  definitions)
                    if(maximo[2]!=200):
                        pass
                    elif(maximo[0]!='' and maximo[2]==200):
                        if(len(outFile['skos-xl:prefLabel'][0]['source'])==0):
                            outFile['skos-xl:prefLabel'][0]['source']="https://dictapi.lexicala.com/senses/"+maximo[1]

                        outFile['source'].append("https://dictapi.lexicala.com/senses/"+maximo[1])

                        tars=extrafunctions.check_prefLabel(outFile, targets, rels)
                        if(len(tars)>0):
                            pref_lex=altLabel_lexicala(maximo[1], targets)
                            if(len(pref_lex)>0):
                                for i in pref_lex:
                                    outFile=extrafunctions.property_add(i[0], i[1], outFile, 'prefLabel', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                            
                        alt_lex=altLabel_lexicala(maximo[1], targets)
                        def_lex=maximo[0]
                        if(len(alt_lex)>0):
                            for i in alt_lex:
                                outFile=extrafunctions.property_add(i[0], i[1], outFile, 'altLabel', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                        if(def_lex!=''):
                            outFile=extrafunctions.property_add(def_lex, lang, outFile, 'definition', rels, "https://dictapi.lexicala.com/senses/"+maximo[1])
                else:
                    pass
    except json.decoder.JSONDecodeError:
        pass
    return(outFile)


def lexicala_term(lang, term):
    search = requests.get("https://dictapi.lexicala.com/search?source=global&language="+lang+"&text="+term+"", auth=('upm2', 'XvrPwS4y'))
    answerSearch=search.json()
    return(answerSearch)

def lexicala_sense(maximo):
    sense = requests.get("https://dictapi.lexicala.com/senses/"+maximo+"", auth=('upm2', 'XvrPwS4y'))
    answerSense=sense.json()
    return(answerSense)

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

def altLabel_lexicala(maximo, targets):
    traductions=[]
    jsonTrad=lexicala_sense(maximo)
    if('translations' in jsonTrad.keys()):
        translations=jsonTrad['translations']
        for j in targets:
            if(j in translations):
                langs=translations[j]
                if('text' in langs):
                    text=langs['text']
                    traductions.append([text,j])
                else:
                    for k in range(len(langs)):
                        text=langs[k]['text']
                        traductions.append([text,j])


    return(traductions)
