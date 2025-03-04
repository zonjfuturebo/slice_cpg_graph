import exe_main
import re


def bfs_slices(id, direction, nodes, methods, api_info):
    """
    广度搜索进行前向、后向切片
    :param id: 敏感函数id
    :param direction: 切片方向
    :param nodes: 已添加pdg信息的cpg节点 node={"backward_node":,"forward_node":,"side_type":,"side_value":}
    :param methods: list，方法名列表[println, func]
    :param api_info: list，所有函数api信息
    :return:
    """
    print("bfs_slices")
    methods_line = {}  # 行号和method节点的映射
    flag = set()  # 防止出现含环的情况
    q = [id]
    slices_lines = list()
    while q:
        index = q.pop(0)  # 弹出一个元素
        if index in flag:
            continue
        flag.add(index)

        if nodes[index]["_label"] == "CALL" and nodes[index]["_id"] != id:  # 如果节点是call类型的节点，则需要获得其参数的位置,后面的条件是防止递归调用的情况
            lines = api_info[(nodes[index]["name"], index)]["arg_line"].split()  # 获取实参的位置
            # 使用正则表达式提取数字 [‘some(10)‘,‘some(20)‘,‘some(30)‘] --> [10, 20, 30]
            lines = [int(re.search(r'\d+', s).group()) for s in lines]
            slices_lines.extend(lines)  # 加入行号

            name = nodes[index]["name"]  # 获取节点的名字
            if name in methods:  # 如果这个节点是程序定义的节点，就需要递归进行bfs
                line = api_info[(name, index)]["lineNumber"]
                methods_line[line] = api_info[(name, index)]["callee_parameter_id"]

        # 将该节点相邻的节点加入到队列当中
        if len(nodes[index][direction]) > 0:
            next = nodes[index][direction]
            q.extend(next)
        if "lineNumber" in nodes[index]:
            slices_lines.append(nodes[index]["lineNumber"])
    return slices_lines, methods_line


id = exe_main.vul_api_id[0]
direction = "forward_node"
nodes = exe_main.nodes
methods = exe_main.methods
api_info = exe_main.api_info
slices_lines, methods_line = bfs_slices(id, direction, nodes, methods, api_info)
print(slices_lines)
print(methods_line)
