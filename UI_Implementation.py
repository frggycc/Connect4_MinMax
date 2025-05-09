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
        self.ai_difficulty = None  # Changed: No default difficulty
        self.game_started = False  # New: Track if game has started
        
        # Create difficulty controls
        self.create_difficulty_controls()
        
        # Create the game board
        self.create_game_board()
        
        # Create status label
        self.status_label = tk.Label(
            self.window,
            text="Please select difficulty to start",  # Changed: Initial message
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
            font=('Inter', 12, 'bold'),
            bg='#3b82f6',
            fg='black',
            activebackground='#2563eb',
            state=tk.DISABLED  # Changed: Initially disabled
        )
        self.reset_button.pack(pady=10)

    def create_difficulty_controls(self):
        # Buttons to be used when trying to select a new mode or a dif level
        difficulty_frame = tk.Frame(self.window, bg='#1e3a8a')
        difficulty_frame.pack(pady=10)
        
        tk.Label(
            difficulty_frame,
            text="AI Difficulty:",
            font=('Inter', 12, 'bold'),
            bg='#1e3a8a',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_buttons = []  # New: Store button references
        
        for level in range(1, 4):
            btn = tk.Button(
                difficulty_frame,
                text=["Easy", "Medium", "Hard"][level-1],
                command=lambda l=level + 1: self.set_difficulty(l),
                font=('Inter', 10, 'bold'),
                bg='#1e40af',  # Changed: All buttons start with same color
                fg='black',
                activebackground='#2563eb'
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.difficulty_buttons.append(btn)  # Store button reference

    def create_game_board(self):
        # Making of the empty board
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
        # Check if game has started
        if not self.game_started or self.game_over or self.current_player == COMPUTER:
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
        # Check if game has started
        if not self.game_started:
            messagebox.showinfo("Info", "Please select a difficulty level first!")
            return
            
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

    def score_position(self, board):
        score = 0

        evaluation_board = np.array([[1, 2, 2, 3, 2, 2, 1],
                                     [2, 2, 3, 5, 3, 2, 2],
                                     [2, 3, 4, 6, 4, 3, 2],
                                     [2, 3, 4, 6, 4, 3, 2],
                                     [2, 2, 3, 5, 3, 2, 2],
                                     [1, 2, 2, 3, 2, 2, 1]])
        
        # Calculate the scores of the computer based on position on board
        score += np.sum(evaluation_board[board == COMPUTER])
        score -= np.sum(evaluation_board[board == PLAYER])

        def count_lines(piece, x_in_a_row):
            count = 0

            # Horizontal
            for row in range(ROWS):
                for col in range(COLUMNS - x_in_a_row + 1):
                    if all(board[row][col + i] == piece for i in range(x_in_a_row)):
                        count += 1
            # Vertical
            for row in range(ROWS - x_in_a_row + 1):
                for col in range(COLUMNS):
                    if all(board[row + i][col] == piece for i in range(x_in_a_row)):
                        count += 1
            # Diagonal (positive)
            for row in range(ROWS - x_in_a_row + 1):
                for col in range(COLUMNS - x_in_a_row + 1):
                    if all(board[row + i][col + i] == piece for i in range(x_in_a_row)):
                        count += 1
            # Diagonal (negative)
            for row in range(x_in_a_row - 1, ROWS):
                for col in range(COLUMNS - x_in_a_row + 1):
                    if all(board[row - i][col + i] == piece for i in range(x_in_a_row)):
                        count += 1
            return count

        # Calculate points for current piece (COMPUTER) based on winning lines
        score += count_lines(COMPUTER, 3) * 450
        score += count_lines(COMPUTER, 2) * 10

        # Recalculate points based on opponent's number of winning lines
        # If opponent has 3 in a row, priotize stopping it
        score -= count_lines(PLAYER, 3) * 500
        score -= count_lines(PLAYER, 2) * 8

        return score

    def is_end_of_game(self, board):
        return (self.check_winner(COMPUTER) or 
                self.check_winner(PLAYER) or 
                self.board_full(board))

    def minimax(self, board, depth, alpha, beta, max_player):
        valid_locations = self.get_valid_columns(board)
        is_terminal = self.is_end_of_game(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner(COMPUTER):
                    return (None, 1000000)
                elif self.check_winner(PLAYER):
                    return (None, -1000000)
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
        # Only allow reset if a difficulty has been selected
        if self.ai_difficulty is None:
            messagebox.showinfo("Info", "Please select a difficulty level first!")
            return
            
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
        """Set the AI difficulty level and start the game"""
        self.ai_difficulty = level
        self.game_started = True  # New: Mark game as started
        self.reset_button.config(state=tk.NORMAL)  # Enable reset button

        colors = [EASY_COLOR, MEDIUM_COLOR, HARD_COLOR]
        
        # Update button colors to show selected difficulty
        for i, button in enumerate(self.difficulty_buttons):
            if i + 1 == level:
                button.config(bg=colors[level - 1])  # Highlight selected
            else:
                button.config(bg='#1e40af')  # Reset others
        
        self.reset_game()
        self.status_label.config(text="Your turn!")  # Update status

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = ConnectFour()
    game.run()