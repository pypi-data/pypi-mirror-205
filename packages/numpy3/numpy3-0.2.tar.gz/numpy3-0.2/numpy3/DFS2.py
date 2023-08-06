from queue import Queue
from queue import LifoQueue
from collections import defaultdict

# graph={
#  'A' : ['B','C', 'D'],
#  'B' : ['E','F'],
#  'C' : ['G','H'],
#  'D' : ['I'],
#  'E' : ['J', 'K'],
#  'G' : ['L'],
#  'I' : ['M'],
#  'K' : ['N']
# }
graph=defaultdict(list)

while True:
    edge=input("Enter an edge as 'source dest (or leave blank to stop):")
    if not edge:
        break
    source,dest =  edge.split()
    graph[source].append(dest)


start_node = input("Enter start node: ")
end_node = input("Enter end node: ")

def bfs(graph,sn,en):
    q = LifoQueue() #initialise queue
    path = [] #visited list (in short)

    q.put(start_node) # put strt in queue
    while q.empty() ==False:
        visit = q.get() #removes first element from queue and stores in visit i.e currently visiting node
        path.append(visit) #put visit in visited
        if path[-1]!=end_node: #if last node of path(i.e visit) is not end node explore more
            for k in graph.keys():#get successor nodes of visit
                if k==visit:
                    value = graph[k]
            if value!=None: #if successor not empty 
                for v in reversed(value): #put successor nodes in queue to be visited if not in path(i.e visited node) 
                    if v not in path:
                        q.put(v)
        else:
            break
    path = list(dict.fromkeys(path))    #remove duplicates from path (this is done in case of loops in graph)
    if end_node in path:
        print(path)
    else:
        print("Node not found")    


bfs(graph,start_node,end_node)