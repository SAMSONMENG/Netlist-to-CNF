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

benchfile = raw_input('What netlist?')
with open(benchfile) as fl:
    lines = fl.readlines()
    fl.close()
fileobject = open("first_" + benchfile,"w+") 
plus1 = 0
for index4, line in enumerate(lines):
    if 'DFF' in line:
        if ('(' not in lines[index4+1] and ')' in lines[index4+1]) or ('DFF' not in lines[index4+1] and ')' in lines[index4+1] and '.QN(' in lines[index4+1]): 
            #breakpoint()
            if line.replace('\n','')[len(line.replace('\n',''))-1] == ')':
                linex = line.replace('\n','') + lines[index4+1].replace(' ','').replace(')','').replace('\n','').replace(';','') + ' );\n'
                fileobject.write(linex)
            elif line.replace('\n','')[len(line.replace('\n',''))-1] != ')':
                linex = line.replace('\n','') + lines[index4+1].replace(' ','').replace(')','').replace('\n','').replace(';','') + ') );\n'
                fileobject.write(linex)
        else:
            fileobject.write(line)
            #plus1 = plus1 + 1
        #elif plus1 == 1:
        #    plue1 = plus1 - 1
        #    continue
        #elif plus1 == 0:
        #    fileobject.write(line)
    elif ('(' not in line and ')' in line) or ('DFF' not in line and ')' in line and '.QN(' in line):
        continue
    else:
        fileobject.write(line)
fileobject.close()

with open("first_" + benchfile) as fl:
    lines = fl.readlines()
    fl.close()
fileobject = open("second_" + benchfile,"w+") 
IN = []
OUT = []
WIRE = []
for index4, line in enumerate(lines):
    if 'input' in line and '[' in line and ']' in line:
        line1 = line.replace('input','')
        line1 = line1.split()
        #breakpoint()
        number = line1[0].replace('[','').replace(']','')
        number1 = number.split(':')[0]
        number2 = number.split(':')[1]
        if int(number1) > int(number2):
            number1 = number1
        else:
            number1 = number2
        inputvar = line1[1].replace(';','')
        for i in range(int(number1)+1):
            IN.append(inputvar+ '_' + str(i) + '_')

    elif 'output' in line and '[' in line and ']' in line:
        line1 = line.replace('output','')
        line1 = line1.split()
        #breakpoint()
        number = line1[0].replace('[','').replace(']','')
        number1 = number.split(':')[0]
        number2 = number.split(':')[1]
        if int(number1) > int(number2):
            number1 = number1
        else:
            number1 = number2
        outputvar = line1[1].replace(';','')
        for i in range(int(number1)+1):
            OUT.append(outputvar+ '_' + str(i) + '_')

    #elif 'wire' in line and '[' in line and ']' in line:
    
    #elif '[' in line and ']' in line:

    else:
        continue
