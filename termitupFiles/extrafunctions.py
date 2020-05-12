import globales
import json

targets_pref=globales.targets_pref
prefLabel_full=globales.prefLabel_full
altLabel_full=globales.altLabel_full
definition_full=globales.definition_full
scheme=globales.scheme
ide_file=globales.ide_file
def check_prefLabel(outFile, targets, rels):
    targetsNull=[]
    prefLabel=outFile['prefLabel']
    if(rels==1):
        for i in range(len(targets)):
            if(targets[i] not in targets_pref):
                targetsNull.append(targets[i])
    else:
        for i in range(len(targets)):
            if(targets[i] not in targets_relation):
                targetsNull.append(targets[i])
    
    return(targetsNull)



def property_add( value, lang, outFile, label,rels, uri ):
    label_file=outFile[label] 
    if(rels==1):
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in prefLabel_full and lang not in targets_pref):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    prefLabel_full.append(plb)
                    targets_pref.append(lang)
                    file_html(scheme, value.strip(' '), ide_file, lang)
                
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in prefLabel_full and alb not in altLabel_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    altLabel_full.append(alb)
            elif(label=='definition'):
                dlb=value.strip(' ')+'-'+lang
                if(dlb not in definition_full):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    definition_full.append(dlb)
        else:
            for i in range(len(label_file)):
                if(label=='prefLabel'):
                    plb=value.strip(' ')+'-'+lang
                    if(plb not in prefLabel_full and lang not in targets_pref ):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        prefLabel_full.append(plb)
                        targets_pref.append(lang)
                        file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in prefLabel_full and alb not in altLabel_full):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        altLabel_full.append(alb)
                elif(label=='definition'):
                    dlb=value.strip(' ')+'-'+lang
                    if(dlb not in definition_full):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        definition_full.append(dlb)
    else:
        if(len(label_file)==0):
            if(label=='prefLabel'):
                plb=value.strip(' ')+'-'+lang
                if(plb not in pref_relation and lang not in targets_relation):
                    label_file.append({'@language':lang, '@value':value.strip(' ')})
                    pref_relation.append(plb)
                    targets_relation.append(lang)
                    file_html(scheme, value.strip(' '), ide_file, lang)
            elif(label=='altLabel'):
                alb=value.strip(' ')+'-'+lang
                if(alb not in pref_relation and lang not in targets_relation):
                    outFile['prefLabel'].append({'@language':lang, '@value':value.strip(' ')})
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
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        pref_relation.append(plb)
                        targets_relation.append(lang)
                        file_html(scheme, value.strip(' '), ide_file, lang)
                elif(label=='altLabel'):
                    alb=value.strip(' ')+'-'+lang
                    if(alb not in pref_relation and lang not in targets_relation):
                        outFile['prefLabel'].append({'@language':lang, '@value':value.strip(' ')})
                        pref_relation.append(alb)
                        targets_relation.append(lang)
                    elif(alb not in pref_relation and alb not in alt_relation):
                        label_file.append({'@language':lang, '@value':value.strip(' ')})
                        alt_relation.append(alb)
    return(outFile)

def file_html(schema, pref, ide, lang):
    try:
        with open('schemas/file_html.json') as f:
            file = json.load(f)
        
        
        file[schema][0][lang].append({'prefLabel':pref, 'ide':ide, 'lang':lang})
        f.close()

        with open('schemas/file_html.json', 'w') as new:
            json.dump(file, new, indent=4,ensure_ascii=False)
    except json.decoder.JSONDecodeError:
       error=''
        #print('JSONDecodeError')
   