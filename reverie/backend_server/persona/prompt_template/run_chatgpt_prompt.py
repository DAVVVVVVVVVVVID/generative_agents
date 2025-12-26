"""
Author: Joon Sung Park (joonspk@stanford.edu)
Modified: ChatGPT API version

File: run_chatgpt_prompt.py
Description: ChatGPT API versions of GPT prompt functions. These functions use
the ChatCompletion API instead of the deprecated Completion API.
"""
import re
import datetime
import sys
import ast

sys.path.append('../../')

from global_methods import *
from persona.prompt_template.gpt_structure import *
from persona.prompt_template.print_prompt import *

def get_random_alphanumeric(i=6, j=6):
  """
  Returns a random alpha numeric strength that has the length of somewhere
  between i and j.

  INPUT:
    i: min_range for the length
    j: max_range for the length
  OUTPUT:
    an alpha numeric str with the length of somewhere between i and j.
  """
  k = random.randint(i, j)
  x = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
  return x


##############################################################################
# CHAPTER 1: Run ChatGPT Prompt (ChatGPT API versions)
##############################################################################

def run_chatgpt_prompt_wake_up_hour(persona, test_input=None, verbose=False):
  """
  Given the persona, returns an integer that indicates the hour when the
  persona wakes up.

  This version uses ChatGPT API (gpt-3.5-turbo) instead of the deprecated
  Completion API.

  INPUT:
    persona: The Persona class instance
  OUTPUT:
    integer for the wake up hour.
  """
  def create_prompt_input(persona, test_input=None):
    if test_input: return test_input
    prompt_input = [persona.scratch.get_str_iss(),
                    persona.scratch.get_str_lifestyle(),
                    persona.scratch.get_str_firstname()]
    return prompt_input

  def __chat_func_clean_up(gpt_response, prompt=""):
    """
    Clean up ChatGPT response to extract wake up hour.
    Expected format: a number followed by 'am', e.g., "8am" or "8 am"
    """
    cr = int(gpt_response.strip().lower().split("am")[0].strip())
    return cr

  def __chat_func_validate(gpt_response, prompt=""):
    """
    Validate that the response can be cleaned up properly.
    """
    try:
      __chat_func_clean_up(gpt_response, prompt="")
      return True
    except:
      return False

  def get_fail_safe():
    """
    Fail-safe response if ChatGPT fails to generate valid output.
    Default wake up time is 8am.
    """
    fs = 8
    return fs

  # ChatGPT parameters (not needed but kept for consistency)
  gpt_param = {"engine": "gpt-3.5-turbo", "max_tokens": 10,
             "temperature": 0.8, "top_p": 1, "stream": False,
             "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

  # Use the same prompt template as the original
  prompt_template = "persona/prompt_template/v2/wake_up_hour_v1.txt"
  prompt_input = create_prompt_input(persona, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)

  # Example output for ChatGPT to follow
  example_output = "8am"

  # Special instruction to guide ChatGPT
  special_instruction = "The output should ONLY be the hour followed by 'am' (e.g., '7am', '8am'). Do not include any other text."

  fail_safe = get_fail_safe()

  # Use ChatGPT safe generate response instead of the old API
  output = ChatGPT_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response=fail_safe,
    func_validate=__chat_func_validate,
    func_clean_up=__chat_func_clean_up,
    verbose=verbose
  )

  if verbose:
    print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]


