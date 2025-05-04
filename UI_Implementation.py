
import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

ROWS = 6
COLUMNS = 7
PLAYER = 1
COMPUTER = 2
EMPTY = 0
CELL_SIZE = 60
PADDING = 10

EASY_COLOR = '#4ade80'    # Green
MEDIUM_COLOR = '#2563eb'  # Blue
HARD_COLOR = '#ef4444'    # Red
PLAYER_COLOR = '#fde047'  # Yellow
COMPUTER_COLOR = '#ef4444' # Red

class ConnectFour:
    def __init__(self):
        # Construction of the game window
        self.window = tk.Tk()
        self.window.title("Connect Four")
        self.window.configure(bg='#1e3a8a')
        
        # Initialize game state
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.game_over = False
        self.current_player = PLAYER
        self.ai_difficulty = 2  # Default to medium difficulty
        
        # Create difficulty controls
        self.create_difficulty_controls()
        
        # Create the game board
        self.create_game_board()
        
        # Create status label
        self.status_label = tk.Label(
            self.window,
            text="Your turn!",
            font=('Inter', 14, 'bold'),
            bg='#1e3a8a',
            fg='white'
        )
        self.status_label.pack(pady=10)
        
        # Create reset button
        self.reset_button = tk.Button(
            self.window,
            text="New Game",
            command=self.reset_game,
            font=('Inter', 12),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb'
        )
        self.reset_button.pack(pady=10)

    def create_difficulty_controls(self):
        # Buttons to be used when trying to select a new mode or a dif level
        difficulty_frame = tk.Frame(self.window, bg='#1e3a8a')
        difficulty_frame.pack(pady=10)
        
        tk.Label(
            difficulty_frame,
            text="AI Difficulty:",
            font=('Inter', 12),
            bg='#1e3a8a',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        for level in range(1, 4):
            btn = tk.Button(
                difficulty_frame,
                text=["Easy", "Medium", "Hard"][level-1],
                command=lambda l=level: self.set_difficulty(l),
                font=('Inter', 10),
                bg='#3b82f6' if level == 2 else '#1e40af',
                fg='white',
                activebackground='#2563eb'
            )
            btn.pack(side=tk.LEFT, padx=2)

    def create_game_board(self):
        # Making of the empty boatd
        self.canvas = tk.Canvas(
            self.window,
            width=COLUMNS * CELL_SIZE + 2 * PADDING,
            height=ROWS * CELL_SIZE + 2 * PADDING,
            bg='#2563eb'
        )
        self.canvas.pack(padx=20, pady=10)
        
        # Create cells
        for row in range(ROWS):
            for col in range(COLUMNS):
                x = col * CELL_SIZE + PADDING
                y = row * CELL_SIZE + PADDING
                self.canvas.create_oval(
                    x + 5, y + 5,
                    x + CELL_SIZE - 5,
                    y + CELL_SIZE - 5,
                    fill='#1e3a8a',
                    outline='#1e3a8a'
                )
        # Bind Mouse Events 
        self.canvas.bind('<Button-1>', self.handle_click)
        self.canvas.bind('<Motion>', self.handle_hover)

    def handle_hover(self, event):
        if self.game_over or self.current_player == COMPUTER:
            return
            
        col = (event.x - PADDING) // CELL_SIZE
        if 0 <= col < COLUMNS:
            self.canvas.delete('hover')
            if self.is_valid_move(col):
                x = col * CELL_SIZE + PADDING
                self.canvas.create_oval(
                    x + 5, 5,
                    x + CELL_SIZE - 5,
                    CELL_SIZE - 5,
                    fill='#fde047',
                    outline='#fde047',
                    stipple='gray50',
                    tags='hover'
                )

    def handle_click(self, event):
        if self.game_over or self.current_player == COMPUTER:
            return
            
        col = (event.x - PADDING) // CELL_SIZE
        if 0 <= col < COLUMNS:
            self.make_move(col)

    def make_move(self, col):
        # Check if win or draw, if neither just switch turns
        if not self.is_valid_move(col):
            return
            
        row = self.get_next_row(col)
        self.board[row][col] = self.current_player
        self.draw_piece(row, col)
        
        if self.check_winner(self.current_player):
            self.game_over = True
            winner = "You win! 🎉" if self.current_player == PLAYER else "Computer wins! 🤖"
            self.status_label.config(text=winner)
            return
            
        if self.is_board_full():
            self.game_over = True
            self.status_label.config(text="It's a draw! 🤝")
            return
            
        self.current_player = COMPUTER if self.current_player == PLAYER else PLAYER
        self.status_label.config(text="Computer thinking..." if self.current_player == COMPUTER else "Your turn!")
        
        if self.current_player == COMPUTER:
            self.window.after(1000, self.make_computer_move)

    def make_computer_move(self):
        col, _ = self.minimax(self.board, self.ai_difficulty, -float('inf'), float('inf'), True)
        self.make_move(col)

    def draw_piece(self, row, col):
        x = col * CELL_SIZE + PADDING
        y = (ROWS - 1 - row) * CELL_SIZE + PADDING
        color = '#fde047' if self.current_player == PLAYER else '#ef4444'
        
        self.canvas.create_oval(
            x + 5, y + 5,
            x + CELL_SIZE - 5,
            y + CELL_SIZE - 5,
            fill=color,
            outline=color
        )

    def is_valid_move(self, col):
        return 0 <= col < COLUMNS and self.board[ROWS-1][col] == EMPTY

    def get_next_row(self, col):
        for row in range(ROWS):
            if self.board[row][col] == EMPTY:
                return row
        return -1

    def check_winner(self, player):
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonal (positive slope)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Check diagonal (negative slope)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_board_full(self):
        return not any(self.board[ROWS-1][col] == EMPTY for col in range(COLUMNS))

    def get_valid_columns(self, board):
        return [col for col in range(COLUMNS) if board[ROWS-1][col] == EMPTY]

    def next_free_row(self, col, board):
        for row in range(ROWS):
            if board[row][col] == EMPTY:
                return row
        return -1

    def place_piece(self, row, col, player, board):
        board[row][col] = player

    def board_full(self, board):
        return not any(board[ROWS-1][col] == EMPTY for col in range(COLUMNS))
    
        """
        Logic from computer.py implementation
        Main changes are:

            -value  = {-100000} to  {-float('inf')} 

        """

    def score_position(self, board):
        score = 0

        evaluation_board = np.array([[3, 4, 5,  7,  5,  4, 3],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [5, 8, 10, 13, 10, 8, 5],
                                    [4, 6, 8,  10, 8,  6, 4],
                                    [3, 4, 5,  7,  5,  4, 3]])
        
        # Calculate the scores of the player and the opponent
        computer_score = np.sum(evaluation_board[board == COMPUTER])
        player_score   = np.sum(evaluation_board[board == PLAYER])

        return computer_score - player_score

    def is_end_of_game(self, board):
        return (self.check_winner(COMPUTER) or 
                self.check_winner(PLAYER) or 
                self.board_full(board))
    '''
    Manimax algortihm is implemented here!
    Uses recursion of this functions to think x steps ahead. The number
    of steps ahead that the computer will "think" is based off of diffciulty
    set by the player. Lower the depth, the easier the game.
    '''   
    

    def minimax(self, board, depth, alpha, beta, max_player):
        valid_locations = self.get_valid_columns(board)
        is_terminal = self.is_end_of_game(board)
        '''
        If the depth is zero or maximum depth is reached, then the game
        is over or no more calculations will be done due to the difficulty set.
        '''

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner(COMPUTER):
                    return (None, 100000)
                elif self.check_winner(PLAYER):
                    return (None, -100000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board))
        
        # Maximize computer
        if max_player:
            value = -float('inf')
            column = random.choice(valid_locations) if valid_locations else None

            for col in valid_locations:
                row = self.next_free_row(col, board)
                temp_board = board.copy()
                self.place_piece(row, col, COMPUTER, temp_board)

                # Calculate a score based on the position of the dropped piece
                new_score = self.minimax(temp_board, depth-1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value
        
        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_locations) if valid_locations else None

            for col in valid_locations:
                row = self.next_free_row(col, board)
                temp_board = board.copy()
                self.place_piece(row, col, PLAYER, temp_board)

                # Calculate a score based on the position of the dropped piece
                new_score = self.minimax(temp_board, depth-1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

    def reset_game(self):
        """Reset the game state and clear the board"""
        # Reset game state
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.game_over = False
        self.current_player = PLAYER
        self.status_label.config(text="Your turn!")
        
        # Clear the canvas completely
        self.canvas.delete("all")
        
        # Recreate the empty board
        for row in range(ROWS):
            for col in range(COLUMNS):
                x = col * CELL_SIZE + PADDING
                y = row * CELL_SIZE + PADDING
                self.canvas.create_oval(
                    x + 5, y + 5,
                    x + CELL_SIZE - 5,
                    y + CELL_SIZE - 5,
                    fill='#1e3a8a',
                    outline='#1e3a8a'
                )
        
        # Rebind events (just to be safe)
        self.canvas.bind('<Button-1>', self.handle_click)
        self.canvas.bind('<Motion>', self.handle_hover)

    def set_difficulty(self, level):
        """Set the AI difficulty level and reset the game"""
        self.ai_difficulty = level
        self.reset_game()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = ConnectFour()
    game.run()