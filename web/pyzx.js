

define(['d3'], function(d3) {

    //require(['pyodid'], function(pyodid) {
        languagePluginLoader.then(function ()  {
        pyodide.runPython('print("python is a go!")');
        });  
    //})

    pythonCode = `
      def do_work(*args):
          import networkx as nx
          print("network imported")
          import pyzx as zx
          print("pyzx imported")
          graph = zx.generate.cliffords(3, 3)
          print(graph)
          print("HELLO WORLD")
      
      

      import micropip
      micropip.install(['networkx','pyzx']).then(do_work)`
      languagePluginLoader.then(() => {
        return pyodide.loadPackage(['micropip'])
      }).then(() => {
        pyodide.runPython(pythonCode);
      })
     

    // styling functions
    function nodeColor(t) {
        if (t == 0) return "black";
        else if (t == 1) return "green";
        else if (t == 2) return "red";
        else if (t == 3) return "yellow";
        else if (t == 4) return "blue";
    }

    function edgeColor(t) {
        if (t == 1) return "black";
        else if (t == 2) return "#08f";
    }

    function nodeStyle(selected) {
        return selected ? "stroke-width: 2px; stroke: #00f" : "stroke-width: 1.5px";
    }

    return {
    showGraph: function(tag, graph, width, height, node_size, connectivity, qasm_string) {

        
        var connectivity_string =JSON.stringify(connectivity.connections);

        console.log(qasm_string)
        console.log(connectivity_string)


        //Basic connectivity example
        //connectivity = {connections:[{source:0,target:1,fidelity:1.599E-2,t:1,index:0},{source:1,target:2,fidelity:9.855E-3,t:1,index:1},{source:2,target:3,fidelity:2.855E-3,t:1,index:2},{source:3,target:4,fidelity:4.855E-3,t:1,index:2}]};
        //connectivity = conn_placeholder;
        //calculate min max fidelities for colour coding
        var max_colour = Math.max.apply(Math, connectivity.connections.map(function(o) { return o.fidelity; }));
        var min_colour = Math.min.apply(Math, connectivity.connections.map(function(o) { return o.fidelity; }));

        //function def to map fidelitleys to colour scale 100-200 for now
        function colour_scale(x) {
            return "rgb(0,0,"+((x-min_colour)/(max_colour-min_colour)*256).toString() +")"
        }
        
        //string to store the rules applied
        var rule_string = "[]";
        
        var ntab = {};
        //hard coded option for node size 
        node_size = 9
        scale = 1;
        auto_hbox = false;
        show_labels = true;
        
        graph.nodes.forEach(function(d) {
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
        });

        var spiders_and_boundaries = graph.nodes.filter(function(d) {
            return d.t != 3;
        });

        graph.links.forEach(function(d) {
            var s = ntab[d.source];
            var t = ntab[d.target];
            d.source = s;
            d.target = t;
            s.nhd.push(t);
            t.nhd.push(s);
        });

        var shiftKey;
        
        //New var added for force simulation
        var simulation = d3.forceSimulation()
        .force("link", d3.forceLink()
        .id(function(d) { return d.id; }).strength(0))  //sim off for now
        //.force("charge", d3.forceManyBody().strength(-20))
        //.force("center", d3.forceCenter(width / 2, height / 2))
    

        
        // SETUP SVG ITEMS

        var svg = d3.select(tag)
            //.attr("tabindex", 1)
            .on("keydown.brush", function() {shiftKey = d3.event.shiftKey || d3.event.metaKey;})
            .on("keyup.brush", function() {shiftKey = d3.event.shiftKey || d3.event.metaKey;})
            //.each(function() { this.focus(); })
            .append("svg")
            .attr("style", "max-width: none; max-height: none")
            .attr("width", width+50)
            .attr("height", height +50);
            //added offset to dimensions of canvas


        //Set up connectivity graph inbetween these lines
        //Connectivity Graph
        //This section generates a directed graph underneath the input qubits 
        //It shows the connectivity between the qubits
        
        var num_qubits = (graph.nodes.filter(function(d) {return d.t == 0;}).length)/2;
        var qnodes = []

        for (let i = 0; i < num_qubits; i++) {
            qnodes.push({name:i, x:graph.nodes[i].x, y:graph.nodes[i].y, t:4,empty:false, phase:'', selecetd:false, previouslySelected:false, index:i, vy:0, vx:0});
        }

        //updates the connectivity object with node object data
        for (let i = 0; i < connectivity.connections.length; i++) {

            // connectivity.connections[i].source = graph.nodes[connectivity.connections[i].source];
            // connectivity.connections[i].target = graph.nodes[connectivity.connections[i].target];
            connectivity.connections[i].source = qnodes[connectivity.connections[i].source];
            connectivity.connections[i].target = qnodes[connectivity.connections[i].target];
        }

        var connectivity_graph = {nodes: qnodes,links:connectivity.connections};
        console.log(connectivity_graph);


        //draw circuit
            
        var circuit_old = new QuantumCircuit();
            circuit_old.importQASM(qasm_string, function(errors) {
                console.log(errors);
        });
        // Assuming we have <div id="drawing"></div> somewhere in HTML
        var old_circ_container = document.getElementById("old_circuit");
        // SVG is returned as string
        var svg2 = circuit_old.exportSVG(true);

        // add SVG into container
        old_circ_container.innerHTML = svg2;
    
        // build the arrow.
        svg.append("svg:defs").selectAll("marker")
           .data(["end"])      // Different link/path types can be defined here
           .enter().append("svg:marker")    // This section adds in the arrows
           .attr("id", String)
           .attr("viewBox", "0 -5 10 10")
           .attr("refX", 15)
           .attr("refY", -1.5)
           .attr("markerWidth", 6)
           .attr("markerHeight", 6)
           .attr("orient", "auto")
           .append("svg:path")
           .attr("d", "M0,-5L10,0L0,5");
        
           //x offset variable for drawing curves for connectivity graph
       var x_off = -100;
       var clink  = svg.append("g")
       .attr("class", "link")
       .selectAll("line")
       .data(connectivity_graph.links)
       .enter().append("path")
       .attr("stroke", function(d) {return colour_scale(d.fidelity)})
       .attr("style", "stroke-width: 1.5px")
       //.attr("marker-end", "url(#end)")
       .attr("d",function(d) {
           console.log("M" + d.source.x + "," + d.source.y  + ","+"Q" + (d.source.x+d.target.x)/2 + x_off + "," + (d.source.y+d.target.y)/2 + "," + d.target.x + "," +d.target.y);
           return "M" + d.source.x + "," + d.source.y + ","+ "Q" + ((parseFloat(d.source.x)+parseFloat(d.target.x)/2) + parseFloat(x_off)).toString() + "," + (d.source.y+d.target.y)/2 + "," + d.target.x + "," +d.target.y
       })
       .attr("fill", "none");

       
       var cnode = svg.append("g")
           .attr("class", "node")
           .selectAll("g")
           .data(connectivity_graph.nodes)
           .enter().append("g")
           .attr("transform", function(d) {
               return "translate(" + d.x + "," + d.y +")";
           });

       cnode.append("circle")
           .attr("r", function(d) {
              return 0.75*node_size;
           })
           .attr("fill", function(d) { return nodeColor(d.t); })
           .attr("stroke", "black");


        //End of connectivity graph setup

        var link = svg.append("g")
            .attr("class", "link")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke", function(d) { return edgeColor(d.t); })
            .attr("style", "stroke-width: 1.5px")
            .attr("class", "link").on("click", function(d) { console.log("clicked");});

        //added new attribute name, type and nhd
        
        var node = svg.append("g")
            .attr("class", "node")
            .selectAll("g")
            .data(graph.nodes)
            .enter().append("g")
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y +")";
            });

        node.filter(function(d) { return d.t != 3; })
            .append("circle")
            .attr("r", function(d) {
               if (d.t == 0) return 0.5 * node_size;
               else return node_size;
            })
            .attr("fill", function(d) { return nodeColor(d.t); })
            .attr("stroke", "black");

        var hbox = node.filter(function(d) { return d.t == 3; });

        hbox.append("rect")
            .attr("x", -0.75 * node_size).attr("y", -0.75 * node_size)
            .attr("width", node_size * 1.5).attr("height", node_size * 1.5)
            .attr("fill", function(d) { return nodeColor(d.t); })
            .attr("stroke", "black");

        node.filter(function(d) { return d.phase != ''; })
            .append("text")
            .attr("y", 0.7 * node_size + 14)
            .text(function (d) { return d.phase })
            .attr("text-anchor", "middle")
            .attr("font-size", "12px")
            .attr("font-family", "monospace")
            .attr("fill", "#00d");

        if (show_labels) {
            node.append("text")
                .attr("y", -0.7 * node_size - 5)
                .text(function (d) { return d.name; })
                .attr("text-anchor", "middle")
                .attr("font-size", "8px")
                .attr("font-family", "monospace")
                .attr("fill", "#ccc");
        }

        
        
       

    

    
        //New variables added between these lines
        //dimension variables have offsets, hard coded for now but that may change
        var width = svg.attr("width")+100,
            height = svg.attr("height")+100,
            radius = node_size;

        var node_count = graph.nodes.length-1,
            link_count = graph.links.length-1;
        
        
        
        //variable to hold slice graphic
        var slice = svg.append("g")
            .attr("class", "link")
            .append("line")
            .attr("stroke", "black")
            .attr("style", "stroke-width: 1.5px")
            .attr("id", "slice");

        //Trying Slice implementation without graphic
        var slice_nog = {x1:null, y1: null, x2: null, y2:null};
            
        var rule_applied = false;
        

        
        //End of new variables
        
        //New functions added between these lines
        
        //graph update
        function update() {
        
        console.log("graph updated");
        
        

            
            svg.selectAll("g").remove();

            clink  = svg.append("g")
       .attr("class", "link")
       .selectAll("line")
       .data(connectivity_graph.links)
       .enter().append("path")
       .attr("stroke", function(d) {return colour_scale(d.fidelity)})
       .attr("style", "stroke-width: 1.5px")
       //.attr("marker-end", "url(#end)")
       .attr("d",function(d) {
           console.log("M" + d.source.x + "," + d.source.y  + ","+"Q" + (d.source.x+d.target.x)/2 + x_off + "," + (d.source.y+d.target.y)/2 + "," + d.target.x + "," +d.target.y);
           return "M" + d.source.x + "," + d.source.y + ","+ "Q" + ((parseFloat(d.source.x)+parseFloat(d.target.x)/2) + parseFloat(x_off)).toString() + "," + (d.source.y+d.target.y)/2 + "," + d.target.x + "," +d.target.y
       })
       .attr("fill", "none");
         
                
                 cnode = svg.append("g")
                    .attr("class", "node")
                    .selectAll("g")
                    .data(connectivity_graph.nodes)
                    .enter().append("g")
                    .attr("transform", function(d) {
                        return "translate(" + d.x + "," + d.y +")";
                    });
         
                cnode.append("circle")
                    .attr("r", function(d) {
                       return 0.75*node_size;
                    })
                    .attr("fill", function(d) { return nodeColor(d.t); })
                    .attr("stroke", "black");
         
                    clink.attr("x1", function(d) { return d.source.x; })
                 .attr("y1", function(d) { return d.source.y; })
                 .attr("x2", function(d) { return d.target.x; })
                 .attr("y2", function(d) { return d.target.y; }); 
            
            
            
            
            link = svg.append("g")
            .attr("class", "link").selectAll("line").data(graph.links).enter().append("line")
            .attr("stroke", function(d) { return edgeColor(d.t); })
            .attr("style", "stroke-width: 1.5px");
            
            node = svg.append("g")
                .attr("class", "node")
                .selectAll("g")
                .data(graph.nodes)
                .enter()
                .append("g")
                .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y +")";
            });
            
            

        

        node.filter(function(d) { return d.t != 3; })
            .append("circle")
            .attr("r", function(d) {
               if (d.t == 0) return 0.5 * node_size;
               else return node_size;
            })
            .attr("fill", function(d) { return nodeColor(d.t); })
            .attr("stroke", "black");

         hbox = node.filter(function(d) { return d.t == 3; });

        hbox.append("rect")
            .attr("x", -0.75 * node_size).attr("y", -0.75 * node_size)
            .attr("width", node_size * 1.5).attr("height", node_size * 1.5)
            .attr("fill", function(d) { return nodeColor(d.t); })
            .attr("stroke", "black");

        node.filter(function(d) { return d.phase != ''; })
            .append("text")
            .attr("y", 0.7 * node_size + 14)
            .text(function (d) { return d.phase })
            .attr("text-anchor", "middle")
            .attr("font-size", "12px")
            .attr("font-family", "monospace")
            .attr("fill", "#00d");

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
            
        if (show_labels) {
            node.append("text")
                .attr("y", -0.7 * node_size - 5)
                .text(function (d) { return d.name; })
                .attr("text-anchor", "middle")
                .attr("font-size", "8px")
                .attr("font-family", "monospace")
                .attr("fill", "#ccc");
                }
        
        simulation
                .nodes(graph.nodes.filter(function(d) {return d.t != 0;}))
                .on("tick", ticked);
      
        simulation.force("link")
                .links(graph.links);     
              
            
            console.log(connectivity_graph);
            console.log(graph);
            
            //BIG ASS TEST CODE TEMPOARY BETWEEN THESE LINES
            
            node.on("mousedown", function(d) {
                /*if (shiftKey) {
                    d3.select(this).select(":first-child").attr("style", nodeStyle(d.selected = !d.selected));
                    d3.event.stopImmediatePropagation();
                } else if (!d.selected) {
                    node.select(":first-child").attr("style", function(p) { return nodeStyle(p.selected = d === p); });*/
                    
                    //New stuff for when a node is selected
                
                    d.selected = true;
                    
                    console.log(graph.nodes.filter(function(d) {return d.selected;})[0]);
                    
                    simulation.alphaTarget(0.05).restart();
                    
                //}
            })
            .call(d3.drag().on("drag", function(d) {
                var dx = d3.event.dx;
                var dy = d3.event.dy;
                // node.filter(function(d) { return d.selected; })
                //     .attr("cx", function(d) { return d.x += dx; })
                //     .attr("cy", function(d) { return d.y += dy; });
            
                //added this thing for the force stuf
                simulation.alphaTarget(0.05).restart();
                
                console.log(rule_applied);
                
                if (rule_applied == false) {
                
                    node.filter(function(d) { return d.selected; })
                    .attr("transform", function(d) {
                        d.x += dx;
                        d.y += dy;
                        return "translate(" + d.x + "," + d.y +")";
                    });

                    update_hboxes();

                    link.filter(function(d) { return d.source.selected ||
                                            (auto_hbox && d.source.t == 3); })
                    .attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; });

                    link.filter(function(d) { return d.target.selected ||
                                            (auto_hbox && d.target.t == 3); })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; });

                // text.filter(function(d) { return d.selected; })
                //     .attr("x", function(d) { return d.x; })
                //     .attr("y", function(d) { return d.y + 0.7 * node_size + 14; });
                
                //New stuff added to check for collison
                
                    var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
                    
                    //checks for nodes connected of teh same type and by a type 0 edge
                    var connected_same_type_nodes = selected_node.nhd.filter(function(d) {return (selected_node.t == d.t) && (connected_by_type0edge(selected_node,d));});
                
                //apply fusion rule when checks passed
                    var to_fuse = false;
                    var dead_node = {};
                    
                    
                    connected_same_type_nodes.forEach(function(d) {if (collided(d,selected_node)) {
                        to_fuse = true;
                        dead_node = d; 
                    
                    }});
                    
                    
                
                    if (to_fuse == true) {
                        rule_applied = true;
                        console.log(rule_applied);
                        fusion(selected_node,dead_node);
                        to_fuse = false;
                        graph.nodes.forEach(function(d) {d.selected = false;});
                        
                        update();
                        console.log(graph);
                    
                     }

                     //implementation of rule that fuses spiders with one edge to qubit nodes that are empty
                var to_recombine = false;
                var recomb_node = {};
                //first check if selected node has one edge and collides with a qnode that is also empty
                if (selected_node.nhd.length == 1) {
                    qnodes.forEach(function(d) {if (collided(d,selected_node) && d.empty == true){
                        to_recombine = true;
                        recomb_node = d;
                    }})
                }

                //now implement recombination
                if (to_recombine == true) {
                    rule_applied = true;
                    recomb(selected_node,recomb_node);
                    update();
                    to_recombine = false;

                }
                
                }
                   
            }).on("end", function() {console.log("mouseup");
                graph.nodes.forEach(function(d) {d.selected = false;}); 
                rule_applied = false;}));


                var timer = 0;
                var delay = 200;
                var prevent = false;
                node.on("click", function(d) {
                    timer = setTimeout(function() {
                        if (!prevent) {
                            d.selected = true;
        
                            var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
                            //Implementation of removing ids
                            if ((selected_node.t == 1 || selected_node.t == 2) && selected_node.nhd.length == 2 && selected_node.phase == 0) {
                                console.log("remove id");
                                remove_node(selected_node);
                                update();
                                d.selected = false;
                
                            }
                
                            if (selected_node.t == 0) {
        
                                qubit_to_spider(selected_node);
                                update();
                                d.selected = false;
                            }
                
                            }
                        
                        prevent = false;
                      }, delay);
                    
                }).on("dblclick", function(d) {
                    console.log("complement rule");
                    clearTimeout(timer);
                    prevent = true;

                    d.selected = true;
        
                    var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
        
                    colour_change(selected_node);

                    update();
                    console.log(graph)
                
                });

                link.on("mousedown", function(d) {
                    console.log("A link was clicked it was");
                    console.log(d);
                    if (ins_red) {
                        //red id
                        rule_applied = true;
                        add_red_id(d);
                        update();
                        rule_applied = false;
                        ins_red = false
        
                    } else {
                        //green id
                        rule_applied = true;
                        add_green_id(d);
                        update();
                        rule_applied = false;
                        ins_red = true
                    }
                
        
        
        
                });
            
            //END OF BIG ASS TEST
            
            console.log(rule_string);
            
            pythonCode2 = `
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


def get_depth(qasm):

    qasm_list=qasm.split("\\n")

    occur_dict = dict()

    #Loop to count the two qubit gates and store the qubits they act on
    for element in qasm_list:
        for i,s in enumerate(element):
            if s == 'q':
                qubit = element[i+2]
                if qubit not in occur_dict.keys():
                    occur_dict[qubit] = 1
                else:
                    #else add phase to existing entry
                    occur_dict[qubit] += 1

    return max(occur_dict.values())

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

    extract_success = graph_qasm[2]

    print(architecture)
    #temporarily doing a full reduce
    #zx.full_reduce(graph_pyzx)

    if extract_success == True:
        extract_msg = "Circuit succesfully extracted"
    else:
        extract_msg = "Warning! Extracted circuit is not equivalent to original circuit!" 

    g_copy = copy.deepcopy(graph_pyzx)

    #add in identities and hadamrads to pyzx graph
    zx.simplify.to_gh(g_copy)
    graph_semi=insert_ids_hadamards(g_copy)

    try:
        circ_from_test=zx.extract.extract_circuit(graph_semi,optimize_czs=False, optimize_cnots=0)
    except:
        return {'qasm':qasm_initial,'score':"Current graph can't be extracted",'initial_qasm':qasm_initial,'stats':zx.circuit.Circuit.from_qasm(qasm_initial).stats()}
    
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

    depth = str(get_depth(circuit_qasm_string))

    stats = stats + " and the circuit depth is: " + depth + " Extraction:" + extract_msg

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
            spider_qubit = graph.qubit(data[i][1])
            node_qubit = data[i][2]
            for v in graph.vertices():
                if graph.qubit(v) == spider_qubit:
                    graph.set_qubit(v,node_qubit) 
                if graph.qubit(v) == node_qubit:
                    graph.set_qubit(v,spider_qubit)

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
    try:
        circ_from_test=zx.extract.extract_circuit(graph_semi.copy(),optimize_czs=False, optimize_cnots=0,quiet=True)
    except:
        return graph,qasm,False

    #remove excess hadamards from qasm string
    qasm_final=remove_haddys(circ_from_test.to_qasm())

    #convert final circuit to qasm string
    final_circuit=zx.circuit.Circuit.from_qasm(qasm_final)

    #convert this to an if statement
    #if true display circuit, if False error message
    extract_success = zx.compare_tensors(zx.circuit.Circuit.to_tensor(final_circuit),zx.circuit.Circuit.to_tensor(zx.circuit.Circuit.from_qasm(qasm)))

                
    return graph,qasm,extract_success
return_score(Implement_Rules(`+rule_string+'),'+connectivity_string+')')
            
            
                // languagePluginLoader.then(function ()  {
                // console.log(pyodide.runPython('import sys'));
                // console.log(pyodide.runPython(`print('hello world')`));
                // pyodide.remotePath
                // pyodide.remotePath = "https://de-luxham.github.io/"
                // pyodide.runPythonAsync('import Implementer\n')
                // console.log('Implementer imported')
                //pyodide.runPython('Implement_Rules('.concat(rule_string,')'))

                // }); 
                pyodide.loadPackage('matplotlib').then(() => {
                    var qasm,qasm_init,score,x,stats;
                    x = pyodide.runPython(pythonCode2);
                    qasm_init = x.initial_qasm;
                    qasm = x.qasm;
                    score = x.score;
                    stats = x.stats;
                    console.log(score);
                    console.log(qasm);
                    var circuit = new QuantumCircuit();
                    circuit.importQASM(qasm, function(errors) {
                        console.log(errors);
                    });
                    var circuit_old = new QuantumCircuit();
                    circuit_old.importQASM(qasm_init, function(errors) {
                        console.log(errors);
                    });
                    // Assuming we have <div id="drawing"></div> somewhere in HTML
                    var circ_container = document.getElementById("circuit");
                    var old_circ_container = document.getElementById("old_circuit");
                    var score_container = document.getElementById("score");
                    var stats_container = document.getElementById("stats");
                    // SVG is returned as string
                    var svg = circuit.exportSVG(true);
                    var svg2 = circuit_old.exportSVG(true);

                    // add SVG into container
                    circ_container.innerHTML = svg;
                    old_circ_container.innerHTML = svg2;

                    stats_container.innerHTML = "Circuit stats:" + stats;

                    score_container.innerHTML = "Current Score:" + score;
                  });
                // languagePluginLoader.then(() => {
                //     pyodide.runPython(pythonCode2);
                //   })
        
            
        
        }

        //svg.attr("opacity",0)
        
        //returns true if nodes have collided
        function collided(node1,node2) {
            return 2*radius >= Math.abs(Math.sqrt(Math.pow(node1.x-node2.x,2)+Math.pow(node1.y-node2.y,2)));
        }
        function connected_by_type0edge(node1,node2) {
            //get links connecting nodes
            var connecting_links
            connecting_links = graph.links.filter(function(d) {return (is_link(d,node1,node2)); });
            var type0 = true
            connecting_links.forEach(function(d) {if (d.t == 2){type0 = false}})
            return type0
        }
        //Get index of link that connects two nodes
        function i_link(n1,n2) {
            
            var i =-1;
            
            graph.links.forEach(function(d, index) {
                if (((d.source.name.localeCompare(n1.name) == 0) && (d.target.name.localeCompare(n2.name) == 0)) || ((d.source.name.localeCompare(n2.name) == 0) && (d.target.name.localeCompare(n1.name) == 0))) {
                    return i = index;
                
                }
            } );
            return i;
        }
        
        //does a link connect two nodes
        function is_link(l,n1,n2) {
            return (((l.source.name.localeCompare(n1.name) == 0) && (l.target.name.localeCompare(n2.name) == 0)) || ((l.source.name.localeCompare(n2.name) == 0) && (l.target.name.localeCompare(n1.name) == 0)));
        }
        //does a link connect to a node

        function single_link(l,n) {
            return ((l.source.name.localeCompare(n.name) == 0) || (l.target.name.localeCompare(n.name) == 0))
        }
        
        //Get index of node
        function i_node(n) {
        
            var i = -1;
            
            graph.nodes.forEach(function(d,index) {
                if (d.name.localeCompare(n.name) == 0) {
                    i = index;
                }
             });
             return i;
        }

        //rules that use the rule string below here

        //remove ids rule
        function remove_node(selected_node) {

            //removes link between node and first member of nhd
            graph.links = graph.links.filter(function(d) {return !(is_link(d,selected_node,selected_node.nhd[0])); });

            //set links whose target/source is selected node and its second neigbour to the first neighbour
            graph.links.forEach(function(d) {
                if (d.target.name.localeCompare(selected_node.name) == 0) {
                    d.target = selected_node.nhd[0];
                
                }
                if (d.source.name.localeCompare(selected_node.name) == 0) {
                    d.source = selected_node.nhd[0];
                
                }
                
            
            });

            //remove id node
            
            graph.nodes = graph.nodes.filter(function(d) {return d.name != selected_node.name});
        
            
            ntab = {};
            
            graph.nodes.forEach(function(d) {
            console.log("node update");
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
            });

            console.log(ntab);
            console.log(graph.nodes);
            console.log(graph.links);

            graph.links.forEach(function(d) {
                s= d.source;
                t = d.target;
                s.nhd.push(t);
                t.nhd.push(s);
        });

                //code to updat the applied rules string with the fusion rule applied
            var ri_string = "";
            //case if this is the first rule applied 
            if (rule_string.length == 2){
            
                rule_string = "[[".concat("\"ri\"",",",selected_node.name,"]]");
            
            } else {
                rule_string = rule_string.slice(0,-1);
                ri_string = ",[".concat("\"ri\"",",",selected_node.name,"]]");
                rule_string = rule_string.concat(ri_string);
            }

            
        }
        
        //fusion rule
        function fusion(selected_node,dead_node) {
        
            console.log("fusion applied");

            //add the phases
            selected_node.phase = add_phases(selected_node.phase,dead_node.phase);
            
            //remove connecting link
            graph.links = graph.links.filter(function(d) {return !(is_link(d,selected_node,dead_node)); });
            //set links whose target is deadnode to selecetd node
            graph.links.forEach(function(d) {
                if (d.target.name.localeCompare(dead_node.name) == 0) {
                    d.target = selected_node;
                
                }
                if (d.source.name.localeCompare(dead_node.name) == 0) {
                    d.source = selected_node;
                
                }
                
            
            });
            
            //remove dead node
            
            graph.nodes = graph.nodes.filter(function(d) {return d.name != dead_node.name});
            
            console.log(graph);
            
             ntab = {};
            
             graph.nodes.forEach(function(d) {
            console.log("node update");
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
            });

            console.log(ntab);
            console.log(graph.nodes);
            console.log(graph.links);

            graph.links.forEach(function(d) {
                s= d.source;
                t = d.target;
                s.nhd.push(t);
                t.nhd.push(s);
        });
            
        //code to updat the applied rules string with the fusion rule applied
        var fuse_string = "";
        //case if this is the first rule applied 
        if (rule_string.length == 2){
            
            rule_string = "[[".concat("\"s\"",",",selected_node.name,",",dead_node.name,"]]");
            
        } else {
            rule_string = rule_string.slice(0,-1);
            fuse_string = ",[".concat("\"s\"",",",selected_node.name,",",dead_node.name,"]]");
            rule_string = rule_string.concat(fuse_string);
        }
            
        }
        
        //split rule
        
        function split(sliced_node, s_line) {

            //Gradient of slice
            var m = (s_line.y2 - s_line.y1)/(s_line.x2 - s_line.x1);
            
            //increment the total node count
            node_count++;

            //Add new node to list of nodes, Can do this by copying slcied node appending then changing its values
            var new_node = {name:node_count.toString(), x:sliced_node.x+20, y:sliced_node.y+20, t:sliced_node.t, phase:sliced_node.phase/2, selecetd:false, previouslySelected:false, index:node_count, vy:0, vx:0};

            //half phase of sliced node
            sliced_node.phase = sliced_node.phase/2;

            graph.nodes.push(new_node);


            //change the connections of existing links
            //and add new node neighbour names to a list
            var new_node_neighbours = [];

            graph.links.forEach(function(d) {
                if ((d.target.name.localeCompare(sliced_node.name) == 0) && (d.source.y > m*(d.source.x - s_line.x1) +s_line.y1)) {
                    d.target = new_node;
                    new_node_neighbours.push(d.source.name);
                
                }
                if ((d.source.name.localeCompare(sliced_node.name) == 0) && (d.target.y > m*(d.target.x - s_line.x1) +s_line.y1)) {
                    d.source = new_node;
                    new_node_neighbours.push(d.target.name);
                
                }
                
             console.log("in links for each loop")
            });

            //construct new neighbour rule string
            var new_neigh_string;
            var x;
            x = new_node_neighbours.toString();
            
            new_neigh_string = "["+x+"]"
            console.log(new_neigh_string);
            //create new link connecting the sliced node and the new one

            //increment the link counter
            link_count++;
            
            var new_link = {source: sliced_node , target: new_node, t:1, index: link_count};

            

            //add this link to the links array
            graph.links.push(new_link);

            //re update neighbour connections

            ntab = {};
            
            graph.nodes.forEach(function(d) {
            console.log("node update");
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
            });


            graph.links.forEach(function(d) {
                s= d.source;
                t = d.target;
                s.nhd.push(t);
                t.nhd.push(s);
            
            });

            //code to updat the applied rules string with the split rule applied
        var split_string = "";
        //case if this is the first rule applied 
        if (rule_string.length == 2){
            
            rule_string = "[[".concat("\"u\"",",",sliced_node.name,",",new_neigh_string,",","0","]]");
            
        } else {
            rule_string = rule_string.slice(0,-1);
            split_string = ",[".concat("\"u\"",",",sliced_node.name,",",new_neigh_string,",","0","]]");
            rule_string = rule_string.concat(split_string);
        }
        }

        //change qubit to spider
        function qubit_to_spider(selected_node) {
            //Implementation of changing qubit to red spider
            
                //set the qubit node to the one specified by comb_red
                // if (comb_red == true) {
                //     selected_node.t = 2;
                //     comb_red = false;
                // }
                // else if (comb_red == false) {
                //     selected_node.t = 1;
                //     comb_red = true;
                // }

                //just make them all red instead
                selected_node.t = 2;

                selected_node.x = selected_node.x + 20
                
                //change connectivity to empty status (used to verify if spider can reconnect to qubit node)
                qnodes.filter(function(d) {return d.name == selected_node.name}).forEach(function(d){d.empty = true})
            
            //code to updat the applied rules string with the fusion rule applied
        var qr_string = "";
        //case if this is the first rule applied 
        if (rule_string.length == 2){
            
            rule_string = "[[".concat("\"qr\"",",",selected_node.name,"]]");
            
        } else {
            rule_string = rule_string.slice(0,-1);
            qr_string = ",[".concat("\"qr\"",",",selected_node.name,"]]");
            rule_string = rule_string.concat(qr_string);
        }
    }
    

        //recombine spider to qubit node
        function recomb(selected_node,recomb_node) {
            selected_node.t = 0;


            recomb_node.empty = false;
            selected_node.x = recomb_node.x;
            selected_node.y = recomb_node.y
            //code to updat the applied rules string with the fusion rule applied
            var rq_string = "";
            //case if this is the first rule applied 
            if (rule_string.length == 2){
            
                rule_string = "[[".concat("\"rq\"",",",selected_node.name,",",recomb_node.name,"]]");
            
            } else {
            rule_string = rule_string.slice(0,-1);
            rq_string = ",[".concat("\"rq\"",",",selected_node.name,",",recomb_node.name,"]]");
            rule_string = rule_string.concat(rq_string);
            }
        }

        //colour change rule
        function colour_change(selected_node) {
            //chnage colour of node
            if (selected_node.t == 1) {
                selected_node.t = 2;
            }
            else if (selected_node.t == 2) {
                selected_node.t = 1;
            }
            //change connecting link types
            var connected_links = graph.links.filter(function(l) {return single_link(l,selected_node);});
                    
            connected_links.forEach(function(l) {
            if (l.t == 1) {
                l.t = 2;
            }
            else if (l.t == 2) {
                l.t = 1;  
            }
            })
            //code to updat the applied rules string with the fusion rule applied
            var cc_string = "";
            //case if this is the first rule applied 
            if (rule_string.length == 2){
            
                rule_string = "[[".concat("\"cc\"",",",selected_node.name,"]]");
            
            } else {
                rule_string = rule_string.slice(0,-1);
                cc_string = ",[".concat("\"cc\"",",",selected_node.name,"]]");
                rule_string = rule_string.concat(cc_string);
            }
        }

        //add red identity 
        function add_red_id(link) {
            //get midpoint of the link to place the new node
            var mid_ptx,mid_pty;
            mid_ptx = (link.source.x + link.target.x)/2;
            mid_pty = (link.source.y + link.target.y)/2;

            //store source and target name for link in new variables to go into the rule string
            var source_name = link.source.name;
            var target_name = link.target.name;

            //increment the total node count
            node_count++;

            //new node to be added
            var new_node = {name:node_count.toString(), x:mid_ptx, y:mid_pty, t:2, phase:"", selecetd:false, previouslySelected:false, index:node_count, vy:0, vx:0};
            
            //add node to the list of nodes
            graph.nodes.push(new_node);

            //update the links new target
            var placeholder_node = link.target;

            link.target = new_node;

            //increment the link counter
            link_count++;
            
            var new_link = {source: placeholder_node, target: new_node, t:1, index: link_count};

            

            //add this link to the links array
            graph.links.push(new_link);

            //re update neighbour connections

            ntab = {};
            
            graph.nodes.forEach(function(d) {
            console.log("node update");
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
            });


            graph.links.forEach(function(d) {
                s= d.source;
                t = d.target;
                s.nhd.push(t);
                t.nhd.push(s);
            
            });

            //code to updat the applied rules string with the fusion rule applied
            var i_string = "";
            //case if this is the first rule applied 
            if (rule_string.length == 2){
            
                rule_string = "[[".concat("\"i\"",",",source_name,",",target_name,",","2","]]");
            
            } else {
                rule_string = rule_string.slice(0,-1);
                i_string = ",[".concat("\"i\"",",",source_name,",",target_name,",","2","]]");
                rule_string = rule_string.concat(i_string);
            }




        }
        //add green identity 
        function add_green_id(link) {
            //get midpoint of the link to place the new node
            var mid_ptx,mid_pty;
            mid_ptx = (link.source.x + link.target.x)/2;
            mid_pty = (link.source.y + link.target.y)/2;

            //store source and target name for link in new variables to go into the rule string
            var source_name = link.source.name;
            var target_name = link.target.name;

            //increment the total node count
            node_count++;

            //new node to be added
            var new_node = {name:node_count.toString(), x:mid_ptx, y:mid_pty, t:1, phase:"", selecetd:false, previouslySelected:false, index:node_count, vy:0, vx:0};
            
            //add node to the list of nodes
            graph.nodes.push(new_node);

            //update the links new target
            var placeholder_node = link.target;

            link.target = new_node;

            //increment the link counter
            link_count++;
            
            var new_link = {source: placeholder_node, target: new_node, t:1, index: link_count};

            

            //add this link to the links array
            graph.links.push(new_link);

            //re update neighbour connections

            ntab = {};
            
            graph.nodes.forEach(function(d) {
            console.log("node update");
            ntab[d.name] = d;
            d.selected = false;
            d.previouslySelected = false;
            d.nhd = [];
            });


            graph.links.forEach(function(d) {
                s= d.source;
                t = d.target;
                s.nhd.push(t);
                t.nhd.push(s);
            
            });

            //code to updat the applied rules string with the fusion rule applied
            var i_string = "";
            //case if this is the first rule applied 
            if (rule_string.length == 2){
            
                rule_string = "[[".concat("\"i\"",",",source_name,",",target_name,",","1","]]");
            
            } else {
                rule_string = rule_string.slice(0,-1);
                i_string = ",[".concat("\"i\"",",",source_name,",",target_name,",","1","]]");
                rule_string = rule_string.concat(i_string);
            }




        }

        //end of rule string rules

        //function to add phases
        function add_phases(phase1,phase2) {
            return (phase1+phase2) % (2*Math.PI);
        }
        
        
        //checks if slice region contains circle
        //more generally checks if point is contained in box defined by sline
        function in_box(circle, s_line) {
            return (((circle.cx >= s_line.x1 && circle.cx <= s_line.x2) || (circle.cx >= s_line.x2 && circle.cx <= s_line.x1)) && ((circle.cy >= s_line.y1 && circle.cy <= s_line.y2) || (circle.cy >= s_line.y2 && circle.cy <= s_line.y1)));
            }
            
        function cuts_circle(circle, s_line) {
            var m = (s_line.y2 - s_line.y1)/(s_line.x2 - s_line.x1);
            var D = Math.pow(2*m*(-m*s_line.x1 + s_line.y2 - circle.cy)-2*circle.cx,2)-4*(Math.pow(m,2)+1)*(Math.pow(circle.cx,2)+Math.pow(-m*s_line.x1 + s_line.y2 - circle.cy,2)-Math.pow(circle.r,2));
            return D > 0;
        }
        
        //update look of graph stuff
        
        //End of new stuff

        function update_hboxes() {
            if (auto_hbox) {
                var pos = {};
                hbox.attr("transform", function(d) {
                    // calculate barycenter of non-hbox neighbours, then nudge a bit
                    // to the NE.
                    var x=0,y=0,sz=0;
                    for (var i = 0; i < d.nhd.length; ++i) {
                        if (d.nhd[i].t != 3) {
                            sz++;
                            x += d.nhd[i].x;
                            y += d.nhd[i].y;
                        }
                    }

                    offset = 0.25 * scale;

                    if (sz != 0) {
                        x = (x/sz) + offset;
                        y = (y/sz) - offset;

                        while (pos[[x,y]]) {
                            x += offset;
                        }
                        d.x = x;
                        d.y = y;
                        pos[[x,y]] = true;
                    }

                    return "translate("+d.x+","+d.y+")";
                });
            }
        }

        update_hboxes();

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        
        //links for connectivity graph
        clink.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

        //Stuff for force directed part
        

        //only coloured nodes are in the simulation
        simulation
          .nodes(graph.nodes.filter(function(d) {return d.t != 0;}))
          .on("tick", ticked);

        simulation.force("link")
          .links(graph.links.filter(function(d) {return ((d.source.t !=0) && (d.target.t != 0));}));

         

        function ticked() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
            
            //stuff to keep nodes inside a box
            
            // node.attr("transform", function(d) {
            //     d.x = Math.max(radius, Math.min(width - radius -100, d.x));
            //     //manualy changed height of box with offset
            //     d.y = Math.max(radius, Math.min(height - radius -100, d.y));
            //     return "translate(" + d.x + "," + d.y +")";
            //  })
        
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        }
          
        
        
        
        // EVENTS FOR DRAGGING AND SELECTION

        //flip variable to determine if qubit node conerts to red or green spider
        var comb_red = true;

        node.on("mousedown", function(d) {
                /*if (shiftKey) {
                    d3.select(this).select(":first-child").attr("style", nodeStyle(d.selected = !d.selected));
                    d3.event.stopImmediatePropagation();
                } else if (!d.selected) {
                    node.select(":first-child").attr("style", function(p) { return nodeStyle(p.selected = d === p); });*/
                    
                    //New stuff for when a node is selected
                
                    d.selected = true;
                    
                    console.log(graph.nodes.filter(function(d) {return d.selected;})[0]);
                    
                    simulation.alphaTarget(0.05).restart();
                    
                //}
            })
            .call(d3.drag().on("drag", function(d) {
                var dx = d3.event.dx;
                var dy = d3.event.dy;
                // node.filter(function(d) { return d.selected; })
                //     .attr("cx", function(d) { return d.x += dx; })
                //     .attr("cy", function(d) { return d.y += dy; });
            
                //added this thing for the force stuff
                
                simulation.alphaTarget(0.05).restart();
                
                
                
                if (rule_applied == false) {
                
                    node.filter(function(d) { return d.selected; })
                    .attr("transform", function(d) {
                        d.x += dx;
                        d.y += dy;
                        return "translate(" + d.x + "," + d.y +")";
                    });

                    update_hboxes();

                    link.filter(function(d) { return d.source.selected ||
                                            (auto_hbox && d.source.t == 3); })
                    .attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; });

                    link.filter(function(d) { return d.target.selected ||
                                            (auto_hbox && d.target.t == 3); })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; });

                // text.filter(function(d) { return d.selected; })
                //     .attr("x", function(d) { return d.x; })
                //     .attr("y", function(d) { return d.y + 0.7 * node_size + 14; });
                
                //New stuff added to check for collison
                
                    var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
                    
                    
                    var connected_same_type_nodes = selected_node.nhd.filter(function(d) {return (selected_node.t == d.t) && (connected_by_type0edge(selected_node,d));});
                
                //apply fusion rule when checks passed
                    var to_fuse = false;
                    var dead_node = {};
                    
                    
                    connected_same_type_nodes.forEach(function(d) {if (collided(d,selected_node)) {
                        to_fuse = true;
                        dead_node = d; 
                    
                    }});
                    
                    
                
                    if (to_fuse == true) {
                        rule_applied = true;
                        console.log(rule_applied);
                        fusion(selected_node,dead_node);
                        to_fuse = false;
                        graph.nodes.forEach(function(d) {d.selected = false;});
                        
                        update();
                        console.log(graph);
                    
                     }

                //implementation of rule that fuses spiders with one edge to qubit nodes that are empty
                var to_recombine = false;
                var recomb_node = {};
                //first check if selected node has one edge and collides with a qnode that is also empty
                if (selected_node.nhd.length == 1) {
                    qnodes.forEach(function(d) {if (collided(d,selected_node) && d.empty == true){
                        to_recombine = true;
                        recomb_node = d;
                    }})
                }

                //now implement recombination
                if (to_recombine == true) {
                    rule_applied = true;
                    recomb(selected_node,recomb_node);
                    update();
                    to_recombine = false;

                }
                
                }  
            }).on("end", function() {console.log("mouseup");
                graph.nodes.forEach(function(d) {d.selected = false;}); 
                rule_applied = false;}));
            
        //Implementation of slice rule
        
        svg.on("mousedown", function () {
            var x = d3.mouse(this)[0];
            var y = d3.mouse(this)[1];
            
            //slice.enter();
            
            
            //slice.attr("x1", function(d) { return x; })
                 //.attr("y1", function(d) { return y; })
            slice_nog.x1 = x;
            slice_nog.y1 = y    
        
               
            }).call(d3.drag().on("drag", function(d) {
                var x = d3.event.x;
                var y = d3.event.y;
                
                //slice.attr("x2", function(d) { return x; })
                     //.attr("y2", function(d) { return y; })
                     //.attr("opacity", 1);
                slice_nog.x2 = x;
                slice_nog.y2 = y; 
               
                
            }).on("end", function() {
                
                if (rule_applied == false) {
                //define line object to hold line coordinates
                    //var s_line = {x1: slice.attr("x1"),x2: slice.attr("x2"), y1:slice.attr("y1"), y2:slice.attr("y2")};
                    var s_line = {x1: slice_nog.x1,x2: slice_nog.x2, y1:slice_nog.y1, y2:slice_nog.y2};

                    var to_slice = false;
                    var sliced_node = {};
                
                    graph.nodes.forEach(function(d) {
                    
                    //circle info for node
                        var circle = {cx: d.x, cy: d.y, r: radius};


                    
                        if (in_box(circle, s_line) && cuts_circle && (d.t != 0) && (d.t != 3)) {
                        console.log(d.name);
                        console.log("Apply slice");
                        to_slice = true;
                        sliced_node = d;
                        
                        
                                           
                        }
                
                    
                    });

                    if (to_slice) {
                        update();
                        rule_applied = true;
                        console.log("before split")
                        split(sliced_node, s_line);
                        console.log("after split")
                        to_slice = false;
                        
                        update();
                        console.log(graph);
                        console.log("graphupdated");
                    }   
                
                
                slice.attr("opacity", 0);
            }
             rule_applied = false
            }));
        
        //End of slice rule implementatio

        //Implementation of inserting identities

        //insertion of identities
        // will have variable that flips each time and Id is inserted so that green or red can be inserted
        var ins_red = false; 
        link.on("mousedown", function(d) {
            console.log("A link was clicked it was");
            console.log(d);
            if (ins_red) {
                //red id
                rule_applied = true;
                add_red_id(d);
                update();
                rule_applied = false;
                ins_red = false

            } else {
                //green id
                rule_applied = true;
                add_green_id(d);
                update();
                rule_applied = false;
                ins_red = true
            }
        



        });
        
    
        //remova of identities
        //Implementation of colour change rule
        var timer = 0;
        var delay = 200;
        var prevent = false;

        node.on("click", function(d) {
            timer = setTimeout(function() {
                if (!prevent) {
                    d.selected = true;

                    var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
                    //Implementation of removing ids
                    if ((selected_node.t == 1 || selected_node.t == 2) && selected_node.nhd.length == 2 && selected_node.phase == 0) {
                        console.log("remove id");
                        remove_node(selected_node);
                        update();
                        d.selected = false;
        
                    }

                    if (selected_node.t == 0) {
        
                        qubit_to_spider(selected_node);
                        update();
                        d.selected = false;
                    }
                }
                
                prevent = false;
              }, delay);
    

        }).on("dblclick", function(d) {
            console.log("complement rule");
            clearTimeout(timer);
            prevent = true;

            d.selected = true;
        
            var selected_node = graph.nodes.filter(function(d) {return d.selected;})[0];
        
            colour_change(selected_node);
            update();
            
        
        });   
    }};
});


