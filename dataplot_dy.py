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

dataset = "sparse"
# dataset = "dense"
# dataset = "cliques"

# folder = f"insertion_result\\{dataset}"
folder = f"deletion_result\\{dataset}"

files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.endswith(".csv")
]

print(files)

vertices=pd.read_csv(files[0])["vertices"]

all_static_time = []
all_dynamic_time = []
for f in files:
    df=pd.read_csv(f)
    all_static_time.append(df["avg_re_matroid_time"].to_numpy())
    all_dynamic_time.append(df["avg_dynamic_time"].to_numpy())


avg_static_time = np.mean(all_static_time, axis=0)
avg_dynamic_time = np.mean(all_dynamic_time, axis=0)
print(avg_dynamic_time)

plt.figure()

plt.plot(vertices, avg_static_time, 'o-', label="static", color='k')  
plt.plot(vertices, avg_dynamic_time, '^--', label="dynamic", color='k')  

plt.xlabel("vertices")
plt.ylabel("time (sec)")
# plt.title('Comparison of Two Groups')
plt.legend() 

plt.savefig(folder+f"\\{dataset}.pdf")

plt.show()

# gain plot
plt.figure()

plt.plot(vertices, (avg_static_time - avg_dynamic_time) / avg_static_time, 'o-', color='k')  

plt.xlabel("vertices")
plt.ylabel("Time Gain")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

plt.savefig(folder+f"\\{dataset}_gain.pdf")

plt.show()