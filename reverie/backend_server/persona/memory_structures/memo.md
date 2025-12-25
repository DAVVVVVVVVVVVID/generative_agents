# 联想记忆数据结构的直观示例

基于 `associative_memory.py` 的代码，以下是一个简化的示例，展示一个“成型”的 `AssociativeMemory` 实例的样子。我假设系统已添加了几个节点（1 个 event、1 个 thought 和 1 个 chat），并从 JSON 文件加载了相关数据。这个示例是虚构的，但基于代码逻辑构建，用于直观理解。

#### 示例假设
- **节点数据**：系统有 3 个节点（node_1: event, node_2: thought, node_3: chat）。
- **关键词**：节点共享关键词如 "coffee"、"morning"。
- **嵌入**：每个节点有对应的向量嵌入（这里简化为短列表）。
- **强度**：关键词 "coffee" 在 event 中出现 2 次，在 thought 中出现 1 次。

#### 1. **ConceptNode 实例的表格展示**
每个 `ConceptNode` 对象的属性如下（用表格列出 3 个示例节点）：

| 属性          | node_1 (event)                          | node_2 (thought)                        | node_3 (chat)                           |
|---------------|------------------------------------------|------------------------------------------|------------------------------------------|
| **node_id**   | "node_1"                                | "node_2"                                | "node_3"                                |
| **node_count**| 1                                       | 2                                       | 3                                       |
| **type_count**| 1                                       | 1                                       | 1                                       |
| **node_type** | "event"                                 | "thought"                               | "chat"                                  |
| **depth**     | 0                                       | 1                                       | 0                                       |
| **created**   | 2025-12-17 08:00:00                     | 2025-12-17 08:05:00                     | 2025-12-17 08:10:00                     |
| **expiration**| None                                    | None                                    | None                                    |
| **s**         | "Isabella"                              | "Isabella"                              | "Isabella"                              |
| **p**         | "drinks"                                | "thinks"                                | "says"                                  |
| **o**         | "coffee"                                | "about morning routine"                 | "Good morning, Klaus"                   |
| **description**| "Isabella drinks coffee in the morning" | "Isabella reflects on her morning"      | "Isabella greets Klaus"                 |
| **embedding_key**| "emb_1"                                | "emb_2"                                | "emb_3"                                |
| **poignancy**| 7.5                                     | 6.0                                     | 5.0                                     |
| **keywords**  | ["coffee", "morning"]                   | ["morning", "routine"]                  | ["greeting", "klaus"]                   |
| **filling**   | None                                    | ["node_1"]                              | [["Isabella: Hi", "Klaus: Hello"]]      |

- **解释**：
  - `s`、`p`、`o` 形成语义三元组（e.g., "Isabella drinks coffee"）。
  - `depth` 为 0 表示根节点，thought 的 `filling` 可能引用其他节点 ID。
  - `keywords` 用于索引，`poignancy` 衡量重要性。

#### 2. **AssociativeMemory 整体结构的字典/列表展示**
以下是 `AssociativeMemory` 实例的结构（用嵌套格式描述，类似 JSON）：

```json
{
  "id_to_node": {
    "node_1": <ConceptNode object for event>,
    "node_2": <ConceptNode object for thought>,
    "node_3": <ConceptNode object for chat>
  },
  "seq_event": [<node_1>],  // 列表：最新 event 在前
  "seq_thought": [<node_2>],
  "seq_chat": [<node_3>],
  "kw_to_event": {
    "coffee": [<node_1>],
    "morning": [<node_1>]
  },
  "kw_to_thought": {
    "morning": [<node_2>],
    "routine": [<node_2>]
  },
  "kw_to_chat": {
    "greeting": [<node_3>],
    "klaus": [<node_3>]
  },
  "kw_strength_event": {
    "coffee": 2,
    "morning": 1
  },
  "kw_strength_thought": {
    "morning": 1,
    "routine": 1
  },
  "embeddings": {
    "emb_1": [0.1, 0.2, 0.3, ...],  // 向量嵌入（假设 768 维）
    "emb_2": [0.4, 0.5, 0.6, ...],
    "emb_3": [0.7, 0.8, 0.9, ...]
  }
}
```

- **解释**：
  - `id_to_node` 是核心字典，用于快速查找节点。
  - `seq_*` 列表按类型存储节点序列，支持历史遍历。
  - `kw_to_*` 字典通过关键词索引节点列表，支持联想检索（e.g., 搜索 "coffee" 返回 event 节点）。
  - `kw_strength_*` 记录关键词频率，用于排序（e.g., "coffee" 强度高，表示重要）。
  - `embeddings` 存储向量，用于潜在的语义相似性计算（代码中加载但未直接使用检索）。

