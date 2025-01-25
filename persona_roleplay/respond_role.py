from openai import OpenAI
import asyncio
import time
from mistralai.client import MistralClient
import os

async def generate_res(role, model_name, sentence, history, profile, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
    # if role == "t_edu":
    #     client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
    #     # print("c")
    # else:
    #     client = OpenAI()
    client = OpenAI()

    p = prompt_gen
    msgs = []
    if role == "agent" : 
        user_prompt = p.format(sentence=sentence, history=history)
    elif role in ["fact_bank", "gen_strategy", "student", "conv"]:
        user_prompt = p.format(sentence=sentence)
        # user_prompt = p.format(sentence=sentence, NAME = profile["NAME"], AGE = profile["AGE"], BELIEF = profile["BELIEF"], BIAS = profile["BIAS"], PERSONALITY = profile["PERSONALITY"], EDU_LEVEL = profile["EDU_LEVEL"])
    elif role == "teacher" or role == "thought":
        user_prompt = p.format(sentence=sentence, history=history)
    elif role in ["strategy", "teacher_st", "eval_s", "t_edu", "test", "evl"]:
        user_prompt = p.format(sentence=sentence, history=history, profile=profile)
    elif role in ["exp", "check", "tea_strat"]:
        user_prompt = p.format(sentence=sentence, history=history, profile=profile, target_statement=target_statement)
    else:
        user_prompt = p.format(sentence=sentence, history=history)
    

    msgs.append({"role": "system", "content": user_prompt})


    #teacher and student take turns
    if role in ["teacher_st", "teacher", "t_edu", "exp", "test", "old"]: 
        for (t,s) in zip(teacher_res, student_res):
            msgs.append({"role": "assistant", "content": t})
            msgs.append({"role": "user", "content": s})
    if role in ["student", "student_bio", "stu"]:
        # msgs.append({"role": "system", "content": user_prompt})
        if zip(teacher_res[:-2], student_res) != None: 
            for (t,s) in zip(teacher_res[:-2], student_res):
                msgs.append({"role": "user", "content": t})
                msgs.append({"role": "assistant", "content": s})
        msgs.append({"role": "user", "content": teacher_res[-1]})
    done = False
    while not done:
        try: 
            if role in ["old","check","", "fact_bank", "find_contradiction", "strategy", "thought", "gen_strategy", "agent", "eval_t", "test", "stu", 'eval_s']:
                response = client.chat.completions.create(
                model=model_name,
            messages=msgs,
            temperature=temperature,
            response_format={ "type": "json_object" }
            )
            # elif role == "t_edu":
            #     response = client.chat(
            #     model="mistral-large-latest",
            # messages=msgs,
            # temperature=temperature,
            # )
            else:
                response = client.chat.completions.create(
                model=model_name,
                messages=msgs,
                temperature=temperature,
                )
            # print("done")
            done = True
        except Exception as e:
            print("error caught, waiting...", e)
            time.sleep(60)
    return response
    