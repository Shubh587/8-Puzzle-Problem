#!/usr/bin/python3
# Developer: Shubh Savani

import argparse
import copy
import sys
from queue import Queue


# Output Solution Arc
def print_state(state):
    for row in range(len(state)):
        for col in range(len(state[row])):
            print(state[row][col], end=" ")
        print()


def print_blank_tile_actions(sequence):
    print("{", end="")
    for ind in range(len(sequence)):
        action = sequence[ind]
        if ind == len(sequence) - 1:
            print(action, end="")
        else:
            print(action, end=", ")
    print("}")


def print_f_values(values):
    print("{", end="")
    for ind in range(len(values)):
        value = values[ind]
        if ind == len(values) - 1:
            print(value, end="")
        else:
            print(value, end=", ")
    print("}")


def output_solution(initial, goal, depth, num_generated, blank_tile_actions, fn_vals):
    print("Initial State:")
    print_state(initial)
    print("Goal State:")
    print_state(goal)
    print(f"Depth of Shallowest Node found by the A* Search Algorithm: {depth}")
    print(f"Number of Nodes Generated by A* Search Algorithm: {num_generated}")
    print("Sequence of Actions by the Blank Tile: ", end="")
    print_blank_tile_actions(blank_tile_actions)
    print("F(n) Values for each State in the Solution Path: ", end="")
    print_f_values(fn_vals)


def write_output_file(input_file_name, initial, goal, depth, num_generated, blank_tile_actions, fn_vals, is_h1_used):
    input_num = int(input_file_name[5])
    heuristic_used = ("h2", "h1")[is_h1_used]
    output_file_name = f"output{input_num}{heuristic_used}.txt"
    sys.stdout = open(output_file_name, "w")

    # Print out the solution info in the correct format
    output_solution(initial, goal, depth, num_generated, blank_tile_actions, fn_vals)


# A* Search Arc

def determine_blank_tile_action(parent, child):
    # Find blank tile position in the parent state
    parent_pos = find_blank_pos(parent)
    child_pos = find_blank_pos(child)

    # Calculate the difference in the x and y positions
    x_diff = child_pos[0] - parent_pos[0]
    y_diff = child_pos[1] - parent_pos[1]

    # output the action based on the x_diff and y_diff values
    if x_diff == -1:
        return 'U'
    elif x_diff == 1:
        return 'D'
    elif y_diff == -1:
        return 'L'
    elif y_diff == 1:
        return 'R'


def search_solution_path(initial, goal, eval_func):
    frontier = Queue()
    reached = []
    evaluated = {}
    eval_scores = {}
    solution_path = []
    blank_tile_sequence = []

    order = 1
    level = 0
    goal_found = False
    goal_state_score = 0
    is_h1_used = eval_func

    # Enqueue initial's children onto frontier
    # 1. Find the neighbors of the initial state
    neighborhood = find_neighbors(initial)
    # 2. Generate child states given neighborhood info
    children = generate_child_states(initial, neighborhood)
    # 3. Place initial state into the solution path
    solution_path.append((order, initial, level))
    # 4. Add the initial state to the dictionary of evaluated states
    evaluated[order] = (initial, level)
    # 5. Increment level and order by 1
    level += 1
    order += 1
    # 6. Enqueue each child, with it's respective order, onto frontier
    for child in children:
        order_child_pair = order, child, level
        frontier.put(order_child_pair)
        order += 1

    # Traverse through each node in the queue.
    # Use eval function as heuristic for determining which node to place in solution path
    # Generate children of selected node
    while not goal_found:
        while not frontier.empty():
            # Get the state from frontier
            entry_pair = frontier.get()
            state_order = entry_pair[0]
            state = entry_pair[1]
            state_level = entry_pair[2]
            # Evaluate the state using f(n) and store order/score pair in eval_scores
            m_dist = calculate_h1_score(state, goal)
            if is_h1_used:
                state_score = m_dist
            else:
                state_score = calculate_h2_score(state, goal, m_dist)
            # Check if the state is the goal state
            if state_score == goal_state_score:
                # If found, then add the goal state to the solution path
                solution_path.append(entry_pair)
                # Set goal_found to True
                goal_found = True
                # Break out of the loop
                break
            eval_scores[state_order] = state_score

            # Place state in the placeholder in case we need to access the state again
            evaluated[state_order] = (state, state_level)

        # Break from the loop if the goal node was found
        if goal_found:
            # Find the depth of the solution path
            depth = solution_path[len(solution_path) - 1][2]
            # Calculate the number of nodes generated
            num_generated = len(evaluated.keys())
            # Find the sequence of moves the blank tile took throughout the solution path
            for ind in range(1, len(solution_path)):
                parent_state = solution_path[ind - 1][1]
                child_state = solution_path[ind][1]
                action = determine_blank_tile_action(parent_state, child_state)
                blank_tile_sequence.append(action)
            # Calculate the scores of each node in the solution path
            scores = []
            for node_info in solution_path:
                state = node_info[1]
                m_dist = calculate_h1_score(state, goal)
                score = 0
                if is_h1_used:
                    score = m_dist
                else:
                    score = calculate_h2_score(state, goal, m_dist)
                scores.append(score)
            return depth, num_generated, blank_tile_sequence, scores, is_h1_used

        # Traverse through each score and see which one is the minimum score
        min_info = -1, sys.maxsize  # initialize to the maximum size an integer can have in Python
        for order in eval_scores.keys():
            state_score = eval_scores[order]
            min_score = min_info[1]
            if state_score < min_score:
                min_info = order, state_score

        # Once min_info is found, check if min_state's level in the tree <= level of last elem in solution path
        min_level = evaluated[min_info[0]][1]
        prev_level = solution_path[len(solution_path) - 1][2]
        if min_level <= prev_level:
            # Clear the solution path
            # Remove all the states in the solution that are greater than or equal to the level of min_state
            solution_path_level = min_level
            while solution_path_level <= prev_level:
                solution_path.pop()
                solution_path_level += 1

        # Generate min_state's children
        # Retrieve the min_state matrix from evaluated
        min_state = evaluated[min_info[0]][0]
        # 1. Find the neighborhood of the min_state
        min_state_neighborhood = find_neighbors(min_state)
        # 2. Pass in the neighborhood and the min_state into generate children func
        min_state_children = generate_child_states(min_state, min_state_neighborhood)
        # Increment the level of the tree
        child_level = min_level + 1
        for child in min_state_children:
            # Increment the order of the child generated
            order += 1
            # Check if the child is not in evaluated
            found = False
            for state_level_pair in evaluated.values():
                state = state_level_pair[0]
                if child == state:
                    found = True
                    break
            if not found:
                # Add child to frontier
                frontier.put((order, child, child_level))

        # Add min_state to the solution path
        min_order = min_info[0]
        solution_path.append((min_order, min_state, min_level))

        # Delete min_state from eval_scores
        del eval_scores[min_order]

        # Add min_order to reached
        reached.append(min_order)


