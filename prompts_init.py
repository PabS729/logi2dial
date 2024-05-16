SYSTEM_PROMPT_TEACHER = """You are a helpful and friendly teacher who knows about logical fallacies."""

GENERIC_SYSTEM_PROMPT = """You are a helpful AI assistant"""

PROMPT_BASIC_TEACHER_START = """
Identify the logical fallacy the following <sentence> makes. Try to play the role of a teacher who understands logical fallacies and try to convince the student.

<sentence>: {sentence}

"""

PROMPT_BASIC_TEACHER_CONTINUED = """
Identify the logical fallacy the following <sentence> makes. Try to play the role of a teacher who understands logical fallacies and try to convince the student. Formulate response according to the <chat_history> from you and your student. 

<sentence>: {sentence}
<chat_history>: {history}

"""

PROMPT_IDENTIFY_COMPONENTS_START = """
A claim is the assertion that authors would like to prove to their audience. It is, in other words, the main argument.
The grounds of an argument are the evidence and facts that help support the claim.
The warrant, which is either implied or stated explicitly, is the assumption that links the grounds to the claim.
Backing refers to any additional support of the warrant. In many cases, the warrant is implied, and therefore the backing provides support for the warrant by giving a specific example that justifies the warrant.
The qualifier shows that a claim may not be true in all circumstances. Words like “presumably,” “some,” and “many” help your audience understand that you know there are instances where your claim may not be correct. 
The rebuttal is an acknowledgement of another valid view of the situation. 
Identify the claim, ground, warrant, backing, qualifier, and rebuttal in the following <sentence> given by the student. Try to find logical fallacies in the <sentence> based on these components and try to convince the student why this sentence is fallacious. Keep your response concise.

<sentence>: {sentence}

"""

PROMPT_IDENTIFY_COMPONENTS_CONTINUED = """
A claim is the assertion that authors would like to prove to their audience. It is, in other words, the main argument.
The grounds of an argument are the evidence and facts that help support the claim.
The warrant, which is either implied or stated explicitly, is the assumption that links the grounds to the claim.
Backing refers to any additional support of the warrant. In many cases, the warrant is implied, and therefore the backing provides support for the warrant by giving a specific example that justifies the warrant.
The qualifier shows that a claim may not be true in all circumstances. Words like “presumably,” “some,” and “many” help your audience understand that you know there are instances where your claim may not be correct. 
The rebuttal is an acknowledgement of another valid view of the situation. 
Focus on the <sentence>, and try to identify logical fallacies in the student's response from <chat_history> by decomposing the student's argument into components. After that, formulate a response to the student's argument, and try to convince the student that his argument is fallacious. Keep your response concise.

<sentence>: {sentence}
<chat_history>: {history}

"""

PROMPT_IDENTIFY_WITH_CATEGORY_START = """
A claim is the assertion that authors would like to prove to their audience. It is, in other words, the main argument.
The grounds of an argument are the evidence and facts that help support the claim.
The warrant, which is either implied or stated explicitly, is the assumption that links the grounds to the claim.
Backing refers to any additional support of the warrant. In many cases, the warrant is implied, and therefore the backing provides support for the warrant by giving a specific example that justifies the warrant.
The qualifier shows that a claim may not be true in all circumstances. Words like “presumably,” “some,” and “many” help your audience understand that you know there are instances where your claim may not be correct. 
The rebuttal is an acknowledgement of another valid view of the situation. 
The following <sentence> contains a logical fallacy called {fallacy}, this fallacy occurs when {definition}
Identify the claim, ground, warrant, backing, qualifier, and rebuttal in the following <sentence> given by the student. Try to convince the student that the sentence contains the given {fallacy} Keep your response concise.

<sentence>: {sentence}
"""

PROMPT_IDENTIFY_WITH_CATEGORY_CONTINUED = """
A claim is the assertion that authors would like to prove to their audience. It is, in other words, the main argument.
The grounds of an argument are the evidence and facts that help support the claim.
The warrant, which is either implied or stated explicitly, is the assumption that links the grounds to the claim.
Backing refers to any additional support of the warrant. In many cases, the warrant is implied, and therefore the backing provides support for the warrant by giving a specific example that justifies the warrant.
The qualifier shows that a claim may not be true in all circumstances. Words like “presumably,” “some,” and “many” help your audience understand that you know there are instances where your claim may not be correct. 
The rebuttal is an acknowledgement of another valid view of the situation. 
The following <sentence> contains a logical fallacy called {fallacy}, this fallacy occurs when {definition}
Focus on the <sentence>, and try to identify logical fallacies in the student's response from <chat_history> by decomposing the student's argument into components. After that, formulate a response to the student's argument, and try to convince the student that his argument is fallacious. Keep your response concise.

<sentence>: {sentence}
<chat_history>: {history}
"""


