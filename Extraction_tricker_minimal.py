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
from Dict import Circuits
from Levels import *
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

    qasm_list=circuit.split('\n')
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
    separator = '\n '
    qasm_final=separator.join(qasm_list_reduced)
    
    return qasm_final
    
#HARD CODED INPUT ==========================================================

graph_pyzx=QFT_N(2,pyzx=True)
graph_qiskit=QFT_N(2,pyzx=False)

#for tensor comparison later
graph_pyzx_initial=QFT_N(2,pyzx=True)
circuit_pyzx_initial=zx.circuit.Circuit.from_graph(graph_pyzx_initial)
#================================================================================



#add in identities and hadamrads to pyzx graph
zx.simplify.to_gh(graph_pyzx)
graph_semi=insert_ids_hadamards(graph_pyzx)

#extract to circuit
circ_from_test=zx.extract.extract_circuit(graph_semi.copy(),optimize_czs=False, optimize_cnots=0,quiet=True)           

#remove excess hadamards from qasm string
qasm_final=remove_haddys(circ_from_test.to_qasm())

#convert final circuit to qasm string
final_circuit=zx.circuit.Circuit.from_qasm(qasm_final)

#convert this to an if statement
#if true display circuit, if False error message
print(zx.compare_tensors(zx.circuit.Circuit.to_tensor(final_circuit),zx.circuit.Circuit.to_tensor(circuit_pyzx_initial)))
