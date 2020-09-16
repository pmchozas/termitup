#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:56:37 2020

@author: pmchozas
"""
import frecuency

'''
f1=open('../data/estatutoterms_mx.txt', 'r')
freqlist=f1.readlines()
print(freqlist)

'''

#no sé de dónde sale ese cero


f1= ['7,violencia',
  '5,política',
  '5,siglo',
  '3,políticos']


for i in f1:
    spl=i.split(',')
    print(spl)
    freq=spl[0]
    print(freq)
