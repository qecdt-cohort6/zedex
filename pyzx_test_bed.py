# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys; sys.path.append('pyzx-master')
import numpy as np
import random, math, os
import pyzx as zx
from fractions import Fraction
from IPython.display import display




#GRAPH GENERATION
#=============================================================================================================
#%config InlineBackend.figure_for mat = 'svg'

#lOADING THE GRAPH THAT QUINN IS WORKING WITH
#Defines the file path for the circuit we want to load
#fname = os.path.join('..','pyzx-master' ,'circuits','Fast', 'mod5_4_before')
#Loads the circuit that we wish to optimise into pyzx
#graph = zx.Circuit.load(fname)
#Alternatively we could have done:
#graph = zx.Circuit.from_quipper_file(fname)




#LOADING THE GRAPH SEBS BEEN WORKING WITH
# =============================================================================

qubit_amount = 3
depth = 4
random.seed(1337)
graph = zx.generate.cliffords(qubit_amount, depth)
display(zx.draw_d3(graph))


    


    
