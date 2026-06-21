./references/prompt.md

# 测试用例JSON版 生成提示词

> 阅读本文档，从指定的输入文件提取数据，输出一个结构化的 JSON 文件。
> JSON 文件将用于 `generate_excel.py` 生成 `功能测试用例设计.xlsx`。

---

## 输入文件

| 用途     | 路径 | 说明                              |
|--------|------|---------------------------------|
| 测试用例设计 | `用例设计/*-用例.md` | 每个模块一个文件 |
| 需求理解   | `用例设计/*-需求理解.md` | 每个模块一个文件，第7节为"待确认问题"表格          |
| 评审报告   | `用例评审/评审报告.md` | 包含评审概览、逐用例评审详情、维度分析、问题清单        |
| 需求目录   | `需求内容/目录.md` | 模块列表和规则编号索引（可选参考）               |
| 风险清单   | `需求内容/08-风险清单与待确认汇总.md` | 在需求文档拆分阶段发现的风险内容（可选参考） |

如果用户指定了特定的功能、模块，这仅对指定模块的进行用例输出
如果没有指定，那么对用例设计中做所有的用例进行输出



## 输出文件

将以下 JSON 结构输出到 `./test_assets.json`。

---

## JSON 结构

```json
{
  "meta": {
    "generated_at": "2026-05-30",
    "review_date": "2026-05-30",
    "modules": ["02-注册与登录", "03-商品与搜索", "04-购物车与下单", "06-用户中心与地址"]
  },

  "stats": {
    "module_counts": [
      {"module": "02-注册与登录", "count": 39},
      {"module": "03-商品与搜索",  "count": 41},
      {"module": "04-购物车与下单", "count": 20},
      {"module": "06-用户中心与地址", "count": 14}
    ],
    "priority_counts": [
      {"priority": "P0", "count": 17},
      {"priority": "P1", "count": 70},
      {"priority": "P2", "count": 27}
    ],
    "type_counts": [
      {"type": "正向", "count": 45},
      {"type": "异常", "count": 25},
      {"type": "边界", "count": 15},
      {"type": "权限", "count": 8},
      {"type": "状态", "count": 6},
      {"type": "配置", "count": 7},
      {"type": "数据一致性", "count": 6}
    ],
    "coverage": [
      {"dimension": "正向功能", "status": "充分", "note": "核心业务流程均有 P0 正向用例覆盖"},
      {"dimension": "异常输入", "status": "充分", "note": "空值、格式错误、不存在、超长等场景均有覆盖"},
      {"dimension": "边界值", "status": "充分", "note": "用户名/密码长度边界、数量边界等均有覆盖"},
      {"dimension": "权限控制", "status": "基本充分", "note": "游客/登录用户权限隔离有覆盖"},
      {"dimension": "状态流转", "status": "基本充分", "note": "注册审核、账号禁用、商品上下架、库存变化等状态均有覆盖"},
      {"dimension": "配置联动", "status": "部分覆盖", "note": "验证码开关、协议开关有覆盖；分类层级、排序配置未深入"},
      {"dimension": "数据一致性", "status": "基本充分", "note": "注册DB记录、登录日志、库存扣减、购物车清除均有验证"}
    ],
    "review_summary": {
      "total_cases": 114,
      "passed": 100,
      "need_modify": 9,
      "need_confirm": 5,
      "modules": "4（02/03/04/06）",
      "conclusion": "有条件通过"
    },
    "pending_questions_by_module": {
      "02-注册与登录": 10,
      "03-商品与搜索": 10,
      "04-购物车与下单": 9,
      "06-用户中心与地址": 7
    },
    "review_issues_by_severity": {
      "必须修改": 2,
      "应该修改": 7,
      "可优化": 5,
      "需确认": 5
    }
  },

  "test_cases": [
    {
      "id": "REG-TC-001",
      "module": "02-注册与登录",
      "sub_module": "用户注册",
      "requirement_source": "REG-002, REG-003, REG-004, REG-005, REG-006",
      "test_point_id": "REG-TP-001",
      "title": "输入合法用户名和密码并勾选协议，验证注册成功",
      "priority": "P0",
      "type": "正向",
      "precondition": "① 后台配置：注册方式=账号注册，注册图片验证码=关闭，注册协议=开启，注册审核=关闭；② 测试用户名未被注册",
      "test_data": "用户名：testuser01（字母+数字，8字符）；密码：pass123（字母+数字，7字符）",
      "steps": "1. 访问注册页面\n2. 在"用户名"输入框输入 testuser01\n3. 在"设置登录密码"输入框输入 pass123\n4. 勾选"阅读并同意"复选框\n5. 点击"注册"按钮",
      "expected": "① 页面提示注册成功（如"注册成功"文案或 toast 提示）\n② 页面跳转至登录页面",
      "cleanup": "登录后台或通过接口删除测试账号 testuser01",
      "notes": "核心主流程"
    }
  ],

  "pending_questions": [
    {
      "id": "02-注册与登录-Q01",
      "module": "02-注册与登录",
      "requirement_location": "R02-01, R02-08",
      "description": "注册成功后是自动登录并跳转首页，还是跳转登录页让用户手动登录？",
      "impact": "注册流程终点、用例设计",
      "confirm_with": "产品经理",
      "handling": "暂未处理（待业务方确认）"
    }
  ],

  "review_issues": [
    {
      "id": "M-001",
      "severity": "必须修改",
      "type": "覆盖充分性",
      "related_cases": "CART-TC-009",
      "related_requirement": "CART-TP-015",
      "description": "CART-TP-015（全选结算，P0）缺少对应测试用例。CART-TC-009 仅覆盖部分勾选场景",
      "suggestion": "补充一条 P0 用例：全选购物车商品→结算→验证确认页包含全部选中商品",
      "status": "待处理"
    }
  ]
}
```

