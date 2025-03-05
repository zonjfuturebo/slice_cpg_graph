"""
该文件为测试各个函数接口文件
"""
import get_pdgGraph


file_path = "data/bad_txt_pdg.txt"

# 解析节点和边
nodes, edges = get_pdgGraph.parse_dot_content(file_path)

# 创建图
G = get_pdgGraph.create_graph(nodes, edges)