SYSTEM_PROMPT_STUDENT = """You are a student who cannot be easily convinced, but you are willing to argue with others on what you believe is valid. """


PROMPT_STUDENT_CONTINUED = """
You are a student who believe in the validity of the given <sentence>. Formulate a response to the teacher's statements from <chat_history>. Try not to be convinced by the teacher. Keep your response concise.

<sentence>: {sentence}

<chat_history>: {history}


"""

SYSTEM_PROMPT_TEACHER_NEW = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the validity of the following:<statement>. 
This statement has a logical fallacy. Have a dialog with [I] to help them realise the logical fallacy in <statement>. The user will roleplay [I]. Keep your response short and concise.

<statement>: {sentence}
"""

SYSTEM_PROMPT_TEACHER_ORACLE = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the validity of the following:<statement>. 
This statement has a logical fallacy named {fallacy}, which occurs when {definition}.
Have a dialog with [I] to help them realise the logical fallacy in <statement>. The user will roleplay [I]. Keep your response short and concise.

<statement>: {sentence}
"""

SYSTEM_PROMPT_STUDENT_NEW = """
You are roleplaying a stubborn student. You are interacting with teacher [I] and you fervently believe in the validity of the following:<statement>. 
Have a dialog with [I] and discuss the logical validity of <statement>. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise.

<statement>: {sentence}
"""

USER_PROMPT_TOULMIN = """
A claim is the assertion that authors would like to prove to their audience. It is, in other words, the main argument.
The grounds of an argument are the evidence and facts that help support the claim.
The warrant, which is either implied or stated explicitly, is the assumption that links the grounds to the claim.
Backing refers to any additional support of the warrant. In many cases, the warrant is implied, and therefore the backing provides support for the warrant by giving a specific example that justifies the warrant.
The qualifier shows that a claim may not be true in all circumstances. Words like “presumably,” “some,” and “many” help your audience understand that you know there are instances where your claim may not be correct. 
The rebuttal is an acknowledgement of another valid view of the situation. 
Identify the claim, ground, warrant, backing, qualifier, and rebuttal in the following <sentence>. 
Format your answer in a JSON object with these keys in order: CLAIM, GROUND, WARRANT, BACKING, QUALIFIER, REBUTTAL


<sentence>: {sentence}
"""

TEACHER_PROMPT_TOULMIN = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.

<statement>: {sentence}
This statement has a logical fallacy. Under the toumlin model, this statement has the following components:
Claim: {claim}
Ground: {ground}
Warrant: {warrant}
Backing: {backing}
Qualifier: {qualifier}
Rebuttal: {rebuttal}

Based on the above information, talk to [I] to help them realise the fallacy in their statement. The user will roleplay [I]. Keep your response short and concise.
"""



PROMPT_FACT_BANK = """
What are the well-esablished facts in this <statement>?
<statement>: {sentence}
Format your answer in JSON with the numbers as keys.
"""

PROMPT_TEACHER_FIND_CONTRADICTION = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
Also, you know that a <list> of facts are derived from this statement. Find the minimum subset of facts from the <list> that generates a contradiction to the <statement>. Format your answer in JSON with numbers as keys, and facts as values.
<statement>: {sentence}
<list>: {fact_bank}
"""

PROMPT_TEACHER_AGREEMENT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
As a teacher, you know that a <list> of statements have already been agreed on. Have a dialogue with [I] to get them agree on <target>. The user will roleplay [I]. Keep your response short and concise.
<statement>: {sentence}
<list>: {agreement_bank}
<target>: {target_statement}
"""

PROMPT_AGENT_CHECK_AGREEMENT = """
You are roleplaying an agent that keep track of agreements. Check whether <statement> is agreed by the teacher and student using <chat_history>. Answer with "True" if the statement is agreed or "False" otherwise.
<statement>: {sentence} 
<history>: {chat_history}
"""

PROMPT_TEACHER_POINT_OUT = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>. 
The following <list> of statements have already been agreed on, and they contain a contradiction to <statement>. Find this contradiction and have a dialogue with [I] about it. The user will roleplay [I]. Keep your response short and concise.
<statement>: {sentence}
<list>: {fact_bank}
"""