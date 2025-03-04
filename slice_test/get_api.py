import json


def get_vul_api_id(api_info):  #
    """
    获得c语言元源程序中的危险函数的信息，api_info是joern获得的相关函数的信息
    :param api_info: 源文件所有函数api信息
    :return: vul_api_id: list，包含源文件中所有敏感函数id
             vul_api_line: list，包含源文件中所有敏感函数name和行号lineNumber
    """
    vul_api_id = []
    vul_api_line = []
    file = open("data/vul_api.txt", "r")  # api.txt是敏感函数列表
    data_set = set()
    for line in file:
        line = line.strip()
        data_set.add(line)  # 将api.txt中的内容取出放到data_set中
    for key in api_info:
        if key[0] in data_set:
            vul_api_id.append(api_info[key]["id"])
            vul_api_line.append((api_info[key]['name'], api_info[key]["lineNumber"]))  # (name,lineNumber)
    return vul_api_id, vul_api_line


def get_all_api(api_path):
    api_info = {}
    with open(api_path, 'r') as file:
        content = file.read().replace("]\n[", ",\n")
        data = json.loads(content)  # data type: list
    for api in data:
        api_info[(api["_3"], api["_1"])] = {"id": api["_1"], "lineNumber": api["_2"], "code": api["_4"],
                                            "arg_line": api["_5"], "arg_id": api["_6"], "callee_id": api["_7"],
                                            "callee_parameter_id": api["_8"],
                                            "name": api["_3"]}  # api["_7"] : list [100, 101, 102]
    return api_info