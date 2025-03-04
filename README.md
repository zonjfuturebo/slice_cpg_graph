# README

## 项目概述
本项目旨在处理C/C++源代码文件，通过静态分析生成控制流图（CPG）和程序依赖图（PDG），并进一步提取API信息、漏洞API标识以及方法调用链。项目主要包含以下功能模块：
1. **路径初始化与预处理**：清理注释，生成Scala脚本文件。
2. **CPG与PDG处理**：解析CPG和PDG信息，生成节点及其依赖关系。
3. **API信息提取**：从源码中提取API调用信息，并识别潜在的漏洞API。
4. **方法调用链生成**：基于漏洞API生成方法调用链。

---

## 文件结构
```
slice_test/
├── exe_main.py          # 主程序入口
├── init.py              # 初始化模块，包括路径设置和注释清理
├── get_cpgNodes.py      # 解析CPG和PDG节点信息
├── get_api.py           # 提取API信息及漏洞API标识
├── get_chain.py         # 生成方法调用链
├── exe_sc.py            # 执行Scala脚本
└── data/                # 数据目录
    ├── CWE/             # 存放CWE相关数据
    │   └── S01/         # 示例数据集
    ├── cpg_json_bad.json # CPG节点信息示例
    ├── pdg_txt_bad.txt   # PDG信息示例
    ├── all_api_bad.txt   # API信息示例
    └── method_chain_bad.json # 方法调用链示例
```


---

## 使用说明

### 环境依赖
- Python 3.x
- Scala（用于执行`.sc`脚本）
- 相关Python库：`os`

### 快速开始
1. **配置工作路径**  
   修改`exe_main.py`中的`work_path`变量，确保其指向项目根目录。

2. **准备输入文件**  
   将待分析的C/C++源文件放入`data/CWE/S01/`目录下，并确保文件名与代码中`file_path`变量一致。

3. **运行主程序**  
   执行以下命令运行主程序：
   ```bash
   python exe_main.py
   ```


4. **查看输出结果**  
   - CPG和PDG节点信息将存储在内存中，可通过调试或日志查看。
   - 方法调用链信息将生成并存储在`method_chain`变量中。

---

## 功能模块详解

### 1. 路径初始化与预处理
- **模块文件**: `init.py`
- **功能**: 
  - 初始化工作路径。
  - 清理源代码中的注释。
  - 生成Scala脚本文件（`.sc`）。

### 2. CPG与PDG处理
- **模块文件**: `get_cpgNodes.py`
- **功能**:
  - 解析CPG JSON文件，生成节点信息。
  - 将PDG信息添加到CPG节点中，形成完整的依赖关系。

### 3. API信息提取
- **模块文件**: `get_api.py`
- **功能**:
  - 提取源代码中的API调用信息。
  - 标识潜在的漏洞API（如`memcpy`）。

### 4. 方法调用链生成
- **模块文件**: `get_chain.py`
- **功能**:
  - 基于漏洞API生成方法调用链。
  - 输出调用链信息，便于后续分析。

---

## 示例数据
项目提供了一组示例数据，位于`data/`目录下：
- `cwe121_bad.c`: 示例C源文件，包含缓冲区溢出漏洞。
- `cpg_json_bad.json`: 示例CPG节点信息。
- `pdg_txt_bad.txt`: 示例PDG信息。
- `all_api_bad.txt`: 示例API信息。
- `method_chain_bad.json`: 示例方法调用链。

---

## 注意事项
1. **路径配置**: 确保`work_path`和相关子路径正确配置。
2. **依赖安装**: 确保已安装Scala环境，并配置好相关依赖。
3. **文件格式**: 输入文件需符合预期格式，否则可能导致解析失败。

---

## 联系方式
如有问题，请联系项目维护者：
- 邮箱: example@example.com
- GitHub: [项目地址](https://github.com/example/slice_test)

--- 

希望本项目能为您的静态分析工作提供帮助！
