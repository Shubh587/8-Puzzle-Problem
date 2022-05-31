# 8-Puzzle-Problem
Implemented A* search algorithm with graph search (with no repeated states) for solving the 8-Puzzle Problem with heuristic functions h1(n) and h2(n). h1(n) is the sum of Manhattan distances of the tiles from their goals. h2(n) is the Nilsson's sequence score defined as P(n) + 3S(n), where P(n) is the Manhattan distances of the tiles from their goal states and S(n) is a piecewise function that depends on the border positions and the center piece position.

Compilation Instructions:
1.	In the terminal type the command: python project1.py InputA.txt hB, where A is the number associated with the input file and B is the number associated with the heuristic function you want to use.
2.	For instance, to run the algorithm on Input1.txt using the h2 heuristic function, the following command would be typed and entered into the terminal: python project1.py Input1.txt h2
3.	This will create an output text file in the same directory indicating which input file was used and which heuristic function was used. 


Output Files for Given States:

Output1h1.txt
Initial State:
4 1 6 

8 3 5 

2 0 7 
Goal State:
8 4 6 

0 1 5 

2 3 7 
Depth of Shallowest Node found by the A* Search Algorithm: 4
Number of Nodes Generated by A* Search Algorithm: 11
Sequence of Actions by the Blank Tile: {U, U, L, D}
F(n) Values for each State in the Solution Path: {6, 4, 4, 2, 0}

Output2h1.txt
Initial State:
4 1 6 
8 3 5 
2 0 7 
Goal State:
8 4 6 
0 1 5 
2 3 7 
Depth of Shallowest Node found by the A* Search Algorithm: 4
Number of Nodes Generated by A* Search Algorithm: 12
Sequence of Actions by the Blank Tile: {L, R, L, D}
F(n) Values for each State in the Solution Path: {33, 21, 22, 20, 0}

Output1h2.txt
Initial State:
2 6 0 
1 3 7 
4 5 8 
Goal State:
1 2 0 
7 5 3 
4 8 6 
Depth of Shallowest Node found by the A* Search Algorithm: 36
Number of Nodes Generated by A* Search Algorithm: 219
Sequence of Actions by the Blank Tile: {L, L, D, R, U, L, R, U, L, R, U, D, U, D, R, U, L, D, L, U, R, R}
F(n) Values for each State in the Solution Path: {10, 10, 10, 10, 10, 10, 10, 8, 8, 8, 6, 6, 8, 6, 8, 6, 4, 6, 6, 6, 4, 2, 0}

Output2h2.txt
Initial State:
2 6 0 
1 3 7 
4 5 8 
Goal State:
1 2 0 
7 5 3 
4 8 6 
Depth of Shallowest Node found by the A* Search Algorithm: 16
Number of Nodes Generated by A* Search Algorithm: 101
Sequence of Actions by the Blank Tile: {L, D, R, U, L, D, D, R, U, U, D, R, R, U}
F(n) Values for each State in the Solution Path: {49, 43, 45, 43, 41, 23, 37, 40, 38, 36, 39, 33, 19, 20, 0}

Output3h2.txt
Initial State:
8 6 3 
0 4 5 
7 2 1 
Goal State:
1 2 3 
4 0 7 
6 5 8 
Depth of Shallowest Node found by the A* Search Algorithm: 43
Number of Nodes Generated by A* Search Algorithm: 172
Sequence of Actions by the Blank Tile: {U, R, D, D, R, L, U, R, D, L, U, L, U, R, D, D, U, D, U, D, U, U, L, D, R, D, L, L, U, U, R, D}
F(n) Values for each State in the Solution Path: {59, 53, 51, 48, 51, 51, 45, 46, 49, 49, 49, 44, 41, 41, 33, 36, 37, 31, 37, 31, 37, 31, 33, 31, 26, 23, 23, 21, 21, 19, 19, 11, 0}
