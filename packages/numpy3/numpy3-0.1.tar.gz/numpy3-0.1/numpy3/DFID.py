from collections import defaultdict

class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DLS(self, src, target, maxDepth):
        if src == target:
            return True
        if maxDepth <= 0:
            return False
        for i in self.graph[src]:
            print(i, end=' ')
            if(self.DLS(i, target, maxDepth-1)):
                return True
        return False

    def DFID(self, src, target, maxDepth):
        print("\n\n")
        for i in range(maxDepth):
            print(f"Iteration {i+1} (from node {src}) : ", end='  ')
            if self.DLS(src, target, i):
                print(f"\n Target is reachable from source within max depth")
                return True
            print()
        print(f"Target is NOT reachable from the source within the max depth")
        return False


graph = Graph(0)
while True:
    edge = input("Enter an edge as 'source dest'(or leave blank to stop): ")
    if not edge:
        break
    source, dest = edge.split()
    # graph.V = max(graph.V, int(source), int(dest))
    graph.addEdge(int(source), int(dest))

src = int(input("Enter the source node: "))
target = int(input("Enter the target node: "))
maxDepth = int(input("Enter the maximum search depth: "))
graph.DFID(src, target, maxDepth)


"""
Enter an edge as 'source dest' (or leave blank to stop): 0 1
Enter an edge as 'source dest' (or leave blank to stop): 0 2
Enter an edge as 'source dest' (or leave blank to stop): 1 6
Enter an edge as 'source dest' (or leave blank to stop): 1 7
Enter an edge as 'source dest' (or leave blank to stop): 2 2
Enter an edge as 'source dest' (or leave blank to stop): 2 3
Enter an edge as 'source dest' (or leave blank to stop): 3 5
Enter an edge as 'source dest' (or leave blank to stop): 4 5
Enter an edge as 'source dest' (or leave blank to stop): 6 2
Enter an edge as 'source dest' (or leave blank to stop): 7 3
Enter an edge as 'source dest' (or leave blank to stop):

Enter the source node: 0
Enter the target node: 5
Enter the maximum search depth: 3
"""