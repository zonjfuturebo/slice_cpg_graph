"""
该文件为测试各个函数接口文件
"""
import get_api
import get_chain
import get_pdgGraph
from slice_test import get_cpgNodes
from slice_test.exe_main import cpg_path, pdg_path

file_path = "data/bad_txt_pdg.txt"
api_path = "data/test_api.json"
method_path = "data/bad_method_call.json"

# 获取cpg节点和pdg节点
cpg_nodes = get_cpgNodes.cpgjson_to_cpgnode(cpg_path)
pdg_nodes, func_list = get_cpgNodes.add_pdg_to_node(pdg_path, cpg_nodes)

# 解析节点和边
nodes, edges = get_pdgGraph.parse_dot_content(file_path)

# 创建pdg图
G = get_pdgGraph.create_graph(nodes, edges)

# 定位漏洞函数
call_node_api = get_api.get_all_api(api_path)
vul_api_id, vul_api_couple = get_api.get_vul_api_id(call_node_api)
print(f"vul_api_id:{vul_api_id}, vul_api_line:{vul_api_couple}")

# 获取方法调用链路
method_chain_path = get_chain.get_method_chain(method_path, vul_api_id, call_node_api, pdg_nodes)
for list in method_chain_path:
    print(list)
