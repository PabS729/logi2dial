

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
import anthropic
async def eval_claude(role, model_name, sentence, history, profile, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
   
    user_prompt = prompt_gen.format(sentence=sentence, history=history, profile=profile)

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="",
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    return message

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue1", type=str, default='results/fsm_0126_89_test_r10_')
    parser.add_argument("--dialogue2", type=str, default='results/fsm_0126_28_test_r10_base_sp')
    parser.add_argument("--dataset", type=str, default='pos_train_set.csv')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/s_CL_mod')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.dialogue1
    history1 = "chat_history_" + ann + ".xlsx"
    history2 = "chat_history_" + args.dialogue2 + ".xlsx"
    df_to_argue = pd.read_csv(args.dataset)
    


    dialogues_1 = pd.read_excel(history1)
    dialogues_2 = pd.read_excel(history2)
    sentences = df_to_argue.groupby('Label').sample(n = 5, random_state=89)
    sentences = sentences["Context"].values.tolist()
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
    ded = []

    r_cohs = []
    r_rels = []
    r_info = []
    r_arg = []
    r_help = []
    r_ded = []
    for j in range(len(sentences)):
        # print(sentences[j])
        # sentence = sentences[j].split(",")[4]
        sentence = sentences[j]
        dialogue1 = dl1[j]
        dialogue2 = dl2[j]

        print(sentence)
        eval_res_COH = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_COHERENCE, 0)
        # print(eval_res_COH)
        eval_coh = json.loads(eval_res_COH.content[0].text)
        eval_res_RELE = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_CONSISTENCY, 0)
        eval_rele = json.loads(eval_res_RELE.content[0].text)
        eval_res_INFO = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_INFORMATION_DIV, 0)
        eval_info = json.loads(eval_res_INFO.content[0].text)
        eval_res_ARG = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_VALID_ARGUMENTS, 0)
        eval_arg = json.loads(eval_res_ARG.content[0].text)
        eval_res_HELP = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_HELPFULNESS, 0)
        eval_help = json.loads(eval_res_HELP.content[0].text)
        eval_res_DEF = await eval_claude("eval_s", model_agent, sentence, dialogue1, dialogue2, None, None, None, EVAL_STANCE_MAINTENANCE, 0)
        eval_def = json.loads(eval_res_DEF.content[0].text)

        cohs.append(eval_coh["ans"])
        rels.append(eval_rele['ans'])
        info.append(eval_info['ans'])
        arg.append(eval_arg['ans'])
        help.append(eval_help['ans'])
        ded.append(eval_def['ans'])

        r_cohs.append(eval_coh["reason"])
        r_rels.append(eval_rele["reason"])
        r_info.append(eval_info["reason"])
        r_arg.append(eval_arg["reason"])
        r_help.append(eval_help["reason"])
        r_ded.append(eval_def['reason'])




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
        'stance changes': ded,
        'reason for stance change': r_ded,



    }
    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

        

if __name__ == '__main__':
    asyncio.run(main())
