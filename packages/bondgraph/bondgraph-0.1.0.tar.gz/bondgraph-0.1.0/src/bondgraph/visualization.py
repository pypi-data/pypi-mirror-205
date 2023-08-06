from bondgraph.core import BondGraph
from bondgraph.common import Node, Bond

import graphviz  # type: ignore

from typing import Dict


def gen_graphviz(bond_graph: BondGraph) -> graphviz.Digraph:
    g = graphviz.Digraph(node_attr={"shape": "none"}, edge_attr={"dir": "both"})

    bond_graph.assign_causalities()

    # Map from bondgraph node to graphviz node name
    node_map: Dict[object, str] = dict()

    n: Node
    for n in bond_graph.get_nodes():
        g.node(n.name, n.visualization_label())
        node_map[n] = n.name

    b: Bond
    for b in bond_graph._bonds:
        if b.effort_in_at_to is True:
            arrowhead_attr = "teelvee"
            arrowtail_attr = "none"
        elif b.effort_in_at_to is False:
            arrowhead_attr = "lvee"
            arrowtail_attr = "tee"
        else:
            arrowhead_attr = "lvee"
            arrowtail_attr = "none"
        g.edge(
            node_map[b.node_from],
            node_map[b.node_to],
            arrowhead=arrowhead_attr,
            arrowtail=arrowtail_attr,
            len="2",
        )

    return g
