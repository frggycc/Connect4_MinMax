import numpy as np
import time
import random
import csv
from UI_Implementation import ConnectFour, ROWS, COLUMNS, PLAYER, COMPUTER, EMPTY

class PerformanceTester(ConnectFour):
    def __init__(self):
        # Skip UI initialization, we're only using the game logic
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.game_over = False
        self.current_player = PLAYER
        self.ai_difficulty = None
        self.game_started = False
        
    def minimax_no_pruning(self, board, depth, max_player):
        """Minimax implementation without alpha-beta pruning for comparison"""
        valid_locations = self.get_valid_columns(board)
        is_terminal = self.is_end_of_game(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner(COMPUTER):
                    return (None, -1000000)
                elif self.check_winner(PLAYER):
                    return (None, 1000000 + 5000)
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
                self.place_piece(row, col, PLAYER, temp_board)

                # Calculate a score based on the position of the dropped piece
                new_score = self.minimax_no_pruning(temp_board, depth-1, False)[1]

                if new_score > value:
                    value = new_score
                    column = col

            return column, value
        
        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_locations) if valid_locations else None

            for col in valid_locations:
                row = self.next_free_row(col, board)
                temp_board = board.copy()
                self.place_piece(row, col, COMPUTER, temp_board)

                # Calculate a score based on the position of the dropped piece
                new_score = self.minimax_no_pruning(temp_board, depth-1, True)[1]

                if new_score < value:
                    value = new_score
                    column = col

            return column, value
    
    def reset_board(self):
        """Reset the game board to initial state"""
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.game_over = False
        self.current_player = PLAYER
        
    def randomize_board(self, num_moves):
        """Randomize the board with a given number of moves"""
        self.reset_board()
        
        for _ in range(num_moves):
            valid_cols = self.get_valid_columns(self.board)
            if not valid_cols:
                break
                
            col = random.choice(valid_cols)
            row = self.next_free_row(col, self.board)
            player = random.choice([PLAYER, COMPUTER])
            self.board[row][col] = player
            
            # Break if the game is already over
            if self.check_winner(PLAYER) or self.check_winner(COMPUTER):
                break
                
    def test_performance(self, num_tests, moves_range=(5, 20), depths=(2, 4, 5)):
        """Test performance of minimax with and without alpha-beta pruning"""
        results = []
        
        for depth in depths:
            for test_num in range(num_tests):
                # Randomize the board with a random number of moves
                num_moves = random.randint(*moves_range)
                self.randomize_board(num_moves)
                
                # If game already has winner, regenerate board
                while self.check_winner(PLAYER) or self.check_winner(COMPUTER):
                    self.randomize_board(num_moves)
                
                board_state = self.board.copy()
                
                # Test with alpha-beta pruning
                start_time = time.time()
                col_with_pruning, _ = self.minimax(board_state, depth, -float('inf'), float('inf'), False)
                time_with_pruning = time.time() - start_time
                
                # Test without alpha-beta pruning
                start_time = time.time()
                col_without_pruning, _ = self.minimax_no_pruning(board_state, depth, False)
                time_without_pruning = time.time() - start_time

                # Calculate speedup factor (mult)
                speedup_factor = time_without_pruning / time_with_pruning if time_with_pruning > 0 else 0
                
                # Store results
                results.append({
                    'test_num': test_num + 1,
                    'depth': depth,
                    'board_moves': num_moves,
                    'column_chosen_with_pruning': col_with_pruning,
                    'column_chosen_without_pruning': col_without_pruning,
                    'time_with_pruning': time_with_pruning,
                    'time_without_pruning': time_without_pruning,
                    'speedup_factor': speedup_factor
                })
                
                print(f"Test {test_num + 1} at depth {depth}: With pruning: {time_with_pruning:.6f}s, Without: {time_without_pruning:.6f}s")
        
        return results
    
    def save_results_to_csv(self, results, filename="connect4_performance_results.csv"):
        """Save performance results to a CSV file"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['test_num', 'depth', 'board_moves', 
                         'column_chosen_with_pruning', 'column_chosen_without_pruning',
                         'time_with_pruning', 'time_without_pruning', 'speedup_factor']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        print(f"Results saved to {filename}")
    
    def analyze_results(self, results):
        """Analyze and summarize the performance results"""
        summary = {}
        
        # Group by depth
        for depth in set(r['depth'] for r in results):
            depth_results = [r for r in results if r['depth'] == depth]
            
            avg_time_with_pruning = sum(r['time_with_pruning'] for r in depth_results) / len(depth_results)
            avg_time_without_pruning = sum(r['time_without_pruning'] for r in depth_results) / len(depth_results)
            avg_speedup = sum(r['speedup_factor'] for r in depth_results) / len(depth_results)
            
            summary[depth] = {
                'avg_time_with_pruning': avg_time_with_pruning,
                'avg_time_without_pruning': avg_time_without_pruning,
                'avg_speedup': avg_speedup,
                'difficulty': "Easy" if depth == 2 else "Medium" if depth == 4 else "Hard"
            }
        
        return summary
    
    def save_summary_to_csv(self, summary, filename="connect4_performance_summary.csv"):
        """Save performance summary to a CSV file"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['depth', 'difficulty', 'avg_time_with_pruning', 
                         'avg_time_without_pruning', 'avg_speedup']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for depth, data in summary.items():
                writer.writerow({
                    'depth': depth,
                    'difficulty': data['difficulty'],
                    'avg_time_with_pruning': data['avg_time_with_pruning'],
                    'avg_time_without_pruning': data['avg_time_without_pruning'],
                    'avg_speedup': data['avg_speedup']
                })
        
        print(f"Summary saved to {filename}")

if __name__ == "__main__":
    print("Starting Connect Four AI Performance Testing...")
    tester = PerformanceTester()
    
    # Run tests with 15 random board positions, testing each difficulty level
    print("Running performance tests...")
    results = tester.test_performance(num_tests=15, moves_range=(5, 25), depths=(2, 4, 5))
    
    # Save detailed results to CSV
    tester.save_results_to_csv(results)
    
    # Analyze and save summary
    summary = tester.analyze_results(results)
    tester.save_summary_to_csv(summary)
    
    # Print summary to console
    print("\nPerformance Summary:")
    print("-" * 80)
    print(f"{'Difficulty':<10} {'Depth':<6} {'Avg W/ Pruning':<15} {'Avg W/o Pruning':<15} {'Speedup':<8}")
    print("-" * 80)
    for depth, data in sorted(summary.items()):
        print(f"{data['difficulty']:<10} {depth:<6} {data['avg_time_with_pruning']:<15.6f} {data['avg_time_without_pruning']:<15.6f} {data['avg_speedup']:<5.2f}x")
    print("-" * 80)
