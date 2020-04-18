"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None
best_action = []

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
    count = 0
    #traverse through each element of the board
    for elem in board:
        for e in elem:
            if e == EMPTY:
                count = count + 1
    #if the number of chances left are odd, it's X's turn, otherwise it's O's turn    
    if count % 2 == 1:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #if the state is a terminal state, then there is no possible action
    if terminal(board):
        return "game over"
    else:
        #traverse through the board and add the location of empty cells to the possible_actions
        possible_actions = []
        for row in range(0, 3):
            for cell in range(0, 3):
                if board[row][cell] is None:
                    possible_actions.append([row, cell])
        return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #make a deep copy if the board so that the original board doesn't change
    m_board = copy.deepcopy(board)
    [i, j] = action
    if m_board[i][j] is None:
        m_board[i][j] = player(board)
        return m_board
    else:
        # the move is not possible , the position may be already occupied
        raise Exception



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # make a deep copy and convert to numpy array
    w_board = copy.deepcopy(board)
    w_board = np.array(w_board)
    
    #check for the rows
    for row in w_board:
        if len(set(row)) == 1:
            return row[0]

    # check for the columns
    for row in np.transpose(w_board):
        if len(set(row)) == 1:
            return row[0]
    
    # check for the first diagonal
    if len(set(np.diagonal(w_board))) == 1:
        return np.diagonal(w_board)[0]

    # check for the second diagonal
    if len(set(np.fliplr(w_board).diagonal())) == 1:
        return np.fliplr(w_board).diagonal()[0]

    # return None if the game is in progress or if no one wins    
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner or if the game board is fully occupied, return true, otherwise return false
    if winner(board) == 'X' or winner(board) == 'O':
        return True
    elif not any(None in x for x in board):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the board is in terminal state , return None
    if terminal(board):
        return None
    else:
        if player(board) == 'X':
            # maximize the utility and return the best possible move for X
            return maxvalue(board, best_action)[1]
        else:
            # minimize the utility and return the best possible move for O
            return minvalue(board, best_action)[1]

def maxvalue(board, best_action):

    if terminal(board):
        return [utility(board), best_action]

    v= -math.inf
    V = -math.inf
    
    # traverse through all actions and get the best possible action which gives maximum value of minvalue
    for action in actions(board):
        V = max(v, minvalue((result(board, action)), best_action)[0])
        if V > v:
            v = V
            best_action = action

    return [v, best_action]

def minvalue(board, best_action):

    if terminal(board):
        return [utility(board), best_action]

    v = math.inf
    V = math.inf

    # traverse through all actions and get the best possible action which gives minimum value of maxvalue
    for action in actions(board):
        V = min(v, maxvalue((result(board, action)), best_action)[0])
        if V < v:
            v = V
            best_action = action

    return [v, best_action]
