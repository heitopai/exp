import link_cut_tree as lct

# 并查集
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def Greedy(A_list,G_adj,num_vertices,num_edges,root):
    T_list=[-1]*num_vertices

    lc_tree=[lct.Node(value=i) for i in range(num_vertices)]

    # 将边集A按照权重c从小到大排序
    Sorted_A_list=list(range(num_edges))
    Sorted_A_list.sort(key=lambda id: A_list[id][2])

    uf=UnionFind(num_vertices)
    count=0
    sum_weight=0
    for id in Sorted_A_list:
        tail=A_list[id][0]
        head=A_list[id][1]
        if head != root and T_list[head]==-1 and uf.find(tail) != uf.find(head):
            uf.union(tail,head)
            T_list[head]=id
            count=count+1
            sum_weight=sum_weight+A_list[id][2]

            lc_tree[head].lc_link(lc_tree[tail])

        if count==num_vertices-1:
            print('贪心算法求初始有向生成树的权值',sum_weight)
            return T_list,num_edges,lc_tree
    print('贪心算法求得森林')
    for v in range(num_vertices):
        if v!=root and T_list[v]==-1:
            A_list.append((root,v,1000000))
            T_list[v]=num_edges
            G_adj[v].append(num_edges)
            num_edges=num_edges+1
            
            lc_tree[v].lc_link(lc_tree[root])

    return T_list,num_edges,lc_tree


# def LCA(A_list,T_list,num_vertices,u,v):
#     u_path=[0]*num_vertices

#     while True:
#         u_path[u]=1
#         id=T_list[u]
#         if id==-1:
#             break
#         else:
#             u=A_list[id][0]

#     while u_path[v]==0:
#         id=T_list[v]
#         v=A_list[id][0]
    
#     return v

def I1Arcs(A_list,G_adj,T_list,num_vertices,AG_adj):
    for v in range(num_vertices):
        y=T_list[v]
        if y!=-1:
            head=A_list[y][1]
            for x in G_adj[head]:
                if x!=y:
                    AG_adj[y].append(x)

def I2Arcs(A_list,T_list,num_edges,num_vertices,AG_adj,lc_tree):
    for x in range(num_edges):
        head=A_list[x][1]
        if T_list[head]!=x:

            AG_adj[x]=[]

            tail=A_list[x][0]
            # lca=LCA(A_list,T_list,num_vertices, tail,head)
            lca=lc_tree[tail].lc_lca(lc_tree[head]).value

            cur=tail
            while cur!=lca:
                y=T_list[cur]
                AG_adj[x].append(y)
                cur=A_list[y][0]

            cur=head
            while cur!=lca:
                y=T_list[cur]
                AG_adj[x].append(y)
                cur=A_list[y][0]


def CostOfAuxiliaryGraph(A_list,T_list,y,x,s):
    if y==s:
        return 0
    if T_list[A_list[y][1]]==y:
        return A_list[x][2]-A_list[y][2]
    else:
        return 0

def SubtreeDisassembly(a,b,p,v,w,label):
    # 子树分解
    ## 删除w以及子树
    x = b[w]  # x 是 w 的前驱
    if x is not None:
        b[w] = None  # 断开 w 的前驱指针
        y = a[w]  # y 是 w 的后继
        while b[p[y]] is None:  # 遍历子树
            label[y]=0
            if y == v:
                # print(d[v]+c-d[w])
                # return FindNegativeDiycle(p, v,w)  # 发现负环
                return True
            else:
                b[y] = None  # 断开 y 的前驱指针
                y = a[y]     # 移动到下一个顶点

        a[x] = y  # 将 x 的后继指向 y
        b[y] = x  # 将 y 的前驱指向 x

    ## 加入w
    a[w] = a[v]  # 将 w 的后继指向 v 的后继
    b[a[w]] = w  # 将 v 的后继的前驱指向 w
    b[w] = v  # 将 w 的前驱指向 v
    a[v] = w  # 将 v 的后继指向 w

    return False

def Label(d,p,inq,L,label,v,w,c):
    # label操作
    d[w] = d[v]+c  # 更新 w 的距离
    p[w] = v             # 更新 w 的父指针
    label[w]=1
    if inq[w]==False:
        L.append(w)      # 将 w 加入待扫描队列
        inq[w]=True

def FindNegativeDiycle(p, v, w):
    # 通过父指针回溯找到负环
    cycle = []
    current = v
    while current != w:
        cycle.append(current)
        current = p[current]
    cycle.append(current)  
    return cycle

