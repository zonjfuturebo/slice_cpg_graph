import re
import networkx as nx
import init


def parse_dot_content(cpg_path):
    """
    解析 DOT 格式的内容，提取节点和边信息。
    :param cpg_path: DOT 格式的字符串内容
    :return: 节点列表和边列表
    """
    nodes = []
    edges = []

    with open(cpg_path, "r") as file:
        content = file.read()
        # sections = content.split('\n\n')  # 根据一个或多个空行划分
        # 使用正则表达式切割字符串
        digraph_blocks = re.split(r'\n(?=digraph)', content.strip())

    for block in digraph_blocks:
        # 使用新的正则表达式匹配节点
        node_pattern = re.compile(
            r'"(\d+)"\s+\[label\s*=\s*<([^,]+),\s*(\d+),\s*(.*?)>\s*\]'
        )
        node_matches = node_pattern.findall(block)

        for match in node_matches:
            node_id, label, line_num, code = match
            nodes.append({
                "id": node_id,
                "label": label,
                "line_num": line_num,
                "code": code.strip()  # 去除前后空格
            })

        edge_pattern = re.compile(
            r'"(?P<source>\d+)"\s*->\s*'
            r'"(?P<target>\d+)"\s*'
            r'\[\s*label\s*=\s*"'
            r'(?P<label>\w+):\s*'
            r'(?P<code>.*)'
            r'"\s*\]'
        )
        edge_matches = edge_pattern.finditer(block)
        for edge in edge_matches:
            edge_info = edge.groupdict()
            edges.append({
                "source": edge_info["source"],
                "target": edge_info["target"],
                "label": edge_info["label"],
                "code": edge_info["code"].strip()  # 清理前后空格
            })

    return nodes, edges


def del_cfg_edges(edges: list):
    for i in range(len(edges)):
        if edges[i]["label"] == "CFG":
            edges.pop(i)
            i -= 1

    return edges


def create_graph(nodes, edges):
    """
    使用 NetworkX 构建图。
    :param nodes: 节点列表
    :param edges: 边列表
    :return: NetworkX 图对象
    """
    g = nx.DiGraph()
    g.add_nodes_from([(node["id"], node) for node in nodes])
    g.add_edges_from([(edge["source"], edge["target"], edge) for edge in edges])

    return g



cpg_path = "data/bad_txt_cpg.txt"
test_cpg_path = init.remove_html_tag(cpg_path)
nodes, edges = parse_dot_content(test_cpg_path)
edges = [edge for edge in edges if edge["label"] != "CFG"]


G = create_graph(nodes, edges)

