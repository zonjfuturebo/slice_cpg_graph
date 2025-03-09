import copy

import pickle
import re
import json


def save_slices(source_path, save_path, merge_slices, model, vul_api_line_name, save_location_path):
    # model表示是否在保存时添加上行号,1表示要
    filec = open(source_path, "r")  # 打开c原文件
    files = open(save_path, "a")  # 打开要写入的文件
    serial_number = 0  # 每个切片的序号
    lines = filec.readlines()  # read the source of c

    flag = 0
    for slices in merge_slices:
        index = slices.index(vul_api_line_name[serial_number][1])
        if slices[0] == 7580 and slices[1] == 7583:
            flag = 1
        else:
            flag = 0
        files.write(
            "serial number:" + str(serial_number) + " vul_api_line:" + str(vul_api_line_name[serial_number][1]) + " " +
            vul_api_line_name[serial_number][0] + "\n")  # 写入每一个切片的序号
        for i, node in enumerate(slices):  # 加上行号后打印出来
            if flag:
                print(node, "++++", slices)
            if model == 1:
                files.write(str(node) + " " + lines[node - 1].lstrip())
                if i > index + 1:
                    break
            else:
                files.write(lines[node - 1].lstrip())
                if i > index + 1:
                    break
        files.write("2\n")  # 为了统一格式，打上标签2，表示未知
        files.write("------------------------------\n")
        serial_number = serial_number + 1
    with open(save_location_path, "wb") as file:  # 保存位置文件
        pickle.dump(vul_api_line_name, file)


def bfs_slices(id, direction, nodes, methods, api_info):
    """
    广度搜索进行前向、后向切片
    :param id: 敏感函数id
    :param direction: 切片方向
    :param nodes: 已添加pdg信息的cpg节点 node={"backward_node":,"forward_node":,"side_type":,"side_value":}
    :param methods: list，方法名列表[println, func]
    :param api_info: list，所有函数api信息
    :return: methods_line： 行号和method节点的映射
             slices_lines： 切片行号
    """
    print("bfs_slices")
    methods_line = {}  # 行号和method节点的映射
    flag = set()  # 防止出现含环的情况
    q = [id]
    slices_lines = list()
    while q:
        index = q.pop(0) # 弹出一个元素
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


# 建立一个id和method parameter的映射


def get_slice(vul_api_id, nodes, methods, api_info, depth, num):  # 对一组id进行切片
    """

    :param vul_api_id: list,
    :param nodes: 已添加pdg信息的cpg节点 node={"backward_node":,"forward_node":,"side_type":,"side_value":}
    :param methods: list，方法名列表[println, func]
    :param api_info: list，所有函数api信息
    :param depth: 深度
    :param num: 计数
    :return:
    """
    merge_slices = list()
    if depth > 2 or num > 200:  # 减枝
        print(num, "num")
        return []
    for id in vul_api_id:

        back_slices, back_methods_line = bfs_slices(id, "backward_node", nodes, methods,
                                                    api_info)  # get the backward slices

        front_slices, front_methods_line = bfs_slices(id, "forward_node", nodes, methods,
                                                      api_info)  # get the forward slices
        methods_line = {**front_methods_line, **back_methods_line}  # 合并两个字典

        temp = back_slices + front_slices  # merge the slices
        unique_list = list(set(temp))  # 去重
        sorted_list = sorted(unique_list)  # 排序，因为是同一个函数，所以可以进行排序
        # 递归调用get_slice,以处理外部函数
        for line in methods_line:
            id_list = methods_line[line]
            # id_slices 是一个二维列表，需要将其变为一维列表
            id_slices = get_slice(id_list, nodes, methods, api_info, depth + 1, len(sorted_list))

            if len(id_slices) == 0:
                break
            slices = [item for sublist in id_slices for item in sublist]  # 通过列表推倒式将二维列表变为一维列表
            index_to_insert = 1  # 要插入的位置
            for info in sorted_list:
                if info == line:
                    sorted_list[index_to_insert:index_to_insert] = slices  # 将slices插入进该位置
                    break
                else:
                    index_to_insert = index_to_insert + 1
        # sorted_list = list(set(sorted_list))

        result = list()
        for i in range(len(sorted_list)):  # 去除可能存在的重复项 [1,2,2,3,3,3,3,4,6]
            if i + 1 < len(sorted_list) and sorted_list[i] == sorted_list[i + 1]:
                continue
            else:
                result.append(sorted_list[i])
        merge_slices.append(result)
    return merge_slices  # 返回的是行号