---

## 字段说明

### test_cases

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 用例ID，全局唯一，如 `REG-TC-001` |
| module | string | 所属模块编号，如 `02-注册与登录` |
| sub_module | string | 子模块名，如 `用户注册` |
| requirement_source | string | 需求编号或章节，多个用逗号分隔。如需求未明确则填 `—` |
| test_point_id | string | 对应测试点ID |
| title | string | 用例标题，一句话描述验证目标 |
| priority | string | `P0` / `P1` / `P2` |
| type | string | `正向` / `异常` / `边界` / `权限` / `状态` / `配置` / `数据一致性` / `探索性/待确认` |
| precondition | string | 可执行的前置条件。多条用 `① ② ③` 编号 |
| test_data | string | 具体、脱敏的测试数据 |
| steps | string | 操作步骤，使用 `\n` 分隔每个步骤。步骤编号 `1. 2. 3.` |
| expected | string | 预期结果，使用 `\n` 分隔每个断言。编号 `① ② ③` |
| cleanup | string | 数据清理或配置恢复动作 |
| notes | string | 备注：待确认、探索性、依赖说明等。无则填空字符串 |

### pending_questions

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 问题编号，格式 `{模块}-Q{序号}`，如 `02-注册与登录-Q01` |
| module | string | 所属模块编号 |
| requirement_location | string | 需求位置（风险编号或需求编号） |
| description | string | 问题描述 |
| impact | string | 对测试设计的影响 |
| confirm_with | string | 建议确认对象，如 `产品经理` `开发团队` |
| handling | string | 当前处理方式 |

### review_issues

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 问题编号，如 `M-001` `S-001` `O-001` `C-001` |
| severity | string | `必须修改` / `应该修改` / `可优化` / `需确认` |
| type | string | 问题类型：`覆盖充分性` / `需求追溯` / `去重` / `可执行性` / `可观察性` / `预期正确性` |
| related_cases | string | 涉及的用例ID，多个用逗号分隔 |
| related_requirement | string | 涉及的需求编号 |
| description | string | 问题描述 |
| suggestion | string | 修改建议 |
| status | string | `待处理` / `已修复` / `已确认` |

---

## 数据提取指南

### 从 `用例设计/*-用例.md` 提取 test_cases

每个测试用例以 `### CASE-ID：标题` 开头，随后是一个表格：

```
| 字段 | 内容 |
|------|------|
| 用例ID | REG-TC-001 |
| 模块 | 用户注册 |
| 需求来源 | REG-002, REG-003 |
| ...
```

将每个表格的"字段"→"内容"映射为 JSON 字段：
- `用例ID` → `id`
- `模块` → `sub_module`（再根据文件名推导 `module`，如 `02-注册与登录`）
- `需求来源` → `requirement_source`
- `测试点ID` → `test_point_id`
- `用例标题` → `title`
- `优先级` → `priority`
- `用例类型` → `type`
- `前置条件` → `precondition`
- `测试数据` → `test_data`
- `操作步骤` → `steps`
- `预期结果` → `expected`
- `清理动作` → `cleanup`
- `备注` → `notes`

### 从 `用例设计/*-需求理解.md` 提取 pending_questions

找到 `## 7. 待确认问题` 下的表格。表格列为：`编号 | 问题 | 影响范围 | 风险引用`。

将每行映射为：
- `编号` → `id` 的一部分（加上模块前缀）
- `问题` → `description`
- `影响范围` → `impact`
- `风险引用` → `requirement_location`

### 从 `用例评审/评审报告.md` 提取 review_issues

找到 `## 四、问题清单` 下的四个子段：
- `### 必须修改（2 项）`
- `### 建议修改（7 项）`
- `### 优化项（5 项）`
- `### 需确认（5 项）`

每个子段下有一张表格，提取数据行。将 severity 映射为对应中文等级。

### 生成 stats

- `module_counts` 和 `priority_counts` 和 `type_counts`：从 test_cases 数组统计得出
- `coverage`：从评审报告 `## 三、维度汇总分析 → 3.3 覆盖充分性` 提取
- `pending_questions_by_module`：从 pending_questions 数组统计
- `review_issues_by_severity`：从 review_issues 数组统计
- `review_summary`：从评审报告 `## 一、评审概览` 提取

---

## 注意事项

1. **不要编造数据**。如果某个字段在源文件中缺失，填空字符串 `""`。
2. **保留原始换行**。steps 和 expected 字段中，用 `\n` 保留原始文件的步骤分隔。
3. **优先级和类型使用标准值**。不要使用 `高/中/低` 或 `功能测试` 等非标准值。
4. **JSON 是纯数据**。不要包含 markdown 格式、HTML 标签或任何富文本。
5. **输出到指定路径**：`test_assets.json`
