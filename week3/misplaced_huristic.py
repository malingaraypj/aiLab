from queue import PriorityQueue

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.g = 0  # Cost from start to this node
        self.f = 0  # Total estimated cost (g + h)

    def path(self):
        node = self
        result = []
        while node:
            result.append(node.state)
            node = node.parent
        return result[::-1]

    def __lt__(self, other):
        return self.f < other.f  # Comparison for priority queue

def misplaced_tiles(state, goal_state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                count += 1
    return count

def get_neighbors(state):
    neighbors = []
    zero_pos = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
    x, y = zero_pos

    # Possible moves: up, down, left, right
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for new_x, new_y in directions:
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in state]  # Deep copy the state
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def a_star(start_state, goal_state):
    open_list = PriorityQueue()
    closed_list = set()
    start_node = Node(start_state)
    start_node.g = 0
    start_node.f = misplaced_tiles(start_state, goal_state)
    open_list.put((start_node.f, start_node))
    
    while not open_list.empty():
        current_node = open_list.get()[1]

        if current_node.state == goal_state:
            return current_node.path()

        closed_list.add(tuple(map(tuple, current_node.state)))

        for neighbor in get_neighbors(current_node.state):
            if tuple(map(tuple, neighbor)) in closed_list:
                continue
            
            tentative_g = current_node.g + 1
            neighbor_node = Node(neighbor, current_node)
            neighbor_node.g = tentative_g
            neighbor_node.f = neighbor_node.g + misplaced_tiles(neighbor, goal_state)

            if not any(neighbor_node.f < n.f and n.state == neighbor for _, n in open_list.queue):
                open_list.put((neighbor_node.f, neighbor_node))

    return None  # No solution found

def get_input_state(prompt):
    while True:
        try:
            print(prompt)
            state = []
            for i in range(3):
                row = list(map(int, input(f"Enter row {i + 1} (space-separated, use 0 for empty): ").strip().split()))
                if len(row) != 3:
                    raise ValueError("Each row must contain exactly 3 numbers.")
                state.append(row)
            return state
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    start_state = get_input_state("Enter the initial state of the 8-puzzle:")
    goal_state = get_input_state("Enter the goal state of the 8-puzzle:")

    solution = a_star(start_state, goal_state)
    if solution:
        print("Solution Path:")
        for step in solution:
            for row in step:
                print(row)
            print()  # Print a blank line between steps
    else:
        print("No solution found.")
