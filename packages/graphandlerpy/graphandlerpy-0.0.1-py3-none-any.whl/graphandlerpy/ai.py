def quicktext():
    print('Hello, welcome to QuickSample package.')

#BFS
from collections import deque
def bfs(graph, root):
    visited = set()
    queue = deque([root])
    visited.add(root)

    while queue:
        vertex = queue.popleft()
        print(str(vertex) + " ", end="")

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                if neighbour not in graph:
                    graph[neighbour] = []


if __name__ == '__main__':
    graph = {'A': ['B', 'C'], 'B': ['D', 'F'], 'C': ['E']}
    print("Following is Breadth First Traversal: ")
    bfs(graph, 'A')


#DFS
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)

    print(start)

    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited


graph = {'0': set(['1', '2']),
         '1': set(['0', '3', '4']),
         '2': set(['0']),
         '3': set(['1']),
         '4': set(['2', '3'])}

dfs(graph, '0')


#DFID
def dfs(start, depth, path, visited):
    path.append(start)
    visited.add(start)
    
    if start == goal:
        return True, path
    
    if depth == 0:
        return False, None
    
    for neighbor, cost in graph[start].items():
        if neighbor not in visited:
            found, new_path = dfs(neighbor, depth - 1, path, visited)
            if found:
                return True, new_path
    
    path.pop()
    visited.remove(start)
    
    return False, None

def dfid(start):
    depth = 0
    
    while True:
        path = []
        visited = set()
        
        found, new_path = dfs(start, depth, path, visited)
        if found:
            cost = sum(graph[new_path[i]][new_path[i+1]] for i in range(len(new_path)-1))
            return new_path, cost
        
        depth += 1
        
        print('='*50)
        print('Depth:', depth)
        print('Open List:', path)
        print('Closed List:', visited)

graph = {
    'A': {'B': 9, 'C': 4},
    'B': {'C': 2, 'D':7, 'E':3},
    'C': {'D': 1, 'E':6},
    'D': {'E': 4,'F':8},
    'E': {'F':2},
    'F': {}

}
start_node, goal = 'A', 'F'
path, cost = dfid(start_node)
print('+'*50)
print('Path:', path)
print('Cost:', cost)


#UCS
from queue import PriorityQueue

def ucs(start, goal):
    open_list = PriorityQueue()
    open_list.put((0, start))

    closed_list = {}

    print('='*50)
    print('Open List:', [(node, cost) for (cost, node) in list(open_list.queue)])
    print('Closed List:', closed_list)

    cost = {start: 0}
    parent = {start: None}

    while not open_list.empty():
        current_cost, current_node = open_list.get()

        closed_list[current_node] = current_cost

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            path.reverse()
            return path, cost[goal]

        for neighbor, neighbor_cost in graph[current_node].items():
            tentative_cost = current_cost + neighbor_cost

            if neighbor in closed_list:
                continue

            if neighbor in cost and tentative_cost >= cost[neighbor]:
                continue

            open_list.put((tentative_cost, neighbor))

            cost[neighbor] = tentative_cost
            parent[neighbor] = current_node

        print('='*50)
        print('Open List:', [(node, cost) for (cost, node) in list(open_list.queue)])
        print('Closed List:', closed_list)

    return None


graph = {
    'A': {'B': 9, 'C': 4},
    'B': {'C': 2, 'D': 7, 'E': 3},
    'C': {'D': 1, 'E': 6},
    'D': {'E': 4, 'F': 8},
    'E': {'F': 2},
    'F': {}
}
path, cost = ucs('A', 'F')
print('Path:', path)
print('Cost:', cost)


#A*
from queue import PriorityQueue

def a_star(start, goal):
    open_list = PriorityQueue()
    open_list.put((0 + heuristic[start], start, 0))
    
    closed_list = {}
    
    cost = {start: 0}
    parent = {start: None}

    print('='*50)
    print('Open List:', list(open_list.queue))
    print('Closed List:', closed_list)
    print('Cost:', cost)
    print('Parent:', parent)
    
    while not open_list.empty():
        current_f, current_node, current_cost = open_list.get()
        
        closed_list[current_node] = (current_cost, heuristic[current_node])
        
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            path.reverse()
            return path, cost[goal]
        
        for neighbor, neighbor_cost in graph[current_node].items():
            tentative_cost = current_cost + neighbor_cost
            
            if neighbor in closed_list:
                continue
            
            if neighbor in cost and tentative_cost >= cost[neighbor]:
                continue
            
            open_list.put((tentative_cost + heuristic[neighbor], neighbor, tentative_cost))
            
            cost[neighbor] = tentative_cost
            parent[neighbor] = current_node
        
        print('='*50)
        print('Open List:', list(open_list.queue))
        print('Closed List:', closed_list)
        print('Cost:', cost)
        print('Parent:', parent)
    
    return None


graph = {
    'A': {'B': 5, 'C': 10},
    'B': {'D': 5},
    'C': {'D': 10},
    'D': {'E': 5},
    'E': {}
}

heuristic = {
    'A': 20,
    'B': 15,
    'C': 10,
    'D': 5,
    'E': 0
}

print(graph)
print(heuristic)

start_node = input("Enter the start node: ")
goal_node = input("Enter the goal node: ")
path, cost = a_star(start_node, goal_node)
print('\n\n\n','-'*80)
print('Path:', path)
print('Cost:', cost)


#Hill Climbing
import random
import math
def objFunc(x):
    return math.sin(x)-math.cos(2*x)
def hillClimb(x, step, maxItr):
    fx = objFunc(x)
    for i in range(maxItr):
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