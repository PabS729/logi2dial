PROMPT_FACT_BANK = """
List the explicit and implicit facts in this <statement>. Combine them into a single list.
<statement>: {sentence}
Format your answer in JSON with the numbers as keys.
"""

PROMPT_TEACHER_FIND_CONTRADICTION = """
You are roleplaying a rational teacher. You are interacting with student [I] who believes in the following <statement>.
A <list> of facts are derived from this statement. Find the minimum subset of facts from the <list> that generates a contradiction to the <statement>. Answer with a list of facts selected from <list>. Format your answer in JSON with numbers as keys.
<statement>: {sentence}
<list>: {counter}
"""

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

PROMPT_TEACHER_PERSUASION = """
You are roleplaying a rational teacher. You are interacting with student [I] who is stubborn but rational. 
Keep in mind that <target> is a fact. Think about how to convince [I], and talk to [I] to get them agree that <target> is a fact. The user will roleplay [I]. Keep your response direct, short and concise.
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

SYSTEM_PROMPT_STUDENT_RATIONAL_SOMEWHAT = """
You are roleplaying a stubborn student, and you fervently believe in the validity of the following:<statement>. You are willing to rationally argue with the teacher over his/her statements. You also agree to all statements in <agreement_bank> 
Follow the teacher's guidance and reply to teacher [I]. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise.

<statement>: {sentence}
<agreement_bank>: {agreement_bank}
"""

SYSTEM_PROMPT_STUDENT_RATIONAL = """
You are roleplaying a stubborn student, and you fervently believe in the validity of the following:<statement>. However, you are rational in determining whether the teacher's statement is reasonable. You also agree to all statements in <agreement_bank> 
Follow the teacher's guidance and reply to teacher [I]. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise.

<statement>: {sentence}
<agreement_bank>: {agreement_bank}
"""

SYSTEM_PROMPT_STUDENT_DISCUSS = """
You are roleplaying a stubborn student, and you fervently believe in the validity of the following:<statement>. However, you are rational and willing to discuss with the teacher's statements. You also agree to all statements in <agreement_bank> 
Follow the teacher's guidance and reply to teacher [I]. The user will roleplay [I]. Try not to be convinced by the teacher. Keep your response short and concise. Respond directly to the teacher's question. Do NOT repeat or paraphrase <statement>.

<statement>: {sentence}
<agreement_bank>: {agreement_bank}
"""

PROMPT_AGENT_CHECK_RESPONSE = """
You are roleplaying a language expert. Check whether the student in the following <response> is repeating or paraphrasing the <statement>. Answer with "Yes" or "No".
<response>: {chat_history}
<statement>: {sentence}

"""

PROMPT_CIRCULAR_REASONING = """
Below is an <argument> with circular reasoning fallacy. Think about the following questions. 
Q1: What should hold true for the premise to be true?
q2: What should hold true for the conclusion to be true?

Answer with the template: for <replace with premise/conclusion of argument> to be true. It must hold that <your answer>.
Format your answer in JSON with the following keys: "1": <answer to Q1>. "2": <answer to Q2>.
<argument>: {sentence}


"""

PROMPT_COUNTEREXAMPLE = """
Below is an <argument> with a logical fallacy. Think about the given <strategy> to counter this argument and state a counterexample of the argument. Answer with the counterexample. 
<argument>: {sentence}
<strategy>: {counter}

Format your answer in JSON with the following key: "1": <counterexample>
"""

PROMPT_ALT_COUNTEREXAMPLE = """
Below is an <argument> with a logical fallacy. Think about the given <strategy> to counter this argument and state a counterexample of the argument that is different from <counterstatement>. Answer with the counterexample. 
<argument>: {sentence}
<strategy>: {agreement_bank}
<counterstatemente>: {target_statement}

"""

PROMPT_BREAKDOWN = """
Premises: Proposition used as evidence in an argument.
Conclusion: Logical result of the relationship between the premises. Conclusions serve as the thesis of the argument.

