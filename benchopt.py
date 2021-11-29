from pdb import set_trace as breakpoint
from math import *
import re
import os, glob
import sys
import random
from yices import *
from collections import defaultdict
from sympy import Symbol
from sympy.logic.inference import satisfiable
import numpy as np 


benchfile = raw_input('What bench?')
with open(benchfile) as fl:
    lines = fl.readlines()
    fl.close()
fileobject = open("new_" + benchfile,"w+") 
DFF1 = []
DFF2 = []
for index4,line in enumerate(lines):
    if 'DFF' in line:
        if ('INPUT' in line or 'OUTPUT' in line):
            continue
        #breakpoint()
        if 'DFF' == line.split('_')[0]:
           x1 = line.replace('\\','').replace('/','').split('=')
           x2 = x1[0].split('_')
           second = x1[1].replace('BUF','').replace(' ','')
           first = x2[3]+ '_' + x2[4]
           #breakpoint()
           i = 5
           while x2[i] != 'DFXLAB':
               first = first + '_' + x2[i]
               i = i + 1
           DFF2.append(second + " " + first)
        elif '= BUF(DFF' in line:
           x1 = line.replace('\\','').replace('/','').split('=')
           x2 = x1[1].split('_')
           second = x1[0].replace(' ','')
           first = x2[3] + '_' + x2[4]
           #breakpoint()
           i = 5
           while x2[i] != 'DFXLAB':
               first = first + '_' + x2[i]
               i = i + 1
           DFF1.append(second + " " + first)
    elif ('INPUT' in line or 'OUTPUT' in line): #and 'clock' not in line:
        fileobject.write(line)
        #breakpoint()
breakpoint()
for item in DFF1:
    for item1 in DFF2:
        if item.split()[1] == item1.split()[1]:
            newline = item.split()[0] + ' = DFF' + item1.split()[0] + '\n'
            #breakpoint()
            fileobject.write(newline)

for index4,line in enumerate(lines):
    if 'DFF' not in line and 'INPUT' not in line and 'OUTPUT' not in line:
        if '=' in line and ('OR' in line or 'NAND' in line or 'NOR' in line or 'NOT' in line or 'AND' in line or 'XOR' in line or 'XNOR' in line):
            line1 = line.split('=')
            line1[0] = line1[0].replace(' ','')
            line1[1] = line1[1].replace(' ','')
            linex = ' = '.join(line1)
            linex = linex.replace('\\','').replace('/','')
            fileobject.write(linex)
        else:
            line = line.replace('\\','').replace('/','')
            fileobject.write(line)
        
        #linevalue = line.split()
#fileobject.writeline(theline)
fileobject.close()


