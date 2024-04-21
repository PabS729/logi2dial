from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAIChat
from langchain.callbacks import get_openai_callback

from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_init import *
from dotenv import load_dotenv
from pathlib import Path
import spacy
import argparse
import pandas as pd
from tqdm import tqdm
from numpy import random

env_path = '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

nlp = spacy.load("en_core_web_sm")

async def generate_response(sentence, chat_history, prompt_sys, prompt_gen, temperature=0):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=temperature, openai_api_key=OPENAI_KEY)
    # llm = OpenAIChat(temperature=temperature, openai_api_key=API_KEY)
    
    await asyncio.sleep(0.1)
    sys_prompt = prompt_sys
        
    p = prompt_gen
    if chat_history != None:
        user_prompt = p.format(sentence=sentence, history=chat_history)
    else:
        user_prompt = p.format(sentence=sentence)
    message = [
                SystemMessage(content=sys_prompt),
                HumanMessage(content=user_prompt)
                ]
    
    result = await llm.agenerate(message)
    # print(results)
    return result


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='CO2022.tsv')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='CO2022_pt1.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate, sep='\t')

    length_of_conversation = 10
    # st = df_to_annotate["Text"].tolist()
    sentences = df_to_argue["sentences"].values.tolist()

    
    if args.sample > 0:
        sentences = random.sample(sentences, args.sample)

    QS = [[], []]
    chat_history = ""
    conversation_teacher = []
    conversation_layman = []

    for i in range(length_of_conversation):

        
        sys_prompt_teacher = SYSTEM_PROMPT_TEACHER
        sys_prompt_layman = SYSTEM_PROMPT_LAYMAN
        prompt_layman = PROMPT_LAYMAN_CONTINUED


        if i == 0:
            prompt_teacher = PROMPT_IDENTIFY_COMPONENTS_START
            results_conversation_teacher = await generate_response(sentences[0], None, sys_prompt_teacher, prompt_teacher, 0)
            teacher_response = results_conversation_teacher.generations[0][0].text
            conversation_teacher.append(teacher_response)
            chat_history += "teacher: " + teacher_response
            chat_history += "\n"
        else:
            prompt_teacher = PROMPT_IDENTIFY_COMPONENTS_CONTINUED
            results_conversation_layman = await generate_response(sentences[0], chat_history, sys_prompt_layman, prompt_layman, 0)
            layman_response = results_conversation_layman.generations[0][0].text
            conversation_layman.append(layman_response)
            chat_history += "layman: " + layman_response
            chat_history += "\n"
            results_conversation_teacher = await generate_response(sentences[0], chat_history, sys_prompt_teacher, prompt_teacher, 0)
            teacher_response = results_conversation_teacher.generations[0][0].text
            conversation_teacher.append(teacher_response)
            chat_history += "teacher: " + teacher_response
            chat_history += "\n"

    conversation_layman.append('.')

    data_dict = {'teacher_response': conversation_teacher, 'layman_response': conversation_layman}
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")
    


if __name__ == '__main__':
    with get_openai_callback() as cb:
        asyncio.run(main())
        print(cb)