# Evaluation Functions Arc

def find_goal_pos(goal_state):
    goal_pos = {}
    # Run through each tile in the goal state to store the pos of each number
    for row in range(len(goal_state)):
        for col in range(len(goal_state[row])):
            tile_num = goal_state[row][col]
            goal_pos[tile_num] = (row, col)
    return goal_pos


def calculate_h1_score(state, goal):
    goal_pos = find_goal_pos(goal)
    # Run through each tile in the state
    # and calculate the Manhattan Distance between state pos and goal pos for each tile
    h1_val = 0
    for row in range(len(state)):
        for col in range(len(state[row])):
            tile_num = state[row][col]
            desired_pos = goal_pos[tile_num]
            # print("Tile Num: ", tile_num)
            # print("Goal Position: ", desired_pos)
            # print("Curr Position: ", (row, col))
            delta_y = abs(desired_pos[1] - col)
            delta_x = abs(desired_pos[0] - row)
            manhattan_distance = delta_y + delta_x
            # print("Manhattan Distance: ", manhattan_distance)
            # print()
            h1_val += manhattan_distance
    return h1_val


def calculate_border_score(state, goal):
    state_border = {}
    goal_border = {}
    score = 0

    # Fill the state_border and goal_border dictionaries with their tile and successor pairs
    for row in range(len(state)):
        for col in range(len(state[row])):
            state_tile_num = state[row][col]
            goal_title_num = goal[row][col]
            state_successor = None
            goal_successor = None
            curr_pos = row, col
            if curr_pos == (0, 0):
                state_successor = state[0][1]
                goal_successor = goal[0][1]
            elif curr_pos == (0, 1):
                state_successor = state[0][2]
                goal_successor = goal[0][2]
            elif curr_pos == (0, 2):
                state_successor = state[1][2]
                goal_successor = goal[1][2]
            elif curr_pos == (1, 2):
                state_successor = state[2][2]
                goal_successor = goal[2][2]
            elif curr_pos == (2, 2):
                state_successor = state[2][1]
                goal_successor = goal[2][1]
            elif curr_pos == (2, 1):
                state_successor = state[2][0]
                goal_successor = goal[2][0]
            elif curr_pos == (2, 0):
                state_successor = state[1][0]
                goal_successor = goal[1][0]
            elif curr_pos == (1, 0):
                state_successor = state[0][0]
                goal_successor = goal[0][0]
            elif curr_pos == (1, 1):
                continue
            state_border[state_tile_num] = state_successor
            goal_border[goal_title_num] = goal_successor
    # Calculate the border score by finding non-matches between the state and goal border dictionaries
    # print(state_border)
    # print(goal_border)
    # print()
    for ind in range(9):
        title_num = str(ind)
        if title_num not in state_border.keys() or title_num not in goal_border:
            continue
        if state_border[title_num] != goal_border[title_num]:
            score += 2
    return score


