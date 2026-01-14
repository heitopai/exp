import re
import pandas as pd

import os
current_path = os.path.dirname(os.path.abspath(__file__))

# 数据集
# dataset="dense"
# dataset="sparse"
dataset="cliques"


# 获取该类数据集下的所有数据文件夹
directory = current_path + '\\insertion_result_LCT\\'  + dataset
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
        "edmonds": re.compile(r"Edmonds算法求DMST的权重和： (\d+)"),
        "insertion_edge": re.compile(r"插入的边为： (\d+) (\d+) (\d+)"),
        "dynamic_time": re.compile(r"基于拟阵交的动态插入有向边的求解时间： ([\d\.]+)"),
        "dynamic": re.compile(r"基于拟阵交的动态插入有向边更新DMST后的权重和： (\d+)"),
        "re_matroid_time": re.compile(r"插入有向边后重新执行基于拟阵交算法的DMST的求解时间： ([\d\.]+)"),
        "re_matroid": re.compile(r"插入有向边后重新执行基于拟阵交算法的DMST的权重和： (\d+)"),
        "re_edmonds": re.compile(r"插入有向边后重新执行Edmonds算法求DMST的权重和： (\d+)"),
        "re_edmonds_time": re.compile(r"插入有向边后重新执行Networkx中基于Edmonds算法的DMST求解时间： ([\d\.]+)"),
    }

    search=["iterations","dynamic_time","dynamic","greedy","iterations","re_matroid","re_matroid_time","re_edmonds_time","re_edmonds"]
    search0=["greedy", "iterations","matroid_time","matroid","edmonds","edmonds_time"]

    # 读取日志文件
    with open(path, 'r', encoding='utf-8') as file:
        log_content = file.read()

    # # 提取信息
    # results = []
    # current_data={}
    # current_insertion_edge={}
    # for line in log_content.splitlines():
    #     for key, pattern in patterns.items():
    #         match = pattern.search(line)
    #         if match:
    #             if key == "timestamp":
    #                 break
    #             elif key=="vertices":
    #                 results.append(current_data)
    #                 current_data={}
    #                 with open(line,'r') as f:
    #                     num_vertices,num_edges,root=map(int,f.readline().strip().split())
    #                     current_data[key]=num_vertices
    #                     current_data["edges"]=num_edges
    #             elif key=="insertion_edge":
    #                 current_insertion_edge[key]=(match.group(1),match.group(2),match.group(3))
    #                 i=0
    #                 for line1 in log_content.splitlines():
    #                     if i==0:
    #                         current_insertion_edge["dynamic_iterations"]=patterns["iterations"].search(line1).group(1)
    #                     elif i==4:
    #                         current_insertion_edge["re_matroid_iterations"]=patterns["iterations"].search(line1).group(1)
    #                     else:
    #                         current_insertion_edge[search[i]]=patterns[search[i]].search(line1).group(1)
    #                     i+=1
    #                     if i==9:
    #                         break
    #                 current_data["insertion_edge"]=current_insertion_edge
    #                 current_insertion_edge={}
    #             else:
    #                 current_data[key]=match.group(1)

    # 提取信息
    results = []
    current_data = {}
    current_insertion_edge = {}
    log_lines = iter(log_content.splitlines())
    j=1

    for line in log_lines:
        if patterns["vertices"].search(line):
            results.append(current_data)
            current_data = {}
            j=1
            with open(line, 'r') as f:
                num_vertices, num_edges, root = map(int, f.readline().strip().split())
                if dataset == "cliques":
                    current_data["vertices"]=patterns["vertices"].search(line).group(1)
                else:
                    current_data["vertices"]=num_vertices
                current_data["edges"] = num_edges
            i=0
            while i<6:
                line1=next(log_lines, None)
                match=patterns[search[i]].search(line1)
                if match:
                    current_data[search[i]]=match.group(1)
                i+=1
        match=patterns["insertion_edge"].search(line)
        if match:
            current_data[f"insertion_edge{j}"] = f"{match.group(1)},{match.group(2)},{match.group(3)}"
            i = 0
            while i < 9:
                line1 = next(log_lines, None)
                
                match=patterns[search[i]].search(line1)
                if match:
                    if i == 0:
                        current_data[f"insertion_edge{j}_dynamic_iterations"] = match.group(1)
                    elif i == 4:
                        current_data[f"insertion_edge{j}_re_matroid_iterations"] = match.group(1)
                    else:
                        current_data[f"insertion_edge{j}_"+search[i]] = match.group(1)
                i += 1
            j+=1
    results.append(current_data)
    # print(len(results))
    # print(results)
    results.remove({})
    # 将结果转换为DataFrame
    df = pd.DataFrame(results)
    # print(df_save)
    # df.to_csv(path+".csv", index=False)

    df_save = pd.DataFrame()
    df_save["vertices"]=df["vertices"].astype(int)
    df_save["edges"]=df["edges"].astype(int)
    df_save["avg_dynamic_iterations"]=sum(df[f"insertion_edge{i}_dynamic_iterations"].astype(int) for i in range(1,4))/3
    df_save["avg_dynamic_iterations"]=df_save["avg_dynamic_iterations"].round(3)
    df_save["avg_re_matroid_iterations"]=sum(df[f"insertion_edge{i}_re_matroid_iterations"].astype(int) for i in range(1,4))/3
    df_save["avg_re_matroid_iterations"]=df_save["avg_re_matroid_iterations"].round(3)
    df_save["avg_dynamic_time"]=sum(df[f"insertion_edge{i}_dynamic_time"].astype(float) for i in range(1,4))/3
    df_save["avg_dynamic_time"]=df_save["avg_dynamic_time"].round(3)
    df_save["avg_re_matroid_time"]=sum(df[f"insertion_edge{i}_re_matroid_time"].astype(float) for i in range(1,4))/3
    df_save["avg_re_matroid_time"]=df_save["avg_re_matroid_time"].round(3)
    df_save["avg_re_edmonds_time"]=sum(df[f"insertion_edge{i}_re_edmonds_time"].astype(float) for i in range(1,4))/3
    df_save["avg_re_edmonds_time"]=df_save["avg_re_edmonds_time"].round(3)

    df_save.sort_values(by="vertices",inplace=True)
    df_save.to_csv(path+".csv", index=False)

    # # 运行时间求平均值
    # all_matroid_time = []
    # all_edmonds_time = []

   
    # for run in results:
    #     if len(run)>0:
    #         df = pd.DataFrame(run["data"])
    #         # print(df["matroid_time"].astype(float))
    #         all_matroid_time.append(df["matroid_time"].astype(float).tolist())
    #         all_edmonds_time.append(df["edmonds_time"].astype(float).tolist())

    # import numpy as np
    # all_edmonds_time = np.array(all_edmonds_time)
    # avg_edmonds_time = np.mean(all_edmonds_time, axis=0)
    # df_save["avg_edmonds_time"]=np.round(avg_edmonds_time,3)

    # all_matroid_time = np.array(all_matroid_time)
    # avg_matroid_time = np.mean(all_matroid_time, axis=0)
    # df_save["avg_matroid_time"]=np.round(avg_matroid_time,3)



    # df_save.drop("matroid_time", axis=1, inplace=True)
    # df_save.drop("edmonds_time", axis=1, inplace=True)
    # df_save["vertices"]=df["vertices"].astype(int)
    # df_save.sort_values(by="vertices",inplace=True)
    # df_save.to_csv(path+".csv", index=False)


    # import matplotlib.pyplot as plt

    # plt.figure()

    # # 绘制两组数据的散点图
    # plt.scatter(df_save["vertices"], df_save["avg_dynamic_time"], color='blue', label="avg_dynamic_time")  # 第一组数据，蓝色
    # plt.scatter(df_save["vertices"], df_save["avg_re_matroid_time"], color='red', label="avg_re_matroid_time")   # 第二组数据，红色
    # plt.scatter(df_save["vertices"], df_save["avg_re_edmonds_time"], color='black', label="avg_re_edmonds_time")

    # # 设置标签和标题
    # plt.xlabel("vertices")
    # plt.ylabel("time (sec)")
    # # plt.title('Comparison of Two Groups')
    # plt.legend()  # 显示图例

    # plt.savefig(path+".png")

