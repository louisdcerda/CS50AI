"""
Tic Tac Toe Player
"""

from ctypes import util
import math
import copy
from this import d
from tkinter import E

from numpy import moveaxis

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # count = 0

    # for i in range(len(board)):
    #     for j in range(len(board)):
    #         if board[i][j] == X:
    #             count += 1

    # if count == 5:
    #     return None
    
    # if count == 0:
    #     return X
    # elif count % 2 == 1:
    #     return X
    # else:
    #     return O


    countx = 0 
    counto = 0

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == X:
                countx += 1
            elif board[row][col] == O:
                counto += 1

    if not terminal(board) and countx == counto:
        return X
    elif countx > counto:
        return O 



    

    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    action = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                action.add((i, j))

    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise NameError("Invalid move")
    elif terminal(board):
        raise NameError("Game is over")
        
    newboard = copy.deepcopy(board)
    
    newboard[action[0]][action[1]] = player(board)

    return newboard




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] == X:
            return X
        elif board[row][0] == board[row][1] == board[row][2] == O:
            return O
    
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] == X:
            return X
        elif board[0][col] == board[1][col] == board[2][col] == O:
            return O

    
    if board[0][0] == board[1][1] == board[2][2] == X or board[0][2] == board[1][1] == board[2][0] == X:
        return X

    if board[0][2] == board[1][1] == board[2][0] == O or board[0][0] == board[1][1] == board[2][2] == O:
       return O

    return None             

def isTie(board):
    """
    Returns True if game is over, False otherwise.
    """

    if terminal(board) == True and utility(board) == 0:
        return True

    return False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                return False

    return True


    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0





def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if terminal(board) == True and utility(board) == 0:
    #     return None


    # for action in actions(board):
    #     if utility(result(board,action)) == 1 and player(result(board,action)) == X:
    #         return action
    #     elif utility(result(board,action)) == -1 and player(result(board,action)) == O:
    #         return action
    #     elif utility(result(board,action)) == 0:
    #         return minimax(result(board,action))



    # if terminal(board):
    #     return None

    # if player(board) == X:
    #     arr = []
    #     for action in actions(board):
    #         arr.append([min_val(result(board,action)), action])
    #     return sorted(arr, key=lambda x: x[0], reverse=True)[0][1]      
    # elif player(board) == O:
    #     arr = []
    #     for action in actions(board):
    #         arr.append([max_val(result(board,action)), action])
    #     return sorted(arr, key=lambda x: x[0])[0][1]


    if board == [[EMPTY]*3]*3:
        return (0,0)

    if player(board) == X:
        v = float("-inf")
        slected_action = None
        for action in actions(board):
            minValRes = min_val(result(board,action))
            if minValRes > v:
                v = minValRes
                slected_action = action

    elif player(board) == O:
        v= float("inf")
        selected_action = None
        for action in actions(board):
            maxValRes = max_val(result(board,action))
            if maxValRes < v:
                v = maxValRes
                slected_action = action

    return slected_action







def max_val(board):
    """
    Returns the maximum value of the current board
    """

    if terminal(board) == True:
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v = max(v, min_val(result(board,action)))
    return v

def min_val(board):
    """
    Returns the minimum value of the current board
    """

    if terminal(board) == True:
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, max_val(result(board,action)))

    return v

