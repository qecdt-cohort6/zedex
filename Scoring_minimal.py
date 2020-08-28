import sys
import numpy as np
import random, math, os
import pyzx as zx
from fractions import Fraction
import webbrowser
import time
import csv
import networkx as nx


            
            
            
#this takes a list as arguement, shape depends on the rule being implemented, but the first element 
#of each row should be the rule to be implemented.
def connections_to_nx_graph(connections):
    print(connections)
    arch_graph = nx.Graph()
    
    a = connections[0]['source']
    b = connections[0]['target']
    c = connections[0]['fidelity']
    print("abc",a,b,c)
    arch_graph.add_edge(int(a),int(b),weight=float(c))
    a = connections[1]['source']
    b = connections[1]['target']
    c = connections[1]['fidelity']
    print("abc",a,b,c)
    arch_graph.add_edge(int(a),int(b),weight=float(c))
    a = connections[2]['source']
    b = connections[2]['target']
    c = connections[2]['fidelity']
    print("abc",a,b,c)
    arch_graph.add_edge(int(a),int(b),weight=float(c))
    print("conn list",connections)

    print("made it to end")
        
 
    return arch_graph


#Function which generates a score given a circuit and an architecture
def return_score(graph_pyzx, architecture):

    circ_from_test=zx.extract.extract_circuit(graph_pyzx,optimize_czs=False, optimize_cnots=0)           
    circuit_qasm_string=circ_from_test.to_qasm()

    two_qubit_gates=[]
    nx_arch=connections_to_nx_graph(architecture)
    connections=architecture 
   
    print(circuit_qasm_string)
    qasm_list=circuit_qasm_string.split(""\n"")
    #Loop to count the two qubit gates and store the qubits they act on
    for element in qasm_list:
        if len(element)>0:
            if element[0] =='c':
            
                two_qubit_gate=[int(element[5]),int(element[11]),False]
                two_qubit_gates.append(two_qubit_gate)
                

    #This set of loops determines if each two qubit gate within the QASM string is possible on the 
    # given architecture
    for i in range(len(two_qubit_gates)):
        for d in connections:
    
            temp_TQG=two_qubit_gates[i]
            if d['source']==temp_TQG[0]:
        
                if d['target']==temp_TQG[1]:
                    temp_TQG[2]=True
                    continue
            
            if d['source']==temp_TQG[1]:
        
                if d['target']==temp_TQG[0]:
                    temp_TQG[2]=True
                    continue
                
   
    #two_qubit_gates=[[0, 1, True], [0, 1, True],[7, 5, False], [3, 13, False]]
    
    #loop through each of the two qubit gates.
    #If gate possible on architecture, assign a score based on the fidelity of the connection
    # If not in the architecture, perform Dijsktrika's algorithm to find the shortest path between two points
    score=100
    for j in range(len(two_qubit_gates)):
        if two_qubit_gates[j][2]==True:
            s=two_qubit_gates[j][0]
            t=two_qubit_gates[j][1]
            for con in connections:
                if con['source']==s and con['target']==t:
                    score=score-1*(con['fidelity'])
        
        #now if node not on architecture, perform Dijstikas alg
        #find mininmal weighted path between the two nodes
        #multiply by 3 as 3 CNOTS per swap, and then mult by 2 to traverse the path then back again
        else:
            path=nx.dijkstra_path(nx_arch, two_qubit_gates[j][0], two_qubit_gates[j][1], weight='weight')
            for i in range(len(path)-2):
                s=path[i]
                t=path[i+1]
                for con in connections:
                    if con['source']==s and con['target']==t:
                        score=score-6*(con['fidelity'])
            
    return score
            
def Implement_Rules(data):
            
    #temporarily hardcoding graph object in
    qubit_amount = 3
    depth = 4
    random.seed(1337)
    graph = zx.generate.cliffords(qubit_amount, depth)
            
    for i in range(len(data)):
        print(type(data[i][0]),data[i][0])
        if data[i][0]=="s":                     #If rule to perform is spider
            zx.rules.apply_rule(graph, zx.rules.spider, [[int(data[i][1]),int(data[i][2])]], check_isolated_vertices=True)
            #display(zx.draw(graph,labels=True))
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
            #display(zx.draw(graph,labels=True))
            print(graph)
            
            
                #The rules called here were written by me, and require lots more testing and rewriting
                #=============================================================================
        if data[i][0]=="i":                     
            neighbours=[]
            neighbours.append(int(data[i][1]))
            neighbours.append(int(data[i][2]))  
            zx.rules.add_identity(graph,tuple(neighbours),data[i][3])
            #display(zx.draw(graph,labels=True))
            print(graph)
            
            
        if data[i][0]=="ri":
            neighbours=[]
            neighbours.append(int(data[i][2]))
            neighbours.append(int(data[i][3]))
            zx.rules.remove_identity(graph,int(data[i][1]),tuple(neighbours))
            #display(zx.draw(graph,labels=True))
            print(graph)
            
            
                
            
               
    html2 ="""<h2>New pyzx graph</h2>
                
                <img src="./data/graph.png" alt="New Circuit" width="500" height="333">
                </body>
                </html>
                """
                
                
    print(graph)
    
    score = return_score(graph,[{'source':0,'target':1,'fidelity':1.599E-2,'t':1,'index':0},{'source':1,'target':2,'fidelity':9.855E-3,'t':1,'index':1},{'source':0,'target':2,'fidelity':4.855E-3,'t':1,'index':2}])
    qasm = circ_dat.to_qasm()
    output = {'qasm':qasm,'score':score}
    return output
        

