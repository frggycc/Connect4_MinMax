import numpy

# Set up out board with zeros
ROWS = 6
COLUMNS = 7
PLAYER = 1
COMPUTER = 2
EMPTY = 0

def create_board():
    return numpy.zeros((ROWS, COLUMNS), dtype=int)

def print_board(board):
    print(" 0 1 2 3 4 5 6 ")
    print("_" * 15)
    for row in range(ROWS - 1, -1, -1):
        print("|", end="")
        for column in range(COLUMNS):
            if board[row][column] == EMPTY:
                print(" ", end="|")
            elif board[row][column] == PLAYER:
                print("X", end="|")
            else:
                print("O", end="|")
        print("")
    print("-" * 15)

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

# Assuming valid_placement checked
def next_free_row(col, board):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            return row
        
# Check if game won with last move
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

def main():
    board = create_board()
    turn = None
    valid_move = False
    winner_found = False
    
    # Decide who will go first
    while True:
        first = input("Who will go first? Player (P) or computer (C)?: ")
        if first == "p" or first == "P":
            print("Player will go first! You are R pieces.")
            turn = PLAYER
            break
        elif first == "C" or first == "c":
            print("Computer will go first! You are R pieces.")
            turn = COMPUTER
            break
        else:
            print("Please enter P or C. \n")

    # At this point, you've decided who goes first
    ''' FIX: STUCK WHEN THERE IS A DRAW '''
    while not winner_found:
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

            # Change players
            turn = COMPUTER

        else:
            print("")
            print_board(board)
            print("PLAYER TWO'S turn - O Pieces")

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
                print("CONGRATS PLAYER 2! YOU WIN!")
                winner_found = True

            # Change players
            turn = PLAYER

if __name__ == "__main__":
    main()
