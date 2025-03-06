import networkx as nx
from exe_test import G, vul_api_id


def bfs_slice_graph(g, vul_api_id):
    """
    针对漏洞API节点进行前向/后向切片，结果用字典存储
    :param g: 输入的有向图（NetworkX DiGraph对象）
    :param vul_api_id: 漏洞API节点ID（支持单个或列表）
    :return: (forward_slices, backward_slices) 前向切片字典和后向切片字典
    """
    # 统一处理为可迭代对象
    ids = [vul_api_id] if isinstance(vul_api_id, int) else vul_api_id

    forward_slices = {}
    backward_slices = {}

    for node_id in ids:
        # 前向切片（沿边方向）
        forward_nodes = list(nx.bfs_tree(g, node_id).nodes())
        forward_slices[node_id] = forward_nodes

        # 后向切片（逆边方向）
        backward_nodes = list(nx.bfs_tree(g.reverse(), node_id).nodes())
        backward_slices[node_id] = backward_nodes

    return forward_slices, backward_slices


forward, backward = bfs_slice_graph(G, vul_api_id)
print(forward,backward)