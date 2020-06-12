import json
import jsonFile


def check_prefLabel(outFile, targets, rels):
    targetsNull=[]
    #print(outFile)
    prefLabel=outFile['skos-xl:prefLabel']
    fp=jsonFile.full_pref(outFile)
    targets_pref=fp[0]
    if(rels==1 or rels==2):
        for i in range(len(targets)):
            if(targets[i] not in targets_pref):
                targetsNull.append(targets[i])
    else:
        for i in range(len(targets)):
            if(targets[i] not in targets_relation):
                targetsNull.append(targets[i])
    
    return(targetsNull)

def property_add( value, lang, outFile, label,rels, uri ):
    if(label=='definition'):
        label_file=outFile[label]
    else:
        label_file=outFile['skos-xl:'+label] 
    fp=jsonFile.full_pref(outFile)
    prefLabel_full=fp[1]
    targets_pref=fp[0]
    altLabel_full=jsonFile.full_alt(outFile)
    definition_full=jsonFile.full_def(outFile)
    #print(uri)
    #print(value)
    #print('--property_add---', altLabel_full)
    if(rels==1 or rels==2):
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in prefLabel_full and lang not in targets_pref):
                    label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    prefLabel_full.append(plb)
                    targets_pref.append(lang)
                    #file_html(scheme, value.strip(' '), ide_file, lang)
                
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in prefLabel_full and alb not in altLabel_full):
                    label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    altLabel_full.append(alb)
            elif(label=='definition'):
                dlb=value.strip(' ')+'-'+lang
                if(dlb not in definition_full):
                    label_file.append({'@language':lang, '@value': value.strip(' ')})
                    definition_full.append(dlb)
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in prefLabel_full and lang not in targets_pref ):
                        label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        prefLabel_full.append(plb)
                        targets_pref.append(lang)
                        #file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in prefLabel_full and alb not in altLabel_full):
                        label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        altLabel_full.append(alb)
                elif(label=='definition'):
                    dlb=value.strip(' ')+'-'+lang
                    if(dlb not in definition_full):
                        label_file.append({'@language':lang, '@value': value.strip(' ')})
                        definition_full.append(dlb)
    else:
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in pref_relation and lang not in targets_relation):
                    label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    pref_relation.append(plb)
                    targets_relation.append(lang)
                    #file_html(scheme, value.strip(' '), ide_file, lang)
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in pref_relation and lang not in targets_relation):
                    label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                    pref_relation.append(alb)
                    targets_relation.append(lang)
                elif(alb not in pref_relation and alb not in alt_relation):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    alt_relation.append(alb)
            
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in pref_relation and lang not in targets_relation ):
                        label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        pref_relation.append(plb)
                        targets_relation.append(lang)
                        #file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in pref_relation and lang not in targets_relation):
                        label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ').replace(' ', '-')+'-'+lang+'-alt', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        pref_relation.append(alb)
                        targets_relation.append(lang)
                    elif(alb not in pref_relation and alb not in alt_relation):
                        label_file.append({'@type':'skos-xl:Label', '@id':value.strip(' ')+'-'+lang+'-pref', 'source': uri, 'literalForm':{'@language':lang, '@value': value.strip(' ')}})
                        alt_relation.append(alb)
    return(outFile)

   