"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: perceive.py
Description: This defines the "Perceive" module for generative agents. 
"""
import sys
sys.path.append('../../')

from operator import itemgetter
from global_methods import *
from persona.prompt_template.gpt_structure import *
from persona.prompt_template.run_gpt_prompt import *

# 生成事件或对话的情感分数
def generate_poig_score(persona, event_type, description): 
  if "is idle" in description: 
    return 1
  # 事件的情感分数
  if event_type == "event": 
    return run_gpt_prompt_event_poignancy(persona, description)[0]
  # 对话的情感分数
  elif event_type == "chat": 
    return run_gpt_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]

# 感知模块：感知角色周围的事件并将其保存到记忆中
def perceive(persona, maze): 
  """
  Perceives events around the persona and saves it to the memory, both events 
  and spaces. 

  We first perceive the events nearby the persona, as determined by its 
  <vision_r>. If there are a lot of events happening within that radius, we 
  take the <att_bandwidth> of the closest events. Finally, we check whether
  any of them are new, as determined by <retention>. If they are new, then we
  save those and return the <ConceptNode> instances for those events. 

  INPUT: 
    persona: An instance of <Persona> that represents the current persona. 
    maze: An instance of <Maze> that represents the current maze in which the 
          persona is acting in. 
  OUTPUT: 
    ret_events: a list of <ConceptNode> that are perceived and new. 
  """
  # PERCEIVE SPACE
  # We get the nearby tiles given our current tile and the persona's vision
  # radius.
  # 感知空间
  # 根据我们当前的瓷砖和角色的视野半径获取附近的瓷砖。 
  nearby_tiles = maze.get_nearby_tiles(persona.scratch.curr_tile, 
                                       persona.scratch.vision_r)

  # We then store the perceived space. Note that the s_mem of the persona is
  # in the form of a tree constructed using dictionaries. 
  # 然后我们存储感知到的空间。请注意，角色的 s_mem 以使用字典构建的树的形式存在。
  for i in nearby_tiles: 
    i = maze.access_tile(i)
    if i["world"]: 
      if (i["world"] not in persona.s_mem.tree): 
        persona.s_mem.tree[i["world"]] = {}
    if i["sector"]: 
      if (i["sector"] not in persona.s_mem.tree[i["world"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]] = {}
    if i["arena"]: 
      if (i["arena"] not in persona.s_mem.tree[i["world"]]
                                              [i["sector"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]][i["arena"]] = []
    if i["game_object"]: 
      if (i["game_object"] not in persona.s_mem.tree[i["world"]]
                                                    [i["sector"]]
                                                    [i["arena"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]][i["arena"]] += [
                                                             i["game_object"]]

  # PERCEIVE EVENTS. 
  # We will perceive events that take place in the same arena as the
  # persona's current arena. 
  # 感知事件 
  # 我们将感知与角色当前arena相同的arena中发生的事件。
  curr_arena_path = maze.get_tile_path(persona.scratch.curr_tile, "arena")
  # We do not perceive the same event twice (this can happen if an object is
  # extended across multiple tiles).
  # 我们不会两次感知同一事件（如果一个对象跨越多个瓷砖，这种情况可能会发生）。
  percept_events_set = set()
  # We will order our percept based on the distance, with the closest ones
  # getting priorities. 
  # 我们将根据距离对我们的感知进行排序，最近的优先考虑。
  percept_events_list = []
  # First, we put all events that are occuring in the nearby tiles into the
  # percept_events_list
  # 首先，我们将附近瓷砖中发生的所有事件放入percept_events_list中
  for tile in nearby_tiles: 
    tile_details = maze.access_tile(tile)
    if tile_details["events"]: 
      if maze.get_tile_path(tile, "arena") == curr_arena_path:  
        # This calculates the distance between the persona's current tile, 
        # and the target tile.
        dist = math.dist([tile[0], tile[1]], 
                         [persona.scratch.curr_tile[0], 
                          persona.scratch.curr_tile[1]])
        # Add any relevant events to our temp set/list with the distant info. 
        for event in tile_details["events"]: 
          if event not in percept_events_set: 
            percept_events_list += [[dist, event]]
            percept_events_set.add(event)

  # We sort, and perceive only persona.scratch.att_bandwidth of the closest
  # events. If the bandwidth is larger, then it means the persona can perceive
  # more elements within a small area. 
  # 我们对其进行排序，并仅感知角色.scratch.att_bandwidth的最近事件。如果带宽更大，则意味着角色可以在一个小区域内感知更多元素。
  percept_events_list = sorted(percept_events_list, key=itemgetter(0))
  perceived_events = []
  for dist, event in percept_events_list[:persona.scratch.att_bandwidth]: 
    perceived_events += [event]

  # Storing events. 
  # <ret_events> is a list of <ConceptNode> instances from the persona's 
  # associative memory. 
  # 存储事件
  # <ret_events>是角色联想记忆中的<ConceptNode>实例列表
  ret_events = []
  for p_event in perceived_events: 
    s, p, o, desc = p_event
    if not p: 
      # If the object is not present, then we default the event to "idle".
      # 如果对象不存在，则将事件默认为“空闲”。
      p = "is"
      o = "idle"
      desc = "idle"
    desc = f"{s.split(':')[-1]} is {desc}"
    p_event = (s, p, o)

    # We retrieve the latest persona.scratch.retention events. If there is  
    # something new that is happening (that is, p_event not in latest_events),
    # then we add that event to the a_mem and return it. 
    # 我们检索最新的角色.scratch.retention事件。如果发生了一些新事件（即p_event不在latest_events中），则我们将该事件添加到a_mem并返回它。
    latest_events = persona.a_mem.get_summarized_latest_events(
                                    persona.scratch.retention)
    if p_event not in latest_events:
      # We start by managing keywords. 
      keywords = set()
      sub = p_event[0]
      obj = p_event[2]
      if ":" in p_event[0]: 
        sub = p_event[0].split(":")[-1]
      if ":" in p_event[2]: 
        obj = p_event[2].split(":")[-1]
      keywords.update([sub, obj])

      # Get event embedding
      desc_embedding_in = desc
      if "(" in desc: 
        desc_embedding_in = (desc_embedding_in.split("(")[1]
                                              .split(")")[0]
                                              .strip())
      if desc_embedding_in in persona.a_mem.embeddings: 
        event_embedding = persona.a_mem.embeddings[desc_embedding_in]
      else: 
        event_embedding = get_embedding(desc_embedding_in)
      event_embedding_pair = (desc_embedding_in, event_embedding)
      
      # Get event poignancy. 
      event_poignancy = generate_poig_score(persona, 
                                            "event", 
                                            desc_embedding_in)

      # If we observe the persona's self chat, we include that in the memory
      # of the persona here.
      # 如果我们观察到角色的自我聊天，我们会将其包含在角色的记忆中。
      chat_node_ids = []
      if p_event[0] == f"{persona.name}" and p_event[1] == "chat with": 
        curr_event = persona.scratch.act_event
        if persona.scratch.act_description in persona.a_mem.embeddings: 
          chat_embedding = persona.a_mem.embeddings[
                             persona.scratch.act_description]
        else: 
          chat_embedding = get_embedding(persona.scratch
                                                .act_description)
        chat_embedding_pair = (persona.scratch.act_description, 
                               chat_embedding)
        chat_poignancy = generate_poig_score(persona, "chat", 
                                             persona.scratch.act_description)
        chat_node = persona.a_mem.add_chat(persona.scratch.curr_time, None,
                      curr_event[0], curr_event[1], curr_event[2], 
                      persona.scratch.act_description, keywords, 
                      chat_poignancy, chat_embedding_pair, 
                      persona.scratch.chat)
        chat_node_ids = [chat_node.node_id]

      # Finally, we add the current event to the agent's memory. 
      ret_events += [persona.a_mem.add_event(persona.scratch.curr_time, None,
                           s, p, o, desc, keywords, event_poignancy, 
                           event_embedding_pair, chat_node_ids)]
      persona.scratch.importance_trigger_curr -= event_poignancy
      persona.scratch.importance_ele_n += 1

  return ret_events




  











