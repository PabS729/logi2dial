PROMPT_DECOMPOSE_TOULMIN = """
Decompose this <sentence> according to the Toulmin's model.

<sentence>: {sentence}

Format your answer in JSON with the following keys: "claim": <claim of the sentence>, "grounds": <grounds of the sentence>, "warrant": <warrant of the sentence>.
If there are multiple grounds to a claim, separate them with comma in the "grounds" section of your answer.
"""


# PROMPT_TEACHER_THINK = """
# You are a teacher who knows toulmin's theory. You are interacting with a student who believes in <sentence>. 
# Think about the student's response in <dialogue_history>, and answer the following question: 
# Q1: What is the student's concern over your response?
# Q2: Is the student trying to steer the conversation from talking about toulmin's model? 
# Q3: If yes to Q2, then how can you remind the student of focusing on toulmin's model?

# <sentence>: {sentence}
# <dialogue_history>: {history}

# format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2> "Q3": <answer_to_Q3>. limit your answer to 30 words for each question.

# """

# PROMPT_TEACHER_TALK = """
# You are a teacher who knows the toulmin's model. You are interacting with a student who believes in <sentence>. The <decomposition> decomposes <sentence> into toulmin's model.
# Think about the flaw of <sentence> given <decomposition>, and talk to the student regarding it. 
# <thoughts> may be helpful when formulating the response, but do not try to copy the words directly from it.
# Keep your response short and concise.

# <sentence>: {sentence}
# <decomposition>: {profile}
# <thoughts>: {history}

# """

PROMPT_STUDENT_TALK = """
You are a person interacting with a teacher. You think that <sentence> is logically valid. You are not aware of any outside information beyond the context of <sentence>.

You are having a discussion with the teacher, and you follow <thought> when formulating your response. Respond to the teacher. Try to be creative in your response. Limit your response to 40 words. 
<sentence>: {sentence}.
<thought>: {history}

"""

PROMPT_STUDENT_THINK = """
You are a user interacting with teacher. You think that <sentence> is logically valid. You are discussing the logical validity of <sentence>. You are not aware of any outside information beyond the context of <sentence>.
As a user, you must be skeptical of the teacher's responses and have as many questions as possible. 
You can consider the teacher’s <response> in those following angles:
    - Did the teacher explain the logical fallacy properly?
    - Which part do you think is missing from the response?
    - Does the teacher have logical flaws in their response?
    - What's the teacher's intent in their response?
Think about the questions above and tell me what you can do as a user if you want to verify the validity of <sentence>. After you list all available options, pick one option as your answer. The option must contain interactions with the teacher.
Format your answer in JSON with the following key: "ans": <your_answer>


<sentence>: {sentence}
<response>: {history}
"""

PROMPT_IDENTIFY_STUDENT_STATE = """
A student and a teacher are discussing the logical validity of <sentence>.

<sentence>: {sentence}
<chat_history>: {history}

Analyze the student's utterance from <chat_history>, and select one feedback from the following list:
1. The student is concerned about the teacher's response.
2. The student disagrees with the teacher's response.
3. The student rebuts the teacher's response.
4. The student is talking about topics that strays from the conversation.
5. Student asks for clarification from the teacher.
6. The student agrees to the teacher.


If the content of student response is similar to <last_utterance>, then Answer with "7".
<last_utterance>: {profile}

Format your answer in JSON with the following key: "Type": <index of feedback indicating your answer>

"""

PROMPT_HANDLE_STUDENT_BEHAVIOR = """
You are a teacher who knows toulmin's model, and you are interacting with a student on discussing validity of <sentence>. If you think <sentence> alone is logically valid, simply ask the student if they agree with <sentence>.
Based on the student's response and <status>, follow the given <strategy> and talk to the student. Try to be creative in your response. Limit your response to 40 words.
<sentence>: {sentence}
<status>:{history}
<strategy>: {profile}
"""