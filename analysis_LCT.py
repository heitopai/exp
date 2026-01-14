import re
import pandas as pd

import os
current_path = os.path.dirname(os.path.abspath(__file__))

# 数据集
dataset="dense"
# dataset="sparse"
# dataset="cliques"

# 获取该类数据集下的所有数据文件夹
directory = current_path + '\\result_LCT\\'  + dataset
all_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

for file in all_files:
    path=directory + '\\' + file

    # 定义正则表达式模式
    patterns = {
        "timestamp": re.compile(r"本次运行时刻： (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"),
        "vertices": re.compile(rf'clique\d+_(\d+)|{dataset}(\d+)\.txt'),
        "greedy": re.compile(r"贪心算法求初始有向生成树的权值 (\d+)"),
        "iterations": re.compile(r"迭代次数： (\d+)"),
        "matroid_time": re.compile(r"基于拟阵交算法的DMST的求解时间： ([\d\.]+)"),
        "matroid": re.compile(r"基于拟阵交算法求DMST的权重和： (\d+)"),
        "edmonds_time": re.compile(r"Networkx中基于Edmonds算法的DMST求解时间： ([\d\.]+)"),
        "edmonds": re.compile(r"Edmonds算法求DMST的权重和： (\d+)")
    }

    # 读取日志文件
    with open(path, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # 提取信息
    results = []
    current_run = {}
    current_data={}
    for line in log_content.splitlines():
        for key, pattern in patterns.items():
            match = pattern.search(line)
            if match:
                if key == "timestamp":
                    results.append(current_run)
                    current_run = {"timestamp": match.group(1), "data": []}
                elif key=="vertices":
                    with open(line,'r') as f:
                        num_vertices,num_edges,root=map(int,f.readline().strip().split())
                        if dataset == "cliques":
                            current_data[key]=match.group(1)
                        else:
                            current_data[key]=num_vertices
                        current_data["edges"]=num_edges
                else:
                    current_data[key]=match.group(1)

        if "edmonds" in current_data:
            current_run["data"].append(current_data)
            current_data = {}
    results.append(current_run)

    # print(results)
    print(len(results))

    # 将结果转换为DataFrame
    df_save = pd.DataFrame(results[1]["data"])

    # 运行时间求平均值
    all_matroid_time = []
    all_edmonds_time = []

   
    for run in results:
        if len(run)>0:
            df = pd.DataFrame(run["data"])
            # print(df["matroid_time"].astype(float))
            all_matroid_time.append(df["matroid_time"].astype(float).tolist())
            all_edmonds_time.append(df["edmonds_time"].astype(float).tolist())

    import numpy as np
    all_edmonds_time = np.array(all_edmonds_time)
    avg_edmonds_time = np.mean(all_edmonds_time, axis=0)
    df_save["avg_edmonds_time"]=np.round(avg_edmonds_time,3)

    all_matroid_time = np.array(all_matroid_time)
    avg_matroid_time = np.mean(all_matroid_time, axis=0)
    df_save["avg_matroid_time"]=np.round(avg_matroid_time,3)



    df_save.drop("matroid_time", axis=1, inplace=True)
    df_save.drop("edmonds_time", axis=1, inplace=True)
    df_save["vertices"]=df["vertices"].astype(int)
    df_save.sort_values(by="vertices",inplace=True)
    df_save.to_csv(path+".csv", index=False)


    # import matplotlib.pyplot as plt

    # plt.figure()

    # # 绘制两组数据的散点图
    # plt.scatter(df_save["vertices"], df_save["avg_matroid_time"], color='blue', label="avg_matroid_time")  # 第一组数据，蓝色
    # plt.scatter(df_save["vertices"], df_save["avg_edmonds_time"], color='red', label="avg_edmonds_time")   # 第二组数据，红色

    # # 设置标签和标题
    # plt.xlabel("vertices")
    # plt.ylabel("time (sec)")
    # # plt.title('Comparison of Two Groups')
    # plt.legend()  # 显示图例

    # plt.savefig(path+".png")

