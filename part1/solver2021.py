#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall, January 2021
#

import sys
from heapq import *

ROWS=4
COLS=5

#prints board in pretty format
def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

""" 
def successors(state):
Returns a list of possible successor states
we are generating board for each of the rows columns with respective directions
and appending it to successors list. This list is returned at the end
"""
def successors(state):
    successors=[]

    #L1
    LOneState=state.copy()
    temp = LOneState[0]
    for i in range(0,4):
        LOneState[i]=LOneState[i+1]
    LOneState[4]=temp
    successors.append(LOneState)

    #L3
    LThState=state.copy()
    temp=LThState[10]
    for i in range(10,14):
        LThState[i]=LThState[i+1]
    LThState[14] = temp
    successors.append(LThState)

    #R2
    RTwoState=state.copy()
    temp=RTwoState[9]
    for i in range(9,5,-1):
        RTwoState[i]=RTwoState[i-1]
    RTwoState[5] = temp
    successors.append(RTwoState)

    #R4
    RFoState=state.copy()
    temp=RFoState[19]
    for i in range(19,15,-1):
        RFoState[i]=RFoState[i-1]
    RFoState[15] = temp
    successors.append(RFoState)

    #U1
    UpOneState=state.copy()
    temp=UpOneState[0]
    for i in range(0,15,5):
        UpOneState[i]=UpOneState[i+5]
    UpOneState[15] = temp
    successors.append(UpOneState)

    #U3
    UpThState=state.copy()
    temp=UpThState[2]
    for i in range(2,17,5):
        UpThState[i]=UpThState[i+5]
    UpThState[17] = temp
    successors.append(UpThState)

    #U5
    UpFivState=state.copy()
    temp=UpFivState[4]
    for i in range(4,19,5):
        UpFivState[i]=UpFivState[i+5]
    UpFivState[19] = temp
    successors.append(UpFivState)

    #D2
    DTwoState=state.copy()
    temp=DTwoState[16]
    for i in range(16,1,-5):
        DTwoState[i]=DTwoState[i-5]
    DTwoState[1] = temp
    successors.append(DTwoState)

    #D4
    DFoState=state.copy()
    temp=DFoState[18]
    for i in range(18,3,-5):
        DFoState[i]=DFoState[i-5]
    DFoState[3] = temp
    successors.append(DFoState)

    return successors

"""
def is_goal(state):
check if we've reached the goal, to check if state is in canonical form
"""
def is_goal(state):
    for i in range(0,20):
        if(state[i]!=i+1):
            return False
    return True

"""
def heuristic(state):
heuristic function that returns cost of state, which is sum of absolute differences of current position
of element and its goal position calculated for each element in state
"""
def heuristic(state):
    cost = 0
    for i in range(0, len(state)):
        if(abs(state[i] -(i+1))!=0):
            cost+=abs(state[i] -(i+1))
    return cost/200

"""
def returnMove(fromState,toState):
returns the move to be done from fromstate to tostate which could be one of
 L1, L3, R2, R4, U1, U3, U5, D2, D4
"""
def returnMove(fromState,toState):
    if(fromState[0]==toState[4]):
        return "L1,"
    if(fromState[10] == toState[14]):
        return "L3,"
    if(fromState[9] == toState[5]):
        return "R2,"
    if(fromState[19] == toState[15]):
        return "R4,"
    if(fromState[0] == toState[15]):
        return "U1,"
    if(fromState[2] == toState[17]):
        return "U3,"
    if(fromState[4] == toState[19]):
        return "U5,"
    if(fromState[16] == toState[1]):
        return "D2,"
    if(fromState[18] == toState[3]):
        return "D4,"

"""
def solve(initial_board):
Solve function starts from initial board, maintains a fringe with cost, board and path
the state in fringe with least cost(returned by heuristic function) is popped, checked if we have reached
the goal state, else, successors are explored if not already visited, cost state and updated path
is added to fringe.
This continued until fringe is empty, if no solution found [] returned
"""
def solve(initial_board):
    fringe=[]
    path=""
    fringe=[(0,initial_board,path)]
    visited=[]
    heapify(fringe)
    while fringe:
        (priority, state, path) = heappop(fringe)
        visited.append(state)
        if is_goal(state):
            return path[:-1].split(",")
        else:
            for s in successors(state):
                data = (heuristic(s),s,path+returnMove(state,s))
                if s not in visited:
                    heappush(fringe, data)
    return []

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(start_state)
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))