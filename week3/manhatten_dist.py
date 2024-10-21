import heapq

class Node:
    def __init__(self, position, g, h):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]

def get_neighbors(position, grid):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        neighbor_pos = (position[0] + direction[0], position[1] + direction[1])
        if 0 <= neighbor_pos[0] < len(grid) and 0 <= neighbor_pos[1] < len(grid[0]) and grid[neighbor_pos[0]][neighbor_pos[1]] == 0:
            neighbors.append(neighbor_pos)
    return neighbors

def a_star(start, goal, grid):
    open_list = []
    closed_list = set()
    start_node = Node(start, 0, manhattan_distance(start, goal))
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node.position == goal:
            return reconstruct_path(current_node)
        
        closed_list.add(current_node.position)

        for neighbor_pos in get_neighbors(current_node.position, grid):
            if neighbor_pos in closed_list:
                continue
            g_cost = current_node.g + 1
            h_cost = manhattan_distance(neighbor_pos, goal)
            neighbor_node = Node(neighbor_pos, g_cost, h_cost)
            neighbor_node.parent = current_node
            if all(neighbor_node.position != node.position or neighbor_node.g < node.g for node in open_list):
                heapq.heappush(open_list, neighbor_node)
    return None

# Example usage for a 3x3 grid
grid = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]
start = (0, 0)
goal = (2, 2)

path = a_star(start, goal, grid)
print(f"Path: {path}")