这个结构支持高效添加（e.g., `add_event`）、检索（e.g., `retrieve_relevant_events`）和保存（序列化为 JSON）。如果添加更多节点，列表和字典会扩展。如果需要代码生成这个示例或修改，请告诉我！

# Scratch 数据结构的直观示例

基于 `scratch.py` 的代码，以下是一个简化的示例，展示一个“成型”的 `Scratch` 实例的样子。我假设系统已从 JSON 文件加载了一个 persona 的状态，包括日常计划、当前行动等。这个示例是虚构的，但基于代码逻辑构建，用于直观理解。

#### 示例假设
- **Persona 数据**：一个名为 "Isabella Rodriguez" 的 persona，年龄 28，正在执行日常行动。
- **时间**：当前时间为 2025-12-17 08:30:00。
- **行动**：当前正在 "drinking coffee"，持续 10 分钟，从 08:25 开始。
- **计划**：f_daily_schedule 有分解的行动序列。

#### 1. **Scratch 实例的属性表格展示**
`Scratch` 类的属性如下（用表格列出主要属性、类型、描述和示例值）：

| 属性                      | 类型          | 描述                                                                 | 示例值                                      |
|---------------------------|---------------|----------------------------------------------------------------------|---------------------------------------------|
| **vision_r**             | int          | 可视范围（视野半径，单位：格子）                                     | 4                                          |
| **att_bandwidth**        | int          | 注意力带宽（待完成）                                                | 3                                          |
| **retention**            | int          | 保留时间（待完成）                                                  | 5                                          |
| **curr_time**            | datetime     | 当前感知时间                                                        | 2025-12-17 08:30:00                        |
| **curr_tile**            | list/tuple   | 当前坐标（x, y）                                                    | [50, 10]                                   |
| **daily_plan_req**       | str          | 每日计划要求                                                        | "Stay home and paint"                       |
| **name**                 | str          | 全名                                                                | "Isabella Rodriguez"                        |
| **first_name**           | str          | 名                                                                  | "Isabella"                                  |
| **last_name**            | str          | 姓                                                                  | "Rodriguez"                                 |
| **age**                  | int          | 年龄                                                                | 28                                         |
| **innate**               | str          | 先天特征（L0）                                                      | "creative, independent"                     |
| **learned**              | str          | 习得特征（L1）                                                      | "Painter who enjoys quiet life"             |
| **currently**            | str          | 当前状态（L2）                                                      | "Preparing for solo art show"               |
| **lifestyle**            | str          | 生活方式                                                            | "Sleeps 7 hours, eats dinner at 6pm"        |
| **living_area**          | str          | 居住区域                                                            | "Hobbs Cafe"                                |
| **daily_req**            | list         | 每日目标列表                                                        | ["Paint", "Eat lunch"]                      |
| **f_daily_schedule**     | list         | 分解的每日计划（[任务, 持续分钟]）                                  | [["wake up", 5], ["drink coffee", 10]]     |
| **f_daily_schedule_hourly_org** | list    | 原始小时计划（未分解）                                              | [["morning routine", 60], ["painting", 120]]|
| **act_address**          | str          | 当前行动地址                                                        | "Hobbs Cafe:cafe:kitchen:coffee machine"    |
| **act_start_time**       | datetime     | 行动开始时间                                                        | 2025-12-17 08:25:00                        |
| **act_duration**         | int          | 行动持续分钟                                                        | 10                                         |
| **act_description**      | str          | 行动描述                                                            | "drinking coffee"                           |
| **act_pronunciatio**     | str          | 行动发音（表情符号）                                                | "☕"                                        |
| **act_event**            | tuple        | 行动事件三元组（s, p, o）                                           | ("Isabella", "drinks", "coffee")            |
| **chatting_with**        | str/None     | 正在聊天对象                                                        | None                                       |
| **chat**                 | list/None    | 聊天记录                                                            | None                                       |
| **act_path_set**         | bool         | 路径是否已设置                                                      | False                                      |
| **planned_path**         | list         | 规划路径（坐标列表）                                                | []                                         |

- **解释**：
  - 属性分为超参数（vision_r 等）、世界信息（curr_time 等）、身份信息（name 等）、计划（daily_req 等）和行动（act_* 等）。
  - 时间相关属性使用 datetime 对象，支持分钟级计算。
  - 列表如 f_daily_schedule 用于动态计划分解。

#### 2. **Scratch 整体结构的字典/列表展示**
以下是 `Scratch` 实例的结构（用嵌套格式描述，类似 JSON，基于 save 方法的序列化逻辑）：

