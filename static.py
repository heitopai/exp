
def ReadGraph(path):
    with open(path,'r') as f:
        num_vertices,num_edges,root=map(int,f.readline().strip().split())
        A_list=[]
        G_adj=[[] for _ in range(num_vertices)]
        id=0
        for _ in range(num_edges):
            u,v,w=map(int,f.readline().strip().split())
            A_list.append((u,v,w))
            G_adj[v].append(id) 
            id=id+1
    return A_list,G_adj,num_vertices,num_edges,root


import os
current_path = os.path.dirname(os.path.abspath(__file__))

# 数据集
# dataset="dense"
# dataset="sparse"
dataset="cliques"

# 获取该类数据集下的所有数据文件夹
directory = current_path + "\\dataset\\" + dataset
folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
print(folders)

for folder in folders:

    import sys
    # 将标准输出重定向到文件
    os.makedirs(current_path + '\\result\\'  + dataset, exist_ok=True)
    sys.stdout = open(current_path + '\\result\\'  + dataset + '\\log' + folder + '.txt', 'a', encoding='utf-8')

    from datetime import datetime
    print('本次运行时刻：',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    all_files = os.listdir(directory + '\\' + folder)
    for file in all_files:
        path=directory + '\\' + folder + '\\' + file
        print(path)
        A_list,G_adj,num_vertices,num_edges,root=ReadGraph(path)


        from Matroid import DMST
        import time
        start=time.time()
        T_list, AG_adj=DMST(A_list,G_adj,num_vertices,num_edges,root)
        end=time.time()
        print("基于拟阵交算法的DMST的求解时间：", end-start)

        if T_list is not None:
            print("基于拟阵交算法求DMST的权重和：",sum([A_list[T_list[v]][2] for v in range(num_vertices) if v!=root]))

        import networkx as nx
        G = nx.DiGraph()
        G.add_nodes_from(list(range(num_vertices)))
        for u,v,w in A_list:
            if v!=root:
                G.add_edge(u,v,weight=w)

        try:
            start=time.time()
            msa=nx.minimum_spanning_arborescence(G)
            end=time.time()
            print("Networkx中基于Edmonds算法的DMST求解时间：", end-start)
            print("Edmonds算法求DMST的权重和：", sum([G[u][v]['weight'] for u,v in msa.edges()]))
        except Exception as e:
            print(f"异常：{e}")

