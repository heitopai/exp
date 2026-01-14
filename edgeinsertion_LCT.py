
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
    os.makedirs(current_path + '\\insertion_result_LCT\\'  + dataset, exist_ok=True)
    sys.stdout = open(current_path + '\\insertion_result_LCT\\'  + dataset + '\\log' + folder + '.txt', 'w', encoding='utf-8')

    from datetime import datetime
    print('本次运行时刻：',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    all_files = os.listdir(directory + '\\' + folder)
    for file in all_files:
        path=directory + '\\' + folder + '\\' + file
        print(path)
        original_A_list,original_G_adj,num_vertices,num_edges,root=ReadGraph(path)

        import copy
        A_list,G_adj=copy.deepcopy(original_A_list),copy.deepcopy(original_G_adj)
        from Matroid_LCT import DMST
        import time
        start=time.time()
        T_list, AG_adj, lc_tree=DMST(A_list,G_adj,num_vertices,num_edges,root)
        end=time.time()
        print("基于拟阵交算法的DMST的求解时间：", end-start)

        print("基于拟阵交算法求DMST的权重和：",sum([A_list[T_list[v]][2] for v in range(num_vertices) if v!=root]))

        import networkx as nx
        G = nx.DiGraph()
        G.add_nodes_from(list(range(num_vertices)))
        for u,v,w in original_A_list:
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

        # 增加有向边
        import random
        random.seed(0)
        insert_edges=[(random.randint(0, num_vertices-1), random.randint(1, num_vertices-1), random.randint(0, 10)) for _ in range(3)]
        for tail,head,weight in insert_edges:


            print('插入的边为：', tail,head,weight)

            T_list_tmp, AG_adj_tmp,A_list_tmp,G_adj_tmp,lc_tree_tmp=copy.deepcopy(T_list), copy.deepcopy(AG_adj),copy.deepcopy(A_list),copy.deepcopy(G_adj),copy.deepcopy(lc_tree)
            
            from Matroid_LCT import EdgeInsertion
            start=time.time()
            T_list_tmp, AG_adj_tmp, _=EdgeInsertion(T_list_tmp,AG_adj_tmp,A_list_tmp,G_adj_tmp,num_vertices,tail,head,weight,lc_tree_tmp)
            end=time.time()
            print("基于拟阵交的动态插入有向边的求解时间：", end-start)
            print("基于拟阵交的动态插入有向边更新DMST后的权重和：",sum([A_list_tmp[T_list_tmp[v]][2] for v in range(num_vertices) if v!=root]))

            A_list_insert,G_adj_insert=copy.deepcopy(original_A_list),copy.deepcopy(original_G_adj)
            A_list_insert.append((tail,head,weight))
            G_adj_insert[head].append(len(original_A_list))
            
            start=time.time()
            T_list_insert, AG_adj_insert, _=DMST(A_list_insert,G_adj_insert,num_vertices,len(A_list_insert),root)
            end=time.time()
            print("插入有向边后重新执行基于拟阵交算法的DMST的权重和：", sum([A_list_insert[T_list_insert[v]][2] for v in range(num_vertices) if v!=root]))
            print("插入有向边后重新执行基于拟阵交算法的DMST的求解时间：", end-start)

            G.add_edge(tail,head,weight=weight)
            try:
                start=time.time()
                msa=nx.minimum_spanning_arborescence(G)
                end=time.time()
                print("插入有向边后重新执行Networkx中基于Edmonds算法的DMST求解时间：", end-start)
                print("插入有向边后重新执行Edmonds算法求DMST的权重和：", sum([G[u][v]['weight'] for u,v in msa.edges()]))
            except Exception as e:
                print(f"异常：{e}")
            G.remove_edge(tail,head)

            sys.stdout.flush()