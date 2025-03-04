import json
import re


def cpgjson_to_cpgnode(cpgjson_path):
    """
    turn the cpgjson to the cpgnode

    change to the cpg node inorder to execute the bfs, every node has an id,
    which exists in the json.
    I add four index --> (backward_node, forward_node, side_type, side_value)

    args:
        cpgjson_path: the path of cpgjson which is imported from the joern

    return:
        the map of node: id --> node

    """
    with open(cpgjson_path, 'r') as file:
        data = json.load(file)  # data type: dict

    nodes = {}  # create a map

    for node in data:
        idx = node["_id"]
        nodes[idx] = node
        nodes[idx]["backward_node"] = list()
        nodes[idx]["forward_node"] = list()
        nodes[idx]["side_type"] = list()
        nodes[idx]["side_value"] = list()

    return nodes


def add_pdg_to_node(pdg_path, nodes):  # 将pdg中的信息加入到nodes当中，即构造pdg图
    """ add the pdg information to node

      Firstly, using the regular expressions to match,
      such as: [('25', '65', 'DDG', 'dataBuffer'), ('25', '65', 'DDG', "memset(dataBuffer, 'A', 99)")]
      then add the pgd information to the node

      args:
          pdg_path: the path of pdg
          nodes: the nodes from cpgjson_to_cpgnode()

      return:
          the nodes have extra info
      """
    with open(pdg_path, "r") as file:
        content = file.read()
        # sections = content.split('\n\n')  # 根据一个或多个空行划分
        # 使用正则表达式切割字符串
        digraph_blocks = re.split(r'\n(?=digraph)', content.strip())
    method = list()  # 用来存放method节点
    for content in digraph_blocks:  # 对每一个函数进行操作, such as [println, func]
        method.append(content.split()[1][1:-1])
        matches = re.findall(r'(\d+)" -> "(\d+)"  \[ label = "(\w+): (.*)"\]', content)  # type: list

        for match in matches:  # （前向节点，后向节点，类型，值）
            forward_node, backward_node, side_type, side_value = match
            # if side_type == "DDG":
            forward_node = int(forward_node)
            backward_node = int(backward_node)
            nodes[forward_node]["backward_node"].append(backward_node)
            nodes[backward_node]["forward_node"].append(forward_node)
            nodes[forward_node]["side_type"].append(side_type)
            nodes[forward_node]["side_value"].append(side_value)
    return nodes, method




