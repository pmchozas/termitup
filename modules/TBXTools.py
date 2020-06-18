import os
import codecs
import sqlite3
import xml.etree.cElementTree as etree
import nltk
from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.collocations import *
import re
import pickle
import gzip
import operator
import sys
import math

#version: 2020/04/11
#Copyright: Antoni Oliver (2020) - Universitat Oberta de Catalunya - aoliverg@uoc.edu
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


class TBXTools:
    '''Class for automatic terminology extraction and terminology management.'''
    def __init__(self):
    
        
    
        self.maxinserts=10000 #controls the maximum number of inserts in memory
        self.sl_lang=""
        self.tl_lang=""
        self.max_id_corpus=0
        
        self.sl_stopwords=[]
        self.tl_stopwords=[]
        self.sl_inner_stopwords=[]
        self.tl_inner_stopwords=[]
        self.sl_exclsions_regexps=[]
        self.tl_exclusion_regexps=[]
        self.sl_morphonorm_rules=[]
        self.tl_morphonorm_rules=[]
        #self.sl_patterns=[]
        #self.tl_patterns=[]
        self.evaluation_terms={}
        self.exclusion_terms={}
        self.exclusion_no_terms={}
        self.ngrams={}
        self.tagged_ngrams={}
        self.term_candidates={}
        self.linguistic_patterns={}
        
        self.knownterms=[]
        ##################################FER METODE
        self.n_min=1
        self.n_max=5
        
        self.punctuation=[".",",",";",":","?","!","'","\"","(",")","-","&","/","«","»","_","%","+","-","*"]
        self.sl_stopwords.extend(self.punctuation)
        self.tl_stopwords.extend(self.punctuation)
        self.sl_inner_stopwords.extend(self.punctuation)
        self.tl_inner_stopwords.extend(self.punctuation)
        
        #FREELING API
        self.FREELINGDIR = "/usr/local";
        self.DATA = self.FREELINGDIR+"/share/freeling/";

    def create_project(self,project_name,sl_lang,tl_lang="null",overwrite=False):
        '''Opens a project. If the project already exists, it raises an exception. To avoid the exception use overwrite=True. To open existing projects, use the open_project method.'''
        if os.path.isfile(project_name) and not overwrite:
                raise Exception("This file already exists")
        
        else:
            if os.path.isfile(project_name) and overwrite:
                os.remove(project_name)
            self.sl_lang=sl_lang
            self.tl_lang=tl_lang
            self.conn=sqlite3.connect(project_name)
            self.cur = self.conn.cursor() 
            self.cur2 = self.conn.cursor()
            with self.conn:
                self.cur = self.conn.cursor()
                self.cur.execute("CREATE TABLE configuration(id INTEGER PRIMARY KEY, sl_lang TEXT, tl_lang TEXT)")
                self.cur.execute("CREATE TABLE sl_corpus(id INTEGER PRIMARY KEY, segment TEXT)")
                self.cur.execute("CREATE TABLE tl_corpus(id INTEGER PRIMARY KEY, segment TEXT)")
                self.cur.execute("CREATE TABLE sl_tagged_corpus(id INTEGER PRIMARY KEY, tagged_segment TEXT)")
                self.cur.execute("CREATE TABLE tl_tagged_corpus(id INTEGER PRIMARY KEY, tagged_segment TEXT)")
                self.cur.execute("CREATE TABLE sl_stopwords (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_stopword TEXT)")
                self.cur.execute("CREATE TABLE sl_inner_stopwords (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_inner_stopword TEXT)")
                self.cur.execute("CREATE TABLE tl_stopwords (id INTEGER PRIMARY KEY AUTOINCREMENT, tl_stopword TEXT)")
                self.cur.execute("CREATE TABLE tl_inner_stopwords (id INTEGER PRIMARY KEY AUTOINCREMENT, tl_inner_stopword TEXT)")
                self.cur.execute("CREATE TABLE sl_exclusion_regexps (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_exclusion_regexp TEXT)")
                self.cur.execute("CREATE TABLE tl_exclusion_regexps (id INTEGER PRIMARY KEY AUTOINCREMENT, tl_exclusion_regexp TEXT)")
                self.cur.execute("CREATE TABLE sl_morphonorm_rules (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_morphonorm_rule TEXT)")
                self.cur.execute("CREATE TABLE tl_morphonorm_rules (id INTEGER PRIMARY KEY AUTOINCREMENT, tl_morphonorm_rule TEXT)")
                #self.cur.execute("CREATE TABLE sl_patterns (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_pattern TEXT)")
                #self.cur.execute("CREATE TABLE tl_patterns (id INTEGER PRIMARY KEY AUTOINCREMENT, tl_pattern TEXT)")
                self.cur.execute("CREATE TABLE evaluation_terms (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_term TEXT, tl_term TEXT)")
                self.cur.execute("CREATE TABLE exclusion_terms (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_term TEXT, tl_term TEXT)")
                self.cur.execute("CREATE TABLE exclusion_noterms (id INTEGER PRIMARY KEY AUTOINCREMENT, sl_term TEXT, tl_term TEXT)")
                self.cur.execute("CREATE TABLE tokens (id INTEGER PRIMARY KEY AUTOINCREMENT, token TEXT, frequency INTEGER)")
                self.cur.execute("CREATE TABLE ngrams (id INTEGER PRIMARY KEY AUTOINCREMENT, ngram TEXT, n INTEGER, frequency INTEGER)")
                self.cur.execute("CREATE TABLE tagged_ngrams (id INTEGER PRIMARY KEY AUTOINCREMENT, ngram TEXT, tagged_ngram TEXT, n INTEGER, frequency INTEGER)")
                
                self.cur.execute("CREATE INDEX indextaggedngram on tagged_ngrams (ngram);")
                
                
                self.cur.execute("CREATE TABLE term_candidates (id INTEGER PRIMARY KEY AUTOINCREMENT, candidate TEXT, n INTEGER, frequency INTEGER, measure TEXT, value FLOAT)")
                self.cur.execute("CREATE TABLE index_pt(id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT, target TEXT, probability FLOAT)")
                self.cur.execute("CREATE INDEX index_index_pt on index_pt (source);")
                self.cur.execute("CREATE TABLE linguistic_patterns (id INTEGER PRIMARY KEY AUTOINCREMENT, linguistic_pattern TEXT)")
                
                self.cur.execute("INSERT INTO configuration (id, sl_lang, tl_lang) VALUES (?,?,?)",[0,self.sl_lang,self.tl_lang])
                self.conn.commit()
                
    def open_project(self,project_name):
        '''Opens an existing project. If the project doesn't exist it raises an exception.'''
        if not os.path.isfile(project_name):
                raise Exception("Project not found")
        else:
            self.conn=sqlite3.connect(project_name)
            self.cur = self.conn.cursor() 
            self.cur2 = self.conn.cursor()
            self.maxsc=0
            self.maxtc=0
            with self.conn:
                self.cur.execute('SELECT sl_lang from configuration where id=0')
                self.sl_lang=self.cur.fetchone()[0]
                self.cur.execute('SELECT tl_lang from configuration where id=0')
                self.tl_lang=self.cur.fetchone()[0]
                #Maximum position in corpora
                self.maxpositions=[]
                self.cur.execute('SELECT max(id) from sl_corpus')
                self.qresult=self.cur.fetchone()[0]
                if not self.qresult==None:
                    self.maxpositions.append(self.qresult)
                else:
                    self.maxpositions.append(0)
                self.cur.execute('SELECT max(id) from tl_corpus')
                self.qresult=self.cur.fetchone()[0]
                if not self.qresult==None:
                    self.maxpositions.append(self.qresult)
                else:
                    self.maxpositions.append(0)
                self.cur.execute('SELECT max(id) from sl_tagged_corpus')
                self.qresult=self.cur.fetchone()[0]
                if not self.qresult==None:
                    self.maxpositions.append(self.qresult)
                else:
                    self.maxpositions.append(0)
                self.cur.execute('SELECT max(id) from tl_tagged_corpus')
                self.qresult=self.cur.fetchone()[0]
                if not self.qresult==None:
                    self.maxpositions.append(self.qresult)
                else:
                    self.maxpositions.append(0)
                self.max_id_corpus=max(self.maxpositions)

                
                #loading of stopwords
                self.cur.execute('SELECT sl_stopword from sl_stopwords')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.sl_stopwords.append(self.d[0])

                self.cur.execute('SELECT tl_stopword from tl_stopwords')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.tl_stopwords.append(self.d[0])

                self.cur.execute('SELECT sl_inner_stopword from sl_inner_stopwords')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.sl_inner_stopwords.append(self.d[0])

                self.cur.execute('SELECT tl_inner_stopword from tl_inner_stopwords')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.tl_inner_stopwords.append(self.d[0])
                    
                self.cur.execute('SELECT sl_exclusion_regexp from sl_exclusion_regexps')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.sl_exclusion_regexps.append(self.d[0])
                    
                self.cur.execute('SELECT tl_exclusion_regexp from tl_exclusion_regexps')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.tl_exclusion_regexps.append(self.d[0])
                    
                self.cur.execute('SELECT sl_morphonorm_rule from sl_morphonorm_rules')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.sl_morphonorm_rules.append(self.d[0])
                
                self.cur.execute('SELECT tl_morphonorm_rule from tl_morphonorm_rules')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.tl_morphonorm_rules.append(self.d[0])
                
                '''self.cur.execute('SELECT sl_pattern from sl_patterns')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.sl_patterns.append(self.d[0])
                    
                self.cur.execute('SELECT tl_pattern from tl_patterns')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.tl_patterns.append(self.d[0])'''
                    
                self.cur.execute('SELECT sl_term,tl_term from evaluation_terms')
                self.data=self.cur.fetchall()
                for self.d in self.data:
                    self.evaluation_terms[self.d[0]]=self.d[1]
    

    #METODES DELETES
    def delete_sl_corpus(self):
        '''Deletes de source language corpus.'''
        with self.conn:
            self.cur.execute('DELETE FROM sl_corpus')
            self.conn.commit()
    
    def delete_tl_corpus(self):
        '''Deletes de target language corpus.'''
        with self.conn:
            self.cur.execute('DELETE FROM tl_corpus')
            self.conn.commit()
    
    def delete_sl_tagged_corpus(self):
        '''Deletes the source language tagged corpus.'''
        with self.conn:
            self.cur.execute('DELETE FROM sl_tagged_corpus')
            self.conn.commit()
    
    def delete_tl_tagged_corpus(self):
        '''Deletes the target language tagged corpu.'''
        with self.conn:
            self.cur.execute('DELETE FROM tl_tagged_corpus')
            self.conn.commit()
    
    def delete_sl_stopwords(self):
        '''Deletes the stop-words for the source language.'''
        self.sl_stopwords=[]
        with self.conn:
            self.cur.execute('DELETE FROM sl_stopwords')
            self.conn.commit()
            
    def delete_tl_stopwords(self):
        '''Deletes the stop-words fot the target language.'''
        self.tl_stopwords=[]
        with self.conn:
            self.cur.execute('DELETE FROM tl_stopwords')
            self.conn.commit()
            
    def delete_sl_inner_stopwords(self):
        '''Deletes the inner stop-words for the source language.'''
        self.sl_inner_stopwords=[]
        with self.conn:
            self.cur.execute('DELETE FROM sl_inner_stopwords')
            self.conn.commit()
            
    def delete_tl_inner_stopwords(self):
        '''Deletes the innter stop-words for the target language.'''
        self.tl_inner_stopwords=[]
        with self.conn:
            self.cur.execute('DELETE FROM tl_inner_stopwords')
            self.conn.commit()
    
    def delete_sl_exclusion_regexps(self):
        '''Deletes the exclusion regular expressions for the source language.'''
        self.sl_exclusion_regexps=[]
        with self.conn:
            self.cur.execute('DELETE FROM sl_exclusion_regexps')
            self.conn.commit()
    
    def delete_tl_exclusion_regexps(self):
        '''Deletes the exclusion regular expressions for the target language.'''
        self.tl_exclusion_regexps=[]
        with self.conn:
            self.cur.execute('DELETE FROM tl_exclusion_regexps')
            self.conn.commit()
            
    def delete_sl_morphonorm_rules(self):
        '''Deletes the morphological normalisation rules for the source language.'''
        self.sl_morphonorm_rules=[]
        with self.conn:
            self.cur.execute('DELETE FROM sl_morphonorm_rules')
            self.conn.commit()
            
    def delete_tl_morphonorm_rules(self):
        '''Deletes the morphological normalisation rules for the target language.'''
        self.tl_morphonorm_rules=[]
        with self.conn:
            self.cur.execute('DELETE FROM tl_morphonorm_rules')
            self.conn.commit()

    def delete_evaluation_terms(self):
        '''Deletes the evaluation terms.'''
        self.evaluation_terms={}
        with self.conn:
            self.cur.execute('DELETE FROM evaluation_terms')
            self.conn.commit()
            
    def delete_exclusion_terms(self):
        '''Deletes the exclusion terms.'''
        self.exclusion_terms={}
        with self.conn:
            self.cur.execute('DELETE FROM exclusion_terms')
            self.conn.commit()   
            
    def delete_exclusion_no_terms(self):
        '''Deletes the exclusion no terms.'''
        self.exclusion_terms={}
        with self.conn:
            self.cur.execute('DELETE FROM exclusion_terms')
            self.conn.commit() 
            
    def delete_linguistic_patterns(self):
        '''Deletes the linguistic patterns for linguistic terminology extraction.'''
        self.exclusion_terms={}
        with self.conn:
            self.cur.execute('DELETE FROM exclusion_terms')
            self.conn.commit() 
    
    def delete_tokens(self):
        '''Deletes the tokens,'''
        self.ngrams={}
        with self.conn:
            self.cur.execute('DELETE FROM tokens')
            self.conn.commit()
            
    def delete_ngrams(self):
        '''Deletes the ngrams.'''
        self.ngrams={}
        with self.conn:
            self.cur.execute('DELETE FROM ngrams')
            self.conn.commit()
            
    def delete_tagged_ngrams(self):
        '''Deletes the tagged ngrams.'''
        self.tagged_ngrams={}
        with self.conn:
            self.cur.execute('DELETE FROM tagged_ngrams')
            self.conn.commit()
    
    def delete_term_candidates(self):
        '''Deletes the term candidates.'''
        self.term_candidates={}
        with self.conn:
            self.cur.execute('DELETE FROM term_candidates')
            self.conn.commit()
                
    
    def load_sl_corpus(self,corpusfile, encoding="utf-8"):
        '''Loads a monolingual corpus for the source language. It's recommended, but not compulsory, that the corpus is segmented (one segment per line). Use TBXTools external tools to segment the corpus. A plain text corpus (not segmented), can be aslo used.'''
        self.cf=codecs.open(corpusfile,"r",encoding=encoding,errors="ignore")
        self.data=[]
        self.continserts=0
        for self.line in self.cf:
            
            self.continserts+=1
            self.max_id_corpus+=1
            self.record=[]
            self.line=self.line.rstrip()
            self.record.append(self.max_id_corpus)
            self.record.append(self.line)
            self.data.append(self.record)
            if self.continserts==self.maxinserts:
                self.cur.executemany("INSERT INTO sl_corpus (id, segment) VALUES (?,?)",self.data)
                self.data=[]
                self.continserts=0
        with self.conn:
            self.cur.executemany("INSERT INTO sl_corpus (id, segment) VALUES (?,?)",self.data)    
        self.conn.commit()
        
    def load_sl_tl_corpus(self,slcorpusfile, tlcorpusfile, encoding="utf-8"):
        '''Loads a bilingual corpus in Moses format (that is, in two independent files. It expects one segment per line.'''
        self.slcf=codecs.open(slcorpusfile,"r",encoding=encoding)
        self.tlcf=codecs.open(tlcorpusfile,"r",encoding=encoding)
        self.sl_data=[]
        self.tl_data=[]
        self.continserts=0
        while 1:
            self.sl_segment=self.slcf.readline()
            if not self.sl_segment:
                break
            self.tl_segment=self.tlcf.readline()
            self.continserts+=1
            self.max_id_corpus+=1
            self.sl_record=[]
            self.tl_record=[]
            self.sl_segment=self.sl_segment.rstrip()
            self.tl_segment=self.tl_segment.rstrip()
            
            self.sl_record.append(self.max_id_corpus)
            self.tl_record.append(self.max_id_corpus)
            self.sl_record.append(self.sl_segment)
            self.tl_record.append(self.tl_segment)
            self.sl_data.append(self.sl_record)
            self.tl_data.append(self.tl_record)
            if self.continserts==self.maxinserts:
                self.cur.executemany("INSERT INTO sl_corpus (id, segment) VALUES (?,?)",self.sl_data)
                self.cur.executemany("INSERT INTO tl_corpus (id, segment) VALUES (?,?)",self.tl_data)
                self.sl_data=[]
                self.tl_data=[]
                self.continserts=0
        with self.conn:
            self.cur.executemany("INSERT INTO sl_corpus (id, segment) VALUES (?,?)",self.sl_data)   
            self.cur.executemany("INSERT INTO tl_corpus (id, segment) VALUES (?,?)",self.tl_data)  
        self.conn.commit()
                    
    def load_tmx(self,tmx_file, sl_code=None, tl_code= None):
        '''Loads a parallel corpus from a TMX file. Source and target language codes should be given. The codes must be the exactly the same as in the TMX file. In no codes are provided, the codes used in the TBXTools project will be used.'''
        self.continserts=0
        if sl_code==None:
            self.sl_code=self.sl_lang
        else:
            self.sl_code=sl_code
        if tl_code==None:
            self.tl_code=self.tl_lang
        else:
            self.tl_code=tl_code
        self.data1=[]
        self.data2=[]
        self.sl_segment=""
        self.tl_segment=""
        self.current_lang=""
        for self.event, self.elem in etree.iterparse(tmx_file,events=("start","end")):
            if self.event=='start':
                if self.elem.tag=="tu" and not self.sl_segment=="" and not self.tl_segment=="":
                    self.continserts+=1
                    self.max_id_corpus+=1
                    self.record1=[]
                    self.record2=[]
                    self.record1.append(self.max_id_corpus)
                    self.record1.append(self.sl_segment)
                    self.data1.append(self.record1)
                    
                    self.record2.append(self.max_id_corpus)
                    self.record2.append(self.tl_segment)
                    self.data2.append(self.record2)
                    self.sl_segment=""
                    self.tl_segment=""
                    if self.continserts==self.maxinserts:
                        self.cur.executemany("INSERT INTO sl_corpus (id, segment) VALUES (?,?)",self.data1) 
                        self.cur.executemany("INSERT INTO tl_corpus (id, segment) VALUES (?,?)",self.data2)
                        self.data1=[]
                        self.data2=[]
                        self.continserts=0
                        self.conn.commit()
                elif self.elem.tag=="tuv":
                    self.current_lang=self.elem.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                elif self.elem.tag=="seg":
                    if self.elem.text:
                        self.segmentext=self.elem.text
                    else:
                        self.segmentext=""
                    if self.current_lang==sl_code:
                        self.sl_segment=self.segmentext
                    if self.current_lang==tl_code:
                        self.tl_segment=self.segmentext                
                        

    def load_sl_tagged_corpus(self,corpusfile,format="TBXTools",encoding="utf-8"):
        '''Loads the source language tagged corpus. 3 formats are allowed:
        - TBXTools: The internal format used by TBXTools. One tagged segment per line.
                f1|l1|t1|p1 f2|l2|t2|p2 ... fn|ln|tn|pn 
        - Freeling: One token per line and segments separated by blank lines
                f1 l1 t1 p1
                f2 l2 t2 p2
                ...
                fn ln tn pn
        - Conll: One of the output formats guiven by the Standford Core NLP analyzer.  On token per line and segments separated by blank lines
                id1 f1 l1 t1 ...
                id2 f2 l2 t2 ...
                ...
                idn fn ln tn ...
        '''
        self.validformarts=["TBXTools","freeling","conll"]
        #TODO: Raise exception if not a valid format.
        self.cf=codecs.open(corpusfile,"r",encoding=encoding)
        if format=="TBXTools":
            
            self.data=[]
            self.continserts=0
            for self.line in self.cf:
                self.continserts+=1
                self.max_id_corpus+=1
                self.record=[]
                self.line=self.line.rstrip()
                self.record.append(self.max_id_corpus)
                self.record.append(self.line)
                self.data.append(self.record)
                if self.continserts==self.maxinserts:
                    self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
                    self.data=[]
                    self.continserts=0
                    
            with self.conn:
                self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)    
            self.conn.commit()
        elif format=="freeling":
            self.data=[]
            self.continserts=0
            self.segment=[]
            for self.line in self.cf:
                self.line=self.line.rstrip()
                if self.line=="":
                    self.continserts+=1
                    self.max_id_corpus+=1
                    self.record=[]
                    self.record.append(self.max_id_corpus)
                    self.record.append(" ".join(self.segment))
                    print(" ".join(self.segment))
                    self.data.append(self.record)
                    if self.continserts==self.maxinserts:
                        self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
                        self.data=[]
                        self.continserts=0
                        self.data=[]
                        self.conn.commit()
                    self.segment=[]
                        
                else:
                    self.camps=self.line.split(" ")
                    self.token=self.camps[0]+"|"+self.camps[1]+"|"+self.camps[2]

                    self.segment.append(self.token)
            with self.conn:
                self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)    
                self.conn.commit()
                    
        
                    
        elif format=="conll":
            self.data=[]
            self.continserts=0
            self.segment=[]
            for self.line in self.cf:
                self.line=self.line.rstrip()
                if self.line=="":
                    self.continserts+=1
                    self.max_id_corpus+=1
                    self.record=[]
                    self.record.append(self.max_id_corpus)
                    self.record.append(" ".join(self.segment))
                    self.data.append(self.record)
                    if self.continserts==self.maxinserts:
                        self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
                        self.data=[]
                        self.continserts=0
                        self.data=[]
                        self.conn.commit()
                    self.segment=[]
                        
                else:
                    self.camps=self.line.split("\t")
                    self.token=self.camps[1]+"|"+self.camps[2]+"|"+self.camps[3]
                    self.segment.append(self.token)
                
                
                
            with self.conn:
                self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)    
            self.conn.commit()
            
            
        


    def load_sl_stopwords(self,fitxer,encoding="utf-8"):
        '''Loads the stopwords for the source language.'''
        self.fc=codecs.open(fitxer,"r",encoding)
        self.data=[]
        self.record=[]
        while 1:
            self.linia=self.fc.readline()
            if not self.linia:
                break 
            self.linia=self.linia.rstrip()
            self.sl_stopwords.append(self.linia)
            self.record.append(self.linia)
            self.data.append(self.record)
            self.record=[]
        
        for self.punct in self.punctuation:
            self.record.append(self.punct)
            self.data.append(self.record)
            self.record=[]
        with self.conn:
            self.cur.executemany("INSERT INTO sl_stopwords (sl_stopword) VALUES (?)",self.data)  
            
    def load_tl_stopwords(self,fitxer,encoding="utf-8"):
        '''Loads the stopwords for the target language.'''
        self.fc=codecs.open(fitxer,"r",encoding)
        self.data=[]
        self.record=[]
        while 1:
            self.linia=self.fc.readline()
            if not self.linia:
                break 
            self.linia=self.linia.rstrip()
            self.tl_stopwords.append(self.linia)
            self.record.append(self.linia)
            self.data.append(self.record)
            self.record=[]
        
        for self.punct in self.punctuation:
            self.record.append(self.punct)
            self.data.append(self.record)
            self.record=[]
        with self.conn:
            self.cur.executemany("INSERT INTO tl_stopwords (tl_stopword) VALUES (?)",self.data) 

    def load_sl_inner_stopwords(self,fitxer,encoding="utf-8"):
        '''Loads the stopwords for the source language.'''
        self.fc=codecs.open(fitxer,"r",encoding)
        self.data=[]
        self.record=[]
        while 1:
            self.linia=self.fc.readline()
            if not self.linia:
                break 
            self.linia=self.linia.rstrip()
            self.sl_inner_stopwords.append(self.linia)
            self.record.append(self.linia)
            self.data.append(self.record)
            self.record=[]
        
        for self.punct in self.punctuation:
            self.record.append(self.punct)
            self.data.append(self.record)
            self.record=[]
        with self.conn:
            self.cur.executemany("INSERT INTO sl_inner_stopwords (sl_inner_stopword) VALUES (?)",self.data)  
            
    def load_tl_inner_stopwords(self,fitxer,encoding="utf-8"):
        '''Loads the inner stopwords for the target language.'''
        self.fc=codecs.open(fitxer,"r",encoding)
        self.data=[]
        self.record=[]
        while 1:
            self.linia=self.fc.readline()
            if not self.linia:
                break 
            self.linia=self.linia.rstrip()
            self.tl_inner_stopwords.append(self.linia)
            self.record.append(self.linia)
            self.data.append(self.record)
            self.record=[]
        
        for self.punct in self.punctuation:
            self.record.append(self.punct)
            self.data.append(self.record)
            self.record=[]
        with self.conn:
            self.cur.executemany("INSERT INTO tl_inner_stopwords (tl_inner_stopword) VALUES (?)",self.data)  

    def load_evaluation_terms(self,arxiu,encoding="utf-8",nmin=0,nmax=1000):
        '''Loads the evaluation terms from a tabulated text'''
        #TODO Load from TBX
        
        self.cf=codecs.open(arxiu,"r",encoding=encoding)
        self.data=[]
        self.continserts=0
        for self.line in self.cf:
            
            self.line=self.line.rstrip()
            self.continserts+=1            
            self.record=[]
            self.line=self.line.rstrip()
            self.camps=self.line.split("\t")
            if len(self.camps)==1:
                if len(self.camps[0].split(" "))>=nmin and len(self.camps[0].split(" "))<=nmax:
                    
                    self.record.append(self.camps[0])
                    self.record.append("_")
                    self.evaluation_terms[self.camps[0]]="_"
                    self.data.append(self.record)
            elif len(self.camps)>1:
                if len(self.camps[0].split(" "))>=nmin and len(self.camps[0].split(" "))<=nmax:
                    self.record.append(self.camps[0])
                    self.record.append(self.camps[1])
                    self.evaluation_terms[self.camps[0]]=self.camps[1]
                    self.data.append(self.record)
            if self.continserts==self.maxinserts:
                
                self.cur.executemany("INSERT INTO evaluation_terms (sl_term,tl_term) VALUES (?,?)",self.data)
                self.data=[]
                self.continserts=0
        with self.conn:
            self.cur.executemany("INSERT INTO evaluation_terms (sl_term,tl_term) VALUES (?,?)",self.data)
    
        self.conn.commit()
    
    def load_exclusion_terms(self,arxiu,encoding="utf-8",nmin=0,nmax=1000):
        '''Loads the exclusion terms from a tabulated text. The terms in the exclusion terms will be deleted from the term candidates. It is useful to store already known terms, and/or term candidates already evaluated either as correct or as incorrect.'''
        self.cf=codecs.open(arxiu,"r",encoding=encoding)
        self.data=[]
        self.continserts=0
        for self.line in self.cf:
            self.line=self.line.rstrip()
            self.continserts+=1            
            self.record=[]
            self.line=self.line.rstrip()
            self.camps=self.line.split("\t")
            if len(self.camps)==1:
                self.record.append(self.camps[0])
                self.record.append("_")
                self.evaluation_terms[self.camps[0]]="_"
            elif len(self.camps)>1:
                self.record.append(self.camps[0])
                self.record.append(self.camps[1])
                self.evaluation_terms[self.camps[0]]=self.camps[1]
            self.data.append(self.record)
            if self.continserts==self.maxinserts:
                self.cur.executemany("INSERT INTO exclusion_terms (sl_term,tl_term) VALUES (?,?)",self.data)
                self.data=[]
                self.continserts=0
        with self.conn:
            self.cur.executemany("INSERT INTO exclusion_terms (sl_term,tl_term) VALUES (?,?)",self.data)
    
        self.conn.commit()

    def load_sl_exclusion_regexps(self,arxiu,encoding="utf-8"):
        '''Loads the exclusionregular expressions for the source language.'''
        self.cf=codecs.open(arxiu,"r",encoding=encoding)
        self.data=[]
        for self.line in self.cf:
            self.line=self.line.rstrip()
            self.record=[]
            self.record.append(self.line)
            self.data.append(self.record)
            
        with self.conn:
            self.cur.executemany('INSERT INTO sl_exclusion_regexps (sl_exclusion_regexp) VALUES (?)',self.data)
            
    def load_tl_exclusion_regexps(self,arxiu,encoding="utf-8"):
        '''Loads the exclusionregular expressions for the target language.'''
        self.cf=codecs.open(arxiu,"r",encoding=encoding)
        self.data=[]
        for self.line in self.cf:
            self.line=self.line.rstrip()
            self.record=[]
            self.record.append(self.line)
            self.data.append(self.record)
            
        with self.conn:
            self.cur.executemany('INSERT INTO tl_exclusion_regexps (sl_exclusion_regexp) VALUES (?)',self.data)

   
    def show_term_candidates(self,limit=-1,minfreq=2, minmeasure=-1, show_frequency=True, show_measure=False, mark_eval=False, verbose=False):
        '''Shows in screen the term candidates.'''
        self.measure=0
        
        with self.conn:
            self.cur.execute("SELECT sl_term FROM exclusion_terms")
            for self.s in self.cur.fetchall():
                self.knownterms.append(self.s[0])
        with self.conn:
            self.cur.execute("SELECT frequency,measure,n,candidate FROM term_candidates order by frequency desc limit "+str(limit))
            for self.s in self.cur.fetchall():
                self.frequency=self.s[0]
                if self.s[1]==None:
                    self.measure==0
                else:
                    self.measure=self.s[1]
                self.n=self.s[2]
                self.candidate=self.s[3]
                if self.n>=self.n_min and self.n<=self.n_max and not self.candidate in self.knownterms:
                    if mark_eval:
                        if self.candidate in self.evaluation_terms:
                            self.candidate="*"+self.candidate
                    if show_frequency:
                        self.cadena=str(self.frequency)+"\t"+self.candidate
                    else:
                        self.cadena=self.candidate
                    print(self.cadena)

    def select_unigrams(self,file,position=-1,verbose=True):
        sunigrams=codecs.open(file,"w",encoding="utf-8")
        self.unigrams={}
        self.cur.execute("SELECT frequency,candidate FROM term_candidates order by value desc, frequency desc, random()")
        #self.cur.execute("SELECT frequency,value,n,candidate FROM term_candidates order by n desc limit "+str(limit))
        for self.s in self.cur.fetchall():
            self.frequency=self.s[0]
            self.candidate=self.s[1].split(" ")[position]
            if self.candidate in self.unigrams:
                self.unigrams[self.candidate]+=self.frequency
            else:
                self.unigrams[self.candidate]=self.frequency
        #for self.candidate in self.unigrams:
        #    print(self.unigrams[self.candidate],self.candidate)
            
        for self.candidate in sorted(self.unigrams, key=self.unigrams.get, reverse=True):
            if verbose:
                cadena=str(self.unigrams[self.candidate])+"\t"+self.candidate
                print(cadena)
            sunigrams.write(cadena+"\n")


    def save_term_candidates(self,outfile,limit=-1,minfreq=2, minmeasure=-1, show_frequency=True, show_measure=False, mark_eval=False, verbose=False):
        '''Saves the term candidates in a file.'''
        out=[]
        self.sortida=codecs.open(outfile,"w",encoding="utf-8")
        self.measure=0
        self.knownterms=[]
        with self.conn:
            self.cur.execute("SELECT sl_term FROM exclusion_terms")
            for self.s in self.cur.fetchall():
                self.knownterms.append(self.s[0])
        with self.conn:
            self.cur.execute("SELECT frequency,value,n,candidate FROM term_candidates order by value desc, frequency desc, random() limit "+str(limit))
            #self.cur.execute("SELECT frequency,value,n,candidate FROM term_candidates order by n desc limit "+str(limit))
            for self.s in self.cur.fetchall():
                self.frequency=self.s[0]
                if self.s[1]==None:
                    self.measure==0
                else:
                    self.measure=self.s[1]
                self.n=self.s[2]
                self.candidate=self.s[3]
                if self.n>=self.n_min and self.n<=self.n_max and not self.candidate in self.knownterms:
                    if mark_eval:
                        if self.candidate in self.evaluation_terms:
                            self.candidate="*"+self.candidate
                    if show_measure and not show_frequency:
                        self.cadena=str(self.measure)+"\t"+self.candidate
                    elif show_frequency and not show_measure:
                        self.cadena=str(self.frequency)+"\t"+self.candidate
                    elif show_frequency and show_measure:
                        self.cadena=str(self.frequency)+"\t"+str(self.measure)+"\t"+self.candidate
                    else:
                        self.cadena=self.candidate
                    if verbose:
                        #print(self.cadena)
                        pass
                    self.sortida.write(self.cadena+"\n")
                    out.append(self.cadena)
        return(out)
                    
    #STATISTICAL TERM EXTRACTION
    
    def ngram_calculation (self,nmin,nmax,minfreq=2):
        '''Performs the calculation of ngrams.'''
        self.ngrams=FreqDist()
        self.tokens=FreqDist()
        self.n_nmin=nmin
        self.n_max=nmax
            
        with self.conn:
            self.cur.execute('SELECT segment from sl_corpus')
            
            for self.s in self.cur.fetchall():
                self.segment=self.s[0]
                for self.n in range(nmin,nmax+2): #we calculate one order bigger in order to detect nested candidates
                    #self.ngs=ngrams(self.sl_tokenizer.tokenize(self.segment), self.n)
                    self.ngs=ngrams(self.segment.split(" "), self.n)
                    for self.ng in self.ngs:
                        self.ngrams[self.ng]+=1
                #for self.token in self.sl_tokenizer.tokenize(self.segment):
                for self.token in self.segment.split(" "):
                    self.tokens[self.token]+=1
                       
        self.data=[]                
        for self.c in self.ngrams.most_common():
            if self.c[1]>=minfreq:
                self.record=[]
                self.record.append(" ".join(self.c[0]))            
                self.record.append(len(self.c[0]))
                self.record.append(self.c[1])   
                self.data.append(self.record)
        with self.conn:
            self.cur.executemany("INSERT INTO ngrams (ngram, n, frequency) VALUES (?,?,?)",self.data) 
            self.conn.commit()
            
        self.data=[]                
        for self.c in self.tokens.most_common():
            self.record=[]
            self.record.append(self.c[0])            
            self.record.append(self.c[1])   
            self.data.append(self.record)
        with self.conn:
            self.cur.executemany("INSERT INTO tokens (token, frequency) VALUES (?,?)",self.data) 
            self.conn.commit()
            
    def statistical_term_extraction(self,minfreq=2):
        '''Performs an statistical term extraction using the extracted ngrams (ngram_calculation should be executed first) Loading stop-words is advisable. '''
        self.cur.execute("DELETE FROM term_candidates")
        self.conn.commit()
        self.cur.execute("SELECT ngram, n, frequency FROM ngrams order by frequency desc")
        self.results=self.cur.fetchall()
        self.data=[] 
        for self.a in self.results:
            self.ng=self.a[0].split(" ")
            self.include=True
            if self.ng[0].lower() in self.sl_stopwords: self.include=False
            if self.ng[-1].lower() in self.sl_stopwords: self.include=False
            for self.i in range(1,len(self.ng)):
                if self.ng[self.i].lower() in self.sl_inner_stopwords:
                    self.include=False
            if self.include:
                self.record=[]
                self.record.append(self.a[0])            
                self.record.append(self.a[1])
                self.record.append(self.a[2])
                self.record.append("freq")
                self.record.append(self.a[2])   
                self.data.append(self.record)
            if self.a[2]<minfreq:
                break
        
        with self.conn:
            self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency, measure, value) VALUES (?,?,?,?,?)",self.data)        
            self.conn.commit()


    def case_normalization(self,verbose=False):
        '''
        Performs case normalization. If a capitalized term exists as non-capitalized, the capitalized one will be deleted and the frequency of the non-capitalized one will be increased by the frequency of the capitalized.
        '''
        self.cur.execute("SELECT candidate,frequency FROM term_candidates")
        self.results=self.cur.fetchall()
        self.auxiliar={}
        for self.r in self.results:
            self.auxiliar[self.r[0]]=self.r[1]
        for self.a in self.results:
            if not self.a[0]==self.a[0].lower() and self.a[0].lower() in self.auxiliar:
                #self.term_candidates.inc(c[0].lower(),self.term_candidates[c[0]])
                #self.term_candidates[c[0].lower()]+=self.term_candidates[c[0]]
                #self.term_candidates.pop(c[0])     
                self.terma=self.a[0]
                self.termb=self.a[0].lower()
                self.freqa=self.a[1]
                self.freqb=self.auxiliar[self.termb]
                
                self.n=len(self.termb.split(" "))
                self.freqtotal=self.freqa+self.freqb
                if verbose:
                    pass
                    #print(self.terma,self.freqa,"-->",self.termb,self.freqb,"-->",self.freqtotal)
                self.cur.execute('DELETE FROM term_candidates WHERE candidate=?', (self.terma,))
                self.cur.execute('DELETE FROM term_candidates WHERE candidate=?', (self.termb,))
                #self.cur.execute("INSERT INTO term_candidates (candidate, n, frequency) VALUES (?,?,?)",(self.termb,self.n,self.freqtotal,))
                self.cur.execute("INSERT INTO term_candidates (candidate, n, frequency, measure, value) VALUES (?,?,?,?,?)",(self.termb,self.n,self.freqtotal,"freq",self.freqtotal))
        self.conn.commit()

    def nest_normalization(self,percent=10,verbose=False):
        '''
        Performs a normalization of nested term candidates. If an n-gram candidate A is contained in a n+1 candidate B and freq(A)==freq(B) or they are close values (determined by the percent parameter, A is deleted B remains as it is)
        '''
        self.cur.execute("SELECT candidate,frequency,n FROM term_candidates order by frequency desc")
        self.results=self.cur.fetchall()
        for self.a in self.results:
            
            self.ta=self.a[0]
            self.fa=self.a[1]
            self.na=self.a[2]
            self.nb=self.na+1
            self.fmax=self.fa+self.fa*percent/100
            self.fmin=self.fa-self.fa*percent/100
            self.cur.execute("SELECT candidate,frequency FROM term_candidates where frequency <="+str(self.fmax)+" and frequency>="+str(self.fmin)+"  and n ="+str(self.nb)+ " and n<="+str(self.n_max))
            self.results2=self.cur.fetchall()
            for self.b in self.results2:
                self.tb=self.b[0]
                self.fb=self.b[1]
                #if abs(self.fa-self.fb)<=max(self.fa,self.fb)/percent:
                if not self.ta==self.tb and not self.tb.find(self.ta)==-1: 
                
                    self.cur.execute('DELETE FROM term_candidates WHERE candidate=?', (self.ta,))
                    if verbose:
                        pass
                        #print(str(self.fa),self.ta,"-->",str(self.fb),self.tb)

        self.conn.commit()

    def regexp_exclusion(self,verbose=False):
        '''Deletes term candidates matching a set of regular expresions loaded with the load_sl_exclusion_regexps method.'''
        self.cur.execute("SELECT sl_exclusion_regexp FROM sl_exclusion_regexps")
        self.results=self.cur.fetchall()
        for self.r in self.results:
            self.nregexp=len(self.r[0].split(" "))
            self.exreg=self.r[0]
            self.cur.execute("SELECT candidate FROM term_candidates where n<="+str(self.n_max))
            self.results=self.cur.fetchall()
            self.cexreg=re.compile(self.exreg)
            for self.a in self.results:
                self.candidate=self.a[0]
                self.ncandidate=len(self.candidate.split(" "))
                self.match=re.match(self.cexreg,self.candidate)
                #self.match=re.match(r'\W+$',self.candidate)
                
                if not self.match==None and self.nregexp==self.ncandidate:
                    self.cur.execute('DELETE FROM term_candidates WHERE candidate=?', (self.candidate,))
                    if verbose:
                        pass
                        #print(self.exreg,"-->",self.candidate)
            self.conn.commit()

    #EVALUATION
    
    
     
    def evaluate_pos(self,limit,order="desc",iterations=1000,ignore_case=True):
        '''Performs the evaluation of the term candidates using the evaluation_terms loaded with the load_evaluation_terms method.'''
        self.correct=0
        self.total=0
        with self.conn:
            for i in range(0,iterations):
                if order=="desc":
                    self.cur.execute("SELECT candidate from term_candidates where n<="+str(self.n_max)+" order by value desc, frequency desc, random() limit "+str(limit))
                elif order=="asc":
                    self.cur.execute("SELECT candidate from term_candidates where n<="+str(self.n_max)+" order by value asc, frequency desc, random() limit "+str(limit))
                else:
                    raise NameError('Order must be desc (decending) or asc (ascending). Defaulf value: desc')
                #self.cur.execute("SELECT candidate from term_candidates order by id limit "+str(limit))
                for self.s in self.cur.fetchall():
                    self.total+=1
                    self.candidate=self.s[0]
                    if ignore_case:
                        if self.candidate in self.evaluation_terms:
                            self.correct+=1
                        elif self.candidate.lower() in self.evaluation_terms:
                            self.correct+=1
                    else:
                        if self.candidate in self.evaluation_terms:
                            self.correct+=1
            self.correct=self.correct/iterations
            self.total=self.total/iterations
            
        try:
            self.precisio=100*self.correct/self.total
            self.recall=100*self.correct/len(self.evaluation_terms)
            self.f1=2*self.precisio*self.recall/(self.precisio+self.recall)
            return(limit,self.correct,self.total,self.precisio,self.recall,self.f1)
        except:
            return(limit,0,0,0,0,0)

    def association_measures(self,measure="raw_freq",n=2):
        self.measurename=measure
        self.bigram_measures = myBigramAssocMeasures()
        self.trigram_measures = myTrigramAssocMeasures()
        self.fd_tokens=nltk.FreqDist()
        self.fd_bigrams=nltk.FreqDist()
        self.fd_trigrams=nltk.FreqDist()
        self.wildcard_fd=nltk.FreqDist()
        self.cur.execute("SELECT token,frequency from tokens")
        for self.s in self.cur.fetchall():
            self.aux=(self.s[0])
            self.fd_tokens[self.aux]+=self.s[1]
            
        self.textcorpus=[]
        self.cur.execute("SELECT segment from sl_corpus")
        for self.segment in self.cur.fetchall():
            #self.textcorpus.extend(self.sl_tokenizer.tokenize(self.segment[0]))
            self.textcorpus.extend(self.segment[0].split(" "))
            
        #BIGRAMS
        if n==2:
            self.cur.execute("SELECT ngram,frequency from ngrams where n=2")
            for self.s in self.cur.fetchall():
                self.aux=(self.s[0].split(" ")[0],self.s[0].split(" ")[1])
                self.fd_bigrams[self.aux]+=self.s[1]
            #self.bigram_finder=BigramCollocationFinder(self.fd_tokens, self.fd_bigrams)
            self.bigram_finder=BigramCollocationFinder.from_words(self.textcorpus)
            if measure=="chi_sq":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.chi_sq)
            elif measure=="chi_sq_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.chi_sq_2g)
            elif measure=="fisher":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.fisher)
            elif measure=="phi_sq":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.phi_sq)
            elif measure=="phi_sq_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.phi_sq_2g)
            elif measure=="dice":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.dice)
            elif measure=="dice_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.dice_2g)
            elif measure=="my_dice":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.my_dice)
            elif measure=="jaccard":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.jaccard)
            elif measure=="jaccard_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.jaccard_2g)
            elif measure=="likelihood_ratio":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.likelihood_ratio)
            elif measure=="loglikelihood_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.loglikelihood_2g)
            elif measure=="pmi":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.pmi)
            elif measure=="pmi_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.pmi_2g)
            elif measure=="poisson_stirling":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.poisson_stirling)
            elif measure=="poisson_stirling_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.poisson_stirling_2g)
            elif measure=="student_t":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.student_t)
            elif measure=="t_score_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.t_score_2g)
            elif measure=="mi_like":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.mi_like)
            elif measure=="raw_freq":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.raw_freq)
                
            elif measure=="tmi_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.tmi_2g)
                
            elif measure=="odds_2g":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.odds_2g)
                
            elif measure=="MI":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.MI)
            elif measure=="MI2":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.MI2)
            elif measure=="MI3":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.MI3)
                
            elif measure=="my_dice":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.my_dice)
            elif measure=="t_score":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.t_score)
            elif measure=="log_likelihood_ratio":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.log_likelihood_ratio)
            
            elif measure=="log_likelihood_ratio_TEXTNSP":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.log_likelihood_ratio_TEXTNSP)
            elif measure=="tmi":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.tmi)
                
               
            elif measure=="poisson_stirling_TEXTNSP":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.poisson_stirling_TEXTNSP)
                
            
            elif measure=="chi_squared":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.chi_squared)
                
            elif measure=="jaccard_TEXTNSP":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.jaccard_TEXTNSP)
                
            elif measure=="pmi_TEXTNSP":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.pmi_TEXTNSP)
            
            
            elif measure=="phi_sq_TEXTNSP":
                self.bigram_measure=self.bigram_finder.score_ngrams(self.bigram_measures.phi_sq_TEXTNSP)
                
           
            else:
                print(sys.exc_info()[0])
                raise NameError('Association measure not implemented')
            self.data=[]
            for self.nose in self.bigram_measure:
                self.record=[]
                self.term_candidate=" ".join(self.nose[0])
                
                self.mvalue=self.nose[1]
                self.record.append(measure)
                self.record.append(self.mvalue)
                self.record.append(self.term_candidate)
                self.data.append(self.record)
        elif n==3:
            
            #TRIGRAMS
            self.cur.execute("SELECT ngram,frequency from ngrams where n=2")
            for self.s in self.cur.fetchall():
                self.aux=(self.s[0].split(" ")[0],self.s[0].split(" ")[1])
                self.fd_bigrams[self.aux]+=self.s[1]
            
            self.cur.execute("SELECT ngram,frequency from ngrams where n=3")
            for self.s in self.cur.fetchall():
                self.wild=(self.s[0].split(" ")[0],self.s[0].split(" ")[2])
                self.aux=(self.s[0].split(" ")[0],self.s[0].split(" ")[1],self.s[0].split(" ")[2])
                self.fd_trigrams[self.aux]+=self.s[1]
                self.wildcard_fd[self.wild]+=self.s[1]
                
            #self.trigram_finder=TrigramCollocationFinder(self.fd_tokens, self.fd_bigrams, self.wildcard_fd, self.fd_trigrams)
            
            '''Construct a TrigramCollocationFinder, given FreqDists for
            appearances of words, bigrams, two words with any word between them,
            and trigrams.'''
            self.trigram_finder=TrigramCollocationFinder.from_words(self.textcorpus)
            if self.measurename=="chi_sq":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.chi_sq)
            
            elif self.measurename=="jaccard":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.jaccard)
            elif self.measurename=="likelihood_ratio":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.likelihood_ratio)
            elif self.measurename=="pmi":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.pmi)
            elif self.measurename=="poisson_stirling":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.poisson_stirling)
            elif self.measurename=="student_t":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.student_t)
            elif self.measurename=="mi_like":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.mi_like)
            elif self.measurename=="raw_freq":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.raw_freq)
                
            elif measure=="pmi_3g":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.pmi_3g)
                
            elif measure=="poisson_stirling_3g":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.poisson_stirling_3g)
                
            elif measure=="tmi_3g":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.tmi_3g)
            
            elif measure=="loglikelihood_3g":
                self.trigram_measure=self.trigram_finder.score_ngrams(self.trigram_measures.loglikelihood_3g)
            else:
                raise NameError('Association measure not implemented')
            self.data=[]
            for self.nose in self.trigram_measure:
                self.record=[]
                self.term_candidate=" ".join(self.nose[0])
                self.mvalue=self.nose[1]
                self.record.append(self.measurename)
                self.record.append(self.mvalue)
                self.record.append(self.term_candidate)
                self.data.append(self.record)
            
            
  
            
        self.conn.executemany("UPDATE term_candidates SET measure=?,value=? where candidate=?",self.data)
        self.conn.commit()
    


    def index_phrase_table(self,phrasetable):
        '''Indexes a phrase table from Moses.'''
        self.entrada=gzip.open(phrasetable, mode='rt')

        self.pt={}
        self.continserts=0
        self.record=[]
        self.data=[]
        while 1:
            self.linia=self.entrada.readline()
            if not self.linia:
                break
            self.linia=self.linia.rstrip()
            self.camps=self.linia.split(" ||| ")
            self.source=self.camps[0].strip()
            self.trad=self.camps[1].strip()
            self.probs=self.camps[2].split(" ")
            if not self.trad[0] in self.punctuation and not self.source[0] in self.punctuation and not self.trad[-1] in self.punctuation and not self.source[-1] in self.punctuation:
                #Currently, four different phrase translation scores are computed:
                #0    inverse phrase translation probability φ(f|e)
                #1    inverse lexical weighting lex(f|e)
                #2    direct phrase translation probability φ(e|f)
                #3    direct lexical weighting lex(e|f)
                #self.probtrad=float(self.probs[1])
                self.probtrad=(float(self.probs[2])*float(self.probs[3]))
                #print(self.source,self.trad,self.probtrad)
                self.record=[]
                self.record.append(self.source)
                self.record.append(self.trad)
                self.record.append(self.probtrad)
                self.data.append(self.record)
                self.continserts+=1
                if self.continserts==self.maxinserts:
                    self.cur.executemany("INSERT INTO index_pt (source, target, probability) VALUES (?,?,?)",self.data)
                    self.data=[]
                    self.continserts=0
                    self.conn.commit()
        with self.conn:
            self.cur.executemany("INSERT INTO index_pt (source, target, probability) VALUES (?,?,?)",self.data)    
        self.conn.commit()
                
        
    def find_translation_ptable(self,sourceterm,maxdec=1,maxinc=1,ncandidates=5,separator=":"):
        '''Finds translation equivalents in an indexed phrase table table. Requires an indexed phrase table and a a list of terms separated by ":".
        The number of translation candidates can be fixed, as well as the maximum decrement and increment of the number of tokens of the translation candidate'''
        #select target from index_pt where source="international conflict";
        self.cur.execute('SELECT target,probability FROM index_pt where source =?',(sourceterm,))
        self.results=self.cur.fetchall()
        self.targetcandidates={}
        for self.a in self.results:
            self.targetterm=self.a[0]
            self.probability=float(self.a[1])
            self.tttokens=self.targetterm.split(" ")
            
            if not self.tttokens[0] in self.tl_stopwords and not self.tttokens[-1] in self.tl_stopwords and len(self.tttokens)>=len(sourceterm.split(" "))-maxdec and len(self.tttokens)<=len(sourceterm.split(" "))+maxinc:
                self.targetcandidates[self.targetterm]=self.probability
        self.sorted_x = sorted(self.targetcandidates.items(), key=operator.itemgetter(1),reverse=True)
        self.results=[]
        for self.s in self.sorted_x:
            self.results.append(self.s[0].replace(":",";"))
        return(separator.join(self.results[0:ncandidates]))
        
                
   
    def start_freeling_api(self,LANG):
        
        freelingpath='/home/aoliverg/eines/Freeling-4.0/FreeLing-4.0/APIs/python'

        try:
            sys.path.append(freelingpath)
            import freeling
        except:
            #pass
            print("No Freeling API available. Verify Freeling PATH: "+freelingpath)
        
        freeling.util_init_locale("default");

        # create language analyzer
        self.la1=freeling.lang_ident(self.DATA+"common/lang_ident/ident.dat");

        # create options set for maco analyzer. Default values are Ok, except for data files.
        self.op1= freeling.maco_options(LANG);
        self.op1.set_data_files( "", 
                           self.DATA + "common/punct.dat",
                           self.DATA + LANG + "/dicc.src",
                           self.DATA + LANG + "/afixos.dat",
                           "",
                           self.DATA + LANG + "/locucions.dat", 
                           self.DATA + LANG + "/np.dat",
                           self.DATA + LANG + "/quantities.dat",
                           self.DATA + LANG + "/probabilitats.dat");

        # create analyzers
        self.tk1=freeling.tokenizer(self.DATA+LANG+"/tokenizer.dat");
        self.sp1=freeling.splitter(self.DATA+LANG+"/splitter.dat");
        self.sid1=self.sp1.open_session();
        self.mf1=freeling.maco(self.op1);

        # activate mmorpho odules to be used in next call
        self.mf1.set_active_options(False, True, True, False,  # select which among created 
                              True, True, False, True,  # submodules are to be used. 
                              True, False, True, True ); # default: all created submodules are used

        # create tagger, sense anotator, and parsers
        self.tg1=freeling.hmm_tagger(self.DATA+LANG+"/tagger.dat",True,2);
        
    def tag_freeling_api(self,corpus="source"):
        with self.conn:
            self.data=[]
            if corpus=="source":
                self.cur.execute('SELECT id,segment from sl_corpus')
            elif corpus=="target":
                self.cur.execute('SELECT id,segment from tl_corpus')
            for self.s in self.cur.fetchall():
                self.id=self.s[0]
                self.segment=self.s[1]
                self.l1 = self.tk1.tokenize(self.segment);
                self.ls1 = self.sp1.split(self.sid1,self.l1,True);
                self.ls1 = self.mf1.analyze(self.ls1);
                self.ls1 = self.tg1.analyze(self.ls1);
                self.ttsentence=[]
                for self.s in self.ls1 :
                  self.ws = self.s.get_words();
                  for self.w in self.ws :
                    self.form=self.w.get_form()
                    self.lemma=self.w.get_lemma()
                    self.tag=self.w.get_tag()
                    self.ttsentence.append(self.form+"|"+self.lemma+"|"+self.tag)
                self.ttsentence=" ".join(self.ttsentence)
                self.record=[]
                self.record.append(self.id)
                self.record.append(self.ttsentence)
                self.data.append(self.record)
                if self.continserts==self.maxinserts:
                    if corpus=="source":
                        self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
                    if corpus=="target":
                        self.cur.executemany("INSERT INTO tl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
                    self.data=[]
                    self.continserts=0
            with self.conn:
                if corpus=="source":
                    self.cur.executemany("INSERT INTO sl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data) 
                if corpus=="target":
                    self.cur.executemany("INSERT INTO tl_tagged_corpus (id, tagged_segment) VALUES (?,?)",self.data)
    def save_sl_tagged_corpus(self,outputfile,encoding="utf-8"):
        self.sortida=codecs.open(outputfile,"w",encoding=encoding)
        self.cur.execute('SELECT tagged_segment from sl_tagged_corpus')
        for self.s in self.cur.fetchall():
            self.tagged_segment=self.s[0]
            self.sortida.write(self.tagged_segment+"\n")

    
    def tagged_ngram_calculation (self,nmin=2,nmax=3,minfreq=2):
        '''Calculates the tagged ngrams.'''
        self.ngrams=FreqDist()
        self.n_nmin=nmin
        self.n_max=nmax
        with self.conn:
            self.data=[]
            self.record=[]
            self.record.append(self.n_min)
            self.data.append(self.record)
            #self.conn.executemany("UPDATE configuration SET n_min=? where id=0",self.data)
            self.data=[]
            self.record=[]
            self.record.append(self.n_max)
            self.data.append(self.record)
            #self.conn.executemany("UPDATE configuration SET n_max=? where id=0",self.data)
            #cur.execute("UPDATE Contacts SET FirstName = ? WHERE LastName = ?", (Fname, Lname))

            self.conn.commit()
            
        with self.conn:
            self.cur.execute('SELECT tagged_segment from sl_tagged_corpus')
            
            for self.s in self.cur.fetchall():
                self.segment=self.s[0]
                
                for self.n in range(nmin,nmax+2): #we calculate one order bigger in order to detect nested candidates
                    self.ngs=ngrams(self.segment.split(" "), self.n)
                    for self.ng in self.ngs:
                        self.ngrams[self.ng]+=1
                        
        self.data=[]                
        for self.c in self.ngrams.most_common():
           if self.c[1]>=minfreq:
                self.candidate=[]
                for self.ngt in self.c[0]:
                    self.candidate.append(self.ngt.split("|")[0])
                self.candidate=" ".join(self.candidate)
                self.record=[]
                self.record.append(self.candidate)
                self.record.append(" ".join(self.c[0])) 
                self.record.append(len(self.c[0]))
                self.record.append(self.c[1])   
                self.data.append(self.record)
        with self.conn:
            self.cur.executemany("INSERT INTO tagged_ngrams (ngram, tagged_ngram, n, frequency) VALUES (?,?,?,?)",self.data) 
            self.conn.commit()
                    
    def translate_linguistic_pattern(self,pattern):
           
        self.aux=[]
        for self.ptoken in pattern.split(" "):
            self.auxtoken=[]
            self.ptoken=self.ptoken.replace(".*","[^\s]+") #ATENCIÓ AIXÓ ÉS NOU, VERIFICAR SI CAL
            for self.pelement in self.ptoken.split("|"):
                if self.pelement=="#":
                    self.auxtoken.append("([^\s]+?)")                    
                elif self.pelement=="":
                    self.auxtoken.append("[^\s]+?")
                else:
                    if self.pelement.startswith("#"):
                        self.auxtoken.append("("+self.pelement.replace("#","")+")")
                    else:
                        self.auxtoken.append(self.pelement)
            self.aux.append("\|".join(self.auxtoken))
        self.tp="("+" ".join(self.aux)+")"
        #self.tpatterns.append(self.tp)
        return(self.tp)       
    
    def load_linguistic_patterns(self,file, encoding="utf-8"):
        '''Loads the linguistic patterns to use with linguistic terminology extraction.'''
        self.entrada=codecs.open(file,"r",encoding=encoding)
        self.linguistic_patterns=[]
        self.data=[]
        self.record=[]
        for self.linia in self.entrada:
            self.linia=self.linia.rstrip()
            self.pattern=self.translate_linguistic_pattern(self.linia)
            self.record.append(self.pattern)
            self.data.append(self.record)
            self.record=[]
        with self.conn:
            self.cur.executemany("INSERT INTO linguistic_patterns (linguistic_pattern) VALUES (?)",self.data)
        
         

    def linguistic_term_extraction(self,minfreq=2):
        '''Performs an linguistic term extraction using the extracted tagged ngrams (tagged_ngram_calculation should be executed first). '''
        self.linguistics_patterns=[]
        with self.conn:
            self.cur.execute("SELECT linguistic_pattern from linguistic_patterns")
            for self.lp in self.cur.fetchall():
                self.linguistic_pattern=self.lp[0]
                self.linguistic_patterns.append("^"+self.linguistic_pattern+"$")
            
        self.cur.execute("SELECT tagged_ngram, n, frequency FROM tagged_ngrams order by frequency desc")
        self.results=self.cur.fetchall()
        self.data=[] 
        
        for self.a in self.results:
            self.include=True
            self.ng=self.a[0]
            self.n=self.a[1]
            self.frequency=self.a[2]
            if self.ng.split(" ")[0].split("|")[1].lower() in self.sl_stopwords: self.include=False
            if self.ng.split(" ")[-1].split("|")[1].lower() in self.sl_stopwords: self.include=False
            if self.frequency<minfreq:
                break
            if self.include:
                for self.pattern in self.linguistic_patterns:
                    self.match=re.search(self.pattern,self.ng)
                    
                    if self.match:
                        if self.match.group(0)==self.ng:
                            
                            self.candidate=" ".join(self.match.groups()[1:])
                            self.record=[]
                            self.record.append(self.candidate)     
                            self.record.append(self.n)
                            self.record.append(self.frequency)   
                            self.record.append("freq")
                            self.record.append(self.frequency)   
                            self.data.append(self.record)
                
        with self.conn:
            #self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency) VALUES (?,?,?)",self.data)  
            self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency, measure, value) VALUES (?,?,?,?,?)",self.data)      
            self.conn.commit()
            
        #eliminem candidats repetits
        self.cur.execute("SELECT candidate, n, frequency FROM term_candidates")
        self.results=self.cur.fetchall()
        self.tcaux={}
        for self.a in self.results:
            if not self.a[0] in self.tcaux:
                self.tcaux[self.a[0]]=self.a[2]
            else:
                self.tcaux[self.a[0]]+=self.a[2]
        
        self.cur.execute("DELETE FROM term_candidates")
        self.conn.commit()
        self.data=[] 
        for self.tc in self.tcaux:
            self.record=[]
            self.record.append(self.tc)            
            self.record.append(len(self.tc.split(" ")))
            self.record.append(self.tcaux[self.tc])   
            self.record.append("freq")
            self.record.append(self.tcaux[self.tc])   
            self.data.append(self.record)
        with self.conn:
            #self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency) VALUES (?,?,?)",self.data)        
            self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency, measure, value) VALUES (?,?,?,?,?)",self.data) 
            self.conn.commit()
            
     
    def learn_linguistic_patterns(self,outputfile,showfrequencies=False,encoding="utf-8",verbose=True,representativity=100):
        self.learntpatterns={}
        self.sortida=codecs.open(outputfile,"w",encoding=encoding)
        self.acufreq=0
        with self.conn:
            self.cur.execute("SELECT sl_term FROM evaluation_terms")
            for self.s in self.cur.fetchall():
                self.cur.execute("SELECT tagged_ngram, n, frequency FROM tagged_ngrams WHERE ngram= ?", (self.s[0],))
                self.results=self.cur.fetchall()
                
                if len(self.results)>0:
                    for self.a in self.results:
                        self.ng=self.a[0]
                        self.n=self.a[1]
                        self.frequency=self.a[2]
                        self.candidate=[]
                        self.ngtokenstag=self.ng.split(" ")
                        for self.ngt in self.ngtokenstag:
                            self.candidate.append(self.ngt.split("|")[0])
                        self.candidate=" ".join(self.candidate)
                        self.t2=self.ng.split(" ")
                        self.t1=self.candidate.split(" ")
                        self.patternbrut=[]
                        for self.position in range(0,self.n):
                            self.t2f=self.t2[self.position].split("|")[0]
                            self.t2l=self.t2[self.position].split("|")[1]
                            self.t2t=self.t2[self.position].split("|")[2]
                            self.patternpart=""
                            if self.t1[self.position]==self.t2l:
                                self.patternpart="|#|"+self.t2t
                            elif self.t1[self.position]==self.t2f:
                                self.patternpart="#||"+self.t2t
                            self.patternbrut.append(self.patternpart)
                        self.pattern=" ".join(self.patternbrut)
                        if self.pattern in self.learntpatterns:
                            self.learntpatterns[self.pattern]+=self.n
                            self.acufreq+=self.n
                        else:
                            self.learntpatterns[self.pattern]=self.n
                            self.acufreq+=self.n
        self.sorted_x = sorted(self.learntpatterns.items(), key=operator.itemgetter(1),reverse=True)
        self.results=[]
        self.acufreq2=0
        for self.s in self.sorted_x:
            self.percent=100*self.acufreq2/self.acufreq
            if self.percent>representativity:
                break
            self.acufreq2+=self.s[1]
            if showfrequencies:
                cadena=str(self.s[1])+"\t"+self.s[0]
            else:
                cadena=self.s[0]
            self.sortida.write(cadena+"\n")
            if verbose:
                print(cadena)
                                
    def find_translation_pcorpus(self,slterm,maxdec=1,maxinc=1,ncandidates=5,separator=":"):
        self.nmin=len(slterm.split(" "))-maxdec
        self.nmax=len(slterm.split(" "))+maxinc
        self.tlngrams=FreqDist()
        with self.conn:
            self.cur.execute('SELECT id, segment from sl_corpus')
            
            for self.s in self.cur.fetchall():
                self.segment=self.s[1]
                self.id=self.s[0]
                
                if self.segment.find(slterm)>-1:
                    self.cur2.execute('SELECT segment from tl_corpus where id="'+str(self.id)+'"')
                    for self.s2 in self.cur2.fetchall():
                        self.tl_segment=self.s2[0]
                        for self.n in range(self.nmin,self.nmax+1):
                            #self.tlngs=ngrams(self.tl_tokenizer.tokenize(self.tl_segment), self.n)
                            self.tlngs=ngrams(self.tl_segment.split(" "), self.n)
                            for self.tlng in self.tlngs:
                                if not self.tlng[0] in self.tl_stopwords and not self.tlng[-1] in self.tl_stopwords:
                                    self.tlngrams[self.tlng]+=1
            self.resultlist=[]
            for self.c in self.tlngrams.most_common(ncandidates):
                self.resultlist.append(" ".join(self.c[0]))
            
            return(separator.join(self.resultlist))


