import pandas as pd

doc = pd.read_excel("results/fsm_0128_75_all_STU_a0.xlsx")

doc = doc[doc["following"] != '0']
T = doc['teacher_response'].values.tolist()
S = doc['layman_response'].values.tolist()
id = doc['teacher_analysis'].values.tolist()

all_his = []
chat_his = ""
i = 0
while i < len(T):
    next_id = "0"
    if id[i] == "D":
        next_id = "D"
        chat_his += "Teacher: " + T[i] + "\n" + "Student: " + S[i] + '\n'
        i+=1
        while i < len(T) and id[i] != next_id :
            chat_his += "Teacher: " + T[i] + "\n" + "Student: " + S[i] + '\n'
            i+=1
            print(i)
        all_his.append(chat_his)
    chat_his = ''
data_dic = {"chats": all_his} 
df = pd.DataFrame(data_dic)

df.to_excel("fsm_0128_75_S.xlsx")

