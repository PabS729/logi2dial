PROMPT_FACT_BANK = """
List the explicit and implicit facts in this <statement>. Combine them into a single list.
<statement>: {sentence}
Format your answer in JSON with the numbers as keys.
"""

# PROMPT_TEACHER_FIND_CONTRADICTION = """
# You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
# A <list> of facts are derived from this statement. Find the minimum subset of facts from the <list> that generates a contradiction to the <statement>. Answer with a list of facts selected from <list>. Format your answer in JSON with numbers as keys.
# <statement>: {sentence}
# <list>: {fact_bank}
# """

PROMPT_IDENTIFY_CATEGORY = """
What logical fallacy does the following <statement> have? 

<statement>: {sentence}

Format your answer in JSON with key: "1": <type of fallacy commited>
"""

PROMPT_TEACHER_AGREEMENT = """
You are roleplaying a rational teacher. You are interacting with student [I]. 
Keep in mind that <target> is a fact. Talk to [I] to get them agree that <target> is a fact. The user will roleplay [I]. Keep your response short and concise.
<list>: {agreement_bank}
<target>: {target_statement}
"""

PROMPT_AGENT_CHECK_AGREEMENT = """
You are roleplaying an agent that keep track of agreements. Check whether the student agrees with <statement> using <chat_history>. Answer with "True" if the statement is agreed by the student, or "False" otherwise.
<statement>: {sentence} 
<history>: {chat_history}
"""

PROMPT_TEACHER_POINT_OUT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
The following <list> of statements have already been agreed on, and they contain a logical contradiction.  Show this contradiction to [I] while emphasizing that the agreed sentences lead to a contradiction. The user will roleplay [I]. Keep your response short and concise.
<statement>: {sentence}
<list>: {fact_bank}
"""

PROMPT_TEACHER_CHECK_AGREEMENT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
Check with the student whether the following <statement> is agreed on.
<statement>: {sentence}
"""

SYSTEM_PROMPT_STUDENT_NEW = """
You are roleplaying a stubborn student, and you fervently believe in the validity of the following:<statement>. You also agree to all statements in <agreement_bank> 
Follow the teacher's guidance and reply to teacher [I]. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise.

<statement>: {sentence}
<agreement_bank>: {agreement_bank}
"""

PROMPT_AGENT_CHECK_RESPONSE = """
You are roleplaying a language expert. Check whether the student in the following <response> is repeating or paraphrasing the <statement>. Answer with "Yes" or "No".
<response>: {chat_history}
<statement>: {sentence}

"""

PROMPT_COUNTEREXAMPLE = """
Below is an <argument> with a logical fallacy. Think about the given <strategy> to counter this argument and state a real-world counterexample of the argument. Answer with the counterexample. 
<argument>: {sentence}
<strategy>: {counter}

Format your answer in JSON with the following key: "1": <counterexample>
"""

PROMPT_BREAKDOWN = """
Premises: Proposition used as evidence in an argument.
Conclusion: Logical result of the relationship between the premises. Conclusions serve as the thesis of the argument.

Find the premises and conclusion in the following <statement>. Paraphrase if necessary. Format your answer in JSON with keys: "1": <premise>. "2": <conclusion>.
<statement>: {sentence}
"""