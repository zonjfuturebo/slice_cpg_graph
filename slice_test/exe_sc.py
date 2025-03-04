import os


def replace_scala(scala_path, source_path):
    """
    替换sc文件中的导入文件
    :param scala_path: sc文件路径
    :param source_path: 源文件路径
    :return:
    """
    exc_content = f"importCode(\"{source_path}\", \"a\")\n"  # 构造查询语句importCode("{source_path}", "a")

    # 需要替换的行号，从1开始计数
    line_to_replace = 7

    # 读取文件内容到内存
    with open(scala_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 检查行号是否超出文件行数范围
    if 0 < line_to_replace <= len(lines):

        if lines[line_to_replace - 1][0:10] != "importCode":
            print("请检查scala文件！！！")
            return 0

        # 替换指定行的内容（行号减1得到列表索引）
        lines[line_to_replace - 1] = exc_content

        # 将修改后的内容写回文件
        with open(scala_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            return 1
    else:
        print(f"文件中没有行号为 {line_to_replace} 的行")
        return 0


def exc_scala(scala_path, source_path):
    # 执行get_all_call.scala文件
    if replace_scala(scala_path, source_path):
        os.system(f"joern --script {scala_path}")
        print("get_all_call.scala执行成功")
        return 1
    else:
        print("get_all_call.scala执行失败")
        return 0