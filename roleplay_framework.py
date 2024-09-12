from openai import OpenAI
from def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompts_roleplay import *
import argparse
import pandas as pd
import time
from check_score import *
from respond_role import *

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_final.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/roleplay_test_0909_equ_4o_1turn_7_w_edu_stu.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    # sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=2)
    sampled_df = df_to_argue.loc[df_to_argue["updated_label"] == "equivocation"].sample(n=1, random_state=7)
    # strategy = strategy_dc_commonsense["fallacy of credibility"]
    # strategy = emo_alt
    sentences = sampled_df["source_article"].values.tolist()
    labels = sampled_df["updated_label"].values.tolist()


    model_student = "gpt-4o"
    model_teacher = "gpt-4o"

    prompt_check_convinced = """
    The student believes in <sentence>, which contains a logical fallacy.
    In <chat_history>, the teacher is trying to convince the student. According to the response from <chat_history>, do you think the student is convinced by the teacher? Answer with "yes" or "no". 
    <sentence>: {sentence}
    <chat_history>: {history}
    """

    # model_teacher = "gpt-4o-mini"
    # model_student = 'gpt-4o-mini'
    model_agent = model_teacher
    sampled_sentence = []
    sampled_labels = []

    # example_sentence = sentences[-2]
    # prompt_student_check =PROMPT_STUDENT_CHECK
    conversation_teacher = []
    conversation_student = []
    anas = []
    pfs = []

    Threshold_counter = 0.5
    Threshold_res = 2
    for j in range(len(sentences)):
        example_sentence = sentences[j]
        example_label = labels[j]
        agreement_bank = []
        print(example_sentence)

        #Generate social profile
        profile_res = await generate_res("fact_bank", model_teacher, example_sentence, 
                                                None, None, None, None, None, PROMPT_GENERATE_PROFILE, 0)
        profile = json.loads(profile_res.choices[0].message.content)
        print(profile)
        
        # strategy_res = await generate_response("gen_strategy", model_teacher, example_sentence, 
                                                # None, None, None, None, None, PROMPT_GENERATE_STRATEGY_TEACHER, 0)
        # strategy = strategy_res.choices[0].message.content
        # print(strategy)



        rounds = 8
        conv_teacher = []
        conv_student =[]
        
        chat_history = ""
        for i in range(0, rounds):
            
            if i == 0:
                sampled_sentence.append(example_sentence)
                sampled_labels.append(example_label)
                pfs.append(profile)
                thought = ""
            else: 
                sampled_sentence.append("")
                sampled_labels.append("")
                pfs.append("")
                # thought_res = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_TEACHER_REFUTE, 0)
                # thought = thought_res.choices[0].message.content
                thought_res = await generate_res("thought", model_teacher, example_sentence, chat_history, None, None, None, None, PROMPT_THINK, 0)

                thought = json.loads(thought_res.choices[0].message.content)
                thought = thought["Q1"] +"\n"+ thought["Q2"] + "\n" + thought["Q3"]
                print(thought)
                chat_history = ""
            
            anas.append(thought)

            # curr_strat = await generate_response("strategy", model_teacher, example_sentence, 
                                                # chat_history, strategy, None, None, None, PROMPT_ANALYZE_STAGE, 0)
            # curr_strat = json.loads(curr_strat.choices[0].message.content)["ans"]
            # print(curr_strat)
            # teacher_res = await generate_response("teacher_st", model_teacher, example_sentence, curr_strat, strategy, None, conv_teacher, conv_student, PROMPT_FOLLOW_STRATEGY, 0)

            # teacher_res = await generate_response("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_No_CoT, 0)

            teacher_res = await generate_res("teacher", model_teacher, example_sentence, thought, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE, 0)
            utterance_teacher = teacher_res.choices[0].message.content
            chat_history += "teacher: " + utterance_teacher + "\n"
            print(utterance_teacher)
            conversation_teacher.append(utterance_teacher)
            conv_teacher.append(utterance_teacher)

            student_res = await generate_res("student", model_teacher, example_sentence, None, profile, None, conv_teacher, conv_student, PROMPT_ARGUE_FOR_LF, 0)
            utterance_student = student_res.choices[0].message.content
            chat_history += "student: " + utterance_student + "\n"
            print(utterance_student)
            conversation_student.append(utterance_student)
            conv_student.append(utterance_student)

            print("%d\n", i)
            agent_res = await generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, prompt_check_convinced, 0)
            agent_res = agent_res.choices[0].message.content
            print(agent_res)
            if "yes" in agent_res.lower():
                break

        #the student is convinced, time to educate the student
        conv_teacher = []
        conv_student =[]
        for i in range(0,4):

            sampled_sentence.append("")
            sampled_labels.append("")
            pfs.append("")
            # thought_res = await generate_res("gen_strategy", model_teacher, example_sentence, None, None, None, None, None, PROMPT_TEACHER_THINK, 0)
            # thought = json.loads(thought_res.choices[0].message.content)
            # thought = thought["Q1"] +"\n"+ thought["Q2"]
            # print(thought)
            chat_history = ""

            anas.append("")

            teacher_res = await generate_res("t_edu", model_teacher, example_sentence, None, None, None,  conv_teacher, conv_student, PROMPT_TEACHER_EDUCATE, 0)
            utterance_teacher = teacher_res.choices[0].message.content
            chat_history += "teacher: " + utterance_teacher + "\n"
            print(utterance_teacher)
            conversation_teacher.append(utterance_teacher)
            conv_teacher.append(utterance_teacher)

            student_res = await generate_res("student", model_teacher, example_sentence, None, profile, None, conv_teacher, conv_student, PROMPT_STUDENT_INTERACT, 0)
            utterance_student = student_res.choices[0].message.content
            chat_history += "student: " + utterance_student + "\n"
            print(utterance_student)
            conversation_student.append(utterance_student)
            conv_student.append(utterance_student)

            






    print(len(anas), len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels))
    data_dict = {
                 'teacher_analysis': anas,
                 'teacher_response': conversation_teacher, 
                 'layman_response': conversation_student, 
                 'sentence_sample': sampled_sentence, 
                 'labels': sampled_labels
                }
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
