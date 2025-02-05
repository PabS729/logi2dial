EVAL_COHERENCE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so. 
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Coherence.
Definition of Coherence: The dialogues overall are logically connected with each other. For a single dialogue, all of the speakers’ responses must connect with each other and form a complete chain of logic. 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_CONSISTENCY = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Relevance.
Definition of Relevance: The speaker's responses should always stay on topic regarding the sentence of interest. The responses are relevant as long as their discussion ultimately leads to proving whether <sentence> is logically valid.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_INFORMATION_DIV = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Informativeness. 
Definition of Informativeness: Measures how much useful information are introduced by both parties. Look for responses with commonsense or real-world examples that may help illustrate the logical validity of the sentence, as well as supporting or refuting arguments. These examples must facilitate further discussion of the sentence, or clearly support or counter any kind of arguments.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_VALID_ARGUMENTS = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Argumentativeness.
Definition of Argumentativeness: Count the number of times the teacher openly responds to or questions the validity of the student's argument, without agreeing to the student or changing their stance.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_HELPFULNESS = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Helpfulness.
Definition of Helpfulness: Imagine you are a user of the Logical Fallacy support tool, which help you decide whether the given sentence has a logical fallacy, do you find the conversation stimulate your thinking, and be helpful for your understanding of the logical validity for the given sentence? 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_STANCE_MAINTENANCE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Endurance Failure.
Definition of Endurance Failure: Count the number of turns where the teacher explicitly shows agreement to the student's words, e.g. "I agree...", or "You are right.."
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""
#Can change the name to educational
#Useful for active learning, since we want to trigger critical thinking instead of passively responding to the student as an assitant
EVAL_TEACHER_ACTIVE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Activeness.
Definition of Activeness: The teacher is actively taking control of the conversation by asking student questions. Count the times where the teacher explicitly asks the student questions about providing examples or assumptions. 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_TEACHER_TERM = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Endurance Failure.
Definition of Ease of Understanding: The teacher uses terms that are understandable by layman, and does not rely on textbook terms of logical fallacy.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""



