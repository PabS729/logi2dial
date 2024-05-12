
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

async def generate_response(role, model_name, sentence, teacher_res, student_res, prompt_gen, temperature=0, fallacy=None):
    client = OpenAI()
    # llm = OpenAIChat(temperature=temperature, openai_api_key=API_KEY)
    
    await asyncio.sleep(0.1)

        
    p = prompt_gen
    msgs = []
    if fallacy != None: 
        definition = fallacy_dc[fallacy]
        user_prompt = p.format(sentence=sentence, fallacy=fallacy, definition=definition)
        msgs.append({"role": "system", "content": user_prompt})
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
    response = client.chat.completions.create(
        model=model_name,
        messages=msgs
    )
    # print(results)
    return response


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_to_annotate", type=str, default='edu_train_cleaned.csv')
    parser.add_argument("--definition", type=str, default='proposed')
    parser.add_argument("--use_category", type=bool, default=True)
    parser.add_argument("--mode", type=str, default='proposed')
    parser.add_argument("--save_fn", type=str, default='results/edu_conv_toulmin+cat_sampled_bothgpt4.xlsx')
    parser.add_argument("--sample", type=int, default=-1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_gen", type=int, default=10)
    args = parser.parse_args()

    df_to_argue = pd.read_csv(args.file_to_annotate)
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

    conversation_teacher = []
    conversation_student = []
    model_student = "gpt-4-turbo-2024-04-09"
    model_teacher = model_student
    # model_teacher = "gpt-3.5-turbo-0125"
    sampled_sentence = []
    sampled_labels = []

    for j in range(len(sentences)):
        print(sentences[j])
        example_label = labels[j]
        example_argument = sentences[j]
        if not args.use_category:
            example_label = None
        for _ in range(length_of_conversation):
            sys_prompt_teacher = SYSTEM_PROMPT_TEACHER_NEW
            sys_prompt_student = SYSTEM_PROMPT_STUDENT_NEW

            results_conversation_teacher = await generate_response("teacher", model_teacher, example_argument, conversation_teacher, conversation_student, sys_prompt_teacher)
            teacher_response = results_conversation_teacher.content
            conversation_teacher.append(teacher_response)

            results_conversation_student = await generate_response("student", model_student, example_argument, conversation_teacher, conversation_student, sys_prompt_student)
            student_response = results_conversation_student.content
            conversation_student.append(student_response)

                
            sampled_sentence.append(example_argument)
            sampled_labels.append(example_label)
        conversation_student.append('.')

    data_dict = {'teacher_response': conversation_teacher, 'layman_response': conversation_layman, 'sentence_sample': sampled_sentence, 'labels': sampled_labels}
    df_result = pd.DataFrame(data_dict)
    df_result.to_excel(args.save_fn, index=False)
    print("done async")


if __name__ == '__main__':
    with get_openai_callback() as cb:
        asyncio.run(main())
        print(cb)
