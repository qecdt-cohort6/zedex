import sys; sys.path.append('..')
import random
import pyzx as zx

import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram, plot_gate_map, plot_circuit_layout
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt




"""Decomposed Gates"""

# This returns a Rn gate as required form the QFT
def Rn(n,ComplexCondugate=False):
    if ComplexCondugate is False:
        return np.exp( (2*np.pi)/(2**n) )
    elif ComplexCondugate is True:
        return np.exp( -(2*np.pi)/(2**n) )
    else:
        return np.exp( (2*np.pi)/(2**n) )

# This is a controled Rn gate are required for the QFT
def cRn(Circ,a,b,n):
	#needs citations
	Circ.rz(Rn(n+1),a)
	Circ.rz(Rn(n+1),b)
	Circ.cx(a,b)
	Circ.rz(Rn(n+1,True),b)
	Circ.cx(a,b)
	
	return Circ

# This is the decomposition of a ccz gate built of CNOT and T gates.
# https://arxiv.org/pdf/0803.2316.pdf
def ccz(circ,a,b,target):
	circ.cx(b,target)
	circ.tdg(target)
	circ.cx(a,target)
	circ.t(target)
	circ.cx(b,target)
	circ.tdg(target)
	circ.cx(a,target)
	circ.t(b)
	circ.t(target)
	circ.cx(a,b)
	circ.t(a)
	circ.tdg(b)
	circ.cx(a,b)
	
	return circ
	
def cccz(circ,a,b,c,target):
	ang = 0.392699#float(np.pi)/8
	circ.rz(ang,a)
	circ.cx(a,b)
	circ.rz(-ang,b)
	circ.cx(a,b)
	circ.rz(ang,b)
	circ.cx(b,c)
	circ.rz(-ang,c)
	circ.cx(a,c)
	circ.rz(ang,c)
	circ.cx(b,c)
	circ.rz(-ang,c)
	circ.cx(a,c)
	circ.rz(ang,c)
	circ.cx(c,target)
	circ.rz(-ang,target)
	circ.cx(a,target)
	circ.rz(ang,target)
	circ.cx(b,target)
	circ.rz(-ang,target)
	circ.cx(a,target)
	circ.rz(ang,target)
	circ.cx(c,target)
	circ.rz(-ang,target)
	circ.cx(a,target)
	circ.rz(ang,target)
	circ.cx(b,target)
	circ.rz(-ang,target)
	circ.cx(a,target)
	circ.rz(ang,target)
	
	return circ



"""Quantum Error Correction"""

def QEC3(pyzx=True):
	
	Three_qec = QuantumCircuit(5)
	Three_qec.cx(0,3)
	Three_qec.cx(1,3)
	Three_qec.cx(1,4)
	Three_qec.cx(2,4)
	
	if pyzx is True:
		return zx.sqasm(Three_qec.qasm(),simplify=False)
	else:
		return Three_qec


def QEC7(pyzx=True):
	
	circ = QuantumCircuit(10)
	
	circ.cx(0,7)
	circ.cx(2,7)
	circ.cx(4,7)
	circ.cx(6,7)
	
	circ.cx(1,8)
	circ.cx(2,8)
	circ.cx(5,8)
	circ.cx(6,8)
	
	circ.cx(3,9)
	circ.cx(4,9)
	circ.cx(5,9)
	circ.cx(6,9)
	
	if pyzx is True:
		return zx.sqasm(circ.qasm(),simplify=False)
	else:
		return circ


def QEC3_1Garanteed(pyzx=True,error_qubit=random.randint(0,3)):
	circ = QuantumCircuit(3)
	circ.cx(0,1)
	circ.cx(0,2)
	"""Error"""
	circ.x(error_qubit)
	circ.cx(0,1)
	circ.cx(0,2)
	circ.h(0)
	circ = ccz(circ,1,2,0)
	circ.h(0)
	
	if pyzx is True:
		return zx.sqasm(circ.qasm(),simplify=False)
	else:
		return circ



	
	

"""Quantum Fourier Transform"""

def QFT2(pyzx=True):
	QFT_2 = QuantumCircuit(2)
	
	QFT_2.h(0)
	
	QFT_2.barrier()
	
	QFT_2 = cRn(QFT_2,0,1,2)
	
	QFT_2.barrier()
	
	QFT_2.h(1)
	
	

	if pyzx is True:
		return zx.sqasm(QFT_2.qasm(),simplify=False)
	else:
		#QFT_2.swap(0,1)
		return QFT_2