def calculate_center_piece_score(state, goal):
    return (1, 0)[goal[1][1] == state[1][1]]


def calculate_h2_score(state, goal, h1_score):
    p_n = h1_score
    border_score = calculate_border_score(state, goal)
    center_piece_score = calculate_center_piece_score(state, goal)
    # print("Border Score: ", border_score)
    # print("Center Piece Score: ", center_piece_score)
    # print()
    s_n = border_score + center_piece_score
    return p_n + 3 * s_n


# def calculate_fn_score(state, goal):
#     h1_score = calculate_h1_score(state, goal)
#     h2_score = calculate_h2_score(state, goal, h1_score)
#     return h1_score + h2_score


# Generating Child States Arc
def find_blank_pos(state):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == '0':
                return row, col  # returns the position of the blank tile for the find_neighbor functions
    return -1, -1  # returns -1,-1 if the blank tile is not found


def find_neighbors(state):
    neighborhood = []  # stores the indices of the blank position and its neighbors in the state

    # Append the position of the blank tile into neighborhood
    blank_tile_pos = find_blank_pos(state)
    if blank_tile_pos == (-1, -1):
        raise ValueError("Invalid input file. State must have a blank position")
    else:
        neighborhood.append(blank_tile_pos)

    # Find it's neighbors based on the position of the blank tile
    # Handle all the corner pieces
    if blank_tile_pos == (0, 0):
        neighborhood.append([(1, 0), (0, 1)])
    elif blank_tile_pos == (0, 2):
        neighborhood.append([(0, 1), (1, 2)])
    elif blank_tile_pos == (2, 2):
        neighborhood.append([(1, 2), (2, 1)])
    elif blank_tile_pos == (2, 0):
        neighborhood.append([(1, 0), (2, 1)])
    # Handle the rest of the border pieces
    if blank_tile_pos == (0, 1):
        neighborhood.append([(0, 0), (0, 2), (1, 1)])
    elif blank_tile_pos == (1, 2):
        neighborhood.append([(0, 2), (1, 1), (2, 2)])
    elif blank_tile_pos == (2, 1):
        neighborhood.append([(2, 0), (2, 2), (1, 1)])
    elif blank_tile_pos == (1, 0):
        neighborhood.append([(0, 0), (2, 0), (1, 1)])
    # Handle the center piece
    if blank_tile_pos == (1, 1):
        neighborhood.append([(1, 0), (0, 1), (1, 2), (2, 1)])
    return neighborhood


def generate_child_states(parent, neighborhood):
    children = []
    for neighbor in neighborhood[1]:
        child = copy.deepcopy(parent)
        child[neighborhood[0][0]][neighborhood[0][1]], child[neighbor[0]][neighbor[1]] = child[neighbor[0]][
                                                                                             neighbor[1]], \
                                                                                         child[neighborhood[0][0]][
                                                                                             neighborhood[0][1]]
        children.append(child)
    return children


# Reading the Input File Arc
def determine_heuristic(eval_func):
    return eval_func == "h1"


def file_reader(file_name):
    states = []
    file = open(file_name)
    for i in range(7):
        line = file.readline()
        row = line.split()
        states.append(row)
    return states


# MAIN METHOD
def main():
    # Get the input file name from the cmd command
    parser = argparse.ArgumentParser(description='Solve 8-Puzzle Problem with A* Search Algorithm with graph search')
    parser.add_argument('filename', help='The input file containing the initial and goal state')
    parser.add_argument('heuristic', help='Which heuristic function to use for the A* search algorithm')
    cmdline = parser.parse_args()
    input_file = cmdline.filename
    heuristic_func = cmdline.heuristic
    is_h1_used = determine_heuristic(heuristic_func)
    # print(input_file)

    # Read the input file and parse the file for the initial state and the goal state
    world = file_reader(input_file)
    initial_state = world[:3]
    goal_state = world[4:]

    # Pass both states into the A* Search algorithm to find the solution path information
    solution_info = search_solution_path(initial_state, goal_state, is_h1_used)
    depth = solution_info[0]
    num_generated = solution_info[1]
    sequence = solution_info[2]
    scores = solution_info[3]
    is_h1_used = solution_info[4]

    # Write output of the program to a file
    write_output_file(input_file, initial_state, goal_state, depth, num_generated, sequence, scores, is_h1_used)


if __name__ == "__main__":
    main()

# ra0Eequ6ucie6Jei0koh6phishohm9
