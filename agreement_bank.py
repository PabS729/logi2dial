from openai import OpenAI
from def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_init import *
import argparse
import pandas as pd
import time

async def generate_response(role, model_name, sentence, 
                            teacher_res, student_res, prompt_gen, temperature=0, components=None):
    client = OpenAI()
    # llm = OpenAIChat(temperature=temperature, openai_api_key=API_KEY)

    p = prompt_gen
    msgs = []
        
    if components != None:
        user_prompt = p.format(sentence=sentence, claim=components['claim'], 
                               ground=components['ground'], warrant=components['warrant'],
                               backing=components['backing'], qualifier=components['qualifier'], 
                               rebuttal=components['rebuttal'])
    else:
        user_prompt = p.format(sentence=sentence)
    
    msgs.append({"role": "system", "content": user_prompt})

    #teacher and student take turns
    if role == "teacher": 
        for (t,s) in zip(teacher_res, student_res):
            msgs.append({"role": "assistant", "content": t})
            msgs.append({"role": "user", "content": s})
    else:
        for (t,s) in zip(teacher_res[:-2], student_res):
            msgs.append({"role": "user", "content": t})
            msgs.append({"role": "assistant", "content": s})
        msgs.append({"role": "user", "content": teacher_res[-1]})
    done = False
    while not done:
        try: 
            response = client.chat.completions.create(
            model=model_name,
        messages=msgs,
        temperature=temperature
        )
            print("done")
            done = True
        except:
            print("error caught, waiting...")
            time.sleep(60)
    return response

