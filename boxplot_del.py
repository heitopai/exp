import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("deletion_result_LCT\\sparse\\log50.txt.csv")

df_melted = df.melt(value_vars=["avg_dynamic_time", "avg_re_matroid_time", "avg_re_edmonds_time"],
                    var_name="Algorithm",
                    value_name="Time")


plt.figure(figsize=(10,6))
sns.boxplot(x="Algorithm", y="Time", data=df_melted)

plt.title("Comparison of Algorithm Running Times")
plt.ylabel("Time (seconds, log scale)")
plt.xlabel("")
plt.grid(True, axis='y', linestyle='--')
plt.show()
