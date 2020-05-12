import json #libreria para utulizar json en python
import globales 
import os 

def jsonFile(ide, scheme, rels, note, context, term, lang_in):  
    newFile=''
    data={}
    
    data={
        '@context':"http://lynx-project.eu/doc/jsonld/skosterm.json",
        '@type':'skos:Concept',
        '@id': ide,
        'inScheme': scheme.replace(' ',''),
        'source':'',
        'source':'',
        'closeMatch':'',
        'exactMatch':'',
        'exactMatch':'',
        'prefLabel':'' ,
        'altLabel':'' ,
        'definition':'' ,
        'note':'' ,
        'example': '',
        'topConceptOf': 'http://lynx-project.eu/kos/'+scheme.replace(' ','')}


    data['prefLabel']=[]
    data['altLabel']=[]
    data['definition']=[]
    data['prefLabel'].append({'@language':lang_in, '@value':term.strip(' ')})
    globales.prefLabel_full.append(term.strip(' ')+'-'+lang_in)
    globales.targets_pref.append(lang_in.strip(' '))

    if(rels==1):
        data['broader']=[]
        data['narrower']=[]
        data['related']=[]

    return(data)

# relation folders
def createRelationFolders(targets, folder, name_file):
    for tar in targets:
        if(tar in folder):
            pass
        else:
            os.mkdir(tar)

        folders=os.listdir(tar)
        relations=['broader', 'narrower', 'related']
        for i in relations:
            if(i not in folders):
                os.makedirs(name_file+tar+"/"+i)


def editFileSchema(scheme):
    file_schema={
    "@context": "http://lynx-project.eu/doc/jsonld/skosterm.json",
    "@id": "labourlaw",
    "conceptScheme": "http://lynx-project.eu/kos/labourlaw/",
    "hasTopConcept": [

    ],
    "label": "labour law",
    "creator": "UPM",
    "date": "March 10",
    "description": "Terminological data about Labour Law in Europe."
    }
    
    
    return(file_schema)




def fix(outFile, find_iate, find_euro, find_lexi, find_wiki, note, context, termin):
    if(len(find_lexi)==0 and len(find_euro)==0 and len(find_iate)==0 and len(find_wiki)==0):
        #outFile['prefLabel'].append({'@language':lang_in, '@value':termin.strip(' ')})
        #prefLabel_full.append(termin.strip(' ')+'-'+lang_in)
        #targets_pref.append(lang_in.strip(' '))
        
        if(len(closeMatch)>0):
            outFile['closeMatch']=closeMatch[0]
        if(context):
            no_find.writerow([termin.strip(' '), 'con contexto'])
        else:
            no_find.writerow([termin.strip(' '), 'sin contexto'])


    if(len(note)):
        outFile['note']=note

    if(context):
        outFile['example']=context
    if(len(outFile['prefLabel'])==0):
        del outFile['prefLabel']
    if(len(outFile['altLabel'])==0):
        del outFile['altLabel']
    if(len(outFile['definition'])==0):
        del outFile['definition']
    if(len(outFile['broader'])==0):
        del outFile['broader']
    if(len(outFile['narrower'])==0):
        del outFile['narrower']
    if(len(outFile['related'])==0):
        del outFile['related']

    if(len(find_euro) and len(find_wiki)):
        outFile['exactMatch']=find_euro[0]
        outFile['exactMatch']='https://www.wikidata.org/wiki/'+find_wiki[0]
        pass
    elif(len(find_euro) and len(find_wiki)==0):
        outFile['exactMatch']=find_euro[0]
        pass
    elif(len(find_wiki) and len(find_euro)==0):
        outFile['exactMatch']='https://www.wikidata.org/wiki/'+find_wiki[0]
        pass
    elif(len(find_wiki)==0 and len(find_euro)==0):
        del outFile['exactMatch']

    if(len(find_iate) and len(find_lexi)):
        outFile['source']="https://iate.europa.eu/entry/result/"+str(find_iate[0])
        outFile['source']="https://dictapi.lexicala.com/senses/"+find_lexi[0]
        pass
    elif(len(find_iate) and len(find_lexi)==0):
        outFile['source']="https://iate.europa.eu/entry/result/"+str(find_iate[0])
        pass
    elif(len(find_lexi) and len(find_iate)==0):
        outFile['source']="https://dictapi.lexicala.com/senses/"+find_lexi[0]
        pass
    elif(len(find_lexi)==0 and len(find_iate)==0):
        del outFile['source']
    
    if(len(note)==0):
        del(outFile['note'])
    if(context==None):
        del(outFile['example'])

    del(outFile['closeMatch'])


    return(outFile)