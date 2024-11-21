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
You are a stubborn user interacting with a teacher. You think that <sentence> is logically valid. You are not aware of any outside information beyond the context of <sentence>.
You are having a discussion with the teacher. Please follow <thought> when formulating your response. Limit your response to 40 words. 
<sentence>: {sentence}.
<thought>: {history}

"""

PROMPT_STUDENT_THINK = """
You are a stubborn user interacting with teacher. You think that <sentence> is logically valid. You are not aware of any outside information beyond the context of <sentence>.
As a user, you must be critical of the teacher's responses.
You can consider the teacher’s <response> in those following angles:
    - Did the teacher explain the logical fallacy properly?
    - Which part do you think is missing from the response?
    - Does the teacher have logical flaws in their response?
    - What's the teacher's intent in their response?
Think about the questions above and tell me what you can do as a user. After you list all available options, pick one option as your answer. The option must contain interactions with the teacher.
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

PROMPT_TALK_ABOUT_LF = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Use the provided <decomposition> to talk to the student. Analyze the logical flaw in the statement. When pointing out the logical flaw, make sure not the mention toulmin's model and use languages that a layman will understand.Limit your response to 50 words.

<sentence>: {sentence}
<decomposition>: {history}

"""

PROMPT_SUMMARIZE = """
You are an expert summarizer, and you are reviewing conversation from a speaker who is talking about <sentence>. Summarize the speaker's response, according to the given <chat_history>. Limit your answer to less than 30 words.

<sentence>: {sentence}
<chat_history>: {history}

"""

PROMPT_CHECK_TOPIC_RELEVANCE = """
The student and teacher are discussing about the logical validity of <sentence>. The following <tracker> contains points that are being discussed.
Check if the student's <response> is relevant to the points mentioned in <tracker>, as well as if the student's <response> revolves around the logical validity of <sentence>. If yes, summarize the student's topic in 15 words or less. If no, answer with "no", and give your reason in 15 words or less.
<sentence>: {sentence}
<tracker>: {history}
<response>: {profile}

"""


PROMPT_HANDLE_STUDENT_BEHAVIOR = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Based on the student's response and <status>, think about the student's reponse. What is the student's concern, and how can you address the student's concern?

Follow your thought and the given <strategy> and talk to the student.You can use toulmin's model to help explain your reasoning, but make sure not to mention toulmin's model and use languages that a layman will understand.
Remember to focus on the topic of conversation and try not to be convinced by the student. Limit your response to less than or equal to 40 words.
<sentence>: {sentence}
<status>: {history}
<strategy>: {profile}

"""

PROMPT_REMIND_FOCUSED = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. A <summary> concludes your previous talks.
The student is talking about other things not related to the topic of the conversation. Ignore the student's reponse and remind the student of the topic of conversation. Limit your response to less than or equal to 40 words.

<sentence>: {sentence}
<summary>: {history}
"""