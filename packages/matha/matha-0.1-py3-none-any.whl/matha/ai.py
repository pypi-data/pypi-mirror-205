#DFS
visited = set()  # Set to keep track of visited nodes of graph.
def dfs(visited, graph, node):  # function for dfs
    if node not in visited:
        print(node, end = " ")
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
graph2 = {
    '0': ['1', '9'],
    '1': ['2'],
    '2': ['0', '3'],
    '9': ['3'],
    '3': ['3']
}
print("\nFollowing is the Depth-First Search for graph 2")
dfs(visited, graph2, '0')


#BFS
visited = []  # List for visited nodes.
queue = []  # Initialize a queue

def bfs(visited, graph, node):  # function for BFS
    visited.append(node)
    queue.append(node)
    while queue:          # Creating loop to visit each node
        m = queue.pop(0)
        print(m, end=" ")
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
'8': [] }
# function calling
print("Following is the Breadth-First Search")
bfs(visited, graph, '5')

#DFID
from collections import defaultdict
# list representation
class Graph:
    def __init__(self,vertices):
        self.V = vertices
        self.graph = defaultdict(list)
    def addEdge(self,u,v):
        self.graph[u].append(v)
    def DLS(self,src,target,maxDepth):
        if src == target : return True
        if maxDepth <= 0 : return False
        for i in self.graph[src]:
                if(self.DLS(i,target,maxDepth-1)):
                    return True
        return False
    def IDDFS(self,src, target, maxDepth):
        for i in range(maxDepth):
            if (self.DLS(src, target, i)):
                return True
        return False
# Create a graph given in the above diagram
g = Graph (7)
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 3)
g.addEdge(1, 4)
g.addEdge(2, 5)
g.addEdge(2, 6)
target = 6; maxDepth = 3; src = 0
if g.IDDFS(src, target, maxDepth) == True:
    print ("Target is reachable from source " +
        "within max depth")
else :
    print ("Target is NOT reachable from source " +
        "within max depth")
    

def astar(self):
    max_distance = sys.maxsize
    q = list()
    fx = self.heuristics[self.start_node] + 0
    q.append([fx, self.start_node])
    while q:
        pair = q.pop(0)
        fx = pair[0]
        node = pair[1]
        dist_so_far = fx - self.heuristics[node]
        if node == self.goal_node:
            if dist_so_far < max_distance:
                max_distance = dist_so_far
        children = []
        if node in self.adjDict:
            children = self.adjDict[node]
        for edge in children:
            child = edge[1]
            weight = edge[0]
            q.append([dist_so_far + weight + self.heuristics[child],
child])
        print(f"min distance to goal node is {max_distance}")
def main():
    print("enter input")
    graph = Graph()
    while True:
        tokens = input().split()
        parent = tokens[0]
        if parent == "-1":
            break
        children = tokens[1:]
        for child in children:
            graph.add_edge(parent, int(
                child.split(",")[1]), child.split(",")[0])
        while True:
            tokens = input().split()
            node = tokens[0]
            if node == "-1":
                break
            value = int(tokens[1])
            graph.add_heuristic(node, value)
    # print(graph.adjDict)
    # print(graph.heuristics)
    # graph.print()
    start_node = input("enter start node: ")
    goal_node = input("enter goal node: ")
    graph.set_start_node(start_node)
    graph.set_goal_node(goal_node)
    graph.astar()
main()

#UCS
import sys
class Graph:
    def __init__(self):
        self.adjDict = dict()
        self.start_node = "S"
        self.goal_node = "S"
    def add_edge(self, u, v, w):
        if u not in self.adjDict:
            self.adjDict[u] = list()
        self.adjDict[u].append([w, v])
    def print(self):
        for key in self.adjDict:
            print(key)
            print(self.adjDict[key])
    def set_start_node(self, node):
        self.start_node = node
    def set_goal_node(self, node):
        self.goal_node = node
    def ucs(self):
        max_distance = sys.maxsize
        q = list()
        visited = list()
        q.append([0, self.start_node])
        # print(q)
        while q:
