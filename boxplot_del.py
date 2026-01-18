import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

# dataset = "sparse"
# dataset = "dense"
dataset = "cliques"

folder = f"deletion_result\\{dataset}"

files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.endswith(".csv")
]

folder1 = f"deletion_result_LCT\\{dataset}"

files1 = [
    os.path.join(folder1, f)
    for f in os.listdir(folder1)
    if f.endswith(".csv")
]

print(files)

df = pd.concat(
    [pd.read_csv(f) for f in files],
    ignore_index=True
)

df1 = pd.concat(
    [pd.read_csv(f) for f in files1],
    ignore_index=True
)

df1.rename(columns={'avg_re_matroid_time': 're_matroid_LCT_time', 'avg_dynamic_time': 'dynamic_LCT_time'}, inplace=True)

df = pd.concat([df, df1['re_matroid_LCT_time'], df1['dynamic_LCT_time']], axis=1)

df.rename(columns={'avg_dynamic_time': 'dynamic_time', 'avg_re_edmonds_time': 're_edmonds_time', 'avg_re_matroid_time': 're_matroid_time'}, inplace=True)

print(df)


df_melted = df.melt(
    value_vars=["dynamic_time", "dynamic_LCT_time" , "re_edmonds_time", "re_matroid_LCT_time", 're_matroid_time'],
    var_name="Algorithm",
    value_name="Time"
)

plt.figure(figsize=(10, 6))

sns.boxplot(
    x="Algorithm",
    y="Time",
    data=df_melted
)
# plt.title("Running Time Distribution (Boxplot)")
plt.ylabel("Time (seconds)")
plt.xlabel("")
plt.grid(True, axis="y", linestyle='--')


os.makedirs("figures\\deletion", exist_ok=True)
plt.savefig(f"figures\\deletion\\{dataset}.pdf")

plt.show()