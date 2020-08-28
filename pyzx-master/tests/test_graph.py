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

import unittest
from fractions import Fraction
import itertools
import sys
if __name__ == '__main__':
    sys.path.append('..')
    sys.path.append('.')

from pyzx.graph import Graph
from pyzx.generate import identity

try:
    import numpy as np
    from pyzx.tensor import compare_tensors
except ImportError:
    np = None


class TestGraphBasicMethods(unittest.TestCase):

    def test_empty_graph(self):
        g = Graph()
        self.assertEqual(g.num_vertices(),0)
        self.assertEqual(g.num_edges(),0)

    def test_add_remove_vertices(self):
        g = Graph()
        v = g.add_vertex()
        self.assertEqual(g.num_vertices(),1)
        g.add_vertices(3)
        self.assertEqual(g.num_vertices(),4)
        g.remove_vertex(v)
        self.assertEqual(g.num_vertices(),3)

    def test_edges(self):
        g = Graph()
        v1, v2, v3 = g.add_vertices(3)
        g.add_edge((v1,v2))
        self.assertEqual(g.num_edges(),1)
        self.assertTrue(g.connected(v1,v2))
        self.assertTrue(v2 in g.neighbours(v1))
        self.assertEqual(g.vertex_degree(v1), 1)
        self.assertFalse(g.connected(v1,v3))
        e = g.edge(v1,v2)
        self.assertEqual(g.edge_type(e),1)
        g.set_edge_type(e,2)
        self.assertEqual(g.edge_type(e),2)
        g.remove_edge(e)
        self.assertEqual(g.num_edges(),0)
        self.assertFalse(g.connected(v1,v2))

    def test_set_attributes(self):
        g = Graph()
        v = g.add_vertex()
        g.set_phase(v,1)
        self.assertEqual(g.phase(v),1)
        g.set_type(v,2)
        self.assertEqual(g.type(v),2)
        g.set_row(v,3)
        self.assertEqual(g.row(v),3)
        g.set_qubit(v,2)
        self.assertEqual(g.qubit(v),2)

    def test_add_edge_table_same_type(self):
        g = Graph()
        v1, v2 = g.add_vertices(2)
        g.set_type(v1,1)
        g.set_type(v2,1)
        etab = {(v1,v2):[2,0]}
        g.add_edge_table(etab)
        self.assertTrue(g.connected(v1,v2))
        self.assertEqual((g.phase(v1),g.phase(v2)),(0,0))
        g.remove_edge(g.edge(v1,v2))
        self.assertFalse(g.connected(v1,v2))
        etab = {(v1,v2):[0,2]}
        g.add_edge_table(etab)
        self.assertFalse(g.connected(v1,v2))
        etab = {(v1,v2): [1,1]}
        g.add_edge_table(etab)
        self.assertEqual(g.edge_type(g.edge(v1,v2)),1)
        self.assertTrue((g.phase(v1)==1  and g.phase(v2)==0) or (g.phase(v1)==0 and g.phase(v2)==1))

    def test_add_edge_table_different_type(self):
        g = Graph()
        v1, v2 = g.add_vertices(2)
        g.set_type(v1,1)
        g.set_type(v2,2)
        etab = {(v1,v2):[0,2]}
        g.add_edge_table(etab)
        self.assertTrue(g.connected(v1,v2))
        self.assertEqual((g.phase(v1),g.phase(v2)),(0,0))
        g.remove_edge(g.edge(v1,v2))
        self.assertFalse(g.connected(v1,v2))
        etab = {(v1,v2):[2,0]}
        g.add_edge_table(etab)
        self.assertFalse(g.connected(v1,v2))
        etab = {(v1,v2): [1,1]}
        g.add_edge_table(etab)
        self.assertEqual(g.edge_type(g.edge(v1,v2)),2)
        self.assertTrue((g.phase(v1)==1  and g.phase(v2)==0) or (g.phase(v1)==0 and g.phase(v2)==1))

    def test_copy(self):
        g = Graph()
        v1, v2 = g.add_vertices(2)
        g.add_edge((v1,v2),2)
        g2 = g.copy()
        self.assertEqual(g.num_vertices(),g2.num_vertices())
        self.assertEqual(g.num_edges(),g2.num_edges())
        v1, v2 = list(g2.vertices())
        self.assertEqual(g.edge_type(g.edge(v1,v2)),2)

    @unittest.skipUnless(np, "numpy needs to be installed for this to run")
    def test_remove_isolated_vertex_preserves_semantics(self):
        g = Graph()
        v = g.add_vertex(1,0,0)
        g2 = g.copy()
        g2.remove_isolated_vertices()
        self.assertTrue(compare_tensors(g,g2))
        self.assertEqual(g2.scalar.to_number(),2)
        g.set_phase(v,Fraction(1))
        g2 = g.copy()
        g2.remove_isolated_vertices()
        self.assertTrue(compare_tensors(g,g2))
        self.assertAlmostEqual(g2.scalar.to_number(),0)

    @unittest.skipUnless(np, "numpy needs to be installed for this to run")
    def test_remove_isolated_pair_preserves_semantics(self):
        for i,j,k in itertools.product([1,2],repeat=3):
            for phase1, phase2 in itertools.product([0,1,2],[0,4,5]):
                with self.subTest(i=i,j=j,k=k,phase1=phase1,phase2=phase2):
                    g = Graph()
                    v = g.add_vertex(i,0,0,phase=phase1)
                    w = g.add_vertex(j,1,0,phase=phase2)
                    g.add_edge((v,w),k)
                    g2 = g.copy()
                    g2.remove_isolated_vertices()
                    self.assertEqual(g2.num_vertices(),0)
                    self.assertTrue(compare_tensors(g,g2))

