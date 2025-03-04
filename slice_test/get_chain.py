import copy
import json
import pickle


def dfs_method_chain(father_id, method_map, res, method_chain: list, depth):
    """
    深度遍历
    :param father_id:
    :param method_map:
    :param res:
    :param method_chain:
    :param depth:
    :return:
    """
    if depth > 7:
        return method_chain
    temp = method_map[father_id]  # 获取调用method_id的方法的id
    if len(temp) == 0 or len(method_chain) > 10:  # 如果递归到头，就存储一下结果, 并且如果大于chain大于10，则停止
        method_chain.append(res)
        return method_chain
    for id in temp:
        res.append(id)
        method_chain = dfs_method_chain(id, method_map, copy.deepcopy(res), copy.deepcopy(method_chain),
                                        depth + 1)  # 注意要用深拷贝
        res.pop()

    return method_chain


def get_method_chain(method_chain_path, vul_api_id, api_info, nodes):  # 存储的是id
    """

    :param method_chain_path:
    :param vul_api_id:
    :param api_info:
    :param nodes:
    :return:
    """
    # {call: caller}
    call_method_map = {}
    method_map = {}

    with open(method_chain_path, 'r') as file:
        data = json.load(file)  # data type: list, 某一个方法被其他方法调用，都是method类型

    for id in vul_api_id:  # 遍历危险函数的id
        method_id = api_info[(nodes[id]["name"], id)]["callee_id"]
        call_method_map[id] = method_id  # 使得危险函数id和其父函数id作映射

    for method in data:  # 某一个method节点被其他method节点调用的映射
        method_map[method["_1"]] = list(set(method["_2"]))  # 为了去重

    method_chain = {}

    for id in vul_api_id:
        temp = call_method_map[id]  # 取出其父函数id
        res = dfs_method_chain(temp, method_map, [], [], 0)

        for sub_list in res:
            sub_list.insert(0, temp)  # 加上危险函数的父函数的id
            sub_list.insert(0, id)  # 再加上自己的id
        method_chain[id] = res
    return method_chain  # {45: [[45, 39, 7]], 63: [[63, 39, 7]], 72: [[72, 39, 7]]}


def deal_view(method_chain, nodes, vul_api_id, path):
    vul_all = {}
    for id in vul_api_id:
        temp = method_chain[id]  # [[]]
        count = 0
        for i in temp:
            name_list2 = [nodes[j]["name"] for j in i]
            linenumber = nodes[id]["lineNumber"]
            name = nodes[id]["name"]
            vul_all[name + "|" + str(linenumber) + "|" + str(count + 1)] = name_list2
            count = count + 1
    # 将method chain写入到文件中,供前端使用
    with open(path, 'wb') as file:
        # 使用pickle的dump函数将列表序列化到文件
        pickle.dump(vul_all, file)
    # {'memset|12': ['memset', 'func'], 'memset|19': ['memset', 'func'], 'memmove|21': ['memmove', 'func']}
    # {673: [[673, 10324], [673, 669]], 9894: [[9894, 9858, 10752, 10958]], 10330: [[10330, 10324], [10330, 669]]}