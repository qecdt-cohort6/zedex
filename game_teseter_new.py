import sys; sys.path.append('pyzx-master')
import numpy as np
import random, math, os
import pyzx as zx
from fractions import Fraction
from IPython.display import display
import webbrowser
import time
import csv
import d3_no_jup
import copy


from Dict import Circuits



import random
ibmq_16_melbourne = {
    "qubits":{
    0:{"fideliy":4.905E-4},
    1:{"fideliy":1.064E-3},
    2:{"fideliy":5.315E-4},
    3:{"fideliy":5.906E-4},
    4:{"fideliy":6.344E-4},
    5:{"fideliy":2.217E-3},
    6:{"fideliy":1.510E-3},
    7:{"fideliy":1.989E-3},
    8:{"fideliy":9.986E-4},
    9:{"fideliy":2.149E-3},
    10:{"fideliy":2.632E-3},
    11:{"fideliy":9.882E-4},
    12:{"fideliy":1.399E-3},
    13:{"fideliy":1.662E-3},
    14:{"fideliy":7.760E-4}
    },"connections":[
    {"source":0, "target":1, "fidelity":1.922E-2},
    {"source":1, "target":2, "fidelity":1.501E-2},
    {"source":2, "target":3, "fidelity":2.366E-2},
    {"source":3, "target":4, "fidelity":1.669E-2},
    {"source":4, "target":5, "fidelity":2.899E-2},
    {"source":5, "target":6, "fidelity":5.361E-2},
    {"source":0, "target":14, "fidelity":3.452E-2},
    {"source":1, "target":13, "fidelity":4.366E-2},
    {"source":2, "target":12, "fidelity":7.133E-2},
    {"source":3, "target":11, "fidelity":4.214E-2},
    {"source":4, "target":10, "fidelity":3.960E-2},
    {"source":5, "target":9, "fidelity":3.976E-2},
    {"source":6, "target":8, "fidelity":6.480E-2},
    {"source":7, "target":8, "fidelity":5.661E-2},
    {"source":8, "target":9, "fidelity":5.160E-2},
    {"source":9, "target":10, "fidelity":4.849E-2},
    {"source":10, "target":11, "fidelity":3.428E-2},
    {"source":11, "target":12, "fidelity":2.444E-2},
    {"source":12, "target":13, "fidelity":2.808E-2},
    {"source":13, "target":14, "fidelity":3.452E-2}]
}

def arq(qubits=[0,1,2,3,4],device = ibmq_16_melbourne):
    our_arq = {
        "qubits":{},
        "connections":{}
    }
        
    for qubit in qubits:
        our_arq["qubits"][qubit] =device["qubits"][qubit]
        
    templist = []
    for item in device["connections"]:
        if item["source"] in qubits and item["target"] in qubits:
            templist.append(item)
    our_arq["connections"] = templist
    
    
            
    return our_arq       
        
        
def choose_qubits(n=5,arq=ibmq_16_melbourne):
            
    if len(arq["qubits"]) < n:
        print("There aren't enough qubits on this architecture for this value of n.")
            
    else:
        qubits = []
        start = random.randint(0,len(arq["qubits"])-1)
        qubits.append(start)
        
        while len(qubits) < n:
            templist = []
            for item in arq["connections"]:
                if item["source"] in qubits and item["target"] not in qubits:
                    templist.append(item["target"])
        
                if item["target"] in qubits and item["source"] not in qubits:
                    templist.append(item["source"])
        
            r = random.randint(0,len(templist)-1)
            qubits.append(templist[r])
        
        return qubits



#LOADING THE GRAPH SEBS BEEN WORKING WITH
# =============================================================================
for item in Circuits:
    graph = Circuits[item]#zx.generate.cliffords(qubit_amount, depth)

    qubit_num = len(list(dict.fromkeys(graph.qubits().values())))
    qlist = choose_qubits(qubit_num)

    arqq = arq(qubits=qlist)

    

    arqq_pass = {'connections':copy.deepcopy(arqq['connections'])}

    print(arqq_pass)
    print(qlist)

    for connection in arqq_pass['connections']:
        connection['source'] = qlist.index(connection['source'])
        connection['target'] = qlist.index(connection['target'])

    g_copy = copy.deepcopy(graph)

    qasm = zx.Circuit.from_graph(g_copy).to_qasm()

    

    html = d3_no_jup.draw(graph,arqq_pass,qasm)
    name = r"./web/level_"+item+".html"
    f = open(name,"w")#r"web/graph_test_copy.html", "w")
    f.write(html)
    f.close()
