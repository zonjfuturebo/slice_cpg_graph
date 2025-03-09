import networkx as nx
from get_cpgGraph import G
import matplotlib.pyplot as plt


vul_api_id = [30064771077]

def dfs_slice_graph(g, vul_api_id):
    # 统一节点ID为字符串类型，并确保输入为单个节点或列表
    if isinstance(vul_api_id, str):
        ids = [vul_api_id]
    elif isinstance(vul_api_id, list):
        ids = [str(id) for id in vul_api_id]
    else:
        raise TypeError("vul_api_id 必须为字符串或字符串列表")

    forward_slices = {}
    backward_slices = {}

    for node_id in ids:
        # 前向切片：原图正向遍历
        forward_tree = nx.dfs_tree(g, node_id)  # 或 nx.bfs_tree
        forward_nodes = list(forward_tree.nodes)
        forward_slices[node_id] = forward_nodes

        # 后向切片：反转图后正向遍历
        reversed_g = g.reverse()
        backward_tree = nx.dfs_tree(reversed_g, node_id)
        backward_nodes = list(backward_tree.nodes)
        backward_slices[node_id] = backward_nodes

    return forward_slices, backward_slices


def extract_merged_subgraph(g, forward_slices, backward_slices):
    # 合并所有切片节点（去重）
    all_nodes = set()
    for nodes in forward_slices.values():
        all_nodes.update(nodes)
    for nodes in backward_slices.values():
        all_nodes.update(nodes)

    # 提取子图并返回新的DiGraph对象
    return g.subgraph(all_nodes).copy()  # 使用copy()确保返回完整图对象而非视图


def visualize_slice(g, forward_slices, backward_slices, vul_node):
    # 合并所有切片节点（去重）
    all_slice_nodes = set()
    for nodes in forward_slices.values():
        all_slice_nodes.update(nodes)
    for nodes in backward_slices.values():
        all_slice_nodes.update(nodes)

    # 准备可视化
    pos = nx.nx_agraph.graphviz_layout(g, prog="dot")  # 固定布局保证一致性
    plt.figure(figsize=(32, 18))

    # 1. 绘制原图基础结构
    nx.draw_networkx_edges(g, pos, alpha=0.3, edge_color="gray")

    # 2. 绘制普通节点（灰色）
    normal_nodes = set(g.nodes()) - all_slice_nodes
    nx.draw_networkx_nodes(g, pos, nodelist=normal_nodes, node_color="lightgray", node_size=300)

    # 3. 高亮切片节点（前向橙色，后向蓝色）
    nx.draw_networkx_nodes(g, pos,
                           nodelist=forward_slices[vul_node],
                           node_color="orange",
                           label="Forward Slice")
    nx.draw_networkx_nodes(g, pos,
                           nodelist=backward_slices[vul_node],
                           node_color="deepskyblue",
                           label="Backward Slice")

    # 4. 突出显示漏洞节点（红色）
    nx.draw_networkx_nodes(g, pos,
                           nodelist=[vul_node],
                           node_color="red",
                           node_size=500,
                           label="Vulnerability Node")

    # 5. 添加标签和图示
    nx.draw_networkx_labels(g, pos, font_size=8)

    # 6. 显示边标签
    edge_labels = nx.get_edge_attributes(g, 'label')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8, font_color='black')

    plt.legend(scatterpoints=1, frameon=False)
    plt.axis("off")
    plt.title("Graph with Slice Highlighting")
    plt.show()





# 使用示例
forward, backward = dfs_slice_graph(G, vul_api_id)
# visualize_slice(G, forward, backward, vul_node=str(vul_api_id[0]))
merged_graph = extract_merged_subgraph(G, forward, backward)
