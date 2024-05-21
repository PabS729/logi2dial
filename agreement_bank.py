from openai import OpenAI
from def_logical_fallacy import *
from ast import parse
from collections import defaultdict
import json
import os
import asyncio
from prompt_bank import *
import argparse
import pandas as pd
import time

role_bank = ["agent", "fact_bank", "find_contradiction", "point_out", "student", "get_agreement", "check_agreement"]

async def generate_response(role, model_name, sentence, history, bank, target_statement, 
                            teacher_res, student_res, prompt_gen, temperature=0):
    client = OpenAI()

    p = prompt_gen
    msgs = []
    if role == "agent" : 
        user_prompt = p.format(sentence=sentence, chat_history=history)
    elif role in ["fact_bank", "student", "check_agreement"]:
        user_prompt = p.format(sentence=sentence)
    elif role in ["find_contradiction", "point_out"]: 
        user_prompt = p.format(sentence=sentence, fact_bank=bank)
    else:
        user_prompt = p.format(sentence=sentence, agreement_bank=bank, target_statement=target_statement)
    

    msgs.append({"role": "system", "content": user_prompt})

    #teacher and student take turns
    if role == "get_agreement": 
        for (t,s) in zip(teacher_res, student_res):
            msgs.append({"role": "assistant", "content": t})
            msgs.append({"role": "user", "content": s})
    if role == "student":
        if zip(teacher_res[:-2], student_res) != None: 
            for (t,s) in zip(teacher_res[:-2], student_res):
                msgs.append({"role": "user", "content": t})
                msgs.append({"role": "assistant", "content": s})
        msgs.append({"role": "user", "content": teacher_res[-1]})
    done = False
    while not done:
        try: 
            if role in ["fact_bank", "find_contradiction"]:
                response = client.chat.completions.create(
                model=model_name,
            messages=msgs,
            temperature=temperature,
            response_format={ "type": "json_object" }
            )
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

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_cleaned.csv')
    parser.add_argument("--components_to_read", type=str, default='decomposed_sentences_toulmin.xlsx')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=False)
    parser.add_argument("--use_toulmin", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/agreement_bank_example4_tuned.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
    df_components = pd.read_excel(args.components_to_read)
    # print(df_to_argue.loc[0])

    length_of_conversation = 5
    # st = df_to_annotate["Text"].tolist()
    sampled_df = df_to_argue.groupby("updated_label").sample(n=1, random_state=1)
    
    sentences = sampled_df["source_article"].values.tolist()
    sentences = [
        "That's what abortion is - killing innocent humans for money. Abortionists are government licensed hit men.""That's what abortion is - killing innocent humans for money. Abortionists are government licensed hit men.",
        "Marie notices that many of her friends have started eating a low-carb diet and drinking protein shakes. Marie decides that if this many friends are eating this way that this must be the healthy way to eat so she joins them. This is an example of which logical fallacy?",
        "You'll make the right decision because you have something that not many people do: you have heart.",
        "Pamela never lies. She told me herself, so it must be true.",

        "When the judge asked the defendant why he hadn't paid his parking fines, he said that he shouldn't have to pay them because the sign said 'Fine for parking here' and so he naturally presumed that it would be fine to park there.",
        "My brother's girlfriend's Mother's hairdresser said that COVID numbers are going down, so I'm not going to bother with my mask",
        "If the argument is supposed to be about whether or not we, as the American public should wear masks, and you argue: 'Asking an infant to wear a mask is ridiculous!'",
        "All forest creatures live in the woods.All leprechauns are forest creatures.Therefore, some leprechauns live in the woods.",
        "Mother: It’s bedtime Jane Jane: Mom, how do ants feed their babies? Mother: Don’t know dear, close your eyes now. Jane: But mama, do ant babies cry when they’re hungry?",
        "every time Joe goes swimming he is wearing his Speedos. Something about wearing that Speedo must make him want to go swimming.",
        "If you don’t say the Pledge of Allegiance, then you must be a traitor.",
        "If I don't take the right classes in high school, then I won't be able to get into a good college. If I don't get into a good college, then I won't be able to get a job. If I can't get a job, then I am going to end up homeless.",
        "Is your stupidity inborn?"
    ]
    print(len(sentences))
    labels = sampled_df["updated_label"].values.tolist()


    model_student = "gpt-4o"
    model_teacher = model_student
    model_agent = model_teacher
    # model_teacher = "gpt-3.5-turbo-0125"
    sampled_sentence = []
    sampled_labels = []

    example_sentence = sentences[5]
    done = False
    prompt_fact_bank = PROMPT_FACT_BANK
    prompt_find_contradiction = PROMPT_TEACHER_FIND_CONTRADICTION
    prompt_teacher_agreement = PROMPT_TEACHER_AGREEMENT
    prompt_student = SYSTEM_PROMPT_STUDENT_NEW
    prompt_agent = PROMPT_AGENT_CHECK_AGREEMENT
    prompt_doublecheck = PROMPT_TEACHER_CHECK_AGREEMENT
    prompt_student_check =PROMPT_STUDENT_CHECK
    agreement_bank = []

    #First, the teacher finds all facts and put them into the fact bank
    fact_bank_res = await generate_response("fact_bank", model_teacher, example_sentence, 
                                            None, None, None, None, None, prompt_fact_bank, 0)
    fact_dict = json.loads(fact_bank_res.choices[0].message.content)
    print(fact_dict)

    #Next, the teacher identifies the minimum set of facts that generates a contradiction
    contradiction_res = await generate_response("find_contradiction", model_teacher, example_sentence, 
                                                None, fact_dict, None, None, None, prompt_find_contradiction, 0)
    contradiction_dict = json.loads(contradiction_res.choices[0].message.content)
    print(contradiction_dict)
    #Iterate through all statements in the minimum set and get the student to agree on them
    conversation_teacher = []
    conversation_student = []
    agreement_bank = []
    for target in contradiction_dict.values():
        count = 0
        done = False
        chat_history = "\n"
        conv_teacher = []
        conv_student = []
        alternative_appr = False
        while not done: 
            teacher_res = await generate_response("get_agreement", model_teacher, example_sentence, 
                                                  None, agreement_bank, target, conv_teacher, conv_student, prompt_teacher_agreement, 0)
            conversation_teacher.append(teacher_res.choices[0].message.content)
            conv_teacher.append(teacher_res.choices[0].message.content)
            chat_history += "teacher: " + teacher_res.choices[0].message.content + "\n"

            student_res = await generate_response("student", model_student, example_sentence, 
                                                  None, None, None, conv_teacher, conv_student, prompt_student, 0)
            conversation_student.append(student_res.choices[0].message.content)
            conv_student.append(student_res.choices[0].message.content)
            chat_history += "student: " + student_res.choices[0].message.content + "\n"
            checked_agreement = await generate_response("check_agreement", model_teacher, target, None, None, None, None, None, prompt_doublecheck, 0)
            parsed_agr = [checked_agreement.choices[0].message.content]
            print(parsed_agr)
            student_res = await generate_response("student", model_student, example_sentence, 
                                                  None, None, None, parsed_agr, [], prompt_student_check, 0)
            rs = student_res.choices[0].message.content
            print(rs)
            doublecheck_history = "teacher: " + parsed_agr[0] + "\n" + "student: " + rs
            agent_res = await generate_response("agent", model_agent, example_sentence, 
                                                doublecheck_history, None, None, None, None, prompt_agent, 0)
            agreed = agent_res.choices[0].message.content
            print(agreed)
            sampled_sentence.append(example_sentence)
            sampled_labels.append("")
            count += 1
            print(count)
            print(chat_history)
            if agreed:
                done = True
                agreement_bank.append(target)
            else:
                if count == length_of_conversation:
                    done = True
                    alternative_appr = True

        if alternative_appr:
            continue


    point_out_res = await generate_response("point_out", model_teacher, example_sentence, 
                                            None, contradiction_dict, None, None, None, PROMPT_TEACHER_POINT_OUT, 0)
    conversation_teacher.append(point_out_res.choices[0].message.content)
    print(point_out_res.choices[0].message.content)
    student_res = await generate_response("student", model_student, example_sentence, 
                                                  None, None, None, conversation_teacher, conversation_student, prompt_student, 0)
    conversation_student.append(student_res.choices[0].message.content)
    print(student_res.choices[0].message.content)
    sampled_sentence.append(example_sentence)
    sampled_labels.append("")


    print(len(conversation_teacher), len(conversation_student), len(sampled_sentence), len(sampled_labels))
    data_dict = {'teacher_response': conversation_teacher, 'layman_response': conversation_student, 'sentence_sample': sampled_sentence, 'labels': sampled_labels}
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    asyncio.run(main())
