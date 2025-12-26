# Fix/chatgpt_2025_12_26 分支修改记录

## 分支目标
通过修改 run_gpt_prompt.py 让代码适应新的 ChatGPT API，使项目能够正常运行。

## 背景
- 原项目使用旧的 OpenAI Completion API (`text-davinci-003`)
- 新代码迁移到 ChatCompletion API (`gpt-3.5-turbo`)
- 原代码保存在 `run_gpt_prompt_old.py` 中

---

## 已完成的修改

### 1. 修复 `run_gpt_prompt_action_arena` 的花括号清理问题

**问题：**
- Prompt 模板使用 `{arena_name}` 格式（如 `{cafe}`, `{kitchen}`）
- ChatGPT 学习这个格式，返回 `{"output": "{cafe}"}`
- 原 cleanup 函数 `split("}")[0]` 导致 `"{cafe}"` → `"{cafe"` (保留左花括号)
- 使用 `"{cafe"` 访问 spatial_memory 时触发 `KeyError: '{cafe'`

**修复：** `run_gpt_prompt.py` 第 676-680 行
```python
def __chat_func_clean_up(gpt_response, prompt=""):
    # Fixed: strip() removes whitespace, then strip("{}") removes braces from both ends
    # This handles cases where ChatGPT returns "{cafe}" format (from prompt template examples)
    cleaned_response = gpt_response.strip().strip("{}")
    return cleaned_response
```

**效果：**
- `"{cafe}"` → `"cafe"` ✅
- `"{cafe"` → `"cafe"` ✅
- `"cafe}"` → `"cafe"` ✅
- `"cafe"` → `"cafe"` ✅

---

### 2. 修复 `run_gpt_prompt_task_decomp` 的列表格式问题

**问题：**
- 期望 ChatGPT 返回字符串格式：`"1. Task...\n2. Task..."`
- 实际 ChatGPT 返回列表格式：`["1. Task...", "2. Task..."]`
- cleanup 函数调用 `gpt_response.split("\n")` 失败（列表没有 split 方法）
- 导致 validate 失败，最终返回 `False` 而不是列表

**修复内容：**

#### a) 修改 example_output 为列表格式（第 465-471 行）
```python
# 之前（字符串）：
example_output = '1. Wake up...\n2. Brush teeth...'

# 现在（列表）：
example_output = [
    "1. Wake up (duration in minutes: 5, minutes left: 55)",
    "2. Brush teeth (duration in minutes: 5, minutes left: 50)",
    "3. Take a shower (duration in minutes: 15, minutes left: 35)",
    "4. Get dressed (duration in minutes: 10, minutes left: 25)",
    "5. Have breakfast (duration in minutes: 25, minutes left: 0)"
]
```

#### b) 修改 special_instruction（第 473 行）
```python
special_instruction = 'The output must be a JSON array of strings. Each string should be a numbered subtask following the format: "1. [subtask] (duration in minutes: [X], minutes left: [Y])". The durations must sum to the total duration specified in the prompt.'
```

#### c) 修改 cleanup 函数兼容列表和字符串（第 394-399 行）
```python
def __chat_func_clean_up(gpt_response, prompt=""):
    # Handle both list (expected from ChatGPT JSON array) and string formats
    if isinstance(gpt_response, list):
        temp = [i.strip() for i in gpt_response]
    else:
        temp = [i.strip() for i in gpt_response.split("\n")]
    # 后续逻辑不变...
```

**效果：**
- ✅ ChatGPT 现在更倾向于返回列表格式（符合 example）
- ✅ cleanup 函数能处理列表（主要路径）
- ✅ cleanup 函数也兼容字符串（防御性编程）
- ✅ `run_gpt_prompt_task_decomp` 不再返回 `False`

---

### 3. 修复 `ChatGPT_safe_generate_response` 的 fail_safe 返回问题

**问题：**
- 文件：`gpt_structure.py` 第 165 行
- 当所有重试失败后，函数返回 `False` 而不是 `fail_safe_response`
- 调用方期望 fail_safe 值（如 `[["asleep", 1]]`），收到 `False` 导致 `TypeError`

**修复：** `gpt_structure.py` 第 165-166 行
```python
# 之前：
return False

# 现在：
print("FAIL SAFE TRIGGERED")
return fail_safe_response
```

**效果：**
- ✅ 失败时返回正确的 fail_safe 值
- ✅ 不再出现 `TypeError: 'bool' object is not iterable`
- ✅ 与老版本 `ChatGPT_safe_generate_response_OLD` 行为一致

---

## 测试结果

### ✅ 已解决的错误
1. `KeyError: '{cafe'` - 花括号清理问题 ✅
2. `TypeError: 'bool' object is not iterable` - fail_safe 返回问题 ✅
3. `run_gpt_prompt_task_decomp` 列表格式问题 ✅

### ⚠️ 发现的新问题
- `generate_action_arena` 触发 FAIL SAFE，返回 `"kitchen"`
- `KeyError: 'kitchen'` - fail_safe 值在当前 sector 中不存在

---

## 修改的文件

1. **run_gpt_prompt.py**
   - 第 676-680 行：`run_gpt_prompt_action_arena` 的 cleanup 函数
   - 第 394-399 行：`run_gpt_prompt_task_decomp` 的 cleanup 函数
   - 第 465-471 行：`run_gpt_prompt_task_decomp` 的 example_output
   - 第 473 行：`run_gpt_prompt_task_decomp` 的 special_instruction

2. **gpt_structure.py**
   - 第 165-166 行：`ChatGPT_safe_generate_response` 的返回值

3. **新增测试文件**（用于问题诊断）
   - `test_action_arena_bug.py` - 测试花括号清理问题
   - `test_prompt_template_analysis.py` - 分析 prompt 模板问题
   - `analysis_old_vs_new_code.py` - 对比老代码和新代码
   - `analysis_comparison_en.md` - 英文分析文档
   - `comparison_string_vs_array.md` - 字符串 vs 数组格式对比

---

## 下一步计划

### 优先级 1：修复 `run_gpt_prompt_action_arena` FAIL SAFE 问题
- 问题：硬编码的 fail_safe `"kitchen"` 不适用于所有场景
- 方案：
  1. 调查为什么 ChatGPT 调用失败（启用 verbose 模式）
  2. 考虑动态 fail_safe（从可用 arenas 中选择）

### 优先级 2：检查其他 `run_gpt_prompt_*` 函数
- 可能遇到类似的列表/字符串格式问题
- 按需修改，采用防御性编程

### 优先级 3：测试完整的模拟流程
- 确保所有 persona 能正常运行
- 验证长时间运行的稳定性

---

## 技术要点总结

### ChatGPT API 格式差异
- **老 API (Completion)**：返回纯文本
- **新 API (ChatCompletion)**：返回 JSON，需要提取 `["output"]`
- **ChatGPT 的"优化"行为**：可能将字符串转为数组，不严格遵循 example

### 修复策略
1. **防御性编程**：cleanup 函数同时支持字符串和列表
2. **明确 example**：使用期望的格式作为 example_output
3. **Fail-safe 机制**：确保失败时返回合理的默认值

### 经验教训
1. Prompt 模板的格式会影响 ChatGPT 的输出
2. ChatGPT 可能"自作主张"优化输出格式
3. cleanup 函数需要能处理多种可能的输入格式
4. Fail-safe 值应该根据上下文动态生成，而不是硬编码

---

## 贡献者
- 修改日期：2025-12-26
- 分支：fix/chatgpt_2025_12_26
