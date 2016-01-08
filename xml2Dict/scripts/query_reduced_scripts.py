# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../lib')
import query_reduced_functions as QF

'''
Usage example
'''
FILE_ds = "../data/GC_10.xml" # data set
FILE_tr = '../data/GC_Tr_100.xml' # training data set

# Load & parse xml file

xmlquery = QF.xmlToQueryList(FILE_tr)
print xmlquery[0]
