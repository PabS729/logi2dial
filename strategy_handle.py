STRATEGY_HANDLE_STUDENT = {
    "1":"Address the student's concern and remind the student of the topic of conversation",#concerned
    "2": "Talk about the point of disagreement and try to reach an agreement", #disagreement
    "3": "Refute the student's argument by pointing out the student's logical flaw, or giving a real-world counterexample", #rebuttal
    "4": "Remind the student of the topic of conversation (about toulmin's model)", #drawing attention away
    "5": "Clarify your explanation according to the student's question. Be sure to stick to the topic of conversation about toulmin's model", #Clarification
    "6": "Carry on the conversation.",
    "7": "Remind the student of the topic of conversation, and ask the student to stop repeating", #repetition
    "D": "Using Toulmin's model, point out the logical flaw in the given statement. Be sure to explain why." #start of conversation, so initial state is null
}

indicator = {
"1":"The student is concerned about the teacher's response.",
"2":"The student disagrees with the teacher's response.",
"3":"The student rebuts the teacher's response.",
"4":"The student is drawing away attention from the topic of the conversation.",
"5": "The student asks for clarification from the teacher.",
"6": "Carry on the conversation.",
"7":"The student is repeating their previous response.",

"D": "" #start of conversation, , so initial state is null
}

toulmin_relationships = {
    "Ad Hominem": "the warrant is logically invalid.",
    "False Cause": "The warrant is logically invalid.",
    "Appeal to Emotion": "The claim and grounds are unrelated to each other.",
    "Appeal to Authority": "The warrant that words said by someone famous must be true is logically incorrect.",
    "Slippery Slope": "The warrant that the chain of actions must happen one after the other is wrong",
    "Slogan": "Claim without grounds."

}