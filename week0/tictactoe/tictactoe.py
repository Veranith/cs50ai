"""
Tic Tac Toe Player
"""

import math
import copy

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

    # test = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn = 0
    for row in board:
        for col in row:
            if col == X:
                turn += 1
            elif col == O:
                turn -= 1
    if turn > 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    availableActions = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                availableActions.add((row, col))
    return availableActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    if i < 0 or i > 2 or j < 0 or j > 2 or board[i][j] != EMPTY:
        raise IndexError
    
    resultBoard = copy.deepcopy(board)
    resultBoard[i][j] = player(resultBoard)
    return resultBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winnerRow = checkWinnerRow(board)
    winnerCol = checkWinnerCol(board)
    winnerDiag = checkWinnerDiag(board)

    if X in [winnerRow, winnerCol, winnerDiag]:
        return X
    elif O in [winnerRow, winnerCol, winnerDiag]:
        return O
    else:
        return None


def checkWinnerRow(board):
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]
    return None

   
def checkWinnerCol(board):
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != None:
            return board[0][col]
    return None


def checkWinnerDiag(board):
    [(0,0),(1,1),(2,2)],
    [(0,2),(1,1),(2,0)]

    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    if result == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    curPlayer = player(board)
    
    moves = actions(board)

    if curPlayer == X:
        maxScore = -math.inf
        for move in moves:
            score = minValue(result(board,move))
            if score > maxScore:
                maxScore = score
                bestAction = move
    else:
        minScore = math.inf
        for move in moves:
            score = maxValue(result(board,move))
            if score < minScore:
                minScore = score
                bestAction = move
        
    return bestAction    


def minValue(state):
    if terminal(state):
        return utility(state)
    score = math.inf
    for action in actions(state):
        score = min(score, maxValue(result(state, action)))

    return score


def maxValue(state):
    if terminal(state):
        return utility(state)
    score = -math.inf

    for action in actions(state):
        score = max(score, minValue(result(state, action)))

    return score
