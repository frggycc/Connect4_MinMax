import numpy
import random
from ConnectFour import winning_move, get_valid_columns, next_free_row, place_piece, board_full

ROWS = 6
COLUMNS = 7
PLAYER = 1
COMPUTER = 2
EMPTY = 0

def score_position(board):
    score = 0

    evaluation_board = numpy.array([[3, 4, 5,  7,  5,  4, 3],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [3, 4, 5,  7,  5,  4, 3]])
    
    # Calculate the scores of the player and the opponent
    computer_score = numpy.sum(evaluation_board[board == COMPUTER])
    player_score   = numpy.sum(evaluation_board[board == PLAYER])

    return computer_score - player_score

def is_end_of_game(board):
    return winning_move(board, COMPUTER) or winning_move(board, PLAYER) or (board_full(board) == True)

'''
Manimax algortihm is implemented here!
Uses recursion of this functions to think x steps ahead. The number
of steps ahead that the computer will "think" is based off of diffciulty
set by the player. Lower the depth, the easier the game.
'''
def minimax(board, depth, alpha, beta, max_player):
    valid_locations  = get_valid_columns(board)
    is_terminal_move = board_full(board)

    '''
    If the depth is zero or maximum depth is reached, then the game
    is over or no more calculations will be done due to the difficulty set.
    '''
    if depth == 0 or is_terminal_move:
        if is_terminal_move:
            if winning_move(board, COMPUTER):
                return (None, 100000)
            elif winning_move(board, PLAYER):
                return (None, -100000)
            else:
                return (None, 0)
            
        else:
            return (None, score_position(board))
        
    # Maximize computer
    if max_player:
        value  = -100000
        column = random.choice(valid_locations)

        for col in valid_locations:
            row        = next_free_row(col, board)
            temp_board = board.copy()
            place_piece(row, col, COMPUTER, temp_board)

            # Calculate a score based on the position of the dropped piece
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value  = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return column, value
    
    # Minimizing player
    else:
        value  = 100000
        column = random.choice(valid_locations)

        for col in valid_locations:
            row        = next_free_row(col, board)
            temp_board = board.copy()
            place_piece(row, col, PLAYER, temp_board)

            # Calculate a score based on the position of the dropped piece
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value  = new_score
                column = col

            alpha = min(alpha, value)
            if alpha >= beta:
                break

        return column, value

