
import sys
import numpy as np
import random, math, os
import pyzx as zx
from fractions import Fraction
import webbrowser
import time
import csv
import networkx as nx
import copy



def insert_ids_hadamards(pyzx_graph1): 
    pyzx_semi=copy.deepcopy(pyzx_graph1)
    edge_list=zx.graph.graph_s.GraphS.edges(pyzx_semi)
    
    edges=[]
    for i in edge_list:
        if pyzx_semi.edge_type(i)==2:
            continue
        else:
            edges.append(i)
            
    
    for edge in edges:
        id1=edge[0]
        id2=edge[1]
        e = pyzx_semi.edge(id1,id2)
        pyzx_semi.remove_edge(e)
        j = pyzx_semi.add_vertex(ty=1)
        pyzx_semi.add_edge((id1,j),1)
        pyzx_semi.add_edge((j,id2),1)
        
    edge_list2=zx.graph.graph_s.GraphS.edges(pyzx_semi)
    for i in edge_list2:
        if pyzx_semi.edge_type(i)!=2:
            pyzx_semi.set_edge_type(i,2)
            
        else:
            continue
    
    return pyzx_semi
    
    
def remove_haddys(circuit):

    qasm_list=circuit.split('\\n')
    qasm_list_reduced=copy.deepcopy(qasm_list)
    qubit_tags=[]
    current_gate=list()
    
    n=int(qasm_list[2][7])
 
    
    
    to_be_deleted=[]
    for i in range(n):
        qubit_tags.append('q['+str(i)+']')
        current_gate.append(None)
        
        
    for k in range(n):
        to_be_tested_indices=[i for i, x in enumerate(qasm_list) if qubit_tags[k] in x]
        
    
        for i in range(len(to_be_tested_indices)-1):
            #stops it deleting chains of say 3 hadamards, where 1 should be left behind
            if to_be_tested_indices[i] in to_be_deleted:
                continue
        
            if qasm_list[int(to_be_tested_indices[i])]==qasm_list[int(to_be_tested_indices[i+1])]:
           
                if to_be_tested_indices[i] not in to_be_deleted:
                    to_be_deleted.append(to_be_tested_indices[i])
                    
                if to_be_tested_indices[i+1] not in to_be_deleted:
                    to_be_deleted.append(to_be_tested_indices[i+1])
                    
        to_be_tested_indices=[]
   
  
    for ele in sorted(to_be_deleted, reverse = True):  
        del qasm_list_reduced[ele]   
            

    qasm_final=str()
    separator = '\\n '
    qasm_final=separator.join(qasm_list_reduced)
    
    return qasm_final

            
            
            
#this takes a list as arguement, shape depends on the rule being implemented, but the first element 
#of each row should be the rule to be implemented.
def connections_to_nx_graph(connections):
    arch_graph = nx.Graph()
    for connect in connections:
        print(connect)
        arch_graph.add_edge(int(connect['source']),int(connect['target']),weight=float(connect['fidelity']))
    return arch_graph


#Function which generates a score given a circuit and an architecture
def return_score(graph_qasm, architecture):

    graph_pyzx = graph_qasm[0]

    qasm_initial = graph_qasm[1]

    print(architecture)
    #temporarily doing a full reduce
    #zx.full_reduce(graph_pyzx)




    g_copy = copy.deepcopy(graph_pyzx)

    #add in identities and hadamrads to pyzx graph
    zx.simplify.to_gh(g_copy)
    graph_semi=insert_ids_hadamards(g_copy)

    circ_from_test=zx.extract.extract_circuit(graph_semi,optimize_czs=False, optimize_cnots=0) 
    
    #remove excess hadamards from qasm string
    qasm_final=remove_haddys(circ_from_test.to_qasm())

    circuit_qasm_string=qasm_final

    two_qubit_gates=[]
    nx_arch=connections_to_nx_graph(architecture)
    connections=architecture 
   
    print(circuit_qasm_string)
    
    qasm_list=circuit_qasm_string.split("\\n")
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
                    score=score-1*(con['fidelity']*100)
        
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
                        score=score-6*(con['fidelity']*100)
    
    print(score)
    
    stats = zx.circuit.Circuit.from_qasm(circuit_qasm_string).stats()

    output = {'qasm':circuit_qasm_string,'score':score,'initial_qasm':qasm_initial,'stats':stats}
            
    return output