def QFT3(pyzx=True):
	QFT_3 = QuantumCircuit(3)
	QFT_3.h(0)

	QFT_3.barrier()

	QFT_3 = cRn(QFT_3,0,1,2)
	
	QFT_3.barrier()
	
	QFT_3 = cRn(QFT_3,0,2,3)
	
	QFT_3.barrier()

	QFT_3.h(1)
	
	QFT_3.barrier()

	QFT_3 = cRn(QFT_3,1,2,2)
	
	QFT_3.barrier()

	QFT_3.h(2)

	

	if pyzx is True:
		return zx.sqasm(QFT_3.qasm(),simplify=False)
	else:
		#QFT_3.swap(0,2)
		return QFT_3


def QFT4(pyzx=True):
	QFT_4 = QuantumCircuit(4)
	QFT_4.h(0)
	
	QFT_4.barrier()

	QFT_4 = cRn(QFT_4,0,1,2)
	
	QFT_4.barrier()
	
	QFT_4 = cRn(QFT_4,0,2,3)
	
	QFT_4.barrier()
	
	QFT_4 = cRn(QFT_4,0,3,4)
	
	QFT_4.barrier()

	QFT_4.h(1)
	
	QFT_4.barrier()

	QFT_4 = cRn(QFT_4,1,2,2)
	
	QFT_4.barrier()
	
	QFT_4 = cRn(QFT_4,1,3,3)
	
	QFT_4.barrier()
	
	QFT_4.h(2)
	
	QFT_4.barrier()

	QFT_4 = cRn(QFT_4,2,3,2)
	
	QFT_4.barrier()

	QFT_4.h(3)

	

	if pyzx is True:
		return zx.sqasm(QFT_4.qasm(),simplify=False)
	else:
		#QFT_4.swap(0,3)
		#QFT_4.swap(1,2)
		return QFT_4


def QFT5(pyzx=True):
	QFT_5 = QuantumCircuit(5)
	QFT_5.h(0)

	QFT_5.rz(Rn(2+1),0)
	QFT_5.rz(Rn(2+1),1)
	QFT_5.cx(0,1)
	QFT_5.rz(Rn(2+1,True),1)
	QFT_5.cx(0,1)

	QFT_5.rz(Rn(3+1),0)
	QFT_5.rz(Rn(3+1),2)
	QFT_5.cx(0,2)
	QFT_5.rz(Rn(3+1,True),2)
	QFT_5.cx(0,2)

	QFT_5.rz(Rn(4+1),0)
	QFT_5.rz(Rn(4+1),3)
	QFT_5.cx(0,3)
	QFT_5.rz(Rn(4+1,True),3)
	QFT_5.cx(0,3)

	QFT_5.rz(Rn(5+1),0)
	QFT_5.rz(Rn(5+1),4)
	QFT_5.cx(0,4)
	QFT_5.rz(Rn(5+1,True),4)
	QFT_5.cx(0,4)

	QFT_5.h(1)

	QFT_5.rz(Rn(2+1),1)
	QFT_5.rz(Rn(2+1),2)
	QFT_5.cx(1,2)
	QFT_5.rz(Rn(2+1,True),2)
	QFT_5.cx(1,2)

	QFT_5.rz(Rn(3+1),1)
	QFT_5.rz(Rn(3+1),3)
	QFT_5.cx(1,3)
	QFT_5.rz(Rn(3+1,True),3)
	QFT_5.cx(1,3)

	QFT_5.rz(Rn(4+1),1)
	QFT_5.rz(Rn(4+1),4)
	QFT_5.cx(1,4)
	QFT_5.rz(Rn(4+1,True),4)
	QFT_5.cx(1,4)

	QFT_5.h(2)

	QFT_5.rz(Rn(2+1),2)
	QFT_5.rz(Rn(2+1),3)
	QFT_5.cx(2,3)
	QFT_5.rz(Rn(2+1,True),3)
	QFT_5.cx(2,3)

	QFT_5.rz(Rn(3+1),2)
	QFT_5.rz(Rn(3+1),4)
	QFT_5.cx(2,4)
	QFT_5.rz(Rn(3+1,True),4)
	QFT_5.cx(2,4)

	QFT_5.h(3)

	QFT_5.rz(Rn(2+1),3)
	QFT_5.rz(Rn(2+1),4)
	QFT_5.cx(3,4)
	QFT_5.rz(Rn(2+1,True),4)
	QFT_5.cx(3,4)

	QFT_5.h(4)

	if pyzx is True:
		return zx.sqasm(QFT_5.qasm(),simplify=False)
	else:
		#QFT_5.swap(0,4)
		#QFT_5.swap(1,3)
		return QFT_5


def QFT_N(n,pyzx=True):
	QFT = QuantumCircuit(n)
	rep = n
	lis = []
	for i in range(n):
		lis.append(i)
		QFT.h(i)
		QFT.barrier()
		for j in np.arange(1,rep):
			QFT = cRn(QFT,i,i+j,1+j)
			QFT.barrier()
            
		rep = rep - 1
	
	
	# ~ return QFT_clean
	if pyzx is True:
		QFT_pyzx = zx.sqasm(QFT.qasm(),simplify=False)
		return QFT_pyzx
	else:
		return QFT