# print(q)
            edge = q.pop(0)
            # print(q)
            if edge[1] in visited:
                continue
            visited.append(edge[1])
            if edge[1] == self.goal_node:
                if edge[0] < max_distance:
                    max_distance = edge[0]
            edges = []
            if edge[1] in self.adjDict:
                edges = self.adjDict[edge[1]]
            for outEdge in edges:
                # print(type(edge[0]))
                # print(type(outEdge[0]))
                q.append([edge[0] + outEdge[0], outEdge[1]])
                q.sort()
        print(f"min distance to goal node is: {max_distance}")
def main():
    print("enter input")
    graph = Graph()
    while True:
        tokens = input().split()
        parent = tokens[0]
        if parent == "-1":
            break
        children = tokens[1:]
        for child in children:
            # print(child)
            # print(child.split(","))
            graph.add_edge(parent, child.split(
                ",")[0], int(child.split(",")[1]))
    # graph.print()
    start_node = input("enter start node: ")
    goal_node = input("enter goal node: ")
    graph.set_start_node(start_node)
    graph.set_goal_node(goal_node)
    graph.ucs()
    # graph.print()
main()                    

#Hill Climbing
import random
import math
def objFunc(x):
    return math.sin(x)-math.cos(2*x)
def hillClimb(x, step, maxItr):
    fx = objFunc(x)
    for _ in range(maxItr):
        dx = (random.random()*2 - 1)*step
        next_x = x+dx
        next_fx = objFunc(next_x)
        if next_fx > fx:
            fx = next_fx
            x = next_x
    return x
x=1
step = 0.01 
maxItr = 1000
res = hillClimb(x, step, maxItr)
print(f'Point found: {res}\nf(x): {objFunc(res)}')

#GENETIC
import random
def fitness(individual):
 return sum(individual)
def genetic_algorithm(population_size, chromosome_size, generations,
mutation_rate):
    population = [[random.randint(0, 1) for j in range(chromosome_size)]
for i in range(population_size)]
    for generation in range(generations):
        fitness_scores = [fitness(individual) for individual in
population]
        parents = []
        for i in range(population_size // 2):
            parent1 = population[fitness_scores.index(max(fitness_scores))]
            fitness_scores[fitness_scores.index(max(fitness_scores))] = -1
            parent2 = population[fitness_scores.index(max(fitness_scores))]
            fitness_scores[fitness_scores.index(max(fitness_scores))] = -1
            parents.append((parent1, parent2))
        population = []
        for parent1, parent2 in parents:
            child1, child2 = parent1[:], parent2[:]
            for i in range(chromosome_size):
                if random.random() < mutation_rate:
                    child1[i] = 1 - child1[i]
                if random.random() < mutation_rate:
                    child2[i] = 1 - child2[i]
            population.append(child1)
            population.append(child2)
    fitness_scores = [fitness(individual) for individual in population]
    return population[fitness_scores.index(max(fitness_scores))]
fittest_individual = genetic_algorithm(
    population_size=100, chromosome_size=10, generations=50,
mutation_rate=0.01)
print("Fittest individual:", fittest_individual)

#ANNEALING
import random
import math
def objFunc(x):
    return math.sin(x)-math.cos(2*x)
def simulatedAnnealing(x, maxItr, T):
    fx = objFunc(x)
    Tmin = 0.0001
    for _ in range(maxItr):
        alpha = 0.99
        T = T*alpha
        dx = (random.random()*2-1)*T
        next_x = x+dx
        next_fx = objFunc(next_x)
        if next_fx > fx or random.random() < math.exp((next_fx-fx)/T):
            x = next_x
            fx = next_fx
        if T < Tmin:
            break
    return x
x=1
maxIter = 1000 
T = 1.0
res = simulatedAnnealing(x, maxIter, T)
# Print the results
print(f'Point found: {res}\nf(x): {objFunc(res)}')