import re
from unicodedata import normalize
def trans_ID(term, lang_in):
	
	cadena = re.sub('[/,+.;:/)([]]*', '',  term)
	n = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                        normalize( "NFD", cadena), 0, re.I
        )
	n = normalize( 'NFC', n)
	uri='http://lynx-project.eu/kos/'+n.replace(' ','-')+'-'+lang_in
	#print('--------URI:',uri)
	return(uri)