def run_chatgpt_prompt_daily_plan(persona, wake_up_hour, test_input=None, verbose=False):
  """
  ChatGPT version: Long term planning that spans a day.

  Returns a list of actions that the persona will take today.
  Usually in the form: 'wake up and complete the morning routine at 6:00 am'

  INPUT:
    persona: The Persona class instance
    wake_up_hour: Integer wake up hour
  OUTPUT:
    a list of daily actions in broad strokes.
  """
  def create_prompt_input(persona, wake_up_hour, test_input=None):
    if test_input: return test_input
    prompt_input = []
    prompt_input += [persona.scratch.get_str_iss()]
    prompt_input += [persona.scratch.get_str_lifestyle()]
    prompt_input += [persona.scratch.get_str_curr_date_str()]
    prompt_input += [persona.scratch.get_str_firstname()]
    prompt_input += [f"{str(wake_up_hour)}:00 am"]
    return prompt_input

  def __chat_func_clean_up(gpt_response, prompt=""):
    cr = []
    _cr = gpt_response.split(")")
    for i in _cr:
      if len(i) > 0 and i[-1].isdigit():
        i = i[:-1].strip()
        if len(i) > 0 and (i[-1] == "." or i[-1] == ","):
          cr += [i[:-1].strip()]
    return cr

  def __chat_func_validate(gpt_response, prompt=""):
    try:
      __chat_func_clean_up(gpt_response, prompt="")
      return True
    except:
      return False

  def get_fail_safe():
    fs = ['wake up and complete the morning routine at 6:00 am',
          'eat breakfast at 7:00 am',
          'read a book from 8:00 am to 12:00 pm',
          'have lunch at 12:00 pm',
          'take a nap from 1:00 pm to 4:00 pm',
          'relax and watch TV from 7:00 pm to 8:00 pm',
          'go to bed at 11:00 pm']
    return fs

  gpt_param = {"engine": "gpt-3.5-turbo", "max_tokens": 500,
               "temperature": 1, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

  prompt_template = "persona/prompt_template/v2/daily_planning_v6.txt"
  prompt_input = create_prompt_input(persona, wake_up_hour, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)

  example_output = '1) wake up and complete the morning routine at 8:00 am, 2) have breakfast at 8:30 am, 3) work on the project from 9:00 am to 12:00 pm, 4) have lunch at 12:00 pm'

  special_instruction = 'The output should be a list of daily activities in the format: "1) activity, 2) activity, 3) activity...". Each activity should include a time or time range.'

  fail_safe = get_fail_safe()

  output = ChatGPT_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response=fail_safe,
    func_validate=__chat_func_validate,
    func_clean_up=__chat_func_clean_up,
    verbose=verbose
  )

  # Add wake up as first activity
  output = ([f"wake up and complete the morning routine at {wake_up_hour}:00 am"] + output)

  if verbose:
    print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]


def run_chatgpt_prompt_generate_hourly_schedule(persona, curr_hour_str, p_f_ds_hourly_org,
                                                hour_str, intermission2=None,
                                                test_input=None, verbose=False):
  """
  ChatGPT version: Generate hourly schedule based on daily plan.

  This is the KEY function that was causing "TOKEN LIMIT EXCEEDED" errors.

  INPUT:
    persona: Persona instance
    curr_hour_str: Current hour string
    p_f_ds_hourly_org: Prior hourly schedule
    hour_str: List of hour strings
    intermission2: Optional additional context
  OUTPUT:
    Activity description for the current hour
  """
  def create_prompt_input(persona, curr_hour_str, p_f_ds_hourly_org, hour_str,
                          intermission2=None, test_input=None):
    if test_input: return test_input
    schedule_format = ""
    for i in hour_str:
      schedule_format += f"[{persona.scratch.get_str_curr_date_str()} -- {i}]"
      schedule_format += f" Activity: [Fill in]\n"
    schedule_format = schedule_format[:-1]

    intermission_str = f"Here the originally intended hourly breakdown of"
    intermission_str += f" {persona.scratch.get_str_firstname()}'s schedule today: "
    for count, i in enumerate(persona.scratch.daily_req):
      intermission_str += f"{str(count+1)}) {i}, "
    intermission_str = intermission_str[:-2]

    prior_schedule = ""
    if p_f_ds_hourly_org:
      prior_schedule = "\n"
      for count, i in enumerate(p_f_ds_hourly_org):
        prior_schedule += f"[(ID:{get_random_alphanumeric()})"
        prior_schedule += f" {persona.scratch.get_str_curr_date_str()} --"
        prior_schedule += f" {hour_str[count]}] Activity:"
        prior_schedule += f" {persona.scratch.get_str_firstname()}"
        prior_schedule += f" is {i}\n"

    prompt_ending = f"[(ID:{get_random_alphanumeric()})"
    prompt_ending += f" {persona.scratch.get_str_curr_date_str()}"
    prompt_ending += f" -- {curr_hour_str}] Activity:"
    prompt_ending += f" {persona.scratch.get_str_firstname()} is"

    if intermission2:
      intermission2 = f"\n{intermission2}"

    prompt_input = []
    prompt_input += [schedule_format]
    prompt_input += [persona.scratch.get_str_iss()]
    prompt_input += [prior_schedule + "\n"]
    prompt_input += [intermission_str]
    if intermission2:
      prompt_input += [intermission2]
    else:
      prompt_input += [""]
    prompt_input += [prompt_ending]

    return prompt_input

  def __chat_func_clean_up(gpt_response, prompt=""):
    cr = gpt_response.strip()
    if len(cr) > 0 and cr[-1] == ".":
      cr = cr[:-1]
    return cr

  def __chat_func_validate(gpt_response, prompt=""):
    try:
      __chat_func_clean_up(gpt_response, prompt="")
      return True
    except:
      return False

  def get_fail_safe():
    fs = "asleep"
    return fs

  gpt_param = {"engine": "gpt-3.5-turbo", "max_tokens": 50,
               "temperature": 0.5, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

  # Use ChatGPT template
  prompt_template = "persona/prompt_template/v3_ChatGPT/generate_hourly_schedule_v2.txt"
  prompt_input = create_prompt_input(persona, curr_hour_str, p_f_ds_hourly_org,
                                     hour_str, intermission2, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)

  example_output = "studying for her music classes"

  special_instruction = "The output should ONLY include the part of the sentence that completes the last line in the schedule above."

  fail_safe = get_fail_safe()

  output = ChatGPT_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response=fail_safe,
    func_validate=__chat_func_validate,
    func_clean_up=__chat_func_clean_up,
    verbose=verbose
  )

  if verbose:
    print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]


