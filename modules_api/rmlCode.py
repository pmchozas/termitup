#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:16:07 2020

@author: pmchozas
"""

import os

os.system("java -jar rmlmapper.jar -m mapping.rml.ttl -o output.nt -d")