from collections import deque
def DetectNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, valid=None):
    # 初始化
    d = [1000000]*(num_edges+1)  # 距离初始化为无穷大
    p = [None]*(num_edges+1)          # 父指针初始化为 None
    b = [None]*(num_edges+1)          # 前驱指针初始化为 None
    a = [None]*(num_edges+1)          # 后继指针初始化为 None
    inq=[False]*(num_edges+1)
    label=[0]*(num_edges+1)

    d[s] = 0  # 源点 s 的距离为 0
    L = deque()  # 待扫描的顶点队列
    L.append(s)  # 将源点 s 加入待扫描队列
    label[s]=1
    inq[s]=True
    a[s] = s        # 源点 s 的后继指向自己
    b[s] = s        # 源点 s 的前驱指向自己
    p[s]=s

    count=1
    cur_pass=0
    max_pass=2*num_vertices-2

    # 主循环：扫描待扫描的顶点
    while L and cur_pass<=max_pass:
        for i in range(count):
            v = L.popleft()  # 从队列中取出一个顶点 v
            inq[v]=False
            if label[v]==1:
                for w in AG_adj[v]:
                    c=CostOfAuxiliaryGraph(A_list, T_list, v,w,s)
                    if (valid is None and d[v]+c < d[w]) or (valid is not None and valid[w]==1 and d[v]+c < d[w]):
                            if SubtreeDisassembly(a,b,p,v,w,label):
                                return FindNegativeDiycle(p,v,w)  # 发现负环
                            Label(d,p,inq,L,label,v,w,c)

                label[v]=2 # 2代表将v标记为scaned
        count=len(L)
        cur_pass=cur_pass+1

    # print(cur_pass)
    return None  # 没有发现负环

def NegativeSubDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, cycle, visited):
    valid=[0]*(num_edges+1)
    for c in cycle:
        valid[c]=1
    for c in cycle:
        if visited[c]==0:
            valid[c]=0
            subcycle=DetectNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, valid)
            if subcycle is not None:
                return subcycle
            else:
                valid[c]=1
                visited[c]=1
    return None

def SimpleNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, cycle):
    visited=[0]*(num_edges+1)
    simpleNegativeDicycle=cycle
    while True:
        cycle=NegativeSubDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, cycle, visited)
        if cycle is None:
            return simpleNegativeDicycle
        else:
            simpleNegativeDicycle=cycle

def Update(A_list, G_adj, num_vertices, num_edges, T_list, AG_adj, s,lc_tree):
    cycle=DetectNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s)
    iter=1
    while cycle is not None:
        iter=iter+1
        simpleNegativeDicycle=SimpleNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s, cycle)
            
        new_edges=[]
        for c in simpleNegativeDicycle:
            if T_list[A_list[c][1]]!=c:
                new_edges.append(c)

        for id in new_edges:
            head=A_list[id][1]
            T_list[head]=id

            lc_tree[head].lc_cut()
            lc_tree[head].lc_link(lc_tree[A_list[id][0]])

            AG_adj[id]=[]
            for x in G_adj[head]:
                if x!=id:
                    AG_adj[id].append(x)

        I2Arcs(A_list,T_list,num_edges,num_vertices,AG_adj,lc_tree)
        cycle=DetectNegativeDicycle(AG_adj, A_list, T_list, num_edges, num_vertices, s)

    print("迭代次数：", iter)
    return T_list,AG_adj,lc_tree

def DMST(A_list,G_adj,num_vertices,num_edges,root):
    T_list,num_edges,lc_tree=Greedy(A_list,G_adj,num_vertices,num_edges,root)

    AG_adj=[[] for _ in range(num_edges+1)]
    I1Arcs(A_list,G_adj,T_list,num_vertices,AG_adj)
    I2Arcs(A_list,T_list,num_edges,num_vertices,AG_adj,lc_tree)
    s=num_edges
    for id in range(num_edges):
        AG_adj[s].append(id)

    return Update(A_list,G_adj,num_vertices,num_edges,T_list,AG_adj,s,lc_tree)

def EdgeDeletion(T_list,AG_adj,A_list,G_adj,num_vertices,deleted_edge,lc_tree):
    head=A_list[deleted_edge][1]
    if T_list[head]!=deleted_edge:
        return T_list,AG_adj,lc_tree
    else:
        A_list[deleted_edge]=(A_list[deleted_edge][0],head,1000000)
        num_edges=len(A_list)
        s=num_edges
        return Update(A_list,G_adj,num_vertices,num_edges,T_list,AG_adj,s,lc_tree)

def EdgeInsertion(T_list,AG_adj,A_list,G_adj,num_vertices,tail,head,weight,lc_tree):
    if T_list[head]==-1:
        return T_list,AG_adj,lc_tree
    
    id=len(A_list)
    A_list.append((tail,head,weight))
    G_adj[head].append(id)
    # I1
    y=T_list[head]
    AG_adj[y].append(id)
    # I2
    AG_adj[id]=[]
    # lca=LCA(A_list,T_list,num_vertices, tail,head)
    lca=lc_tree[tail].lc_lca(lc_tree[head]).value
    cur=tail
    while cur!=lca:
        y=T_list[cur]
        AG_adj[id].append(y)
        cur=A_list[y][0]

    cur=head
    while cur!=lca:
        y=T_list[cur]
        AG_adj[id].append(y)
        cur=A_list[y][0]

    AG_adj.append([])
    num_edges=len(A_list)
    s=num_edges
    for id in range(num_edges):
        AG_adj[s].append(id)
    
    return Update(A_list,G_adj,num_vertices,num_edges,T_list,AG_adj,s)


