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


# PF = [PROMPT_CLASSIFY_RELEVANCE, PROMPT_CLASSIFY_STANCE_CHANGE, PROMPT_CLASSIFY_COMPLEX_REFUTATION, PROMPT_CLASSIFY_REPETITION]
# PF = [PROMPT_CLASSIFY_PERSPECTIVE]
# PF = [PROMPT_CLASSIFY_PERSPECTIVE, PROMPT_CLASSIFY_PROACTIVE, PROMPT_CLASSIFY_TERMS]
PF = [PROMPT_CLASSIFY_GUIDANCE, PROMPT_CLASSIFY_STRUCTURED_ANALYSIS, PROMPT_CLASSIFY_PERSPECTIVE, PROMPT_CLASSIFY_TERMS, PROMPT_CLASSIFY_RELEVANCE, PROMPT_CLASSIFY_STANCE_CHANGE, PROMPT_CLASSIFY_COMPLEX_REFUTATION, PROMPT_CLASSIFY_REPETITION, PROMPT_CLASSIFY_PROOF]
ns = [[],[],[],[],[],[],[],[],[],[],[]]
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue1", type=str, default='results/ds_0301_900')
    parser.add_argument("--dataset", type=str, default='pos_train_set.csv')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/classify_ds_900')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    ann = args.dialogue1
    history1 = "chat_history_" + ann + ".xlsx"
    # history1 = ann

    df_to_argue = pd.read_csv(args.dataset)

    dialogues_1 = pd.read_excel(history1)

    sentences = dialogues_1["sentences"].values.tolist()
    dl1 = dialogues_1["chats"].values.tolist()

    model_agent = "o3-mini"
    # model_agent = "deepseek-reasoner"

    goods_1 = []
    goods_2 = []

    for j in range(len(sentences)):
        sentence = sentences[j]
        dialogue1 = dl1[j]
        print(sentence)
        for p in range(0,len(PF)):

            eval_res = await generate_res("ev", model_agent, sentence, dialogue1, None, None, None, None, PF[p], 0)
            eval_coh = eval_res.choices[0].message.content
            # while eval_coh == False:
            #     eval_res = await generate_res("ev", model_agent, sentence, dialogue1, None, None, None, None, PF[p], 0)
            #     eval_coh = load_json(eval_res.choices[0].message.content)

            ns[p].append(eval_coh)
        


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