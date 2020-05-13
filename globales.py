import csv
# header for Wikidata queries
url = 'https://query.wikidata.org/sparql'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
prefLabel_full=[]
altLabel_full=[]
definition_full=[]
targets_pref=[]
broader_full=[]
narrower_full=[]
related_full=[]
pref_relation=[]
alt_relation=[]
targets_relation=[]

find_iate=[]
find_euro=[]
find_lexi=[]
find_wiki=[]
dict_domains=[]
closeMatch=[]
scheme=''
ide_file=''
file_schema={}
new_no_find=open('no_find.csv', 'w')
no_find = csv.writer(new_no_find)

targets=''
lang=''