def new_spider(g, matches):
    
    rem_verts = []
    etab = dict()
    types = g.types()

    for m in matches:
        
        v0, v1 = m[0], m[1]

        g.set_phase(v0, g.phase(v0) + g.phase(v1))

        if g.merge_vdata != None:
            g.merge_vdata(g, v0, v1)

        if g.track_phases:
            g.fuse_phases(v0,v1)

        # always delete the second vertex in the match
        rem_verts.append(v1)

        # edges from the second vertex are transferred to the first
        for w in g.neighbors(v1):
            if v0 == w: continue
            e = (v0,w)
            if e not in etab: etab[e] = [0,0]
            etab[e][g.edge_type((v1,w))-1] += 1
    return (etab, rem_verts, [], True)

            
def Implement_Rules(data):
            
    #temporarily hardcoding graph object in
    qasm = """`.concat(qasm_string,`"""

    graph = zx.Circuit.from_qasm(qasm).to_graph()


    
            
    for i in range(len(data)):
        print(type(data[i][0]),data[i][0])
        if data[i][0]=="s":                     #If rule to perform is spider
            zx.rules.apply_rule(graph, new_spider, [[int(data[i][1]),int(data[i][2])]], check_isolated_vertices=True)
            #display(zx.draw(graph,labels=True))
            print(graph)
                            
        if data[i][0]=="u":  
            neighbours=data[i][2]                   #If rule to perform is unspider
            neighbours =[int(x) for x in neighbours]
            data[i][1]=int(data[i][1])          #target node
            data[i][3]=Fraction(data[i][3])          #targets phase 
            #data[i][3]=int(data[i][3])          # Qubit/row index - where to position on graph
            #data[i][4]=int(data[i][4])          #Column index (row in pyzx) where to position on graph
                            
            #for j in range(5, len(data[i])):       #Neeed to loop over every nearest neighbour to cast it to integer
                                                                    #start at the nearest neighbour entries
                #neighbours.append(int(data[i][j])) 
            zx.rules.unspider(graph, [data[i][1], tuple(neighbours),data[i][3] ])
            #display(zx.draw(graph,labels=True))
            print(graph)
            
            
                #The rules called here were written by me, and require lots more testing and rewriting
                #=============================================================================
        if data[i][0]=="i":                     
            id1 = data[i][1]
            id2 = data[i][2]
            e = graph.edge(id1,id2)
            graph.remove_edge(e)
            j = graph.add_vertex(ty=data[i][3])
            graph.add_edge((id1,j),1)
            graph.add_edge((j,id2),1)
            print(graph)
            
            
        if data[i][0]=="ri":
            j = int(data[i][1])
            graph.add_edge((list(graph.neighbors(j))[0],list(graph.neighbors(j))[1]),1)
            graph.remove_vertex(j)
            print(graph)
        
        #rules for changing qubit nodes to red spiders and vice versa

        if data[i][0] == "qr":
            graph.inputs.remove(data[i][1])
            graph.set_type(data[i][1],2)
        
        if data[i][0] == "rq":
            graph.inputs.append(data[i][1])
            graph.set_type(data[i][1],0)

        if data[i][0] == "cc":

            def selector(v,s):
                return v == s

            s = data[i][1]

            def f(v):
                return selector(v,s)
            
            zx.to_rg(graph,select=f)
            
            
              
            



    #add in identities and hadamrads to pyzx graph
    zx.simplify.to_gh(graph)
    graph_semi=insert_ids_hadamards(graph)

    #extract to circuit
    circ_from_test=zx.extract.extract_circuit(graph_semi.copy(),optimize_czs=False, optimize_cnots=0,quiet=True)           

    #remove excess hadamards from qasm string
    qasm_final=remove_haddys(circ_from_test.to_qasm())

    #convert final circuit to qasm string
    final_circuit=zx.circuit.Circuit.from_qasm(qasm_final)

    #convert this to an if statement
    #if true display circuit, if False error message
    print(zx.compare_tensors(zx.circuit.Circuit.to_tensor(final_circuit),zx.circuit.Circuit.to_tensor(zx.circuit.Circuit.from_qasm(qasm))))

                
    return graph,qasm
return_score(Implement_Rules(`+rule_string+'),'+connectivity_string+')')