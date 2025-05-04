import numpy
import random
from ConnectFour import winning_move, get_valid_columns, next_free_row, place_piece, board_full

ROWS = 6
COLUMNS = 7
PLAYER = 1
COMPUTER = 2
EMPTY = 0

'''
Score Position: Our evaluation function based on two facotrs
1. Dropping into a desirable a position:
   is. There are many more oppurtunities for a winning move if a piece
   lands in the center rather than somewhere like the corner.
2. Potentential winning lines:
   Dropping a piece into a column where a 2-in-a-row is made is more 
   desirable than dropping a piece into a position where it's alone. Same
   goes for dropping a piece into a 3-in-a-row; It's more desirable than
   dropping it into a 2-in-a-row
'''
def score_position(board, piece):
    score = 0
    opponent_piece = PLAYER
    
    def count_lines(player, x_in_a_row):
        count = 0

        # Horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - x_in_a_row + 1):
                if all(board[row][col + i] == player for i in range(x_in_a_row)):
                    count += 1
        # Vertical
        for row in range(ROWS - x_in_a_row + 1):
            for col in range(COLUMNS):
                if all(board[row + i][col] == player for i in range(x_in_a_row)):
                    count += 1
        # Diagonal (positive)
        for row in range(ROWS - x_in_a_row + 1):
            for col in range(COLUMNS - x_in_a_row + 1):
                if all(board[row + i][col + i] == player for i in range(x_in_a_row)):
                    count += 1
        # Diagonal (negative)
        for row in range(x_in_a_row - 1, ROWS):
            for col in range(COLUMNS - x_in_a_row + 1):
                if all(board[row - i][col + i] == player for i in range(x_in_a_row)):
                    count += 1
        return count

    # Certain piece positions have advantage
    evaluation_board = numpy.array([[3, 4, 5,  7,  5,  4, 3],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [3, 4, 5,  7,  5,  4, 3]])
    
    # Better score if their pieces are in desirable positions
    piece_score      = numpy.sum(evaluation_board[board == piece])
    opponent_score   = numpy.sum(evaluation_board[board == opponent_piece])

    # Calculate points for current piece (COMPUTER) based on winning lines
    score += count_lines(COMPUTER, 3) * 100
    score += count_lines(COMPUTER, 2) * 75

    # Calculate points opponent (PLAYER) based on winning lines
    score -= count_lines(PLAYER, 3) * 90
    score -= count_lines(PLAYER, 2) * 60

    # Consider the positions of each individual piece
    score += piece_score - opponent_score

    return score

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
            return (None, score_position(board, COMPUTER))
        
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

            beta = min(beta, value)
            if alpha >= beta:
                break

        return column, value

