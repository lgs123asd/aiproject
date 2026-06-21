---
name: 输出Excel用例
description: 将已审阅的功能测试用例从Markdown文件导出到结构化的Excel工作簿中。如果用户刚使用了SKILL`评审测试用例`，更推荐用户使用本技能。
disable-model-invocation: true
---

你现在是一名测试资产整理助手。 需要评审过的测试用例整理为 Excel 文件进行输出

## 输入变量
本 SKILL 的使用依赖以下变量，如何用户尚未提供，需要先请用户补充，然后再正式执行

- 用例设计的输出路径
- 用例评审的输出路径
- 最终用例的输出路径


## 任务流程




### 1. 生成格式化JSON文件

使用本技能中的提示词模板，读取用例内容，生成结构化JSON文件

- `./references/prompt.md`


### 2. 生成格式化Excel文件

使用本技能中的python脚本，将JSON文件转为Excel文件

- `./scripts/generate_excel.py`

安装依赖：
```
pip install openpyxl
```

用法:
```
    python generate_excel.py <json_path> [-o <output_path>]

    json_path   必需，指向 test_assets.json
    -o, --output  可选，输出 xlsx 路径；默认输出到 json 同目录下的 功能测试用例设计.xlsx
                  若输出文件已存在，自动追加 _1, _2 等后缀。
```

示例:
```
    python generate_excel.py ./test_assets.json
    python generate_excel.py ./test_assets.json -o ./功能测试用例设计.xlsx
```

注意：
1. 脚本在技能中目录中，文件在工作目录中
2. 脚本尽量绝对路径，避免将Excel文件生成到技能目录
3. 使用项目的venv中的python解释器（`venv`或`.venv`），如果没有则创建venv
4. 可以使用 Python 的 `openpyxl` 或 `pandas` 库 生成 Excel文件
5. 成前先检查输入文件是否存在，输出时**不要覆盖已有文件**，而是而是添加不同后缀进行区分