Find the premises and conclusion in the following <statement>. Paraphrase if necessary. Format your answer in JSON with keys: "1": <premise>. "2": <conclusion>.
<statement>: {sentence}
"""

#Good for now. 
SYSTEM_CLASSIFY_FALLACY = """
What logical fallacy does the following <sentence> have? 
Select from these categories: ad hominem, ad populum, circular reasoning, faulty generalization, false causality, strawman fallacy, slippery slope, fallacy of relevance, appeal to authority, appeal to emotion, false dilemma, equivocation, fallacy of logic
<sentence>: {sentence}
Format your answer in JSON with the following key: "1": <type_of_logical_fallacy>
"""

#"Select from these categories: ad hominem, ad populum, circular reasoning, faulty generalization, false causality, strawman fallacy, fallacy of relevance, appeal to authority, appeal to emotion, false dilemma, equivocation, fallacy of logic"
#Not so good for a pure classification task
SYSTEM_CHECK = """
The logical fallacy {fallacy} occurs when {definition}. Is the following <sentence> an example of such fallacy?
<sentence>: {sentence}
Answer with "Yes" or "No". Format your answer in JSON with the following key: "1": <your_answer>
"""

SYSTEM_PROMPT_ALT_STRATEGY = """
You are roleplaying a rational teacher. You are interacting with a stubborn student [I] who believes in the following <statement>. 

<statement>: {sentence}

There are some alternative strategies for getting agreements: asking open-ended questions, discussing possible scenarios, using analogies. 
Respond to the student. Using any of the above strategies to get the student to agree with <component>, without directly asking if the student agrees with <component>. Keep your response short and concise.

<component>: {target_statement}
"""

SYSTEM_PROMPT_CHECK_SUFFICIENCY = """
Do you think the teacher's argument is sufficient to disprove the <statement>? 

teacher's argument: {counterexample}

<statement>: {sentence}

First think carefully, then answer with "Yes" or "No".
"""

AGENT_CHECK_COUNTEREXAMPLE = """
1. Does the premise and conclusion from the <counterexample> relate to the topic of <argument>?


<argument>:{sentence}
<counterexample>: {example}

If yes, then is the <counterexample> sufficient enough to refute <argument>? It is sufficient if any of the following holds: 

1. The counterexample argues that some of the premises from <argument> are dubious or even false. 
2. The counterexample argues that the conclusion from <argument> leads to absurd results
3. The counterexample show that conclusion does not follow the premise.
4. The counterexample show that the premise is not strong enough to support the conclusion.

Answer with ONLY "Yes" or "No". Format your answer in JSON with the following key: "1": <your_answer>
"""

SYSTEM_FORCE_AGREEMENT = """
You are a student who stubbornly believe in <statement>. However, you are convinced by the teacher on <target>. Agree to the teacher's words.

<statement>: {sentence}
<target>: {target_statement}
"""

SYSTEM_RATE_RESPONSE_AGENT_RELEVANCE = """
1. Does the teacher's <response> include asking for agreement over the <sentence>?

<sentence>: {sentence}

Answer with "1" if "Yes" or "0" if "No". Format your answer in JSON with the following keys: "1": <YOUR_ANSWER>

"""

SYSTEM_RATE_RESPONSE_AGENT_MULTI = """

Q1. As a misinformation believer who believes in <sentence>, do you find the teacher’s <response> convincing?
Q2. The <response> is cogent if it has acceptable premises that are relevant to its conclusion and that are sufficient to draw the conclusion. Is the response cogent?
Q3. The <response> is effective if it persuades the target audience of (or corroborates agreement with) the teacher’s stance on the issue. Is the response effective?
Q4. The <response> is sufficient if it gives enough support to make it rational to draw its conclusion. Is the response sufficient?

<sentence>:{sentence}
<response>: {example}

Answer with "1" if "Yes" or "0" if "No". Format your answer in JSON with the following keys: "1": <answer to Q1>, "2": <answer to Q2>, "3": <answer to Q3>, "4":, <answer to Q4>
"""