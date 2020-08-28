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
import json
from fractions import Fraction
import pyzx as zx
__all__ = ['init', 'draw']
try:
   in_webpage = True
   javascript_location = '/js/scripts'
except ImportError:
   in_webpage = False
# Provides functions for displaying pyzx graphs in jupyter notebooks using d3
_d3_display_seq = 0
# javascript_location = '../js'
# TODO: avoid duplicate (copied from drawing.py)
def phase_to_s(a, t):
    if (a == 0 and t != 3): return 0
    if (a == 1 and t == 3): return 0
    if not isinstance(a, Fraction):
        a = Fraction(a)
    ns = 1 if a.numerator == 1 else a.numerator
    ds = 1 if a.denominator == 1 else a.denominator
    # unicode 0x03c0 = pi
    return ns/ds
def draw(g, arqq, qasm, scale=None, auto_hbox=True, labels=False):
    global _d3_display_seq
    if not in_webpage: 
        raise Exception("This method only works when loaded in a webpage or Jupyter notebook")
    if not hasattr(g, 'vertices'):
        g = g.to_graph(zh=True)

    g = zx.circuit.Circuit.from_qasm(qasm).to_graph()

    _d3_display_seq += 1
    seq = _d3_display_seq
    if scale == None:
        scale = 800 / (g.depth() + 2)
        if scale > 50: scale = 50
        if scale < 20: scale = 20
    node_size = 0.2 * scale
    if node_size < 2: node_size = 2
    w = (g.depth() + 2) * scale
    h = (g.qubit_count() + 3) * scale
    nodes = [{'name': str(v),
              'x': (g.row(v) + 1) * scale,
              'y': (g.qubit(v) + 2) * scale,
              't': g.type(v),
              'phase': phase_to_s(g.phase(v), g.type(v)) }
             for v in g.vertices()]
    links = [{'source': str(g.edge_s(e)),
              'target': str(g.edge_t(e)),
              't': g.edge_type(e) } for e in g.edges()]
    graphj = json.dumps({'nodes': nodes, 'links': links})

    connectivity = json.dumps(arqq)
    #Outputting the HTML version of the graph, turned into a javascript object
    #Seperation is as  the .format was having trouble with the curly brackets
    #not the prettiest but works
    html1 = """<!DOCTYPE html>
    <meta charset="utf-8">
    <style> body { font-family: sans-serif; }
.pyzx_graph_div {
  zoom:1;
  margin: 10px 50px 20px;
  width: 100%;
  height: 30%;
  position:relative;
}
.opt_circ {
  zoom: 0.35;
  font-size: 15pt;
  float: right;
  position:relative;
}
.div3 {
  margin: auto;
  text-align: center;
  width: 10%;
  border: 3px solid red;
  font-size: 10px;
  position:relative;
}
.div5 {
  margin: auto;
  text-align: center;
  width: 50%;
  border: 3px solid red;
  font-size: 10px;
  position:relative;
}
.org_circ {
  zoom: 0.35;
  float:left;
  position:relative;
}
.title_box {
  text-align: center;
  width: 100%;
  height:4%;
  border: 3px solid green;
  font-size: 20px;
  position: relative;
}
body{width: 95%;height: 95%;}
    </style>
    <body>
        <div class="title_box"><p>Zedex: Pre-Alpha testing</p></div>
        <div class="div3" id="score"></div>
        <div class="div5"  id="stats"></div>
        <div  class="pyzx_graph_div"  id="graph-output-1" ></div>
        <div class="opt_circ" title="Optimised Circuit" id="circuit"></div>
        <div  class="org_circ" style="float:left" title="Original Circuit"  id="old_circuit"></div>
    <script type="text/javascript" src="https://unpkg.com/quantum-circuit"></script>
    <script src="require.js"></script>
    <!--<script>window.languagePluginUrl = "https://de-luxham.github.io/web/";</script>-->
    
    <script type="text/javascript" src="https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.js"></script>
    
    <script type="text/javascript">
    
     require.config({
            paths: {
                    "d3": "d3.v4.min",
                    "pyzx": "pyzx",
                    "pyodid": "pyodide" //This is a CDN and could be unstable, long term should be changed to local files pyodide.js
                    }
            });"""
    html2= """require(['pyzx'], function(pyzx) {{
            pyzx.showGraph('#graph-output-1',
            JSON.parse('{1}'), {2}, {3}, {4} ,JSON.parse('{5}') ,`{6}`);
        }});
        </script>""".format(seq, graphj, w, h, node_size, connectivity, qasm) 
    html3="""
    <script type="text/javascript">
    require(['pyodid'], function(pyodid) {
             languagePluginLoader.then(function ()  {
             console.log(pyodide.runPython('import sys'));
             console.log(pyodide.runPython(`print('hello world')`));
             });
             languagePluginLoader.then(() => {
             console.log(self.pyodide.runPython(`print('hello world')`));
             });
        });
        </script>
    """
    return html1+html2


    