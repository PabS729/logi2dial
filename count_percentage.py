import pandas as pd
import random
import math
fi = pd.read_excel("okk_all_gpt.xlsx", index_col=None)
# from sklearn.utils import shuffle


fks = []
kdd = [k for k in fi.keys() if k not in ["sentences", "chats"]]


fi_1 = fi.drop_duplicates(["sentences"])
print(len(fi_1["sentences"]))
fi2 = pd.read_excel("classification_results/okk_all_new_2.xlsx")
# comb = pd.concat([fi_1, fi2], axis=0)
comb = fi
# comb.replace(to_replace=r'yes*|Yes*',
#            value="yes")
# comb.replace()
# print(comb)
# comb.to_excel("all_talk_ds.xlsx")
for k in kdd:
    # comb[k] = comb[k].str.replace(r'yes*|Yes*', "yes")
    # comb[k] = comb[k].str.replace(r'no*|No*', "no")
    fks.append(comb[k].values.tolist())
# print(comb)
# ln = [k for k in fi.keys()]
st_note_yes = {}
st_note_no = {}
for k in kdd:
    st_note_yes[k] = []
    st_note_no[k] = []
print(len(comb))
for (ar, k) in zip(fks, kdd):
    print(k)
    yes = 0
    no = 0
    # print(ar)
    ct = 0
    for j,st in zip(ar, comb["sentences"]):
        # print(j)
        # print(ct)
        left = str(j).lower().split("the answer should be")
        # print(left)
        if len(left) > 1 and "yes" in left[1]:
            yes+=1
            st_note_yes[k].append(st)
        elif "yes" in left:
            yes+=1
            st_note_yes[k].append(st)
        else:
            no+=1
            st_note_no[k].append(st)
        ct+=1
    
    print(yes, no)
    print(len(st_note_yes[k]),len(st_note_no[k]))

for k in kdd:
    random.seed(20)
    if k in ["perspective", "activeness"]:
        continue
    # rd_yes = random.sample(st_note_yes[k], 15)
    # rd_no = random.sample(st_note_no[k], 15)
    # nl_yes = comb.query("sentences == @rd_yes and ")
    # nl_no = comb.query("sentences == @rd_no"
    nl_yes = comb[comb[k] == "yes"].sample(n=15, random_state = 10)
    nl_no = comb[comb[k] == "no"].sample(n=15, random_state = 10)

    comab = pd.concat([nl_yes, nl_no], axis=0)
    # comab.filter(["sentences", "chats", k]).to_excel("res_"+k+".xlsx")
    shuf = comab.filter(["sentences", "chats"]).sample(frac=1)

    shuf.to_excel("shuf_gpt_" + k + ".xlsx")



# print(st_note_yes[k][:30])
    