#TSR

    def tsr(self,termsfile,encoding="utf-8", type="strict",max_iterations=10000000000): #IMPLEMENTED ONLY FOR BIGRAMS
        self.component={}
        self.firstcomponent={}
        self.middlecomponent={}
        self.lastcomponent={}
        self.entrada=codecs.open(termsfile,"r",encoding=encoding)
        for self.linia in self.entrada:
            self.linia=self.linia.rstrip()
            self.camps=self.linia.split(" ")
            if len(self.camps)==1: #UNIGRAMS
                self.firstcomponent[self.camps[0]]=1
                self.lastcomponent[self.camps[0]]=1
            if len(self.camps)>=2:
                self.firstcomponent[self.camps[0]]=1
                self.lastcomponent[self.camps[-1]]=1
                self.component[self.camps[0]]=1
                self.component[self.camps[-1]]=1
                if len(self.camps)>=3:
                    for self.i in range(1,len(self.camps)):
                        self.middlecomponent[self.camps[self.i]]=1
                        self.component[self.camps[self.i]]=1
        self.new=True
        self.newcandidates={} #candidate-frequency
        self.hashmeasure={}
        self.hashvalue={}
        
        self.newcandidatestempstric={} #candidate-frequency
        self.hashmeasuretempstrict={}
        self.hashvaluetempstric={}

        self.newcandidatestempflexible={} #candidate-frequency
        self.hashmeasuretempflexible={}
        self.hashvaluetempflexible={}
        
        self.newcandidatestempcombined={} #candidate-frequency
        self.hashmeasuretempcombined={}
        self.hashvaluetempcombined={}
        
        self.iterations=0
        while self.new:
            self.iterations+=1
            print("ITERATION",self.iterations)
            self.new=False
            self.cur.execute("SELECT candidate,n,frequency,measure,value FROM term_candidates")
            self.results=self.cur.fetchall()
            self.auxiliar={}
            for self.r in self.results:
                self.candidate=self.r[0]
                self.n=self.r[1]
                self.frequency=self.r[2]
                self.measure="tsr"#self.r[3]
                self.value=max_iterations-self.iterations#self.r[4]
                self.rcamps=self.candidate.split(" ")
                if type=="strict":
                    if self.rcamps[0] in self.firstcomponent and self.rcamps[-1] in self.lastcomponent:
                        if not self.candidate in self.newcandidates:
                            #print(self.r)
                            self.newcandidates[self.candidate]=self.frequency
                            self.hashmeasure[self.candidate]=self.measure
                            self.hashvalue[self.candidate]=self.value
                            self.new=True
                            self.firstcomponent[self.rcamps[0]]=1
                            self.lastcomponent[self.rcamps[-1]]=1
                elif type=="flexible":
                    if self.rcamps[0] in self.firstcomponent or self.rcamps[-1] in self.lastcomponent:
                        if not self.candidate in self.newcandidates:
                            self.newcandidates[self.candidate]=self.frequency
                            self.hashmeasure[self.candidate]=self.measure
                            self.hashvalue[self.candidate]=self.value
                            self.new=True
                            self.firstcomponent[self.rcamps[0]]=1
                            self.lastcomponent[self.rcamps[-1]]=1
                            self.component[self.rcamps[0]]=1
                            self.component[self.rcamps[-1]]=1
                elif type=="combined":
                    if self.iterations==1:
                        if self.rcamps[0] in self.firstcomponent and self.rcamps[-1] in self.lastcomponent:
                            if not self.candidate in self.newcandidates:
                                self.newcandidates[self.candidate]=self.frequency
                                self.hashmeasure[self.candidate]=self.measure
                                self.hashvalue[self.candidate]=self.value
                                self.new=True
                                self.firstcomponent[self.rcamps[0]]=1
                                self.lastcomponent[self.rcamps[-1]]=1
                                self.component[self.rcamps[0]]=1
                                self.component[self.rcamps[-1]]=1
                    else:
                        if self.rcamps[0] in self.firstcomponent or self.rcamps[-1] in self.lastcomponent:
                            if not self.candidate in self.newcandidates:
                                self.newcandidatestempcombined[self.candidate]=self.frequency
                                self.hashmeasuretempcombined[self.candidate]=self.measure
                                self.hashvaluetempcombined[self.candidate]=self.value
                                self.new=True
                                self.firstcomponent[self.rcamps[0]]=1
                                self.lastcomponent[self.rcamps[-1]]=1
                                self.component[self.rcamps[0]]=1
                                self.component[self.rcamps[-1]]=1
                          
                 
            if self.iterations>=max_iterations:
                break
            print(self.iterations,self.new)
        with self.conn:
            self.cur.execute('DELETE FROM term_candidates')
            self.conn.commit()
        
                    
        data=[]
        for self.c in self.newcandidates:
            self.termb=self.c
            self.n=len(self.c.split(" "))
            self.freqtotal=self.newcandidates[self.c]
            self.measure=self.hashmeasure[self.c]
            self.value=self.hashvalue[self.c]
            record=[]
            record.append(self.termb)
            record.append(self.n)
            record.append(self.freqtotal)
            record.append(self.measure)
            record.append(self.value)
            data.append(record)
        with self.conn:
            self.cur.executemany("INSERT INTO term_candidates (candidate, n, frequency, measure, value) VALUES (?,?,?,?,?)",data)
            
        self.conn.commit()   

