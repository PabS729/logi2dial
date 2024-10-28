PROMPT_DECOMPOSE_TOULMIN = """
Decompose this <sentence> according to the Toulmin's model.

<sentence>: {sentence}

Format your answer in JSON with the following keys: "claim": <claim of the sentence>, "grounds": <grounds of the sentence>, "warrant": <warrant of the sentence>
"""

PROMPT_TEACHER_THINK = """
You are a teacher who knows toulmin's theory. You are interacting with a student who believes in <sentence>. 
Think about the student's response in <dialogue_history>, and answer the following question: 
Q1: What is the student's concern over your response?
Q2: Is the student trying to steer the conversation from talking about toulmin's model? 
Q3: If yes to Q2, then how can you remind the student of focusing on toulmin's model?

<sentence>: {sentence}
<dialogue_history>: {history}

format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2> "Q3": <answer_to_Q3>. limit your answer to 30 words for each question.

"""

PROMPT_TEACHER_TALK = """
You are a teacher who knows the toulmin's model. You are interacting with a student who believes in <sentence>. The <decomposition> decomposes <sentence> into toulmin's model.
Think about the flaw of <sentence> given <decomposition>, and talk to the student regarding it. 
<thoughts> may be helpful when formulating the response, but do not try to copy the words directly from it.
Keep your response short and concise.

<sentence>: {sentence}
<decomposition>: {profile}
<thoughts>: {history}

"""