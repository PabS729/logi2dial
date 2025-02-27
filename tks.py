import pandas as pd

reads = pd.read_excel("all_talk.xlsx")


ks = [k for k in reads.keys() if (k not in ["sentences","chats"]) ]

for j in ks:
    print(j)
    fn = "shuf_lab_new_" + str(j) + ".xlsx"
    print(fn)
    new_r = pd.read_excel(fn)
    # new_r_d = new_r[""]
    sts = new_r["chats"].values.tolist()
    small_k = []
    for s in sts:
        filt_s = reads[reads["chats"] == s]
        small_k.append(filt_s)
    smk = pd.concat(small_k)
    smk.to_excel("ks_" + j + ".xlsx")