class TestGraphCircuitMethods(unittest.TestCase):

    def setUp(self):
        """Sets up a two qubit circuit containing a single CNOT with some phases."""
        self.graph = Graph()
        g = self.graph
        i1 = g.add_vertex(0,0,0) #add_vertex(type,qubit_index,row_index,phase=0)
        i2 = g.add_vertex(0,1,0)
        g.inputs = [i1,i2]
        v = g.add_vertex(1,0,1,Fraction(1,2))
        w = g.add_vertex(2,1,1,Fraction(1,1))
        o1 = g.add_vertex(0,0,2)
        o2 = g.add_vertex(0,1,2)
        g.outputs = [o1, o2]
        g.add_edges([(i1,v),(i2,w),(v,w),(v,o1),(w,o2)])
        self.i1, self.i2, self.v, self.w, self.o1, self.o2 = i1, i2, v, w, o1, o2

    def test_qubit_index_and_depth(self):
        g = self.graph
        self.assertEqual(g.depth(),2)
        self.assertEqual(g.qubit_count(),2)

    def test_adjoint(self):
        g = self.graph
        adj = g.adjoint()
        self.assertEqual(g.num_vertices(),adj.num_vertices())
        self.assertEqual(g.num_edges(),adj.num_edges())
        self.assertEqual(g.depth(), adj.depth())
        self.assertEqual(g.qubit_count(), adj.qubit_count())

        v = [i for i in g.vertices() if g.type(i)==1][0]
        w = [i for i in adj.vertices() if adj.type(i)==1][0]
        self.assertEqual(g.phase(v),(-adj.phase(v))%2)
        self.assertEqual(g.vertex_degree(v),adj.vertex_degree(w))

    def test_compose_basic(self):
        g = self.graph.copy()
        g.compose(g)
        self.assertEqual((len(g.inputs),len(g.outputs)),(2,2))

    def test_compose_unitary(self):
        g = self.graph
        g.set_edge_type(g.edge(self.v,self.o1),2)
        g2 = g.adjoint()
        g2.compose(g)
        self.assertTrue(compare_tensors(g2,identity(2), False))

if __name__ == '__main__':
    unittest.main()