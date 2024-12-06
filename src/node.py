import heapq
import math

class Node:
    #class copied from Google AI completely, A* algorithm was adapted to fit the game
    #heavily inspired from Google AI after searching "What might an A* algorithm look like that finds a path from one coordintate to another"
    def __init__(self, x, y, g=0, h=0):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = None

    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()

def distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def astar(grid, start, end, hitrange, targetted):
    open_set = []
    closed_set = set()

    start_node = Node(start[0], start[1])
    end_node = Node(end[0], end[1])

    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)
        if distance(current_node, end_node)<=hitrange:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]
        closed_set.add((current_node.x, current_node.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            neighbor_x = current_node.x + dx
            neighbor_y = current_node.y + dy
            #if('air' in targetted):
            if 0<=neighbor_x<len(grid) and 0<=neighbor_y<len(grid[0]) and (grid[neighbor_x][neighbor_y] in [0, 2]) and (neighbor_x, neighbor_y) not in closed_set:
                neighbor_node = Node(neighbor_x, neighbor_y)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = abs(neighbor_x - end_node.x) + abs(neighbor_y - end_node.y)
                neighbor_node.parent = current_node
                heapq.heappush(open_set, neighbor_node)
                #air units pseudocode
            # else:
            #     if 0<=neighbor_x<len(grid) and 0<=neighbor_y<len(grid[0]) and (grid[neighbor_x][neighbor_y] in [0, 2]) and (neighbor_x, neighbor_y) not in closed_set:
            #         neighbor_node = Node(neighbor_x, neighbor_y)
            #         neighbor_node.g = current_node.g + 1
            #         neighbor_node.h = abs(neighbor_x - end_node.x) + abs(neighbor_y - end_node.y)
            #         neighbor_node.parent = current_node
            #         heapq.heappush(open_set, neighbor_node)
    return None