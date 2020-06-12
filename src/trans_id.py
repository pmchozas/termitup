import re

def trans_ID(term, lang_in):
	
	cadena = re.sub('[/,+.;:/)([]]*', '',  term)
	uri='http://lynx-project.eu/kos/'+cadena.replace(' ','-')+'-'+lang_in
	print(uri)
	return(uri)