"""Grover Search Algorithm"""

"""2-qubit GSA"""

def GSA2_0(circ):
    circ.x(0)
    circ.x(1)
    
    circ.h(2)
    circ = ccz(circ,0,1,2)
    circ.h(2)
    
    circ.x(0)
    circ.x(1)
    return circ
    
def GSA2_1(circ):
    circ.x(0)
    circ.x(1)
    
    circ.h(2)
    circ = ccz(circ,0,1,2)
    circ.h(2)
    return circ
    
def GSA2_2(circ):
    circ.x(1)
    
    circ.h(2)
    circ = ccz(circ,0,1,2)
    circ.h(2)
    
    circ.x(1)
    return circ

def GSA2_3(circ):
    circ.h(2)
    circ = ccz(circ,0,1,2)
    circ.h(2)
    return circ


def GSA2(hidden_element=0,pyzx=True):
	
	GSA2 = QuantumCircuit(3)

	GSA2.h(0)
	GSA2.h(1)
	GSA2.h(2)
	##Hiden cell
	if hidden_element ==0:
		GSA2 = GSA2_0(GSA2)
	elif hidden_element ==1:
		GSA2 = GSA2_1(GSA2)
	elif hidden_element ==2:
		GSA2 = GSA2_2(GSA2)
	else:
		GSA2 = GSA2_3(GSA2)
	
	GSA2.h(0)
	GSA2.h(1)

	GSA2.x(0)
	GSA2.x(1)

	GSA2.cz(0,1)

	GSA2.x(0)
	GSA2.x(1)

	GSA2.h(0)
	GSA2.h(1)
	
	if pyzx is True:
		return zx.sqasm(GSA2.qasm(),simplify=False)
	else:
		return GSA2
	
"""3-qubit GSA"""

def GSA3_hidden_element(circ,k=0):
	if k == 0:
		circ.x(0)
		circ.x(1)
		circ.x(2)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(0)
		circ.x(1)
		circ.x(2)
		return circ
		
	elif k == 1:
		circ.x(0)
		circ.x(1)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(0)
		circ.x(1)
		return circ
		
	elif k == 2:
		circ.x(0)
		circ.x(2)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(0)
		circ.x(2)
		return circ
			
	elif k == 3:
		circ.x(0)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(0)
		return circ
		
	elif k == 4:
		circ.x(1)
		circ.x(2)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(1)
		circ.x(2)
		return circ
			
	elif k == 5:
		circ.x(1)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(1)
		return circ
		
	elif k == 6:
		circ.x(2)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(2)
		return circ
			
	elif k == 7:
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		return circ
		
	else:
		print("k set to ", 0)
		circ.x(0)
		circ.x(1)
		circ.x(2)
		
		circ.h(3)
		circ = cccz(circ,0,1,2,3)
		circ.h(3)
		
		circ.x(0)
		circ.x(1)
		circ.x(2)
		return circ


def GSA3(hidden_element=0,iterations=2,pyzx=True):
	
	
	
	GSA3 = QuantumCircuit(4)

	GSA3.h(0)
	GSA3.h(1)
	GSA3.h(2)
	GSA3.h(3)
	
	
	for i in range(iterations):
		##Hiden cell
		
		GSA3 = GSA3_hidden_element(GSA3,k=hidden_element)
		
		GSA3.h(0)
		GSA3.h(1)
		GSA3.h(2)

		GSA3.x(0)
		GSA3.x(1)
		GSA3.x(2)

		GSA3 = ccz(GSA3,0,1,2)

		GSA3.x(0)
		GSA3.x(1)
		GSA3.x(2)

		GSA3.h(0)
		GSA3.h(1)
		GSA3.h(2)

	if pyzx is True:
		return zx.sqasm(GSA3.qasm(),simplify=False)
	else:
		return GSA3


"""Quantum Half Adder"""
# http://www.dmphotonics.com/GreyhawkOptics/DovePrism/barbosa_pra_06.pdf

def QHA(pyzx=True):
	circ = QuantumCircuit(3)
	
	circ.h(2)
	circ = ccz(circ,0,1,2)
	circ.h(2)
	
	circ.cx(1,2)
	
	if pyzx is True:
		return zx.sqasm(circ.qasm(),simplify=False)
	else:
		return circ


"""Random Circuit"""

def RandoCirc(qubit_number=5,depth=50):
	
	return zx.generate.cliffords(qubit_number,depth)



"""Circuit"""





"""Circuit"""





