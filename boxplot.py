import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

# folder = "result\\sparse"
folder = "result_LCT\\sparse"

files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.endswith(".csv")
]

print(files)

df = pd.concat(
    [pd.read_csv(f) for f in files],
    ignore_index=True
)

print(df)

# df = pd.read_csv("result_LCT\\sparse\\log30.txt.csv")

df_melted = df.melt(
    value_vars=["avg_edmonds_time", "avg_matroid_time"],
    var_name="Algorithm",
    value_name="Time"
)


plt.figure(figsize=(10, 6))

sns.boxplot(
    x="Algorithm",
    y="Time",
    data=df_melted
)
plt.title("Running Time Distribution (Boxplot)")
plt.ylabel("Time (seconds)")
plt.xlabel("")
plt.grid(True, axis="y", linestyle='--')

plt.show()