inputdone = 0
outputdone = 0
wireline = ''
for index4, line in enumerate(lines):
    if 'input' in line:
        if '[' in line and ']' in line:
            continue
        elif IN == []:
            fileobject.write(line)
        else:
            fileobject.write(line.replace(';',','))
            for index ,item in enumerate(IN):
                wireline = wireline + item + ', '
                if (index+1)%6 == 0:
                    wireline = wireline + '\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
                elif index == len(IN)-1:
                    #breakpoint()
                    wireline = wireline.replace(',','')
                    wireline = wireline.split()
                    wireline = ', '.join(wireline)
                    wireline = wireline + ';\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
            inputdone = 1
    elif 'output' in line:
        if '[' in line and ']' in line:
            continue
        elif OUT == []:
            fileobject.write(line)
        else:
            fileobject.write(line.replace(';',','))
            for index ,item in enumerate(OUT):
                wireline = wireline + item + ', '
                if (index+1)%6 == 0:
                    wireline = wireline + '\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
                elif index == len(OUT)-1:
                    wireline = wireline.replace(',','')
                    wireline = wireline.split()
                    wireline = ', '.join(wireline)
                    wireline = wireline + ';\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
            outputdone = 1
    elif 'wire' in line and '[' not in line and ']' not in line and '//' not in line:
        if outputdone == 0:
            for index ,item in enumerate(OUT):
                wireline = wireline + item + ', '
                if index == 5:
                    wireline = 'output ' + wireline + '\n'
                    fileobject.write("  " + wireline)
                    wireline = ''
                elif (index+1)%6 == 0:
                    wireline = wireline + '\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
                elif index == len(OUT)-1:
                    wireline = wireline.replace(',','')
                    wireline = wireline.split()
                    wireline = ', '.join(wireline)
                    wireline = wireline + ';\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
            outputdone = 1
        if inputdone == 0:
            for index ,item in enumerate(IN):
                wireline = wireline + item + ', '
                if index == 5:
                    wireline = 'input ' + wireline + '\n'
                    fileobject.write("  " + wireline)
                    wireline = ''
                elif (index+1)%6 == 0:
                    wireline = wireline + '\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
                elif index == len(IN)-1:
                    wireline = wireline.replace(',','')
                    wireline = wireline.split()
                    wireline = ', '.join(wireline)
                    wireline = wireline + ';\n'
                    fileobject.write("         " + wireline)
                    wireline = ''
            inputdone = 1
        fileobject.write(line)
    elif 'wire' in line and '[' in line and ']' in line:
        continue
    elif '[' in line and ']' in line:
        line = line.replace('[','_').replace(']','_')
        fileobject.write(line)
    else:
        fileobject.write(line)
    
fileobject.close()
breakpoint()

with open("second_" + benchfile) as fl:
    lines = fl.readlines()
    fl.close()

fileobject = open("new_" + benchfile,"w+") 
newWire = []
newDFF = []
newINV = []
Unumber = 0;
lastline = lines[len(lines)-3].split()
#breakpoint()
U = lastline[1].replace('U','')
Unumber = int(U)
for index4,line in enumerate(lines):
    if 'DFF' in line and 'QN' in line:
        if '.Q(' in line:
            Unumber = Unumber + 1
            #breakpoint()
            newline =  line.split()
            ORGone = newline[5].replace('.Q','').replace(',','')
            INVone = newline.pop(len(newline)-2)
            INVone = INVone.replace('.QN','')
            newline[5] = newline[5].replace(',','')
            newline1 = '  ' + ' '.join(newline)
            newDFF.append(newline1)
            newINV.append('  INV_X1 U' + str(Unumber) + '( .A' + ORGone + ', .ZN' + INVone + ' );' + '\n')
        else:
            #breakpoint()
            Unumber = Unumber + 1
            newline = line.split()
            needINV = newline[len(newline)-2].replace('.QN','').replace('(','').replace(')','')
            newwire = needINV + '_new_'
            newWire.append(newwire)
            newline[len(newline)-2] = newline[len(newline)-2].replace('.QN','.Q').replace(needINV,newwire)
            newline1 = '  ' + ' '.join(newline)
            newDFF.append(newline1)
            newINV.append('  INV_X1 U' + str(Unumber) + '( .A(' + newwire + '), .ZN(' + needINV + ') );' + '\n')

wireline= ''
breakpoint()

for index4, line in enumerate(lines):
    if 'wire' in line and '//' not in line:
        fileobject.write(line)
        for index, item in enumerate(newWire):
            wireline = wireline + item + ', '
            if (index+1)%5 == 0:
                wireline = wireline + '\n'
                fileobject.write("         " + wireline)
                wireline = ''

    elif 'DFF' in line:
        for index, item in enumerate(newDFF):
            if line.split()[1] == item.split()[1]:
                theline = item + '\n'
                fileobject.write(theline)
                break
            elif index == len(newDFF)-1: 
                fileobject.write(line)
            else:
                continue
    
    elif 'U' + U in line:
        #breakpoint()
        fileobject.write(line)
        for item in newINV:
            theline = item
            fileobject.write(theline)
    else:
        fileobject.write(line)

fileobject.close()

    #fileobject.write(line)
            
            
            


#INV_X1 U17322 ( .A(g3230), .ZN(n16294) );
