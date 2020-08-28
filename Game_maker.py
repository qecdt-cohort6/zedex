import sys; sys.path.append('pyzx-master')
import numpy as np
import random, math, os
import pyzx as zx
from fractions import Fraction
from IPython.display import display
import webbrowser
import time
import csv
import qiskit
from qiskit import QuantumCircuit as qc
import d3_no_jup



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

# qubit_amount = 3
# depth = 4
# random.seed(1337)
# graph = zx.generate.cliffords(qubit_amount, depth)

qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
h q[0];
cx q[0],q[1];
cx q[0],q[2];
cx q[0],q[3];
cx q[0],q[4];"""

graph = zx.Circuit.from_qasm(qasm).to_graph()


# display(zx.draw(graph, labels =True), )

# circ_qasm=zx.extract.streaming_extract(graph)               #Converts the graph to QASM string
# old_circuit=qc.from_qasm_str(circ_qasm.to_qasm())           #Converts that QASM string to a Quantum Circuit
# old_diagram = old_circuit.draw(output="mpl")                #Draws and saves circuit
# old_diagram.savefig("data/old.png", format="png")
# =============================================================================




# =============================================================================
# #LOADING A GRAPH FROM A QISKIT CIRCUIT 
# 
# ghz = qc(5, 5)
# ghz.h(0)
# for idx in range(1,5):
#     ghz.cx(0,idx)
# ghz.barrier(range(5))
# ghz.measure(range(5), range(5))
# ghz.draw(output='mpl')
# graph=zx.sqasm(ghz.qasm())
# display(zx.draw(graph,labels=True))
# =============================================================================













#Converts the pyzx graph to a HTML/Javascript object 
#This writes the generated HTML version of the graph to a html file which can be viewed in browser
html = d3_no_jup.draw(graph)
f = open(r"web/ghz_prototype.html", "w")
f.write(html)
f.close()
url = os.getcwd()+ 'web/ghz_prototype.html'   #This automatically opens the graph in a chrome tab ready to be altered
webbrowser.open('file://' + url,2)



#Want the python script to idle whislt the user is  performing rules on the JS object
#Once the user has finished updating the JS object, it will output a text file.
#If this text file exists then the loop will execute the commands in the text file
# while not os.path.exists("updates.csv"):
#     time.sleep(1)


# if os.path.isfile("updates.csv"):           
#     data=[]
#     with open('updates.csv', 'r') as file:          #Reading the data in from the CSV file and appending it to a list
#         reader = csv.reader(file)
#         for line in reader:
#             data.append(line)
#                                             #Looping over all the functions that need to be carried out.
    
#     for i in range(len(data)):
#         if data[i][0]=="s":                     #If rule to perform is spider
#             zx.rules.apply_rule(graph, zx.rules.spider, [[int(data[i][1]),int(data[i][2])]], check_isolated_vertices=True)
#             display(zx.draw(graph,labels=True))
#             print(graph)
            
#         if data[i][0]=="u":  
#             neighbours=[]                   #If rule to perform is unspider
#             data[i][1]=int(data[i][1])          #target node
#             data[i][2]=Fraction(data[i][2])          #targets phase 
#             data[i][3]=int(data[i][3])          # Qubit/row index - where to position on graph
#             data[i][4]=int(data[i][4])          #Column index (row in pyzx) where to position on graph
            
#             for j in range(5, len(data[i])):       #Neeed to loop over every nearest neighbour to cast it to integer
#                                                     #start at the nearest neighbour entries
#                 neighbours.append(int(data[i][j])) 
#             zx.rules.unspider(graph, [data[i][1], tuple(neighbours),data[i][2] ], data[i][4] , data[i][3] )
#             display(zx.draw(graph,labels=True))
#             print(graph)


# #The rules called here were written by me, and require lots more testing and rewriting
# #=============================================================================
#         if data[i][0]=="i":                     
#             neighbours=[]
#             neighbours.append(int(data[i][1]))
#             neighbours.append(int(data[i][2]))  
#             zx.rules.add_identity(graph,tuple(neighbours),data[i][3])
#             display(zx.draw(graph,labels=True))
#             print(graph)


#         if data[i][0]=="ri":
#             neighbours=[]
#             neighbours.append(int(data[i][2]))
#             neighbours.append(int(data[i][3]))
#             zx.rules.remove_identity(graph,int(data[i][1]),tuple(neighbours))
#             display(zx.draw(graph,labels=True))
#             print(graph)
# #=============================================================================


  

#     circ_qasm=zx.extract.streaming_extract(graph)               #Extracting a QASM string from the graph
#     New_Circuit=qc.from_qasm_str(circ_qasm.to_qasm())           #Define a new Qiskit circuit from the QASM string
#     diagram = New_Circuit.draw(output="mpl")                    #Save and output new circuit
#     diagram.savefig("data/new.png", format="png")
    
    
#                                                         #displaying the origonal  circuit along with the newly reduced one
#     html2 ="""<h2>Circuit Comparison</h2>
#     <img src="./data/old.png" alt="Old Circuit" width="500" height="333">
#     <img src="./data/new.png" alt="New Circuit" width="500" height="333">
#     </body>
#     </html>
#     """
    
#     p = open(r"circuits.html", "w")
#     p.write(html2)
#     p.close()
#     url = os.getcwd()+'/' + 'circuits.html'
#     webbrowser.open(url,2)
    


    
