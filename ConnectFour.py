import numpy
from computer import *

# Set up boards with zeros
ROWS = 6
COLUMNS = 7
PLAYER = 1
COMPUTER = 2
EMPTY = 0

def create_board():
    return numpy.zeros((ROWS, COLUMNS), dtype=int)

def print_board(board):
    print("  0   1   2   3   4   5   6")
    print("_" * 29)
    for row in range(ROWS - 1, -1, -1):
        print("|", end="")
        for column in range(COLUMNS):
            if board[row][column] == EMPTY:
                print("   ", end="|")
            elif board[row][column] == PLAYER:
                print(" X ", end="|")
            else:
                print(" O ", end="|")
        print("")
    print("-" * 29)

# Run after running checks (valid place AND next free row)
def place_piece(row, col, player, board):
    board[row][col] = player

# Check if column is full or not ([col - 1][row - 1] == 0, then OK)
def valid_placement(col, board):
    # Top row of column still empty = stil have space
    if board[ROWS - 1][col] == EMPTY:
        return True
    else:
        return False
    
'''
Returns a list of columns that are still valid to place a piece in.
'''
def get_valid_columns(board):
    valid_columns = []
    for col in range(COLUMNS):
        if board[ROWS - 1][col] == EMPTY:
            valid_columns.append(col)

    return valid_columns

'''
Assuming valid_placement checked, have piece land in next available 
row from the bottom.
'''
def next_free_row(col, board):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            return row
        
'''
TODO
Default depth set to 2: Currently, too easy and AI ends up only
picking center columns rather than picking based on winning lines
'''
def pick_best_move(board, player):
    depth = 4

    # Computer is the maximizing player
    if player == COMPUTER:
        column, minimax_score = minimax(board, depth, -100000, 100000, True)
    else:
        column, minimax_score = minimax(board, depth, -100000, 100000, False)

    return column

'''
Check if game won with the last move.
'''
def winning_move(board, player):
    # Check for horizontal win
    for col in range(COLUMNS - 3):
        for row in range(ROWS):
            if (
                board[row][col] == player and 
                board[row][col + 1] == player and 
                board[row][col + 2] == player and
                board[row][col + 3] == player
                ):
                return True

    # Check for vertical win    
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (
                board[row][col] == player and 
                board[row + 1][col] == player and 
                board[row + 2][col] == player and
                board[row + 3][col] == player
                ):
                return True
            
    # Diagonal win, positive
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if (
                board[row][col] == player and 
                board[row + 1][col + 1] == player and 
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player
                ):
                return True

    # Diagonal win, negative
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):
            if (
                board[row][col] == player and 
                board[row - 1][col + 1] == player and 
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player
                ):
                return True
            
    return False

'''
Check if the board is full but no one had won.
'''
def board_full(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            if(board[row][col] == 0):
                return False
            
    return True

def main():
    # Create board and establish turn
    board = create_board()
    turn  = None

    # Set bool values to false
    valid_move   = False
    winner_found = False
    
    # Decide who will go first
    while True:
        first = input("Who will go first? \nPlayer (P) or computer (C)?: ")
        if first == "p" or first == "P":
            print("Player will go first! You are X pieces.")
            turn = PLAYER
            break
        elif first == "C" or first == "c":
            print("Computer will go first! You are O pieces.")
            turn = COMPUTER
            break
        else:
            print("Please enter P or C. \n")

    # At this point, you've decided who goes first
    while not winner_found and (not board_full(board)):
        if turn == PLAYER:
            print("")
            print_board(board)
            print("PLAYER ONE'S turn - X Pieces")

            # reset valid_move value
            valid_move = False
            while not valid_move:
                col = int(input("Choose a column: "))
                if col >= COLUMNS or col < 0:
                    print("Choose a number between 0 and 6")
                    continue

                # Check if valid placement
                if valid_placement(col, board):
                    valid_move = True
                else:
                    print("Column is full. Choose another column.")

            # Place piece
            row = next_free_row(col, board)
            place_piece(row, col, turn, board)

            # Check if winner
            if winning_move(board, turn):
                print_board(board)
                print("CONGRATS PLAYER 1! YOU WIN!")
                winner_found = True
            
            ''' 
            TODO: Change "winner_found" to game over since a tie is possible; 
            avoid having two variables to dstinguish if winner is found or tie occurs
            '''
            # Check if board is full but no winner --> Tie
            if not winner_found and board_full(board):
                print_board(board)
                print("It's a draw!")
                winner_found = True

            # Change players
            turn = COMPUTER

        else:
            # AI using minimax to pick the best move based on the depth set
            col = pick_best_move(board, COMPUTER)
            row = next_free_row(col, board)
            place_piece(row, col, COMPUTER, board)

            print_board(board)
            print("COMPUTER placed piece in column ", col)

            # Check if winner
            if winning_move(board, turn):
                print_board(board)
                print("CONGRATS PLAYER 1! YOU WIN!")
                winner_found = True
            
            ''' 
            TODO: Change "winner_found" to game over since a tie is possible; 
            avoid having two variables to dstinguish if winner is found or tie occurs
            '''
           # Check if board is full but no winner --> Tie
            if not winner_found and board_full(board):
                print_board(board)
                print("It's a draw!")
                winner_found = True

            # Change players
            turn = PLAYER

if __name__ == "__main__":
    main()
