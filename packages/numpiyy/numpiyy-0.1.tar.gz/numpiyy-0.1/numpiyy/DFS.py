# graph={}

# def dfs(graph, start, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(start)

#     print(start)

#     for next in graph[start] - visited:
#         dfs(graph, next, visited)
#     return visited


# # graph = {'0': set(['1', '2','3']),
# #          '1': set(['3']),
# #          '2': set(['4']),
# #          '3': set(['5','6']),
# #          '4': set(['7','5']),
# #          '5': set(['2']),
# #          '6': set([]),
# #          '7': set([])
# #         }


# nodes=int(input("Enter the number of nodes : "))
# edges=int(input("Enter the number of edges : "))

# Nodes=[]
# print("Enter the nodes :")
# for _ in range(nodes):
#     node=(input())
#     Nodes.append(node)
#     graph[node]=set()

# print("Enter the edges : ")
# for node in Nodes:
#     num=int(input("Enter the number of edges for node "+node+" : "))
#     print("Enter the edges :")
#     for i in range(num):
#         graph[node].add(input())

# startNode=input("Enter the start node : ")


# print("The DFS traversal is as follows :")
# dfs(graph, startNode)



from queue import Queue
from queue import LifoQueue

graph={
 'A' : ['B', 'D'],
 'B' : ['C','F'],
 'C' : ['E','G'],
 'D' : ['F'],
 'E' : ['B', 'F'],
 'F' : ['A'],
 'G' : ['E']
}
start_node = 'A'
end_node = 'G'

def ret_value(k):
    for key, value in graph.items():
        if key==k:
            return value
        

def dfs(graph, start_node, end_node):
    q = LifoQueue()
    path = []
    if start_node in graph:
        q.put(start_node)
        while q.empty()==False:
            visit = q.get()
            path.append(visit)
            if path[-1] != end_node:
                eles = ret_value(visit)
                if eles != None:
                    for i in eles:
                        if i not in path:
                            q.put(i)
            else:
                break

    path = list(dict.fromkeys(path))
    print('path = ', path)

dfs(graph, start_node, end_node)