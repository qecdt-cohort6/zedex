# PyZX - Python library for quantum circuit rewriting 
#        and optimisation using the ZX-calculus
# Copyright (C) 2018 - Aleks Kissinger and John van de Wetering

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

try:
	import igraph as ig
except ImportError:
	print("python-igraph not available")
	ig = None

from .base import BaseGraph

class GraphIG(BaseGraph):
	"""Implementation of :class:`~graph.base.BaseGraph` using ``python-igraph`` 
	as its backend"""
	backend = 'igraph'
	def __init__(self):
		BaseGraph.__init__(self)
		self.graph = ig.Graph(directed=False)
		self.graph.vs['_a'] = None
		self.graph.vs['_t'] = None
		self.graph.vs['_q'] = None
		self.graph.vs['_r'] = None
		self.graph.es['_t'] = None
		self._maxq = -1
		self._maxr = -1
		self.inputs = []
		self.outputs = []

	# since igraph uses consecutive indexing, vindex() == num_vertices()
	def vindex(self):
		return self.num_vertices()

	def depth(self): 
		self._maxr = max(self._rindex.values())
		return self._maxr
	def qubit_count(self): return self._maxq + 1

	def add_vertices(self, amount, vertex_data=None):
		self.graph.add_vertices(amount)
		n = self.num_vertices()
		return range(n - amount, n)

	def add_edges(self, edges, edge_data=None):
		self.graph.add_edges(edges)

	def remove_vertices(self, vertices):
		self.graph.delete_vertices(vertices)

	def remove_isolated_vertices(self):
		self.graph.vs.select(_degree=0).delete()

	def remove_edges(self, edges):
		self.graph.delete_edges(edges)

	def num_vertices(self):
		return len(self.graph.vs)

	def num_edges(self):
		return len(self.graph.es)

	def vertices(self):
		return range(len(self.graph.vs))

	def edges(self):
		return range(len(self.graph.es))

	def edge(self, s, t):
		return self.graph.es[s,t][0].index
	
	def edge_st(self, edge):
		edge = self.graph.es[edge]
		return (edge.source, edge.target)

	def edge_s(self, edge):
		edge = self.graph.es[edge]
		return edge.source

	def edge_t(self, edge):
		edge = self.graph.es[edge]
		return edge.target

	def neighbours(self, vertex):
		return self.graph.neighbors(vertex)

	def vertex_degree(self, vertex):
		return self.graph.degree(vertex)

	def incident_edges(self, vertex):
		return self.graph.incident(vertex, mode=ig.ALL)

	def connected(self,v1,v2):
		return self.graph.are_connected(v1,v2)

	def edge_type(self, e):
		if e in self.graph.es:
			t = self.graph.es[e]['_t']
			return 1 if t == None else t
		else:
			return 0

	def set_edge_type(self, e, t):
		self.graph.es[e]['_t'] = t


	def type(self, v):
		t = self.graph.vs[v]['_t']
		return t if t != None else 0

	def types(self):
		return self.graph.vs['_t']

	def set_type(self, v, t):
		self.graph.vs[v]['_t'] = t
		
	def phase(self, vertex):
		a = self.graph.vs[vertex]['_a']
		return a if a != None else 0

	def phases(self):
		return [a if a != None else 0 for a in self.graph.vs['_a']]

	def set_phase(self, vertex, phase):
		self.graph.vs[vertex]['_a'] = phase % 2

	def qubit(self, vertex):
		return self.graph.vs[vertex]['_q'] or -1
	def qubits(self):
		return self.graph.vs['_q']
	def set_qubit(self, vertex, q):
		if q > self._maxq: self._maxq = q
		self.graph.vs[vertex]['_q'] = q

	def row(self, vertex):
		return self.graph.vs[vertex]['_r'] or -1
	def rows(self):
		return self.graph.vs['_r']
	def set_row(self, vertex, r):
		if r > self._maxr: self._maxr = r
		self.graph.vs[vertex]['_r'] = r

	def set_vdata(self, v, key, val):
		self.graph.vs[v][key] = val

	def vdata_keys(self, v):
		return [a for a in self.graph.vertex_attributes() if a != '_a' and a != '_t' and a != '_q' and a != '_r']

	def vdata(self, v, key, default=0):
		try:
			val = self.graph.vs[v][key]
			if not val: val = default
		except KeyError:
			val = default
		return val