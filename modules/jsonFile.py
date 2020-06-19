import json #libreria para utulizar json en python
import os 
import re
from unicodedata import normalize
import logging
#format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
logging.basicConfig(filename='myapp.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

def jsonFile(ide, scheme, rels, note, context, term, lang_in, file_schema, n):  
    newFile=''
    data={}
    
    data={
        '@context':"http://lynx-project.eu/doc/jsonld/skosterm.json",
        '@type':'skos:Concept',
        '@id': ide,
        'inScheme': scheme.replace(' ',''),
        'source':[],
        'closeMatch':[],
        'exactMatch':[],
        'jurisdiction': 'http://dbpedia.org/page/Spain',
        'skos-xl:prefLabel':'' ,
        'skos-xl:altLabel':'' ,
        'definition':'' ,
        'note':'' ,
        'example': '',
        'topConceptOf': 'http://lynx-project.eu/kos/'+scheme.replace(' ','')}
    
    ide_split=ide.split('/')
    file_schema['hasTopConcept'].append(ide_split[-1])

    data['skos-xl:prefLabel']=[]
    data['skos-xl:altLabel']=[]
    data['definition']=[]

    data['skos-xl:prefLabel'].append({'@type':'skos-xl:Label', '@id':n.lower().strip(' ').replace(' ', '-')+'-'+lang_in+'-pref', 'source': '', 'literalForm':{'@language':lang_in, '@value': term.strip(' ')}})

    if(rels==1):
        data['broader']=[]
        data['narrower']=[]
        data['related']=[]

    return(data)

# relation folders
def createRelationFolders(targets, folder):
    for tar in targets:
        if(tar in folder):
            pass
        else:
            os.mkdir(tar)

        folders=os.listdir(tar)
        relations=['broader', 'narrower', 'related']
        for i in relations:
            if(i not in folders):
                os.makedirs(tar+"/"+i)


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

def fix(outFile, note, context, termin):
    if(len(note)):
        outFile['note']=note
    if(context):
        outFile['example']=context
    if(len(outFile['skos-xl:prefLabel'])==0):
        del outFile['skos-xl:prefLabel']
    if(len(outFile['skos-xl:altLabel'])==0):
        del outFile['skos-xl:altLabel']
    if(len(outFile['definition'])==0):
        del outFile['definition']
    if(len(outFile['broader'])==0):
        del outFile['broader']
    if(len(outFile['narrower'])==0):
        del outFile['narrower']
    if(len(outFile['related'])==0):
        del outFile['related']

    if(len(note)==0):
        del(outFile['note'])
    if(context==None):
        del(outFile['example'])

    uri_source=len(outFile['source'])
    uri_close=len(outFile['closeMatch'])
    logging.info('FOUND source: '+str(uri_source))
    logging.info('FOUND closeMatch: '+str(uri_close))

    if(len(outFile['source'])==1):
        sour=outFile['source'][0]
        outFile['source']=sour
    if(len(outFile['closeMatch'])==1):
        sour=outFile['closeMatch'][0]
        outFile['closeMatch']=sour



    if(len(outFile['closeMatch'])==0):
        del(outFile['closeMatch'])
    if(len(outFile['source'])==0):
        del(outFile['source'])
    if(len(outFile['exactMatch'])==0):
        del(outFile['exactMatch'])



    if(outFile['skos-xl:prefLabel'][0]['source']==''):
        del outFile['skos-xl:prefLabel'][0]['source']

    return(outFile)

def full_alt(outFile):
    altLabel_full=[]
    if('skos-xl:altLabel' in outFile.keys()):
        altLabel=outFile['skos-xl:altLabel']
        for a in range(len(altLabel)):
            value=altLabel[a]['literalForm']['@value']
            lang=altLabel[a]['literalForm']['@language']
            altLabel_full.append(value+'-'+lang)

    return(altLabel_full)


def full_pref(outFile):
    prefLabel_full=[]
    targets_pref=[]
    if('skos-xl:prefLabel' in outFile.keys()):
        prefLabel=outFile['skos-xl:prefLabel']
        for p in range(len(prefLabel)):
            value=prefLabel[p]['literalForm']['@value']
            lang=prefLabel[p]['literalForm']['@language']
            targets_pref.append(lang)
            prefLabel_full.append(value+'-'+lang)
    return(targets_pref, prefLabel_full)

def full_def(outFile):
    definition_full=[]
    if('definition' in outFile.keys()):
        definition=outFile['definition']
        #print(definition)
        for d in range(len(definition)):
            value=definition[d]['@value']
            lang=definition[d]['@language']
            definition_full.append(value+'-'+lang)

    return(definition_full)

def full_rels(outFile, relation):
    relation_full=[]
    if(relation in outFile.keys()):
        relation=outFile[relation]
        #print(relation)
        for d in range(len(relation)):
            value=relation[d]
            relation_full.append(value)

    return(relation_full)

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s



def outFile_full(outFile):
    fp=full_pref(outFile)
    prefLabel_full=fp[1]
    altLabel_full=full_alt(outFile)
    definition_full=full_def(outFile)
    alts=[]
    list_acentos=[]
    for a in altLabel_full:
        acento=re.search("[áéíóúÁÉÍÓÚ]+", a.lower())
        if(acento!=None):
            sin=normalize(a)
            list_acentos.append(a+'|'+sin)
            alts.append(sin.lower())
        else:
            alts.append(a.lower())
            
    alts2 = []
    delete=[]
    for i in alts:
        if i not in alts2:
            alts2.append(i)
        else:
            delete.append(i)
    
    for a in alts2:
        if(a in prefLabel_full):
            delete.append(a)
            ind=alts2.index(a)
            alts2.pop(ind)
    
    indices=[]
    pos=[]
    delete2=[]
    if('altLabel' in outFile.keys()):
        for i in range(len(outFile["altLabel"])):
            alt=outFile["altLabel"][i]["@value"]
            lang=outFile["altLabel"][i]["@language"]
            item=outFile["altLabel"][i]
            ambos=alt+'-'+lang
            acento=re.search("[áéíóúÁÉÍÓÚ]+", alt.lower())
            sin=normalize(alt)
            ambos=sin+'-'+lang
            if(ambos.lower() in delete and ambos.lower() not in indices):
                pos.append(i)
                indices.append(ambos.lower())
                delete2.append(item)
            

        for i in delete2:
            ind=outFile["altLabel"].index(i)
            del outFile["altLabel"][ind]

        if(len(delete2)>0):
            outFile_full(outFile)

    return(outFile)




def topConcept(outFile,  file_schema):
    if('broader' in outFile.keys()):
        del outFile['topConceptOf']

    elif('broader' not in outFile.keys() ):
        file_schema['hasTopConcept'].append(outFile['@id'])
    return(outFile)
    

