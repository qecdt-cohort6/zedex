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


#this takes a list as arguement, shape depends on the rule being implemented, but the first element 
#of each row should be the rule to be implemented.

def Implement_Rules(data):

    #temporarily hardcoding graph object in
    graph = zx.generate.cliffords(qubit_amount, depth)

    for i in range(len(data)):
            if data[i][0]=="s":                     #If rule to perform is spider
                zx.rules.apply_rule(graph, zx.rules.spider, [[int(data[i][1]),int(data[i][2])]], check_isolated_vertices=True)
                display(zx.draw(graph,labels=True))
                print(graph)
                
            if data[i][0]=="u":  
                neighbours=[]                   #If rule to perform is unspider
                data[i][1]=int(data[i][1])          #target node
                data[i][2]=Fraction(data[i][2])          #targets phase 
                data[i][3]=int(data[i][3])          # Qubit/row index - where to position on graph
                data[i][4]=int(data[i][4])          #Column index (row in pyzx) where to position on graph
                
                for j in range(5, len(data[i])):       #Neeed to loop over every nearest neighbour to cast it to integer
                                                        #start at the nearest neighbour entries
                    neighbours.append(int(data[i][j])) 
                zx.rules.unspider(graph, [data[i][1], tuple(neighbours),data[i][2] ], data[i][4] , data[i][3] )
                display(zx.draw(graph,labels=True))
                print(graph)


    #The rules called here were written by me, and require lots more testing and rewriting
    #=============================================================================
            if data[i][0]=="i":                     
                neighbours=[]
                neighbours.append(int(data[i][1]))
                neighbours.append(int(data[i][2]))  
                zx.rules.add_identity(graph,tuple(neighbours),data[i][3])
                display(zx.draw(graph,labels=True))
                print(graph)


            if data[i][0]=="ri":
                neighbours=[]
                neighbours.append(int(data[i][2]))
                neighbours.append(int(data[i][3]))
                zx.rules.remove_identity(graph,int(data[i][1]),tuple(neighbours))
                display(zx.draw(graph,labels=True))
                print(graph)


    

    G_OUT=zx.draw(graph,labels=True)
    G_OUT.savefig("data/graph.png", format="png")
    html2 ="""<h2>New pyzx graph</h2>
    
    <img src="./data/graph.png" alt="New Circuit" width="500" height="333">
    </body>
    </html>
    """
    
    p = open(r"circuits.html", "w")
    p.write(html2)
    p.close()
    url = os.getcwd()+'/' + 'circuits.html'
    webbrowser.open(url,2)
    #==================