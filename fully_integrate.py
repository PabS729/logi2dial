import pandas as pd


# dffs = []
# for i in range(50, 250, 50):
#     fname = "chat_history_results/bsc_0222_base_2_"+str(i)+"_o.xlsx"
#     fn_2 = "eval_results/classify_bs_2_"+str(i)+"_o3_added0.xlsx"
#     df = pd.read_excel(fname)
#     df_2 = pd.read_excel(fn_2)
#     df = pd.concat([df, df_2], axis = 1)
#     dffs.append(df)

# new_df = pd.concat(dffs, axis=0)
# new_df.to_excel("okk_all_2.xlsx")

dffs = []
for i in range(50, 250, 50):
    fname = "eval_results/classify_bs_4_"+str(i)+"_o3_added0.xlsx"
    df = pd.read_excel(fname)
    dffs.append(df)

new_df = pd.concat(dffs, axis=0)

nf = new_df.to_excel("okk4.xlsx")