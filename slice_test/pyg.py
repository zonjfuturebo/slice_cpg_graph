import get_subgraph
import torch
from torch_geometric.utils.convert import from_networkx

# 承接一下图信息
graph = get_subgraph.merged_graph

def check_graph_info(G):
    print("Nodes with attributes:")
    for node, attrs in G.nodes(data=True):
        print(f"Node: {node}, Attributes: {attrs}")
    print("***********************")
    for edge in G.edges(data=True):
        print(f"Edge: {edge}")

# 执行
check_graph_info(graph)


def nx2pyg(graph):
    g_pyg_data = from_networkx(graph)
    print(g_pyg_data.)
