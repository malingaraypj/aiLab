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

def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Skip the empty space
                goal_pos = [(index, row.index(state[i][j])) for index, row in enumerate(goal) if state[i][j] in row][0]
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance

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
    start_node = Node(start, 0, manhattan_distance(grid, goal))
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
            h_cost = manhattan_distance(grid, goal)
            neighbor_node = Node(neighbor_pos, g_cost, h_cost)
            neighbor_node.parent = current_node
            if all(neighbor_node.position != node.position or neighbor_node.g < node.g for node in open_list):
                heapq.heappush(open_list, neighbor_node)
    return None

def get_grid_from_input():
    grid = []
    print("Enter the initial state (3x3 grid) with 0 for the empty space:")
    for i in range(3):
        row = list(map(int, input(f"Enter row {i + 1} (space-separated): ").strip().split()))
        if len(row) != 3:
            raise ValueError("Each row must contain exactly 3 numbers.")
        grid.append(row)
    return grid

def get_goal_from_input():
    goal = []
    print("Enter the goal state (3x3 grid):")
    for i in range(3):
        row = list(map(int, input(f"Enter row {i + 1} (space-separated): ").strip().split()))
        if len(row) != 3:
            raise ValueError("Each row must contain exactly 3 numbers.")
        goal.append(row)
    return goal

if __name__ == "__main__":
    grid = get_grid_from_input()
    goal = get_goal_from_input()
    start = [(i, row.index(0)) for i, row in enumerate(grid) if 0 in row][0]

    path = a_star(start, goal, grid)
    if path:
        print("Path to goal:", path)
    else:
        print("No solution found.")