```json
{
  "vision_r": 4,
  "att_bandwidth": 3,
  "retention": 5,
  "curr_time": "December 17, 2025, 08:30:00",
  "curr_tile": [50, 10],
  "daily_plan_req": "Stay home and paint",
  "name": "Isabella Rodriguez",
  "first_name": "Isabella",
  "last_name": "Rodriguez",
  "age": 28,
  "innate": "creative, independent",
  "learned": "Painter who enjoys quiet life",
  "currently": "Preparing for solo art show",
  "lifestyle": "Sleeps 7 hours, eats dinner at 6pm",
  "living_area": "Hobbs Cafe",
  "daily_req": ["Paint", "Eat lunch"],
  "f_daily_schedule": [["wake up", 5], ["drink coffee", 10]],
  "f_daily_schedule_hourly_org": [["morning routine", 60], ["painting", 120]],
  "act_address": "Hobbs Cafe:cafe:kitchen:coffee machine",
  "act_start_time": "December 17, 2025, 08:25:00",
  "act_duration": 10,
  "act_description": "drinking coffee",
  "act_pronunciatio": "☕",
  "act_event": ["Isabella", "drinks", "coffee"],
  "chatting_with": null,
  "chat": null,
  "act_path_set": false,
  "planned_path": []
}
```

- **解释**：
  - 结构基于 save 方法的 JSON 输出，支持加载和保存状态。
  - 列表如 daily_req 和 f_daily_schedule 支持动态更新。
  - 时间字段序列化为字符串（"%B %d, %Y, %H:%M:%S" 格式）。
  - 这个结构用于短期记忆管理，支持行动检查（e.g., `act_check_finished`）和计划索引（e.g., `get_f_daily_schedule_index`）。

这个结构支持 persona 的状态管理、行动执行和保存。如果需要代码生成这个示例或修改，请告诉我！

### Spatial Memory 数据结构的直观示例

基于 `spatial_memory.py` 的代码，以下是一个简化的示例，展示一个“成型”的 `MemoryTree` 实例的样子。我假设系统已从 JSON 文件加载了一个 persona 的空间记忆树，包括世界、区域、场所和游戏对象。这个示例是虚构的，但基于代码逻辑构建，用于直观理解。

#### 示例假设
- **树结构**：系统有 1 个世界（the_ville），包含 2 个区域（double studio 和 cafe），每个区域有多个场所，每个场所有游戏对象列表。
- **层次**：world → sector → arena → [game objects]。
- **用途**：用于查询可访问的区域、场所和对象，支持 persona 的空间导航。

#### 1. **MemoryTree 实例的树结构展示**
`MemoryTree` 的核心是 `self.tree`，一个嵌套字典。以下用表格描述层次结构（示例世界 "the_ville"）：

| 层次          | 示例键/值                                                                 |
|---------------|---------------------------------------------------------------------------|
| **world**     | "the_ville"                                                              |
| **sector**    | "double studio" (under "the_ville")                                      |
| **arena**     | "bedroom" (under "double studio") → ["bed", "nightstand", "lamp"]       |
|               | "kitchen" (under "double studio") → ["fridge", "stove", "table"]        |
| **sector**    | "cafe" (under "the_ville")                                               |
| **arena**     | "main area" (under "cafe") → ["counter", "chair", "menu"]                |
|               | "back room" (under "cafe") → ["storage", "sink"]                         |

- **解释**：
  - 树结构支持递归遍历（e.g., `print_tree` 方法）。
  - 每个 arena 是游戏对象列表，用于查询可访问物品。
  - 查询方法如 `get_str_accessible_sectors` 返回 world 下的 sectors 键列表。

#### 2. **MemoryTree 整体结构的字典/列表展示**
以下是 `MemoryTree` 实例的结构（用嵌套格式描述，类似 JSON，基于加载的树数据）：

```json
{
  "tree": {
    "the_ville": {
      "double studio": {
        "bedroom": ["bed", "nightstand", "lamp"],
        "kitchen": ["fridge", "stove", "table"],
        "bathroom": ["toilet", "sink"]
      },
      "cafe": {
        "main area": ["counter", "chair", "menu"],
        "back room": ["storage", "sink"]
      }
    }
  }
}
```

- **解释**：
  - `tree` 是唯一的属性，存储整个空间层次。
  - 支持保存为 JSON（`save` 方法）和加载（`__init__`）。
  - 查询方法基于树遍历，如 `get_str_accessible_sector_arenas("the_ville:double studio")` 返回 "bedroom, kitchen, bathroom"。
  - 这个结构用于空间记忆，支持 persona 在世界中的定位和导航。

这个结构支持空间数据的管理和查询。如果需要代码生成这个示例或修改，请告诉我！
