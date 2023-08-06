#vidhi
gn = [
    [99,1,2,99,99,99,99,99],
    [99,99,99,99,99,99,4,7],
    [99,99,7,1,99,99,99,99],
    [99,99,99,99,99,5,99,99],
    [99,99,99,99,99,12,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,2,99,99],
    [99,99,99,99,99,3,99,99]
]

hn = [-1,5,6,4,15,0,5,8]

# fn = Gn+ hn
nodes=[]
indexes = []

visited = []

def astar(initial, goal, pre):
    if initial == goal:
        return True

    print('GN', gn[initial])
    for i in gn[initial]:
        if i != 99:
            print('Gn', i)
            print('Hn', hn[gn[initial].index(i)])
            nodes.append(i + hn[gn[initial].index(i)] + pre)
            indexes.append(gn[initial].index(i))
    print('Fn', nodes)
    print('INDEXES', indexes)
    visited.append(initial)
    initial = indexes[nodes.index(min(nodes))]
    print('Min', min(nodes))
    pre = min(nodes)
    nodes.remove(min(nodes))
    indexes.remove(initial)
    print('Initial', initial)
    print('Goal', goal)
    print('====================')
    astar(initial, goal, pre)

        
initial = 0
goal = 5
astar(0, 5, 0)

for i in visited:
    if i == 5:
        print(i)
    else:
        print(i, '->', end='')

x = []
for i in range(len(visited)):
    x.append(visited[len(visited)-i-1])

print(x, '\n')

for i in x:
    if gn[i][goal] != 99:
        print(gn[i].index(gn[i][goal]), '->', end='')

        goal = i

print(goal)




def aStarAlgo(start_node, stop_node):
    

    open_set = set(start_node) # {A}, len{open_set}=1
    closed_set = set()
    g = {} # store the distance from starting node
    parents = {}
    g[start_node] = 0
    parents[start_node] = start_node # parents['A']='A"

    while len(open_set) > 0 :
        n = None

        for v in open_set: # v='B'/'F'
            if n == None or g[v] + heuristic(v) < g[n] + heuristic(n):
                n = v # n='A'

        if n == stop_node or Graph_nodes[n] == None:
            pass
        else:
            for (m, weight) in get_neighbors(n):
             # nodes 'm' not in first and last set are added to first
             # n is set its parent
                if m not in open_set and m not in closed_set:
                    open_set.add(m)      # m=B weight=6 {'F','B','A'} len{open_set}=2
                    parents[m] = n       # parents={'A':A,'B':A} len{parent}=2
                    g[m] = g[n] + weight # g={'A':0,'B':6, 'F':3} len{g}=2


            #for each node m,compare its distance from start i.e g(m) to the
            #from start through n node
                else:
                    if g[m] > g[n] + weight:
                    #update g(m)
                        g[m] = g[n] + weight
                    #change parent of m to n
                        parents[m] = n

                    #if m in closed set,remove and add to open
                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)

        if n == None:
            print('Path does not exist!')
            return None

        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if n == stop_node:
            path = []

            while parents[n] != n:
                path.append(n)
                n = parents[n]

            path.append(start_node)

            path.reverse()

            print('Path found: {}'.format(path))
            return path


        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_set.remove(n)# {'F','B'} len=2
        closed_set.add(n) #{A} len=1

    print('Path does not exist!')
    return None

#define fuction to return neighbor and its distance
#from the passed node
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None
#for simplicity we ll consider heuristic distances given
#and this function returns heuristic distance for all nodes
 
def heuristic(n):
    H_dist = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }

    return H_dist[n]

#Describe your graph here
Graph_nodes = {
    'A': [('B', 6), ('F', 3)],
    'B': [('C', 3), ('D', 2)],
    'C': [('D', 1), ('E', 5)],
    'D': [('C', 1), ('E', 8)],
    'E': [('I', 5), ('J', 5)],
    'F': [('G', 1),('H', 7)] ,
    'G': [('I', 3)],
    'H': [('I', 2)],
    'I': [('E', 5), ('J', 3)],
}

# Graph_nodes={
#     'S':[('1',3),('4',4)],
#     '1':[('2',4),('4',5)],
#     '2':[('3',4),('5',5)],
#     '3':[],
#     '4':[('5',2)],
#     '5':[('6',4)],
#     '6':[('7',3)],
#     '7':[]
# }
aStarAlgo('A', 'J')