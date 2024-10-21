function A_Star_Misplaced_Tiles(start_state, goal_state)
    open_list ← priority_queue containing start_state with f(start_state) = 0
    closed_list ← empty set
    g[start_state] ← 0
    parents[start_state] ← None

    while open_list is not empty:
        current_state ← state in open_list with lowest f(n)

        if current_state equals goal_state:
            return reconstruct_path(parents, current_state)

        remove current_state from open_list
        add current_state to closed_list

        for each neighbor of current_state:
            if neighbor is in closed_list:
                continue

            tentative_g ← g[current_state] + 1  # g(n) = depth of the node

            if neighbor is not in open_list or tentative_g < g[neighbor]:
                parents[neighbor] ← current_state
                g[neighbor] ← tentative_g
                f[neighbor] ← g[neighbor] + misplaced_tiles(neighbor, goal_state)

                if neighbor is not in open_list:
                    add neighbor to open_list with priority f[neighbor]

    return failure  # No solution found

function misplaced_tiles(state, goal_state)
    count ← 0
    for each tile in state:
        if tile is not in its correct position and tile is not blank:
            count ← count + 1
    return count

function reconstruct_path(parents, current_state)
    path ← empty list
    while current_state is not None:
        add current_state to path
        current_state ← parents[current_state]
    return reverse(path)
