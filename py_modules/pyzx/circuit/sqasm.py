from .qasmparser import QASMParser
from ..rules import *
from ..simplify import simp

__all__ = ['sqasm']

# versions of these rules which instruct the simplifier *not* to remove
# isolated vertices. n.b. remove_ids already does this, but this might change
# in the future...
def spider_nocheck(g, ms):
    etab,rem_v,rem_e,check = spider(g, ms)
    return (etab, rem_v, rem_e, False)

def remove_ids_nocheck(g, ms):
    etab,rem_v,rem_e,check = remove_ids(g, ms)
    return (etab, rem_v, rem_e, False)

def sqasm(s, simplify=True):
    p = QASMParser()
    c = p.parse(s, strict=False)
    g = c.to_graph(zh=True)
    for r,sp in p.registers.items():
        if len(r) > 0 and r[0].isupper():
            for q in range(sp[0],sp[0]+sp[1]):
                if r[0] != 'Z':
                    v = g.inputs[q]
                    v1 = list(g.neighbours(v))
                    if len(v1) > 0 and g.type(v1[0]) != 0: g.set_type(v, g.type(v1[0]))
                    else: g.set_type(v, 1)
                    g.inputs[q] = None
                    g.scalar.add_power(-1)

                if r[0] != 'A':
                    v = g.outputs[q]
                    v1 = list(g.neighbours(v))
                    if len(v1) > 0 and g.type(v1[0]) != 0: g.set_type(v, g.type(v1[0]))
                    else: g.set_type(v, 1)
                    g.outputs[q] = None
                    g.scalar.add_power(-1)
        
    g.inputs = [x for x in g.inputs if not x is None]
    g.outputs = [x for x in g.outputs if not x is None]
    
    while simplify:
        i = simp(g, '', match_spider_parallel, spider_nocheck, quiet=True)
        i += simp(g, '', match_ids_parallel, remove_ids_nocheck, quiet=True)
        if i == 0: break
    
    g.pack_circuit_rows()
    return g