def run_chatgpt_prompt_action_sector(action_description, persona, maze,
                                     test_input=None, verbose=False):
  """
  ChatGPT version: Determine which sector the persona should go to for an action.

  INPUT:
    action_description: Description of the action
    persona: Persona instance
    maze: Maze/world instance
  OUTPUT:
    Sector name where the action should take place
  """
  def create_prompt_input(action_description, persona, maze, test_input=None):
    act_world = f"{maze.access_tile(persona.scratch.curr_tile)['world']}"

    prompt_input = []
    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [persona.scratch.living_area.split(":")[1]]
    x = f"{act_world}:{persona.scratch.living_area.split(':')[1]}"
    prompt_input += [persona.s_mem.get_str_accessible_sector_arenas(x)]

    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [f"{maze.access_tile(persona.scratch.curr_tile)['sector']}"]
    x = f"{act_world}:{maze.access_tile(persona.scratch.curr_tile)['sector']}"
    prompt_input += [persona.s_mem.get_str_accessible_sector_arenas(x)]

    if persona.scratch.get_str_daily_plan_req() != "":
      prompt_input += [f"\n{persona.scratch.get_str_daily_plan_req()}"]
    else:
      prompt_input += [""]

    # Filter accessible sectors
    accessible_sector_str = persona.s_mem.get_str_accessible_sectors(act_world)
    curr = accessible_sector_str.split(", ")
    fin_accessible_sectors = []
    for i in curr:
      if "'s house" in i:
        if persona.scratch.last_name in i:
          fin_accessible_sectors += [i]
      else:
        fin_accessible_sectors += [i]
    accessible_sector_str = ", ".join(fin_accessible_sectors)

    prompt_input += [accessible_sector_str]

    action_description_1 = action_description
    action_description_2 = action_description
    if "(" in action_description:
      action_description_1 = action_description.split("(")[0].strip()
      action_description_2 = action_description.split("(")[-1][:-1]
    prompt_input += [persona.scratch.get_str_name()]
    prompt_input += [action_description_1]
    prompt_input += [action_description_2]
    prompt_input += [persona.scratch.get_str_name()]

    return prompt_input

  def __chat_func_clean_up(gpt_response, prompt=""):
    cr = gpt_response.strip()
    return cr

  def __chat_func_validate(gpt_response, prompt=""):
    try:
      gpt_response = __chat_func_clean_up(gpt_response, prompt="")
      return True
    except:
      return False

  def get_fail_safe():
    fs = "kitchen"
    return fs

  gpt_param = {"engine": "gpt-3.5-turbo", "max_tokens": 15,
               "temperature": 0, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

  prompt_template = "persona/prompt_template/v3_ChatGPT/action_location_sector_v2.txt"
  prompt_input = create_prompt_input(action_description, persona, maze, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)

  example_output = "Johnson Park"

  special_instruction = "The value for the output must contain one of the area options above verbatim (including lower/upper case)."

  fail_safe = get_fail_safe()

  output = ChatGPT_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response=fail_safe,
    func_validate=__chat_func_validate,
    func_clean_up=__chat_func_clean_up,
    verbose=verbose
  )

  # Validate output is in accessible sectors
  y = f"{maze.access_tile(persona.scratch.curr_tile)['world']}"
  x = [i.strip() for i in persona.s_mem.get_str_accessible_sectors(y).split(",")]
  if output not in x:
    output = persona.scratch.living_area.split(":")[1]

  if verbose:
    print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]
