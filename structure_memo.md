# 项目结构说明 — structure_memo.md ✅

## 完整目录（详细版）
下面列出仓库中更全面的目录树与关键信息，便于查找文件或快速定位实现点。

- 根目录
  - `README.md`：项目说明、安装与运行示例。
  - `requirements.txt`：Python 依赖。
  - `Claud.md`：项目总览（摘要版）。
  - `structure_memo.md`：本文件（更详尽的结构说明）。
  - `LICENSE`, `cover.png`, `.gitignore`, `.gitattributes` 等。

- `reverie/`
  - `compress_sim_storage.py` — 压缩仿真为可演示包（用于 frontend demo）。
  - `global_methods.py` — 脚本级工具（文件/CSV 操作、复制目录等）。
  - `backend_server/`
    - `reverie.py` — ReverieServer 类（主循环、fork/save/replay、CLI）。关键点：`start_server`, `save`, `open_server`。
    - `maze.py` — 地图加载与瓦片管理（`tiles`, `address_tiles`, `get_nearby_tiles`, `access_tile` 等）。
    - `path_finder.py` — 路径搜索函数（`path_finder`）。
    - `test.py` — 辅助测试脚本。
    - `utils.py` — 运行配置/路径/API key（需用户提供）。

    - `persona/` — 智能体实现
      - `persona.py` — `Persona` 类：封装记忆、调用认知模块（`perceive`, `retrieve`, `plan`, `reflect`, `execute`）。
      - `memory_structures/`
        - `scratch.py` — 短期记忆（当前行为、日程、聊天、路径），包含 `get_curr_event_and_desc()`, `add_new_action()` 等方法。
        - `associative_memory.py` — 联想记忆（事件/思想/聊天序列），保存并支持检索/embedding 操作（`add_event`, `add_thought`, `retrieve_relevant_events` 等）。
        - `spatial_memory.py` — 空间记忆树（由 path tester 构建）。
      - `cognitive_modules/` — 认知流水线模块（每个模块有明确职责）：
        - `perceive.py`：感知模块（`perceive(persona, maze)`）；筛选视野内事件、计算 embedding 与 poignancy。
        - `retrieve.py`：检索模块（`retrieve(persona, perceived)` / `new_retrieve`）；计算 recency/relevance/importance 并返回候选记忆节点。
        - `plan.py`：规划模块（`generate_hourly_schedule`, `generate_task_decomp`, `generate_action_*` 等）；生成日程、任务分解与动作地址/事件三元组。
        - `execute.py`：执行模块（`execute(persona, maze, personas, plan)`）；生成路径（`planned_path`）并输出下一步移动与描述。
        - `reflect.py`：反思模块（`reflect(persona)`, `run_reflect`）；根据阈值触发，生成思考并写入记忆。
        - `converse.py`：对话模块（`agent_chat_v1/2`, `generate_one_utterance`, `open_convo_session`）；管理代理间或交互式会话并将结果入库。
      - `prompt_template/` — LLM 提示模板目录（`v1/`, `v2/`, `v3_ChatGPT/` 等）及拼装器脚本（`run_gpt_prompt.py`, `gpt_structure.py`）。

- `environment/frontend_server/`（Django 前端）
  - `manage.py`, `wsgi.py` 等 Django 启动工具与设置（`settings/`）。
  - `templates/`：前端页面（`base.html`, `path_tester/`, `demo/`, `simulator_home` 等）。
  - `static_dirs/`
    - `assets/`：角色图片、地图素材（`the_ville`）、精灵图（`atlas.png` / `atlas.json`）。
    - `css/`, `img/`：样式与静态图片。
  - `storage/`（仿真数据）
    - `<sim_code>/`
      - `reverie/meta.json`（仿真元数据：start_date, curr_time, maze_name, persona_names, step 等）
      - `environment/<step>.json`（前端输出的环境状态）
      - `movement/<step>.json`（后端写出的移动结果）
      - `personas/<name>/bootstrap_memory/`：个人记忆存档
        - `spatial_memory.json`, `scratch.json`, `associative_memory/`（`nodes.json`, `embeddings.json`, `kw_strength.json` 等）
  - `compressed_storage/`：压缩后演示包目录（用于 demo 页面）。
  - `temp_storage/`：前后端通信临时文件（`curr_sim_code.json`, `curr_step.json`, `path_tester_env.json`, `path_tester_out.json` 等）。

- 其他重要脚本/文件
  - `reverie/compress_sim_storage.py` — 压缩演示用函数（将 `storage/<sim>` 转为 demo 包）。
  - 若新增历史数据：`environment/frontend_server/static_dirs/assets/the_ville/agent_history_init_*.csv` 用于批量加载 agent 历史。