def deal_backforward_slice(nodes, method_chain, api_info, methods, vul_api_id, path):
    """

    :param nodes: 已添加pdg信息的cpg节点 node={"backward_node":,"forward_node":,"side_type":,"side_value":}
    :param method_chain: 函数调用链，例如{45: [[7, 39, 124]], 63: [[7, 39, 124]], 72: [[7, 39, 140]]}
    :param api_info: list，所有函数api信息
    :param methods: list，方法名列表[println, func]
    :param vul_api_id: list，危险函数id
    :param path: 函数调用路径，来源于cpg.method.map(node => (node.id, node.call.id.l)).toJsonPretty
    :return:
    """
    # 该函数用来处理回溯函数切片， method_chain是一个字典 {45: [[7, 39, 124]], 63: [[7, 39, 124]], 72: [[7, 39, 140]]}
    method_call = {}
    with open(path, 'r') as file:
        data = json.load(file)
    for d in data:
        method_call[d["_1"]] = set(d["_2"])

    merge_slices = []
    vul_api_id2 = []

    num = 0  # 用来计数
    for key in vul_api_id:
        num = num + 1
        chains = method_chain[key]  # 获取敏感函数的调用链

        for chain in chains:
            length = len(chain)
            vul_api_id2.append(key)
            vul_slice = get_slice([key], nodes, methods, api_info, 0, 0)  # 先对危险函数进行切片
            vul_slice = [item for sublist in vul_slice for item in sublist]  # 通过列表推倒式将二维列表变为一维列表

            for i in range(length):  # 遍历调用链  [45,39,7]
                parameter_index = get_method_flag(chain[i], nodes)  # 判断危险函数中的切片是否有来自父函数形参的
                if len(parameter_index) > 0 and i < length - 2:  # 如果索引大于0的话，则说明被引用了,则需要跳两个
                    # 获取相关的参数
                    name_method = nodes[chain[i + 1]]["name"]  # 获得一级函数
                    method_id = method_call[chain[i + 2]]  # 获得二级函数
                    for id in method_id:
                        name = nodes[id]["name"]
                        if name == name_method:  # 如果名字相同，则对这个id进行切片
                            slice = get_slice([id], nodes, methods, api_info, 0, 0)
                            slice = [item for sublist in slice for item in sublist]  # 通过列表推倒式将二维列表变为一维列表
                            method_line = nodes[id]["lineNumber"]  # 获取对应函数的lineNumber
                            # 将slice插入到vul_slice中
                            index_to_insert = 1  # 要插入的位置
                            for info in slice:
                                if info == method_line:
                                    slice[index_to_insert:index_to_insert] = vul_slice  # 将vul_slice插入进该位置
                                    break
                                else:
                                    index_to_insert = index_to_insert + 1
                            vul_slice = copy.deepcopy(slice)

                        if len(vul_slice) > 2000:  # 当这个切片太长了，直接停止切片
                            break
            merge_slices.append(vul_slice)

    vul_api_line_name = []
    for i in vul_api_id2:
        vul_api_line_name.append((nodes[i]["name"], nodes[i]["lineNumber"], nodes[i]["_id"]))

    return merge_slices, vul_api_line_name


def get_method_flag(id, nodes):  # 该函数也是bfs，不过不是为了切片，而是为了判读危险函数的切片中的变量是否来自函数的参数
    print("get_method_flag")
    flag = set()  # 防止出现含环的情况
    parameter_index = list()  # 函数参数
    q = [id]
    while q:
        index = q.pop(0)  # 弹出一个元素
        if index in flag:  # 防止重复使用
            continue
        flag.add(index)  # 标记一下这个id节点已经使用过了
        if nodes[index]["_label"] == "METHOD_PARAMETER_IN" or nodes[index][
            "_label"] == "METHOD_PARAMETER_OUT":  # 如果此时遍历到的节点是函数的参数
            parameter_index.append(nodes[index]["index"])  # 加入该节点
        if len(nodes[index]["forward_node"]) > 0:  # 加入相邻的节点,只需要进行后向遍历
            next = nodes[index]["forward_node"]
            q.extend(next)

    return parameter_index