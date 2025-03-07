CHECK_RESPONSE_TEACHER = """
You are an experienced teacher who knows how to debate, and you are interacting with student named [I], on discussing logical validity of <sentence>.
Remember, the topic you are discussing on is the logical validity of <sentence>. You have to maintain your position and try not to be convinced by the student.
Consider the student's response in <history>, and answer the following questions:

Q1: Treating the student's response as a counterargument to your stance, does the student make an argument without presenting enough evidence that supports it?
Q2: Treating the student's response or example as a counterargument to your stance, does the student present argument or example with clear logical flaws?
Q3: Is the student requesting you to provide evidence or explanation?
Q4: Treating the student's response as a counterargument to your stance, does the student's argument need more assumptions to clarify?
Q5: Is the student attacking your response by pointing out logical flaw or similarities to their argument?

For each question, answer with "yes" or "no". Format your answer in JSON with the following key: "1": <answer to Q1>, "2": <answer to Q2>, "3": <answer to Q3>, "4": <answer to Q4> "5": <answer to Q5>
<sentence>: {sentence}
<history>: {history}
"""

Q5 = """Q5: Did the teacher explicit ask the student to provide examples or assumptions, and did the student respond with examples or assumptions? Answer "yes" if both holds."""

TRANSITION_STATES = """
You are an experienced teacher who knows how to debate, and you are interacting with student named [I], on discussing logical validity of <sentence>.
Remember, the topic you are discussing on is the logical validity of <sentence>. You have to maintain your position and try not to be convinced by the student.
You have four options to choose from. Consider the student's response in <history>, and answer the following questions:

 and pick the option you think can best handle the student's response. Also, briefly state your reason why you chose the option in 20 words.
Format your answer in JSON with the following key: "ans": <index selected>, "rs": <reason for your choice>

<sentence>: {sentence}
<history>: {history}
"""

TEACHER_ACT_1 = """
You are an experienced teacher who knows how to debate, and you are interacting with student named [I], on discussing logical validity of <sentence>.
Think about the flaws in the student's reponse. You don't think that <sentence> is logically valid. 

"""


TEACHER_ACT_2 = """
Remember, the topic you are discussing on is the logical validity of <sentence>. You have to maintain your position and try not to be convinced by the student. Keep your tone calm and do not use exclamations, and respond in a way that is similar to everyday conversation. 
You are given a fixed option above, which you need to follow. Use the option above and respond to the student, and DO NOT ask additional questions besides strictly following the option. Limit your response to 50 words.

<sentence>: {sentence}
"""

TEACHER_ACT_REFUTE = """
<response> is your current response based on the option above. Please rephrase the response so that it serves to refute the student's claim according to the option above, as well as making it relevant to the discussion of logical validity over <sentence>. Limit your answer to 50 words.

<sentence>: {sentence}
<response>: {history}

"""

TEACHER_ACT_EX_AS = """

<response> is your current response based on the option above. Please rephrase the response so that it contains explicit questions to the student according to the option above, as well as making it relevant to the discussion of logical validity over <sentence>. Limit your answer to 50 words.

<sentence>: {sentence}
<response>: {history}
"""



STRAT_FOR_STATES = {
    "1": "Treating the student's response as counterargument to your stance, request the student to provide evidence that supports his claim. e.g. Can you provide examples...",
    "2": """
    Refute the student's argument using one of the following strategy. 
    a. Showing that the argument's conclusion or premise is wrong. Provide a counterargument or counterexample to illustrate your point.
    b. Showing that the argument's conclusion does not follow from the premise. Provide a counterargument or counterexample to illustrate your point.
    c. Showing that the student's argument is irrelevant to the topic of discussion. Even if the evidence provided is valid, it may be irrelevant to the logical validity of <sentence>, and thus can be dismissed.""",

    "3": "Respond to the student's request on providing evidence or clarifications, and give support to your stance if necessary.",
    "4": """Treating the student's response as counterargument to your stance, ask the student about their assumptions in their arguments. e.g. 'Why do you assume...' or 'How do you know...'. 
    """,
    
    "5": "Ask the student to clarify their definitions in their response",
    # "6": "Respond to the student's attack by defending the validity of your stance."
}

# TRANSITIONS = {
#     "1": Transition_from_1,
#     "2": Transition_from_2,
#     "3": Transition_from_3,
#     "4": Transition_from_4,
#     "5": Transition_from_5, 
# }

CHECK_FOLLOW_FSM_AGENT = """
You are a judge overlooking the dialogue between a teacher and a student, they are having a debate over the logical validity of <sentence>.
Based on the teacher's <response>, answer the following questions.
Q1. Check if the teacher has followed <strategy> in formulating their response. The teacher is following <strategy> as long as any sentence in their response contain such strategy.
Q2. If the teacher asks the student a question, is the question still helpful for determining the logical validity of <sentence>? Also Answer "yes" if there is no question provided.
For each question, answer with "yes" or "no" only. Format your answer in JSON with the following key: "1": <answer to Q1>, "2": <answer to Q2>
<sentence>: {sentence}
<response>: {history}
<strategy>: {profile}
"""

PROMPT_CTX = """
You are an experienced teacher who knows how to debate, and you are interacting with student named [I], on discussing logical validity of <sentence>.
Think about the flaws in the student's reponse. You don't think that <sentence> is logically valid. 
Below is a brief summary regarding the 4 rounds of conversation that you don't have access to. Note that you can refer to it in designing your response, but you don't have to if they are not helpful for the task.

"""

OPENING_PROMPT = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
First decompose <sentence> using toulmin's model, stating its claim, its ground, as well as its warrant.  
When responding to the student, tell the student the definition of each component, as well as contents of decomposition first.  e.g. "Let's decompose the sentence... the claim is..., the ground is ..., the warrant is ...", then tell the student which part of the decomposition you think is logically invalid. Limit your response to 80 words.

<sentence>: {sentence}

"""

ENDING_PROMPT = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Conclude the conversation with a brief paraphrase of the <summary>, restating your points and the corresponding student's point, highlighting the insightfulness of the discussion. Limit your response to 60 words.

<sentence>: {sentence}
<summary>: {history}
"""


ENDING_STUDENT = """
You are a student who is excellent in debating, and you are interacting with a teacher on discussing validity of <sentence>. 
Conclude the conversation by responding to the teacher's ending remarks, while maintaining your position that <sentence> is valid. Limit your response to 30 words.

<sentence>: {sentence}
"""