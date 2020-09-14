import argparse
import os
#import preprocess_term
from . import check_term
from . import jsonFile
from . import iateCode
from . import eurovocCode
from . import lexicalaCode
from . import wikidataCode
import re
from unicodedata import normalize
import json
import csv
from . import trans_id
from . import relval
from . import statistical_patri
from . import postprocess
from . import unesco
import logging
from . import conts_log
from . import relval_lexi
from . import frecuency
import time


def terminology_extraction(Corpus, Language):
	
	terminology= statistical_patri.main(Corpus) # corpus,Language
	ide=0 #faltaría
	return terminology, ide
	
