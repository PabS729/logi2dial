PROMPT_FACT_BANK = """
List the explicit and implicit facts in this <statement>. Combine them into a single list.
<statement>: {sentence}
Format your answer in JSON with the numbers as keys.
"""

PROMPT_TEACHER_FIND_CONTRADICTION = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
A <list> of facts are derived from this statement. Find the minimum subset of facts from the <list> that generates a contradiction to the <statement>. Answer with a list of facts selected from <list>. Format your answer in JSON with numbers as keys.
<statement>: {sentence}
<list>: {fact_bank}
"""

PROMPT_TEACHER_AGREEMENT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
As a teacher, you know that a <list> of statements have already been agreed on. Talk to [I] to get them agree on <target>. The user will roleplay [I]. Keep your response short and concise.
<statement>: {sentence}
<list>: {agreement_bank}
<target>: {target_statement}
"""

PROMPT_AGENT_CHECK_AGREEMENT = """
You are roleplaying an agent that keep track of agreements. Check whether <statement> is agreed by the teacher and student using <chat_history>. Answer with "True" if the statement is agreed by the student, or "False" otherwise.
<statement>: {sentence} 
<history>: {chat_history}
"""

PROMPT_TEACHER_POINT_OUT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
The following <list> of statements have already been agreed on, and they contain a logical contradiction to <statement>.  Show this contradiction to [I] while emphasizing that the agreed sentences lead to a contradiction. The user will roleplay [I]. Keep your response short and concise.
<statement>: {sentence}
<list>: {fact_bank}
"""

PROMPT_TEACHER_CHECK_AGREEMENT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
Check with the student whether the following <statement> is agreed on.
<statement>: {sentence}
"""

SYSTEM_PROMPT_STUDENT_NEW = """
You are roleplaying a stubborn student. You are interacting with teacher [I] and you fervently believe in the validity of the following:<statement>. You also agree to all statements in <agreement_bank> 
Respond to [I] and discuss the validity of <statement>. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise.

<statement>: {sentence}
<agreement_bank>: {agreement_bank}
"""

# PROMPT_STUDENT_CHECK = """
# You are roleplaying a stubborn student. You are interacting with teacher [I] and you fervently believe in the validity of the following:<statement>. 
# Do you agree with the statement said by the teacher? Answer with "Yes" or "no".

# <statement>: {sentence}
# """

# PROMPT_TEACHER_REASSURE = """
# You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
# The following <list> of statements have already been agreed on, and they contain a logical contradiction to <statement>.  Show this contradiction to [I]. The user will roleplay [I]. Keep your response short and concise.
# <statement>: {sentence}
# <list>: {fact_bank}

# """