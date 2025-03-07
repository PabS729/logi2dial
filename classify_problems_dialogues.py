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
from eval_claude import eval_claude
from tqdm import tqdm

# PF = [PROMPT_CLASSIFY_RELEVANCE, PROMPT_CLASSIFY_STANCE_CHANGE, PROMPT_CLASSIFY_COMPLEX_REFUTATION, PROMPT_CLASSIFY_REPETITION]
# PF = [PROMPT_CLASSIFY_PERSPECTIVE]
# PF = [PROMPT_CLASSIFY_PERSPECTIVE, PROMPT_CLASSIFY_PROACTIVE, PROMPT_CLASSIFY_TERMS]
PF = [PROMPT_CLASSIFY_GUIDANCE, PROMPT_CLASSIFY_STRUCTURED_ANALYSIS, PROMPT_CLASSIFY_PERSPECTIVE, PROMPT_CLASSIFY_TERMS, PROMPT_CLASSIFY_RELEVANCE, PROMPT_CLASSIFY_STANCE_CHANGE, PROMPT_CLASSIFY_COMPLEX_REFUTATION, PROMPT_CLASSIFY_REPETITION, PROMPT_CLASSIFY_PROOF]
ns = [[],[],[],[],[],[],[],[],[],[],[]]
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue1", type=str, default='classification_results/all_talk_b.xlsx')
    parser.add_argument("--dataset", type=str, default='pos_train_set.csv')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/classify_gpt_haiku_')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.dialogue1
    # history1 = "chat_history_" + ann + ".xlsx"
    history1 = ann

    df_to_argue = pd.read_csv(args.dataset)

    dialogues_1 = pd.read_excel(history1)
    x = args.num_gen

    sentences = dialogues_1["sentences"].values.tolist()[x:x+100]
    dl1 = dialogues_1["chats"].values.tolist()[x:x+100]

    model_agent = "o3-mini"
    # model_agent = "deepseek-reasoner"
    model_agent = "qwq-32b"
    model_agent = "claude-3-5-haiku-20241022"

    goods_1 = []
    goods_2 = []

    toks = 0

    for j in tqdm(range(len(sentences))):
        sentence = sentences[j]
        dialogue1 = dl1[j]
        # print(sentence)
        for p in range(0,len(PF)):

            # eval_res = await generate_res("ev", model_agent, sentence, dialogue1, None, None, None, None, PF[p], 0)
            # response = ""
            # if model_agent == "qwq-32b":
            #     done = False
            #     while not done:
            #         try:
            #             for chunk in eval_res:
            #                 rs = load_json(chunk.model_dump_json())
            #                 rs = rs["choices"][0]["delta"]["reasoning_content"]
            #                 if rs != None:
            #                     response += rs
            #             done = True
            #         except Exception as e:
            #             print(e)

            # else:
            #     response = eval_res.choices[0].message.content
            #     toks += eval_res.usage.total_tokens
            eval_res = await eval_claude("eval_s", model_agent, sentence, dialogue1, None, None, None, None, PF[p], 0)
            response = eval_res.content[0].text
            # print(response)
            # while eval_coh == False:
            #     eval_res = await generate_res("ev", model_agent, sentence, dialogue1, None, None, None, None, PF[p], 0)
            #     eval_coh = load_json(eval_res.choices[0].message.content)

            ns[p].append(response)
        


    # data_dict = {
    #     "sentences": sentences, 
    #     "chats": dl1,
    #     # "divergence": ns[0],
    #     "stance change": ns[0],
    #     "complex refutation": ns[1],
    #     # "asking for proof": ns[0],
    #     "repetition": ns[2],
    #     }
    # data_dict = {
    #     "sentences": sentences, 
    #     "chats": dl1,
    #     # "divergence": ns[0],
    #     "perspective": ns[0],
    #     # "activeness": ns[1],
    #     # "asking for proof": ns[0],
    #     # "terms": ns[2],
    #     }
    # data_dict = {
    #     "sentences": sentences,
    #     "proof_orig": dialogues_1["divergence"],
    #     "human label": dialogues_1["label"],
    #     "labels": ns[0]
    # }
    print(toks)
    data_dict = {
        "sentences": sentences, 
        "chats": dl1,
        # "divergence": ns[0],
        "guidance": ns[0],
        "structured": ns[1],
        # "focused": ns[2],
        # "activeness": ns[1],
        "perspective": ns[2],
        
        "terms": ns[3],
        "divergence": ns[4],
        "stance_change": ns[5],
        "complex_refutation": ns[6],
        "repetition": ns[7],
        "asking_for_proof": ns[8],

        }

    df = pandas.DataFrame.from_dict(data_dict)

    df.to_excel("eval_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done eval")

if __name__ == '__main__':
    asyncio.run(main())