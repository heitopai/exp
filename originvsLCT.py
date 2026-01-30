import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14
})

# dataset = "sparse"
dataset = "dense"
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

vertices=pd.read_csv(files[0])["vertices"]

all_matroid_time = []
all_edmonds_time = []
all_matroidLCT_time = []
for f in files:
    df=pd.read_csv(f)
    all_matroid_time.append(df["avg_matroid_time"].to_numpy())
    all_edmonds_time.append(df["avg_edmonds_time"].to_numpy())

for f1 in files1:
    df1=pd.read_csv(f1)    
    all_matroidLCT_time.append(df1["avg_matroid_time"].to_numpy())

avg_matroid_time = np.mean(all_matroid_time, axis=0)
avg_edmonds_time = np.mean(all_edmonds_time, axis=0)
avg_matroidLCT_time = np.mean(all_matroidLCT_time, axis=0)

print(avg_edmonds_time)

plt.figure()

plt.plot(vertices, avg_matroid_time, 'o-', label="Matroid", color='k')  
plt.plot(vertices, avg_edmonds_time, '^:', label="Edmonds", color='k')  
plt.plot(vertices, avg_matroidLCT_time, 's--', label="Matroid_LCT", color='k') 

plt.xlabel("vertices")
plt.ylabel("time (sec)")
# plt.title('Comparison of Two Groups')
plt.legend() 

plt.savefig(f"originvsLCT.pdf")

plt.show()