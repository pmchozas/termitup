#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:12:38 2020

@author: pmchozas
"""


def extract_context(myterm, corpus):
    term=myterm.term
    term=term.lower()
    corpus=corpus.split('. ')
    linedict={}
    corpus=corpus.lower()
    for line in corpus:
        if term in line:
            tokenlist=line.split(' ')
            listlen=len(tokenlist)
            linedict[listlen]=''
            linedict[listlen]=line
            
   
    max_len=max(linedict.keys())
    
    myterm.context= linedict[max_len].strip()
        
    return myterm
            
            



