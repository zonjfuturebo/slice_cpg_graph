import re
import networkx as nx
import matplotlib.pyplot as plt

def parse_dot_content(pdg_path):
    """
    解析 DOT 格式的内容，提取节点和边信息。
    :param pdg_path: DOT 格式的字符串内容
    :return: 节点列表和边列表
    """
    nodes = []
    edges = []

    with open(pdg_path, "r") as file:
        content = file.read()
        # sections = content.split('\n\n')  # 根据一个或多个空行划分
        # 使用正则表达式切割字符串
        digraph_blocks = re.split(r'\n(?=digraph)', content.strip())

    for content in digraph_blocks:  # 对每一个函数进行操作, such as [println, func]
        pattern = re.compile(
            r'\"(?P<node_id>\d+)\"\s*\[label\s*=\s*<'
            r'(?P<label>[^>]+)'
            r'>\s*\]'
        )
        # 查找所有匹配项
        matches = pattern.findall(content)
        # 打印匹配结果
        for match in matches:
            node_id, label = match
            nodes.append((node_id, label))
            print(f"Node ID: {node_id}, Label: {label}")



        matches = re.findall(r'(\d+)" -> "(\d+)"  \[ label = "(\w+): (.*)"\]', content)  # type: list

        for match in matches:
            source, target, label, code = match
            edges.append((source, target, {"label": label, "code": code}))

    return nodes, edges

def create_graph(nodes, edges):
    """
    使用 NetworkX 构建图。
    :param nodes: 节点列表
    :param edges: 边列表
    :return: NetworkX 图对象
    """
    G = nx.DiGraph()  # 创建有向图

    # 添加节点
    G.add_nodes_from(nodes)

    # 添加边
    G.add_edges_from(edges)

    return G
