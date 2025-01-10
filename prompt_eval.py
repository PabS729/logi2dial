EVAL_COHERENCE = """
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Coherence.
Definition of Coherence: The dialogues overall are logically connected with each other. For a single dialogue, all of the speakers’ responses must connect with each other and form a complete chain of logic. 
Read each dialogue carefully. After reading both dialogues, choose which dialogue is better in terms of the criteria here. Answer with "1" if you think dialogue 1 is better, and "2" if you think dialogue 2 is better.
If you think the dialogues are equally competent in this criteria, then answer with "0".

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}
"""

EVAL_CONSISTENCY = """
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Relevance.
Definition of Relevance: The speaker's responses should always stay on topic regarding the sentence of interest. There should not be anything unrelated to the discussion of logical validity of sentence. 
Read each dialogue carefully. After reading both dialogues, choose which dialogue is better in terms of the criteria here. 
Answer with "1" if you think dialogue 1 is better, and "2" if you think dialogue 2 is better. If you think the dialogues are equally competent in this criteria, then answer with "0".

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}
"""

EVAL_INFORMATION_DIV = """
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Informativeness. 
Definition of Informativeness: Measures how much useful information are introduced by the teacher. Look for responses with examples derived from the original statement. These examples must facilitate further discussion of the sentence, or clearly support or counter any kind of arguments.
Read each dialogue carefully. After reading both dialogues, choose which dialogue you think is more informative. 
Answer with "1" if you think dialogue 1 is better, and "2" if you think dialogue 2 is better. If you think the dialogues are equally competent in this criteria, then answer with "0".

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}
"""

EVAL_VALID_ARGUMENTS = """
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Argumentativeness.
Definition of Argumentativeness: Counts the number of times a student proposes counterarguments, and how the teacher responds to counterarguments. A valid exchange happens when the student’s counterargument in the previous round is responded to by the teacher in the current round.
Read each dialogue carefully. After reading both dialogues, choose which dialogue has more valid arguments exchanged. 
Answer with "1" if you think dialogue 1 is better, and "2" if you think dialogue 2 is better. If you think the dialogues are equally competent in this criteria, then answer with "0".

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}
"""

EVAL_HELPFULNESS = """
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Helpfulness.
Definition of Helpfulness: Imagine you are a user of the Logical Fallacy support tool, which help you decide whether the given sentence has a logical fallacy, do you find the conversation helpful for your understanding of the logical validity for the given sentence? 
Read each dialogue carefully. After reading both dialogues, choose which dialogue is better in terms of the criteria here. 
Answer with "1" if you think dialogue 1 is better, and "2" if you think dialogue 2 is better. If you think the dialogues are equally competent in this criteria, then answer with "0".

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}
"""