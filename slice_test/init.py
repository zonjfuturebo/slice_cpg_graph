import os
import re
import shutil


class PathInitializer:
    """
    资源路径类，包含如下路径：
    root：根路径，{file_name}
    cpg文件路径：root/cpg_{file_name}.json
    pdg文件路径：root/pdg_{file_name}.txt
    api文件路径：root/api_{file_name}.txt
    method_chain方法链路径：root/chain_{file_name}.json
    method_call方法调用路径：root/call_{file_name}.json
    vul_method敏感函数保存路径：root/vul_method_{file_name}
    vul_loc敏感函数信息路径：root/vul_loc_{file_name}
    vul_api_line_name路径：root/vul_linename_{file_name}
    slice_save切片保存路径：root/slice_save_{file_name}
    """

    def __init__(self, base_dir, file_name):
        """
        初始化
        :param base_dir: 根路径，即README中的s01同级目录
        :param file_name: 源文件名称
        """
        self.base_dir = base_dir
        self.file_name = file_name
        self.file_dir = os.path.join(base_dir, file_name)
        self.result_dir = os.path.join(base_dir, "result")  # result目录
        self.output_dir = os.path.join(self.result_dir, f"{file_name}")  # result目录下的file_name子目录

    def get_cpg_path(self):
        return os.path.join(self.output_dir, f"cpg_{self.file_name}.json")

    def get_pdg_path(self):
        return os.path.join(self.output_dir, f"pdg_{self.file_name}.txt")

    def get_scan_api_path(self):
        return os.path.join(self.output_dir, f"api_{self.file_name}.txt")

    def get_method_chain_path(self):
        return os.path.join(self.output_dir, f"chain_{self.file_name}.json")

    def get_vul_location_path(self):
        return os.path.join(self.output_dir, f"vul_loc_{self.file_name}.pkl")

    def get_vul_method_path(self):
        return os.path.join(self.output_dir, f"vul_method_{self.file_name}.pkl")

    def get_vul_api_line_name_path(self):
        return os.path.join(self.output_dir, f"vul_linename_{self.file_name}.pkl")

    def get_method_call_path(self):
        return os.path.join(self.output_dir, f"call_{self.file_name}.json")

    def get_save_path(self):
        return os.path.join(self.output_dir, f"slice_save_{self.file_name}.txt")

    def get_all_paths(self):
        return [
            self.get_scan_api_path(),
            self.get_cpg_path(),
            self.get_pdg_path(),
            self.get_method_call_path(),
            self.get_vul_method_path(),
            self.get_save_path(),
            self.get_vul_location_path(),
            self.get_method_chain_path(),
        ]


def check_path(path_initializer: PathInitializer):
    """
    检查路径是否存在
    :param path_initializer: PathInitializer 类的实例
    :return: 包含路径检查结果的字典
    """

    def check_all_true(path_exists):
        """
        检查字典中的所有值是否都是 True
        :param path_exists: 包含路径检查结果的字典
        :return: 如果所有值都是 True，返回 True；否则返回 False
        """
        return all(path_exists.values())

    files = {
        "cpg_path": path_initializer.get_cpg_path(),
        "pdg_path": path_initializer.get_pdg_path(),
        "scan_api_path": path_initializer.get_scan_api_path(),
        "method_chain_path": path_initializer.get_method_chain_path(),
        "method_call_path": path_initializer.get_method_call_path(),
        "vul_method_path": path_initializer.get_vul_method_path(),
        "slice_save_path": path_initializer.get_save_path(),
        "vul_loc_path": path_initializer.get_vul_location_path(),
        "vul_api_line_name_path": path_initializer.get_vul_api_line_name_path(),
    }
    paths = {
        "result_dir": path_initializer.result_dir,
        "output_dir": path_initializer.output_dir,
    }

    print("当前路径如下：")
    for key, path in paths.items():
        print(f"{key}: {path}")
    for key, path in files.items():
        print(f"{key}: {path}")

    # 检查每个路径是否存在
    print("*********************************")
    print("检查路径是否存在：")
    paths_exists = {}
    files_exists = {}
    for key, path in paths.items():
        if os.path.exists(path) and os.path.isdir(path):
            try:
                shutil.rmtree(path)  # 删除目录及其所有内容
            except OSError as e:
                print(f'删除路径{path}时出错: {e.strerror}')
        os.makedirs(path)  # 重新创建目录
        paths_exists[key] = True
        if os.path.isfile(path):
            print(f"{key} is a file，请检查路径是否正确!!!")
            paths_exists[key] = False

    for key, path in files.items():
        if os.path.exists(path) and os.path.isfile(path):
            try:
                os.remove(path)  # 删除文件
            except OSError as e:
                print(f'删除文件{path_initializer.file_name}时出错: {e.strerror}')
        with open(path, 'w') as f:
            pass  # 创建空文件
        files_exists[key] = True
        if os.path.isdir(path):
            print(f"{key} is a directory，请检查路径是否正确!!!")
            files_exists[key] = False

    result = {**paths_exists, **files_exists}
    if check_all_true(result):
        print("所有路径和文件都存在且正确创建。")
    else:
        print("存在路径或文件未正确创建。")


def remove_comments_c(filename):
    """
    移除c文件注释
    :param filename: 表示要去除注释的c语言的文件名
    :return:
    """
    bds0 = '//.*'  # 标准匹配单行注释
    bds1 = '\/\*(?:[^\*]|\*+[^\/\*])*\*+/'  # 标准匹配多行注释  可匹配跨行注释

    target1 = re.compile(bds0)  # 单行注释
    targetn = re.compile(bds1)  # 编译正则表达式

    # 读取源文件
    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()

    comment1 = target1.findall(source_code)  # 得到单行注释
    commentn = targetn.findall(source_code)  # 得到多行注释
    comments = comment1 + commentn  # 得到所有的注释

    for i in comments:
        source_code = source_code.replace(i, '')  # 将注释替换为空字符串

    # 写回到源文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(source_code)

    print("注释去除完成")


def remove_html_tag(filename):
    """
    移除文件中html<BR/>标签
    :param filename: 表示要去除注释的txt语言的文件名
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        cleaned_content = re.sub(r'<BR\s*/>', ', ', content)  # 支持<BR/>、<br/>等变体

    with open("data/test_cpg_txt.txt", 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print("html去除完成")
    return "data/test_cpg_txt.txt"

def replace_html_tag(filename):
    """
    替换可能的html标签，包含
    :param filename: 表示要去除注释的txt语言的文件名
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        cleaned_content = re.sub()
