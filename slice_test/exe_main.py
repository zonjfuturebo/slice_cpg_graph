import os

import get_api
import get_chain
import get_cpgNodes
import init
import exe_sc

# 工作路径仍需要动态修改
work_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(work_path, "data")
CWE_path = os.path.join(data_path, "CWE")
s01_path = os.path.join(CWE_path, "S01")
file_path = os.path.join(s01_path, "cwe121_bad.c")
sc_path = os.path.join(work_path, "sc\\bad.sc")

file_name, _ = os.path.splitext(os.path.basename(file_path))

# step0:初始化工作路径，删除注释，生成sc文件
path_init = init.PathInitializer(s01_path, file_name)
# init.check_path(path_init)
# init.remove_comments_c(file_path)
cpg_path = path_init.get_cpg_path()
pdg_path = path_init.get_pdg_path()
# step1:执行sc文件
exe_sc.exc_scala(sc_path, file_path)

# step2:处理cpg，pdg信息
# sub_step1:处理cpg信息，获取cpg_nodes
cpg_nodes = get_cpgNodes.cpgjson_to_cpgnode(cpg_path)
pdg_node, func_list = get_cpgNodes.add_pdg_to_node(pdg_path, cpg_nodes)
# sub_step2:生成cpg图和pdg图信息









# nodes = get_cpgNodes.cpgjson_to_cpgnode("data/cpg_json_bad.json")  # 获得程序的信息
# # nodes = {21474836480: {'name': 'CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01_bad',
# #                        '_id': 21474836480,
# #                        'signature': 'int64_t()',
# #                        'methodFullName': 'CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01_bad',
# #                        '_label': 'BINDING',
# #                        'backward_node': [],
# #                        'forward_node': [],
# #                        'side_type': [],
# #                        'side_value': []},{...},{...},...
# # nodes = {_id: cpg_info}
# nodes, methods = get_cpgNodes.add_pdg_to_node("data/pdg_txt_bad.txt", nodes)  # 将pdg图添加到nodes中
# # nodes 同上，添加pdg信息'backward_node'，'forward_node'，'side_type'，'side_value'
# # methods = ['CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01_bad']
#
# api_info = get_api.get_all_api("data/all_api_bad.txt")
# # api_info = {(name,id):{id, lineNumber, code, arg_line, arg_id, callee_id, callee_parameter_id, name}}
#
# vul_api_id, vul_api_line = get_api.get_vul_api_id(api_info)
# # vul_api_id = [30064771077]
# # vul_api_line = [('memcpy', 10)]
#
# method_chain = get_chain.get_method_chain("data/method_chain_bad.json", vul_api_id, api_info, nodes=nodes)
# method_chain = {30064771077: [[30064771077, 111669149697]]}
