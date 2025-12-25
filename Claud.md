# Generative Agents — 项目概述与结构 ✅

## 概要
- 目的：实现论文《Generative Agents: Interactive Simulacra of Human Behavior》中描述的模拟系统 —— 构建一个由“人物（personas）”驱动的世界，核心流为感知、检索、规划、执行与反思。仓库包含后端模拟引擎和基于 Django 的前端可视化与回放功能。

## 快速开始（概要）
- 在后端 `reverie/backend_server` 中添加 `utils.py`，放入 OpenAI API Key。
- 启动环境服务器：`cd environment/frontend_server && python manage.py runserver`
- 启动模拟：`cd reverie/backend_server && python reverie.py`，按提示选择 fork 的基线仿真并使用 `run <steps>` 运行，使用 `fin` 保存。

---

## 顶层目录与主要模块说明 🔧

- **`reverie/`** — 核心模拟代码与工具
	- `backend_server/` — 模拟引擎
		- `reverie.py` — ReverieServer：主循环，加载/分支仿真，管理 persona 生命周期、步进、保存与回放，以及交互式 CLI。
		- `maze.py` — 世界表示：瓦片矩阵、碰撞、分区（sector/arena）、游戏对象、地址反查与邻域搜索。
		- `path_finder.py` — 路径规划工具，供 persona 移动时使用。
		- `global_methods.py` & `utils.py` — 通用工具函数（IO、CSV、文件检查），`utils.py` 还承载 API key 与路径配置。
		- `compress_sim_storage.py` — 将仿真压缩为演示用的格式。

	- `persona/` — 智能体代码（认知模块）
		- `persona.py` — Persona 类：初始化记忆、协调认知流水线并驱动移动。
		- `memory_structures/` — 记忆结构
			- `scratch.py` — 短期记忆：当前动作、日程、反思参数等（含 `get_curr_event_and_desc()` 等方法，后端用于更新瓦片事件）。
			- `associative_memory.py` — 联想记忆（事件 / 思想流），检索与序列化。
			- `spatial_memory.py` — 个体学习到的空间/地点信息。
		- `cognitive_modules/` — 模块化认知步骤：`perceive.py`, `retrieve.py`, `plan.py`, `reflect.py`, `execute.py`, `converse.py`。
		- `prompt_template/` — LLM 提示模板与拼装器（用于计划、对话、任务分解等）。

- **`environment/frontend_server/`** — Django 前端与仿真数据
	- `manage.py` / Django 配置与视图：提供地图、回放与 demo 页面。
	- `static_dirs/` — 精灵图、视觉资源、CSS 等前端资源。
	- `templates/` — 模拟器页面、演示与回放页面模板。
	- `storage/` — 保存的仿真目录（每个仿真带 `reverie/meta.json`、按步骤的 `environment/*.json`、以及 `personas/<name>/bootstrap_memory/*`）。
	- `compressed_storage/` — 已压缩的演示文件夹。

- **其他文件**
	- `requirements.txt` — 运行依赖（Django、OpenAI、Selenium、numpy 等）。
	- `README.md` — 安装、运行与论文引用说明。

---

## 数据流与运行流程（简要） 🔁
- 从 `environment/frontend_server/storage/` 的基线仿真分支（fork）开始，Reverie 会复制该目录并在 `reverie/meta.json` 标记 fork 来源，生成工作副本。
- 前端每步输出一个环境 JSON（各 persona 的 XY 坐标等），ReverieServer 监听这些文件并对每个 persona 执行认知序列：
	1. `persona.perceive(maze)`：感知附近事件
	2. `persona.retrieve(perceived)`：从联想记忆中检索上下文
	3. `persona.plan(...)`：生成/更新短期或当天计划
	4. `persona.execute(...)`：输出下一步的目标瓦片、表情（emoji）、描述
	5. `persona.reflect()`：生成思考/笔记（可选）
- ReverieServer 将移动信息写入 `movement/<step>.json` 供前端展示，并推进时间与步计数。

## 状态保存位置
- 单个仿真目录：`.../storage/<sim_code>/personas/<Persona Name>/bootstrap_memory/`
	- 包含：`spatial_memory.json`, `scratch.json`，以及联想记忆相关文件（embeddings、nodes、kw_strength 等），这些会在 `Persona` 初始化时加载，并在 `ReverieServer.save()` 时写回。

---

## 给贡献者的提示 / 修改行为的入口 ✍️
- 修改智能体推理或新增行为：优先查看 `reverie/backend_server/persona/cognitive_modules/` 和 `prompt_template/`（修改 prompt 是改变 LLM 输出的最直接方式）。
- 修改世界（地图、对象）：编辑 `environment/frontend_server/static_dirs/assets/the_ville/matrix` 中的 CSV（由 Tiled 导出）。
- 调试：`reverie/backend_server/test.py` 含若干检查；`reverie.py` 的交互式 CLI 便于实时探查。

---

## 小贴士与注意事项 💡
- 后端需要 `utils.py` 中配置 OpenAI Key 与路径（见 `README.md`）。
- `scratch.py` 与 `associative_memory.py` 对数据形状有假设（例如事件元组长度），可通过加入防御性检查提高健壮性。
- 回放与演示基于存储的 JSON；使用 `compress_sim_storage.py` 压缩仿真以便更好的演示效果。

---

## 参考
- 论文："Generative Agents: Interactive Simulacra of Human Behavior"（Park 等，2023）

---

如需，我可以（1）把某一部分展开并加入示例路径，或（2）添加架构图，或（3）把贡献者任务拆成检查清单并写入此文件。✅
