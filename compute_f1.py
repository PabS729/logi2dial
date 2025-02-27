import pandas as pd

reads = pd.read_excel("okk_all.xlsx")


ks = [k for k in reads.keys() if (k not in ["sentences","chats"]) ]

for j in ks:
    fn = "shuf_fin_" + j + ".xlsx"
    comp = pd.read_excel(fn)

    TP = len(comp[comp[j].str.contains("yes") and comp[j].str.contains("yes")])
    FP = len(comp["yes" in comp[j].lower() and "no" in comp["label"].lower()])
    TN = len(comp["no" in comp[j].lower() and "no" in comp["label"].lower()])
    FN = len(comp["no" in comp[j].lower() and "yes" in comp["label"].lower()])

    F1 = 2 * TP / (2 * TP + FP + FN) 
    print(j + " f1-score: " + str(F1))