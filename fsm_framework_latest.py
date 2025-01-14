from openai import OpenAI
from contradict_app.def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import copy
import os
from prompts_toulmin import * 
import argparse
import pandas as pd
import time
from persona_roleplay.prompts_roleplay import *
from persona_roleplay.respond_role import *
from strategy_handle import * 
from Intent_prompts import *

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='pos_train_set.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_banks", type=bool, default=True)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--use_FSM", type=bool, default=True)
    parser.add_argument("--save_fn", type=str, default='results/n_0110_all_15_prod_ent_w')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=0)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    sampled_df = df_to_argue.sample(n=1, random_state=15)
    
    # df_lf = pd.read_csv
    # df_components = pd.read_excel(args.components_to_read)
    # sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "ad populum"].sample(n=1, random_state=15)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["Context"].values.tolist()
    labels = sampled_df["Label"].values.tolist()
    # sentences = ["In fact, it's starting to fall apart not because of lawsuits -- though they are a problem, and John Edwards and I are committed to fixing them -- but because of the larger issue that we don't cover Americans."]
    # labels =["false causality"]
    model_student = "gpt-4o"
    model_teacher = "gpt-4o"

    # sentences = ["Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way."]
    # labels = ["Slippery Slope"]

    # sentences = ["You know, nobody likes who shot John, but I think the first negative campaign run in this election was by Governor Clinton, and I'm not going to sit there and be a punching bag; I'm going to stand up and say, hey, listen, here's my side of it."]
    # labels = ["appeal to emotion"]
    # sentences = ["After all, the Welfare Reform Act, which Al Gore promised to lead the effort on to get people off of welfare to set time limits, to get people to enjoy the dignity of work. That was a bipartisan act that was adopted. The Anti - Crime Act that has helped to lower crime more than 20% in our country was also bipartisan. The Balanced Budget Act of 1997 which was critical to getting our economy to the point and our government to the point of unprecedented surplus we enjoy today also was bipartisan, and Al Gore was involved."]
    # labels = ["false cause"]
    # model_teacher = "gpt-4o-mini"
    # model_student = 'gpt-4o-mini'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    conversation_teacher = []
    conversation_student = []
    sums = []
    anas = []
    pfs = []
    chats = []
    reles = []
    coll_agr = []
        
    coll_bank = []

    lm_thought = []
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #Generates toulmin Decomposition of sentence.
        if args.use_toulmin:
            toulmin_res = await generate_res("gen_strategy", model_student, example_sentence, 
                                                    None, None, None, None, None, PROMPT_DECOMPOSE_TOULMIN, 0)
            toulmin = json.loads(toulmin_res.choices[0].message.content)
            print(toulmin)

            opening_res = await generate_res("conv", model_teacher, example_sentence, 
                                                    None, None, None, None, None, PROMPT_OPENING, 0)
            conversation_teacher.append(opening_res.choices[0].message.content)
            conversation_student.append(STUDENT_RESPONDS)

            anas.append('')
            lm_thought.append('') 
            sums.append('')
            reles.append('')
            coll_bank.append([])
            coll_agr.append([])


        rounds = 7

        

        chat_history = ""
        full_chat = ""
        summary = ""
        agr_bank = []

        #Check if student agrees with the components. Ideally, the student should agree with all of them.
        if args.use_toulmin:
            ct = 0
            for k in toulmin.keys():
                disagr_bank = []
                conv_teacher = []
                conv_student =[]
                decomp = toulmin[k]
                teacher_res = await generate_res("t", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_AGREE_COMP, 0)
                conv_teacher.append(teacher_res.choices[0].message.content)
                utterance_teacher = teacher_res.choices[0].message.content
                if ct == 0:
                    conversation_teacher.append(START_UTTER+utterance_teacher)
                else: 
                    conversation_teacher.append(utterance_teacher)
                print(utterance_teacher)
                student_res = await generate_res("student_bio", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
                conv_student.append(student_res.choices[0].message.content)
                utterance_student = student_res.choices[0].message.content
                print(utterance_student)
                conversation_student.append(utterance_student)
                anas.append("")
                lm_thought.append("")
                sums.append("")
                reles.append("")
                coll_bank.append([])
                coll_agr.append([])
                agr_bank.append(k + ": " + decomp)
                if "yes" in student_res:
                    continue
                ct += 1
        
        # for k in toulmin.keys():
        if True:
            conv_teacher = []
            conv_student =[]
            if args.use_toulmin:
                # decomp = toulmin[k]
                # print(decomp)
            # teacher_res = await generate_res("t", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_JUDGEMENT, 0)
            
            #Teacher check the logical validity of sentence, and ask the student if they agree with the judgement
                teacher_res = await generate_res("", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_JUDGEMENT, 0)
                teacher_r = json.loads(teacher_res.choices[0].message.content)
                flaw_part = teacher_r["2"]
                teacher_res = teacher_r["1"]
            else:
                teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)
                teacher_res = teacher_res.choices[0].message.content
            conv_teacher.append(teacher_res)
            utterance_teacher = teacher_res
            print(utterance_teacher)
            # student_res = await generate_res("student_bio", model_teacher, example_sentence, "["+ k + ": " + decomp + "]", None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            
            #student responds. 
            if args.use_toulmin:
                student_res = await generate_res("student_bio", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_STUDENT_RESPOND, 0)
            else:
                student_res = await generate_res("student", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_STUDENT_STUBBORN, 0)
            utterance_student = student_res.choices[0].message.content
            conv_student.append(utterance_student)
            
            print(utterance_student)
            anas.append("")
            lm_thought.append("")
            sums.append("")
            reles.append("")
            coll_bank.append([])
            conversation_teacher.append(utterance_teacher)
            conversation_student.append(utterance_student)
            cp_agr = copy.deepcopy(agr_bank)
            coll_agr.append(cp_agr)
            # agr_bank.append()

            #If yes, end conversation
            if "yes" in student_res.choices[0].message.content.lower():
                print("initial agreement")
                if args.use_banks:
                    agr_bank.append(conv_teacher[-1])
                continue

            # if no, enter debate
            else: 
                tmp = conv_teacher[-1]
                disagr_bank = []
                #if the student disagrees, enter discussion
                for i in range(0, rounds):
                    # print(i)
                    if i == 0:
                        sampled_sentence.append(example_sentence)
                        sampled_labels.append(example_label)

                        thought = "D"
                        reles.append("")
                        coll_bank.append([])
                        # coll_agr.append([])
                    else: 
                        
                        sampled_sentence.append("")
                        sampled_labels.append("")

                        #checks the relevance and potential repetition of the student's response
                        thought = 0
                        if args.use_banks:
                            relevance_res = await generate_res("check", model_teacher, example_sentence, disagr_bank, 
                                                               utterance_student, agr_bank, conv_teacher, conv_student, PROMPT_CHECK_DISAGREEMENT, 0)
                            relevance = json.loads(relevance_res.choices[0].message.content)
                            print(relevance)
                            reles.append(relevance)

                            #if the student's response is not addressed previously, then we have a new topic. Identify the student's states to be used later
                            if "yes" in relevance["Q1"].lower() and "no" in relevance["Q3"].lower():
                                agreement_bank.append(relevance)
                                # disagr_bank.append(relevance)
                                thought_res = await generate_res("strategy", model_teacher, example_sentence, chat_history, 
                                                                 None, None, None, None, PROMPT_IDENTIFY_STUDENT_STATE, 0)

                                thought = json.loads(thought_res.choices[0].message.content)["Type"]

                                strat_teacher = await generate_res("tea_strat", model_teacher, example_sentence, chat_history, 
                                                                 indicator[str(thought)], toulmin, None, None, PROMPT_DESIGN_STRATEGY, 1)
                                strat_teacher = strat_teacher.choices[0].message.content
                                print(strat_teacher)
                            #Otherwise, the student have asked about things that are previously discussed
                            elif "yes" in relevance["Q3"].lower(): 
                                thought = 7
                            else:
                                thought = 4
                            
                            #add to disagreement bank if new disagreement is proposed
                            if "yes" in relevance["Q2"].lower():
                                disagr_bank.append(relevance["Q2"])
                            cp_bank = copy.deepcopy(disagr_bank)
                            coll_bank.append(cp_bank)
                        
                            print(thought)
                        elif args.use_FSM:
                            thought_res = await generate_res("strategy", model_teacher, example_sentence, chat_history, 
                                                                 None, None, None, None, PROMPT_IDENTIFY_STUDENT_STATE, 0)
                            thought = json.loads(thought_res.choices[0].message.content)["Type"]
                            reles.append("")
                            coll_bank.append([])
                            print(thought)
                        else:
                            reles.append("")
                            coll_bank.append([])
                        chat_history = ""
                        
                    
                    # anas.append(thought)

                    # print(curr_strat)
                        
                    anas.append(thought)
                    print(disagr_bank)

                    if i == 0 and args.use_toulmin:
                        #teacher's initial analysis and judgement of the sentence
                        teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF, 0)
                        summary = ""
                    elif args.use_FSM and (thought == 4 or thought == 7):
                        print("taken")

                        #teacher's response when the student is repeating topics that has been previously discussed
                        teacher_res = await generate_res("teacher_st", model_teacher, example_sentence, summary, relevance["Q3"], None, [], conv_student[-1], PROMPT_REMIND_FOCUSED, 0)
                    elif args.use_FSM:
                        #teacher's response according to detected student behavior
                        # teacher_res = await generate_res("tea", model_teacher, example_sentence, summary, None, None, conv_teacher, conv_student, BASE_PROMPT+STRATEGY_HANDLE_STUDENT[str(thought)]+END_PROMPT , 1)
                        teacher_res = await generate_res("exp", model_teacher, example_sentence, indicator[str(thought)], STRATEGY_HANDLE_STUDENT[str(thought)], summary, conv_teacher, conv_student, PROMPT_HANDLE_STUDENT_BEHAVIOR, 0)
                    elif args.use_toulmin:
                        print("cont toulmin")
                        teacher_res = await generate_res("tea", model_teacher, example_sentence, toulmin, None, None, conv_teacher, conv_student, PROMPT_TALK_ABOUT_LF_CONV, 0)
                    else:
                        teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)


                    utterance_teacher = teacher_res.choices[0].message.content
                    chat_history += "teacher: " + utterance_teacher + "\n"
                    print(utterance_teacher)
                    conversation_teacher.append(utterance_teacher)
                    conv_teacher.append(utterance_teacher)
                    
                    #summarizes the teacher's responses
                    summary = await generate_res("sum", model_teacher, example_sentence, conv_teacher, None, None, None, None, PROMPT_SUMMARIZE, 0)
                    summary = summary.choices[0].message.content
                    if i == 0:
                        agreement_bank.append(summary)
                    print(summary)
                    sums.append(summary)

                    #Student CoT
                    student_res_thought = await generate_res("", model_teacher, example_sentence, conv_teacher[-1] + "\n" + summary, None, None, conv_teacher, conv_student, PROMPT_STUDENT_THINK, 1)
                    student_res_thought = json.loads(student_res_thought.choices[0].message.content)["ans"]
                    print("student thinks:" + student_res_thought)
                    lm_thought.append(student_res_thought)
                    student_res = await generate_res("student_bio", model_student, example_sentence, student_res_thought, None, None, conv_teacher, conv_student, PROMPT_STUDENT_TALK, 1)
                    
                    utterance_student = student_res.choices[0].message.content
                    print(utterance_student)
                    conversation_student.append(utterance_student)
                    conv_student.append(utterance_student)
                    
        
                    chat_history += "student: " + utterance_student + "\n"

                    #check whether the student agrees with the teacher
                    agent_res = await generate_res("eval_s", model_student, example_sentence, chat_history, summary, None, conv_teacher, conv_student, PROMPT_AGENT_CHECK, 0)
                    res = agent_res.choices[0].message.content
                    print(res)
                    if "no" not in res.lower():
                        print("student agreed")
                        if args.use_banks:
                            if len(disagr_bank) != 0:
                                agr_bank.append(disagr_bank[int(res) - 1])
                                del disagr_bank[int(res) - 1]
                            
                    cp_agr = copy.deepcopy(agr_bank)
                    coll_agr.append(cp_agr)
                    print(cp_agr)
                    full_chat += chat_history
                    if i >= 5:
                        agent_res = await generate_res("eval_s", model_student, example_sentence, conv_student, disagr_bank, None, None, None, PROMPT_CHECK_FIN_AGREEMENT, 0)
                        res = agent_res.choices[0].message.content
                        print(res)
                        if "yes" in res.lower():
                            teacher_res = await generate_res("exp", model_teacher, example_sentence, summary, None, None, conv_teacher, conv_student, PROMPT_FINISH, 0)
                            conversation_teacher.append(teacher_res.choices[0].message.content)
                            conversation_student.append("Ok. I think I have learned everything necessary about the logical validity of the sentence. Thanks a lot for helping me!")
                            cp_agr = copy.deepcopy(agr_bank)
                            coll_agr.append(cp_agr)
                            cp_bank = copy.deepcopy(disagr_bank)
                            coll_bank.append(cp_bank)
                            sums.append("")
                            reles.append("")
                            anas.append("")
                            lm_thought.append("")
                            break
    
                    #after 7 rounds, check if all comments are fully addressed by the teacher. 
                    # if i >= 7:
                    #     agent_res = await generate_res("eval_s", model_student, example_sentence, conv_teacher, disagr_bank, None, None, None, PROMPT_AGENT_CHECK, 0)
                    #     res = agent_res.choices[0].message.content
                    #     print(res)
                    #     if "yes" in res.lower():
                    #         break
                    

                    

        chats.append(full_chat)


    print(len(lm_thought), len(anas), len(conversation_teacher), len(conversation_student), len(lm_thought), len(sums), len(reles), len(coll_agr), len(coll_bank))
    data_dict = {
                 'teacher_analysis': anas,
                 'layman_thought': lm_thought, 
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                #  'tracker': agr,
                 'summary': sums,
                 'student_check_relevance': reles,
                 'disagreement_bank': coll_bank,
                 'agreement_bank': coll_agr
                }
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn + str(args.num_gen) + ".xlsx", index=False)

    # df_chats = pd.DataFrame({"chats": chats})
    # df_chats.to_excel("chat_history_" + args.save_fn + str(args.num_gen) + ".xlsx", index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
