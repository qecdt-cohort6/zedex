"""Dictionaries of the architectures"""

ibmq_16_melbourne = {
	"qubits":{
	0:{"fidelity":4.905E-4},
	1:{"fidelity":1.064E-3},
	2:{"fidelity":5.315E-4},
	3:{"fidelity":5.906E-4},
	4:{"fidelity":6.344E-4},
	5:{"fidelity":2.217E-3},
	6:{"fidelity":1.510E-3},
	7:{"fidelity":1.989E-3},
	8:{"fidelity":9.986E-4},
	9:{"fidelity":2.149E-3},
	10:{"fidelity":2.632E-3},
	11:{"fidelity":9.882E-4},
	12:{"fidelity":1.399E-3},
	13:{"fidelity":1.662E-3},
	14:{"fidelity":7.760E-4}
	},

	"connections":[
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

ibmq_london = {
	"qubits":{
	0:{"fideliy":1.365E-3},
	1:{"fideliy":3.532E-4},
	2:{"fideliy":4.474E-4},
	3:{"fideliy":3.177E-4},
	4:{"fideliy":3.831E-4}
	},

	"connections":[
	{"source":0, "target":1, "fidelity":1.599E-2},
	{"source":1, "target":2, "fidelity":9.855E-3},
	{"source":1, "target":3, "fidelity":1.081E-2},
	{"source":3, "target":4, "fidelity":1.736E-2}]
}

ibmq_burlington = {
	"qubits":{
	0:{"fideliy":3.638E-4},
	1:{"fideliy":5.280E-4},
	2:{"fideliy":1.414E-3},
	3:{"fideliy":4.813E-4},
	4:{"fideliy":3.667E-4}
	},

	"connections":[
	{"source":0, "target":1, "fidelity":8.556E-3},
	{"source":1, "target":2, "fidelity":2.358E-2},
	{"source":1, "target":3, "fidelity":1.674E-2},
	{"source":3, "target":4, "fidelity":1.056E-2}]
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


default_qubits = {
    "q1":[[0],[1],[2],[3],[4],[5]],
    "q2":[[4, 10],[1, 13],[11, 12],[5, 4],[2, 12],[14, 13]],
    "q3":[[13, 1, 2],[9, 10, 5],[12, 2, 11],[13, 1, 0],[2, 3, 12],
          [11, 3, 4],[9, 5, 6],[8, 9, 6],[3, 2, 12],[9, 10, 5]],
    "q4":[[5, 4, 3, 6],[3, 4, 10, 2],[1, 2, 0, 12],[3, 11, 4, 12],
          [13, 14, 12, 1],[10, 4, 9, 11],[9, 5, 8, 10],[10, 9, 4, 11],
          [10, 4, 9, 5],[2, 1, 13, 12],[5, 6, 8, 9],[0,1,13,14]],
    "q5":[[13, 12, 14, 1, 0],[4, 3, 11, 2, 10],[1, 13, 12, 14, 2],
          [5, 4, 9, 8, 10],[8, 6, 9, 5, 7],
          [13, 14, 12, 11, 2],[11, 12, 10, 3, 9],[0, 1, 2, 12, 3],
          [9, 10, 5, 8, 11],[3, 4, 5, 6, 9],
          [7, 8, 9, 10, 4],[5, 6, 4, 10, 8],[2, 1, 13, 14, 3],
          [3, 2, 12, 4, 13],[7, 8, 4, 9, 5]],
    "q6":[[0, 1, 2, 12, 13, 14],[4, 5, 6, 8, 9, 10],
          [0, 1, 13, 12, 11, 3],[3, 4, 5, 6, 8, 7],
          [0, 1, 2, 3, 12, 13],[8, 9, 10, 11, 4, 5],
          [4, 5, 6, 7, 8, 9],[1, 2, 3, 14, 13, 12],
          [0, 1, 2, 3, 13, 14],[4, 5, 7, 8, 9, 10]],
    "q7":[[0,1,2,3,12,13,14],[4,5,6,7,8,9,10],
          [0,1,2,3,4,5,6],[14,13,12,11,10,9,8],
          [0,1,2,3,4,14,13],[7,8,9,10,11,3,4],
          [0,1,2,3,4,12,13],[7,8,9,10,11,5,4],
          [14,1,2,3,4,12,13],[7,8,9,10,3,5,4],
          [0,1,2,3,4,5,13],[7,8,9,10,11,12,3],
          [0,1,2,3,4,5,12],[7,8,9,10,11,12,4],
          [0,1,2,3,4,13,11],[7,8,9,10,11,4,6]],
    "q8":[[0,1,2,3,14,13,12,11],[3,4,5,6,11,10,9,8],
          [7,8,9,10,11,12,13,14],[0,1,13,12,11,3,4,5],
          [0,1,2,3,4,5,14,13],[7,8,9,10,11,12,2,3],
          [0,1,2,3,4,5,13,12],[7,8,9,10,11,12,3,4],
          [0,1,2,3,4,5,11,12],[13,8,9,10,11,12,3,4],
          [14,1,2,3,4,5,13,12],[7,8,9,10,11,2,3,4],
          [13,14,2,3,4,5,11,12],[1,8,9,10,11,2,3,4],
          [0,1,2,3,4,5,6,12],[7,8,9,10,11,12,13,4]],
    "q9":[[0,1,2,3,4,14,13,12,11],[3,4,5,6,11,10,9,8,7],
          [7,8,9,10,11,12,13,14,0],
          [0,1,2,3,4,5,14,13,12],[2,3,4,12,11,10,9,8,7],
          [0,1,2,3,4,5,13,12,11],[3,4,5,12,11,10,9,8,7],
          [14,1,2,3,4,5,13,12,11],[3,4,5,2,11,10,9,8,7],
          [0,1,2,3,4,5,6,14,13],[7,8,9,10,11,12,13,1,2],
          [0,1,2,3,4,5,6,12,13],[7,8,9,10,11,12,13,3,2],
          [0,1,2,3,4,5,6,12,11],[7,8,9,10,11,12,13,3,4],
          [1,2,3,4,5,6,12,13,14],[7,8,9,10,11,12,1,3,2],
          [13,14,2,3,4,5,6,12,11],[7,8,9,10,11,1,2,3,4],
          [7,8,9,10,11,12,13,14,1],[7,8,9,10,11,12,13,14,6],
          [7,8,9,10,11,12,13,14,2],[7,8,9,10,11,12,13,14,5],
          [7,8,9,10,11,12,13,14,3],[7,8,9,10,11,12,13,14,4]],
    "q10":[[0,1,2,3,4,10,11,12,13,14],[2,3,4,5,6,8,9,10,11,12],
           [0,1,2,3,4,5,10,11,12,13],[2,3,4,5,6,8,9,10,11,12],
           [0,1,2,3,4,5,14,13,12,11],[3,4,5,6,7,12,11,10,9,8],
           [0,1,7,8,9,10,11,12,13,14]],
}


def choose_qubits(n=5,arq=ibmq_16_melbourne):
    import random
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


def arch_visual(arch,tech=ibmq_16_melbourne,prefix = "Arch",folder = ""):
	import matplotlib.pyplot as plt
	import numpy as np
	for i in range(len(arch)):
		arch[i] = str(arch[i])
	
	ploty = {
		"0":{"x":0.5,"y":1.5},
		"1":{"x":1.5,"y":1.5},
		"2":{"x":2.5,"y":1.5},
		"3":{"x":3.5,"y":1.5},
		"4":{"x":4.5,"y":1.5},
		"5":{"x":5.5,"y":1.5},
		"6":{"x":6.5,"y":1.5},
		"7":{"x":7.5,"y":0.5},
		"8":{"x":6.5,"y":0.5},
		"9":{"x":5.5,"y":0.5},
		"10":{"x":4.5,"y":0.5},
		"11":{"x":3.5,"y":0.5},
		"12":{"x":2.5,"y":0.5},
		"13":{"x":1.5,"y":0.5},
		"14":{"x":0.5,"y":0.5}
	}

	fig, ax = plt.subplots()

	for item in tech["connections"]:
		s = str(item["source"])
		t = str(item["target"])
		c = item['fidelity']
		c_norm = ((c*1E2)-1)/(8-1)
		#print(c_norm)
		if s in arch and t in arch:
			
			if ploty[s]["x"] > ploty[t]["x"]:
				xxs = [ploty[s]["x"]-0.2,ploty[t]["x"]+0.2]
			elif ploty[s]["x"] < ploty[t]["x"]:
				xxs = [ploty[s]["x"]+0.2,ploty[t]["x"]-0.2]
			else:
				xxs = [ploty[s]["x"],ploty[t]["x"]]

			if ploty[s]["y"] > ploty[t]["y"]:
				yys = [ploty[s]["y"]-0.2,ploty[t]["y"]+0.2]
			elif ploty[s]["y"] < ploty[t]["y"]:
				yys = [ploty[s]["y"]+0.2,ploty[t]["y"]-0.2]
			else:
				yys = [ploty[s]["y"],ploty[t]["y"]]

				
			RGB = [0.9,1-c_norm,1]
			ax.plot(xxs,yys,color=RGB,linewidth=7.0,zorder=0)
			ax.set_axisbelow(True)

	xs = []
	ys = []
	for item in arch:
		c = tech["qubits"][float(item)]['fidelity']
		c_norm = (((c*1E3)-0.4)/(3-0.4))
		RGB = [0,0.8,c_norm]

		ax.add_artist(plt.Circle((ploty[item]["x"], 
								  ploty[item]["y"]), 
								  0.3,
								  linewidth=1,
								  color = RGB,
								  zorder=9))
		ax.add_artist(plt.Circle((ploty[item]["x"], 
								  ploty[item]["y"]), 
								  0.3,
								  linewidth=1,
								  fill=False,
								  color = [0,0,0],
								  zorder=10))
		ax.annotate(item,
					xy=(ploty[item]["x"],ploty[item]["y"]-0.13),
					fontsize=15,
					ha="center",
					zorder=10)
		xs.append(ploty[item]["x"])
		ys.append(ploty[item]["y"])

	ax.axis('off')   

	
	if min(xs) == max(xs):
		
		ax.set(xlim=[min(xs)-0.5, max(xs)+2],
		   ylim=[min(ys)-2.5, max(ys)+0.5],aspect=1)

		ax.plot([min(xs),max(xs)+1,max(xs)+1,min(xs),min(xs)],
				[min(ys)-0.5-0.7,min(ys)-0.5-0.7,
				 min(ys)-0.5-0.3,min(ys)-0.5-0.3,min(ys)-0.5-0.7],
				 color=[0,0,0],zorder=10)
		ax.annotate("CNOT error rate",xy=(min(xs),min(ys)-0.5-0.2))
		ax.annotate("1E-2",xy=(min(xs),min(ys)-0.5-0.87),fontsize=7)
		ax.annotate("8E-2",xy=(max(xs)+1-0.35,min(ys)-0.5-0.87),fontsize=7)
		for i in np.linspace(min(xs),max(xs)+1,500):
			c = (i-min(xs))/(max(xs)-min(xs)+1)
			ax.plot([i,i],[min(ys)-0.5-0.3,min(ys)-0.5-0.7],color=[0.9,1-c,1])

		ax.plot([min(xs),max(xs)+1,max(xs)+1,min(xs),min(xs)],
				[min(ys)-0.5-1.65,min(ys)-0.5-1.65,
				 min(ys)-0.5-1.25,min(ys)-0.5-1.25,min(ys)-0.5-1.65],
				 color=[0,0,0],zorder=10)
		ax.annotate("Single-qubit error rate",xy=(min(xs),min(ys)-0.5-1.15))
		ax.annotate("4E-4",xy=(min(xs),min(ys)-0.5-1.82),fontsize=7)
		ax.annotate("3E-3",xy=(max(xs)+1-0.35,min(ys)-0.5-1.82),fontsize=7)
		for i in np.linspace(min(xs),max(xs)+1,500):
			c = (i-min(xs))/(max(xs)-min(xs)+1)
			ax.plot([i,i],[min(ys)-0.5-1.25,min(ys)-0.5-1.65],color=[0,0.8,c])
		
		
	else:
		
		ax.set(xlim=[min(xs)-0.5, max(xs)+0.5],
		   ylim=[min(ys)-2.5, max(ys)+0.5],aspect=1)

		ax.plot([min(xs),max(xs),max(xs),min(xs),min(xs)],
				[min(ys)-0.5-0.7,min(ys)-0.5-0.7,
				 min(ys)-0.5-0.3,min(ys)-0.5-0.3,min(ys)-0.5-0.7],
				 color=[0,0,0],zorder=10)
		ax.annotate("CNOT error rate",xy=(min(xs),min(ys)-0.5-0.2))
		ax.annotate("1E-2",xy=(min(xs),min(ys)-0.5-0.87),fontsize=7)
		ax.annotate("8E-2",xy=(max(xs)-0.35,min(ys)-0.5-0.87),fontsize=7)
		for i in np.linspace(min(xs),max(xs),500):
			c = (i-min(xs))/(max(xs)-min(xs))
			ax.plot([i,i],[min(ys)-0.5-0.3,min(ys)-0.5-0.7],color=[0.9,1-c,1])

		ax.plot([min(xs),max(xs),max(xs),min(xs),min(xs)],
				[min(ys)-0.5-1.65,min(ys)-0.5-1.65,
				 min(ys)-0.5-1.25,min(ys)-0.5-1.25,min(ys)-0.5-1.65],
				color=[0,0,0],zorder=10)
		ax.annotate("Single-qubit error rate",xy=(min(xs),min(ys)-0.5-1.15))
		ax.annotate("4E-4",xy=(min(xs),min(ys)-0.5-1.82),fontsize=7)
		ax.annotate("3E-3",xy=(max(xs)-0.35,min(ys)-0.5-1.82),fontsize=7)
		for i in np.linspace(min(xs),max(xs),500):
			c = (i-min(xs))/(max(xs)-min(xs))
			ax.plot([i,i],[min(ys)-0.5-1.25,min(ys)-0.5-1.65],color=[0,0.8,c])
			


	fig.savefig("".join([folder,prefix,"_","_".join(arch),".png"]))
