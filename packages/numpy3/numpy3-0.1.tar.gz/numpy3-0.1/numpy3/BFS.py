# graph={}
# graph={
#  'Delhi': ['Agra', 'Punjab', 'Haryana'],
#  'Agra': ['Jaipur','Bhopal', 'Gujarat'],
#  'Punjab': ['Gujarat', 'Jaipur','Bhopal'],
#  'Haryana': ['Gujarat', 'Jaipur','Bhopal'],
#  'Gujarat': ['Lucknow', 'Daman'],
#  'Jaipur': ['Lucknow','Daman','Raipur'],
#  'Bhopal': ['Daman','Raipur'],
#  'Lucknow': ['Mumbai','Pune', 'Nagpur'],
#  'Daman': ['Mumbai','Pune', 'Nagpur'],
#  'Raipur': ['Mumbai','Pune', 'Nagpur'],
#  'Mumbai': ['Nashik','Goa', 'Hyderabad'],
#  'Pune': ['Nashik','Goa', 'Hyderabad'],
#  'Nagpur': ['Nashik','Goa', 'Hyderabad'],
#  'Nashik': ['Andhra Pradesh','Puducherry', 'Chennai'],
#  'Goa': ['Andhra Pradesh','Puducherry', 'Chennai'],
#  'Hyderabad': ['Andhra Pradesh','Puducherry', 'Chennai'],
#  'Chennai': ['Kerala'],
#  'Andhra Pradesh': ['Kerala'],
#  'Puducherry': ['Kerala'],
#  'Kerala':['Kochi'],
#  'Kochi':[]
# }


# def bfs(node):

#     visited = [False] * (len(graph))
#     queue = []

#     visited.append(node)
#     queue.append(node)

#     while queue:
#         v = queue.pop(0)
#         print(v, end="  ")

#         for neigh in graph[v]:
#             if neigh not in visited:
#                 visited.append(neigh)
#                 queue.append(neigh)


# nodes=int(input("Enter the number of nodes : "))
# edges=int(input("Enter the number of edges : "))

# Nodes=[]
# print("Enter the nodes :")
# for _ in range(nodes):
#     node=(input())
#     Nodes.append(node)
#     graph[node]=[]

# print("Enter the edges : ")
# for node in Nodes:
#     num=int(input("Enter the number of edges for node "+node+" : "))
#     print("Enter the edges :")
#     for i in range(num):
#         graph[node].append(input())

# startNode=input("Enter the start node : ")


# print("The BFS traversal is as follows :")
# bfs(startNode)

# bfs('Delhi')
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
        

def bfs(graph, start_node, end_node):
    q = Queue()
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

bfs(graph, start_node, end_node)