def L_LLR(a,b,c):
    '''Auxiliar function to calculate Log Likelihood Ratio'''
    L=(c**a)*((1-c)**(b-a))
    return(L)
            
class myBigramAssocMeasures(nltk.collocations.BigramAssocMeasures):
    """
    A collection of bigram association measures. Each association measure
    is provided as a function with three arguments::

        bigram_score_fn(n_ii, (n_ix, n_xi), n_xx)

    The arguments constitute the marginals of a contingency table, counting
    the occurrences of particular events in a corpus. The letter i in the
    suffix refers to the appearance of the word in question, while x indicates
    the appearance of any word. Thus, for example:

        n_ii counts (w1, w2), i.e. the bigram being scored
        n_ix counts (w1, *)
        n_xi counts (*, w2)
        n_xx counts (*, *), i.e. any bigram

    This may be shown with respect to a contingency table::

                w1    ~w1
             ------ ------
         w2 | n_ii | n_oi | = n_xi
             ------ ------
        ~w2 | n_io | n_oo |
             ------ ------
             = n_ix        TOTAL = n_xx
             
    Amb la terminologia de Pazienza

                w1    ~w1
             ------ ------
         w2 | n_ii O11| n_oi O12| = n_xi
             ------ ------
        ~w2 | n_io O21| n_oo O22|
             ------ ------
             = n_ix        TOTAL = n_xx
             
             N=O11+O12+O21+O22= n_xx
             R1=O11+O12 = n_xi
             R2=O21+O22
             C1=O11+O21=n_ix
             C2=O12+O22= n_oi+n_oo
             
        TENIM: n_ii, n_ix_xi_tuple, n_xx
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
    """
    #NOVES
    
    def chi_sq_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        x2 = 2 * (((n11 - m11)/m11)**2 + ((n12 - m12)/m12)**2 + ((n21 - m21)/m21)**2 + ((n22 -m22)/m22)**2)
        return(x2)
    def phi_sq_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)

        PHI2 = ((n11 * n22) - (n21 * n21))**2/(n1p * np1 * np2 * n2p)
        return(PHI2)
    
    def t_score_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        m11 = n1p * np1 / npp
 
        T_score = (n11 - m11)/math.sqrt(n11)
        
        return(T_score)
    def dice_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        dice=2*n11/(np1 + n1p)
        return(dice)
        
    def jaccard_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        jaccard = n11 / (n11 + n12 + n21)
        return(jaccard)
        
    def loglikelihood_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        try:
            LogLikelihood = 2 * (n11 * math.log((n11/m11),2) + n12 * math.log((n12/m12),2) + n21 * math.log((n21/m21),2) + n22 * math.log((n22/m22),2))
        except:
            LogLikelihood=0
        return(LogLikelihood)
        
    def MI(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Church Mutual Information accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        self.E11=n_xi*n_ix/n_xx
        self.part=n_ii/self.E11
        self.MI=math.log(self.part,2)
        return(self.MI)
        
    def MI2(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Church Mutual Information Variant accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        self.E11=n_xi*n_ix/n_xx
        self.part=(n_ii/self.E11)**2
        self.MI2=math.log(self.part,2)
        return(self.MI2)
        
    def MI3(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Church Mutual Information Variant accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        self.E11=n_xi*n_ix/n_xx
        self.part=(n_ii/self.E11)**3
        self.MI3=math.log(self.part,2)
        return(self.MI3)
    
    def pmi_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        PMI =   math.log((n11/m11),2)
        return(PMI)
        
    def poisson_stirling_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        PoissonStirling = n11 * ( math.log(n11,2) - math.log(m11,2) - 1)
        return(PoissonStirling)
        
        
    def tmi_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        try:
            tmi = ((n11/npp) * math.log((n11/m11),) + (n12/npp) * math.log((n12/m12),2) + (n21/npp) * math.log((n21/m21),2) + (n22/npp) * math.log((n22/m22),2))
        except:
            tmi=0
        return(tmi)
    
    def odds_2g(self,n_ii, n_ix_xi_tuple, n_xx):
        '''chi_sq - Pearson's chi-squared according to NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi        
        
        n11=n_ii
        n12=n_io
        n21=n_oi
        n22=n_oo
        n1p=n11+n12
        np1=n11+n21
        n2p=n21+n22
        np2=n12+n22
        npp=n_xx

        m11 = (n1p*np1/npp)
        m12 = (n1p*np2/npp)
        m21 = (np1*n2p/npp)
        m22 = (n2p*np2/npp)
        
        if n21==0:n21=1
        if n12==0:n12=1
        ODDS_RATIO = (n11*n22)/(n21*n12)
        return(ODDS_RATIO)
        
        #VELLES
    
        
    def my_dice(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Recalculation of dice accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        self.DF=2*n_ii/(n_xi+n_ix)
        return(self.DF)
        
    def t_score(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Recalculation of student_t accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        self.E11=n_xi*n_ix/n_xx
        self.TS=(n_ii-self.E11)/math.sqrt(n_ii)
        return(self.TS)
        
    def L_LLR(self,a,b,c):
        '''Auxiliar function to calculate Log Likelihood Ratio'''
        L=(c**a)*((1-c)**(b-a))
        return(L)
    
    def log_likelihood_ratio(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of Log Likelihood Ratio accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        r=n_xi/n_xx
        r1=n_ii/n_ix
        r2=n_oi/(n_oi+n_oo)
        
        NOM=L_LLR(n_ii,n_ix,r)*L_LLR(n_oi,(n_oi+n_oo),r)
        DEN=L_LLR(n_ii,n_ix,r1)*L_LLR(n_oi,(n_oi+n_oo),r2)
        if not DEN==0 and NOM/DEN>0:
            self.LLR=-2*math.log((NOM/DEN),2)
        else:
            self.LLR=0
        return(self.LLR)
        
    def log_likelihood_ratio_TEXTNSP(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of Log Likelihood Ratio accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        m11=(n_ix*n_xi)/n_xx
        m12=(n_io+n_oo)*n_xi/n_xx
        m21=n_ix*(n_io+n_oo)/n_xx
        m22=(n_oi+n_oo)*(n_io+n_oo)/n_xx
        try:
            self.LLR=2*((n_ii*math.log((n_ii/m11),2))+(n_oi*math.log((n_oi/m12),2))+(n_io*math.log((n_io/m21),2))+(n_oo*math.log((n_oo/m22),2)))
        except:
            self.LRR=0
        
        return(self.LLR)
        
    def tmi(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of True Mutual Information according to Text:NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        self.E11=n_xi*n_ix/n_xx
        self.PMI=math.log((n_ii/self.E11),2)
        
        
        self.tmi=(n_ii/n_xx)*self.PMI+(n_oi/n_xx)*self.PMI+(n_io/n_xx)*self.PMI+(n_oo/n_xx)*self.PMI
        print(self.E11,self.PMI,self.tmi)
        return(self.tmi)
        
    def poisson_stirling_TEXTNSP(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of Log Likelihood Ratio accoding to Pazienza'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi

        m11=(n_ix*n_xi)/n_xx
        
        self.PS=n_ii*(math.log((n_ii/m11),2)-1)
        
        return(self.PS)
        
    def chi_squared(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of chi_sq according to Text-NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        phi2=((n_ii*n_oo)-(n_io*n_io))**2/(n_xi*n_ix*(n_oi+n_oo)*(n_io+n_oo))
        self.chi_sqr=n_xx*phi2
        return(self.chi_sqr)
        
    def jaccard_TEXTNSP(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of Jaccard according to Text-NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi
        
        self.jaccard=n_ii/(n_ii+n_oi+n_io)
        return(self.jaccard)
        
    def pmi_TEXTNSP(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of pmi according to Text-NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi

        m11=n_ix*n_xi/n_xx
        self.PMI=math.log((n_ii/m11),2)
        
        return(self.PMI)
        
    def phi_sq_TEXTNSP(self,n_ii, n_ix_xi_tuple, n_xx):
        '''Calculation of phi_sq according to Text-NSP'''
        (n_ix, n_xi) = n_ix_xi_tuple
        n_oo=n_xx-n_ix-n_xi
        
        n_io=n_ix-n_ii
        n_oi=n_xi-n_ii
        n_oo=n_xx-n_ix-n_xi

        self.phi2=((n_ii*n_oo)-(n_io*n_io))**2/(n_xi*n_ix*(n_oi+n_oo)*(n_io+n_oo))
        
        return(self.phi2)

class myTrigramAssocMeasures(nltk.collocations.TrigramAssocMeasures):
    
    def pmi_3g(cls, *dades):     
        n_iii=dades[0]
        n_xxx=dades[3]
        n_iix_tuple=dades[1]
        n_ixx_tuple=dades[2]
        (n_iix, n_ixi, n_xii) = n_iix_tuple
        (n_ixx, n_xix, n_xxi) = n_ixx_tuple
        n1pp=n_ixx+n_ixi+n_iix+n_iii
        np1p=n_xix+n_xii+n_iix+n_iii
        npp1=n_xxi+n_xii+n_xii+n_ixi+n_iii
        n2pp=n_xxx+n_xxi+n_xix+n_xii
        np2p=n_xxx+n_xxi+n_ixx+n_ixi
        npp2=n_xxx+n_ixi+n_ixx+n_iix
        
        n111=n_iii
        nppp=n_xxx
        
        m111=n1pp*np1p*npp1/(nppp*nppp)
        PMI=math.log((n111/m111),2)
        return(PMI)
        
    def poisson_stirling_3g(cls, *dades):     
        n_iii=dades[0]
        n_xxx=dades[3]
        n_iix_tuple=dades[1]
        n_ixx_tuple=dades[2]
        (n_iix, n_ixi, n_xii) = n_iix_tuple
        (n_ixx, n_xix, n_xxi) = n_ixx_tuple
        n1pp=n_ixx+n_ixi+n_iix+n_iii
        np1p=n_xix+n_xii+n_iix+n_iii
        npp1=n_xxi+n_xii+n_xii+n_ixi+n_iii
        n2pp=n_xxx+n_xxi+n_xix+n_xii
        np2p=n_xxx+n_xxi+n_ixx+n_ixi
        npp2=n_xxx+n_ixi+n_ixx+n_iix
        
        n111=n_iii
        nppp=n_xxx
        
        m111=n1pp*np1p*npp1/nppp
        poisson_stirling=m111*(math.log(n111,2)-math.log(m111,2)-1)
        return(poisson_stirling)
        
    def tmi_3g(cls, *dades):     
        n_iii=dades[0]
        n_xxx=dades[3]
        n_iix_tuple=dades[1]
        n_ixx_tuple=dades[2]
        (n_iix, n_ixi, n_xii) = n_iix_tuple
        (n_ixx, n_xix, n_xxi) = n_ixx_tuple
        n1pp=n_ixx+n_ixi+n_iix+n_iii
        np1p=n_xix+n_xii+n_iix+n_iii
        npp1=n_xxi+n_xii+n_xii+n_ixi+n_iii
        n2pp=n_xxx+n_xxi+n_xix+n_xii
        np2p=n_xxx+n_xxi+n_ixx+n_ixi
        npp2=n_xxx+n_ixi+n_ixx+n_iix
        
        n111=n_iii
        n112=n_iix
        n121=n_ixi
        n122=n_ixx
        n211=n_xii
        n212=n_xix
        n221=n_xxi
        n222=n_xxx
        
        nppp=n_xxx
        m111=n1pp*np1p*npp1/nppp
        m112=n1pp*np1p*npp2/nppp
        m121=n1pp*np2p*npp1/nppp
        m122=n1pp*np2p*npp2/nppp
        m211=n2pp*np1p*npp1/nppp
        m212=n2pp*np1p*npp2/nppp
        m221=n2pp*np2p*npp1/nppp
        m222=n2pp*np2p*npp2/nppp
        try:
            tmi = (n111/nppp * math.log((n111/m111),2) + n112/nppp * math.log((n112/m112),2) + n121/nppp * math.log((n121/m121),2) + n122/nppp * math.log((n122/m122),2) + n211/nppp * math.log((n211/m211),2) + n212/nppp * math.log((n212/m212),2) + n221/nppp * math.log((n221/m221),2) + n222/nppp * math.log((n222/m222),2))
        except:
            tmi=0
        
        return(tmi)
        
        
    def loglikelihood_3g(cls, *dades):     
        n_iii=dades[0]
        n_xxx=dades[3]
        n_iix_tuple=dades[1]
        n_ixx_tuple=dades[2]
        (n_iix, n_ixi, n_xii) = n_iix_tuple
        (n_ixx, n_xix, n_xxi) = n_ixx_tuple
        n1pp=n_ixx+n_ixi+n_iix+n_iii
        np1p=n_xix+n_xii+n_iix+n_iii
        npp1=n_xxi+n_xii+n_xii+n_ixi+n_iii
        n2pp=n_xxx+n_xxi+n_xix+n_xii
        np2p=n_xxx+n_xxi+n_ixx+n_ixi
        npp2=n_xxx+n_ixi+n_ixx+n_iix
        
        n111=n_iii
        n112=n_iix
        n121=n_ixi
        n122=n_ixx
        n211=n_xii
        n212=n_xix
        n221=n_xxi
        n222=n_xxx
        
        nppp=n_xxx
        m111=n1pp*np1p*npp1/nppp
        m112=n1pp*np1p*npp2/nppp
        m121=n1pp*np2p*npp1/nppp
        m122=n1pp*np2p*npp2/nppp
        m211=n2pp*np1p*npp1/nppp
        m212=n2pp*np1p*npp2/nppp
        m221=n2pp*np2p*npp1/nppp
        m222=n2pp*np2p*npp2/nppp
        try:
            Log_Likelihood = 2 * (n111 * math.log((n111/m111),2) + n112 * math.log((n112/m112),2) + n121 * math.log((n121/m121),2) + n122 * math.log((n122/m122),2) + n211 * math.log((n211/m211),2) + n212 * math.log((n212/m212),2) + n221 * math.log((n221/m221),2) + n222 * math.log((n222/m222),2))
        except:
            Log_Likelihood=0
        
        return(Log_Likelihood)
 
  
    
