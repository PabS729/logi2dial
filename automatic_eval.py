from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
import argparse
import pandas as pd
import time
from persona_roleplay.respond_role import *
import pandas
from prompt_eval import *

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='results/roleplay_test_1007_MISTRAL_')
    parser.add_argument("--components_to_read", type=str, default='chat_history_results/roleplay_test_1007_MISTRAL_')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/storytelling_test_1008_MISTRAL_')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.file_to_annotate + str(args.num_gen) + ".xlsx"
    history1 = "chat_history_" + args.file_to_annotate + ".xlsx"
    history2 = args.components_to_read + ".xlsx"
    df_to_argue = pd.read_excel(ann)
    


    dialogues_1 = pd.read_excel(history1)
    dialogues_2 = pd.read_excel(history2)
    sentences = dialogues_1["sentences"].values.tolist()
    dl1 = dialogues_1["chats"].values.tolist()
    dl2 = dialogues_2["chats"].values.tolist()
    # print(df_to_argue.loc[0])

    length_of_conversation = 5

    # model_student = "gpt-4o"
    model_agent = "gpt-4o"

    cohs = []
    rels = []
    info = []
    arg = []
    help = []

    r_cohs = []
    r_rels = []
    r_info = []
    r_arg = []
    r_help = []

    for j in range(len(sentences)):
        # print(sentences[j])
        # sentence = sentences[j].split(",")[4]
        sentence = sentences[j]
        dialogue1 = dl1[j]
        dialogue2 = dl2[j]

        print(sentence)
        eval_res_COH = await generate_res("eval_t", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_COHERENCE, 0)
        eval_coh = json.loads(eval_res_COH.choices[0].message.content)
        eval_res_RELE = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_CONSISTENCY, 0)
        eval_rele = json.loads(eval_res_RELE.choices[0].message.content)
        eval_res_INFO = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_INFORMATION_DIV, 0)
        eval_info = json.loads(eval_res_INFO.choices[0].message.content)
        eval_res_ARG = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_VALID_ARGUMENTS, 0)
        eval_arg = json.loads(eval_res_ARG.choices[0].message.content)
        eval_res_HELP = await generate_res("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_HELPFULNESS, 0)
        eval_help = json.loads(eval_res_HELP.choices[0].message.content)

        cohs.append(eval_coh["ans"])
        rels.append(eval_rele['ans'])
        info.append(eval_info['ans'])
        arg.append(eval_arg['ans'])
        help.append(eval_help['ans'])

        r_cohs.append(eval_coh["reason"])
        r_rels.append(eval_rele["reason"])
        r_info.append(eval_info["reason"])
        r_arg.append(eval_arg["reason"])
        r_help.append(eval_help["reason"])




    data_dict = {
        "sentences": sentences,
        "coherence": cohs,
        "reason for coherence": r_cohs,
        "relevance": rels,
        "reason for relevance": r_rels,
        "informativeness": info,
        "reason for informativeness": r_info,
        "argumentativeness": arg,
        "reason for argumentativeness": r_arg,
        "helpfulness":help,
        "reason for helpfulness": r_help,



    }
    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

        

if __name__ == '__main__':
    asyncio.run(main())
