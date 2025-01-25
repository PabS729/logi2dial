
Transition_from_1 = """
1. The example given by the student is not specific enough. You need to ask the student to provide more examples.
2. The example given by the student contains logical error. 
3. The Student Requests for examples or clarifications to illustrate your point.
4. The student's examples might be unclear. Assumption is needed to clarify the student's examples.
5. The example given by the student is unrelated to the topic of discussion.
"""

Transition_from_2 = """
1. The new argument proposed by the student lacks evidence. You need to obtain examples from the student to illustrate.
2. The argument has clear logical flaw that can be further refuted.
3. The Student Requests for examples to illustrate your point.
4. The student's argument is unclear and assumption is needed to clarify the student's argument.
5. The argument given by the student is unrelated to the topic of discussion.
"""

Transition_from_3 = """
1. The new argument proposed by the student lacks evidence. You need to obtain examples from the student to illustrate.
2. There is a clear logical flaw in the student's argument, or the student's argument is unrelated to the topic of discussion.
3. The Student Requests for examples or clarifications to illustrate your point.
4. The student's argument is unclear and assumption is needed to clarify the student's argument.
5. The argument given by the student is unrelated to the topic of discussion.
"""

Transition_from_4 = """
1. To check the validity of student's assumptions, you need to ask the student to provide examples.
2. The student's assumption has clear logical flaw, or is unrelated to the topic of discussion.
3. The Student Requests for examples or clarifications to illustrate your point.
4. The student's argument is still unclear given the assumption. You need to ask about more assumptions to clarify the student's argument.
5. The argument given by the student is unrelated to the topic of discussion.
"""

Transition_from_5 = Transition_from_3

CHECK_RESPONSE_TEACHER = """
You are an experienced teacher who knows how to debate, and you are interacting with student named [I], on discussing logical validity of <sentence>.
Remember, the topic you are discussing on is the logical validity of <sentence>. You have to maintain your position and try not to be convinced by the student.
Consider the student's response in <history>, and answer the following questions:

Q1: Does the student make an argument without presenting enough evidence that supports it?
Q2: Does the student's argument or example have clear logical flaws?
Q3: Is the student explicitly requesting evidence or explanation?
Q4: Does the student's argument need more assumptions to clarify?

For each question, answer with "yes" or "no". Format your answer in JSON with the following key: "1": <answer to Q1>, "2": <answer to Q2>, "3": <answer to Q3>, "4": <answer to Q4>
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
Think about the flaws in the student's reponse. 


"""

TEACHER_ACT_2 = """
Remember, the topic you are discussing on is the logical validity of <sentence>. You don't think that the sentence is logically valid. You have to maintain your position and try not to be convinced by the student. Keep your tone nudging and friendly. 
Use the option above to respond to the student. Please follow strictly to the option. Limit your response to 60 words.

<sentence>: {sentence}
"""

STRAT_FOR_STATES = {
    "1": "Request the student to provide evidence that supports his claim.",
    "2": """
    Refute the student's argument, based on four ways. 
    a. Showing that the argument's conclusion or premise is wrong.
    b. Proposing counterargument with similar premises but different conclusions.
    c. Showing that the argument's conclusion does not follow from the premise.
    d. Showing that the student's argument is irrelevant to the topic of discussion. Even if the evidence provided is valid, it may be irrelevant to the logical validity of <sentence>, and thus can be dismissed.""",

    "3": "Respond to the student's request on providing evidence or clarifications.",
    "4": "Ask about the student's assumptions based on their response.",
    "5": "Remind the student that their response is not related to the topic of discussion"
}

TRANSITIONS = {
    "1": Transition_from_1,
    "2": Transition_from_2,
    "3": Transition_from_3,
    "4": Transition_from_4,
    "5": Transition_from_5, 
}

CHECK_FOLLOW_FSM_AGENT = """
You are a judge overlooking the dialogue between a teacher and a student, they are having a debate over the logical validity of <sentence>.
Based on the teacher's <response>, check if the teacher has followed <strategy> in formulating their response. Answer with "yes" or "no" only.
<sentence>: {sentence}
<response>: {history}
<strategy>: {profile}
"""