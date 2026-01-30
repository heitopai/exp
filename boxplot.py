import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14
})

dataset = "sparse"
# dataset = "dense"
# dataset = "cliques"

folder = f"result\\{dataset}"

files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.endswith(".csv")
]

folder1 = f"result_LCT\\{dataset}"

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

df1.rename(columns={'avg_matroid_time': 'matroid_LCT_time'}, inplace=True)

df = pd.concat([df, df1['matroid_LCT_time']], axis=1)

df.rename(columns={'avg_matroid_time': 'matroid_time', 'avg_edmonds_time': 'edmonds_time'}, inplace=True)

print(df)


df_melted = df.melt(
    value_vars=["edmonds_time", "matroid_time"],
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


os.makedirs("figures1\\static", exist_ok=True)
plt.savefig(f"figures1\\static\\{dataset}.pdf")

plt.show()