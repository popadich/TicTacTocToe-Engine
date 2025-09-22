"""
Tic Tac Toc Toe Tournament Runner

This script automates a series of games between a human and a machine player
for the Tic Tac Toc Toe engine. It is designed to test the playability of the
game and to facilitate the adjustment of heuristic weights for an improved
user experience. The script interacts with an external executable ('tttt')
to simulate moves for both human and machine players, parses the results,
and prints the sequence of moves for analysis.

Weights File Format:
    The weights file should be a CSV with two columns:
    - Column 1: Name of the weight configuration 
    - Column 2: String of 25 space-separated integers (the 5x5 weight matrix)
    
    Example weights.txt:
        alpha,"0 -2 -5 -11 -27 2 0 3 12 0 5 -3 1 0 0 11 -12 0 0 0 23 0 0 0 0"
        beta,"0 -2 -5 -1 -57 2 0 3 12 0 5 -3 1 0 0 11 -12 0 0 0 90 0 0 0 0"

Usage:
    python3 tournament.py                    # Use first available weights
    python3 tournament.py -w alpha           # Use specific weight configuration
    python3 tournament.py -f custom.txt      # Use different weights file

Functions:
    load_weights_from_file(filename):
        Loads weight configurations from a CSV file with format: name,weight_string
        
    run_tttt_tournament(player, board, weights=None):
        Executes the 'tttt' engine with the specified player and board state,
        optionally using custom weights, returning the engine's output.

    main():
        Runs a sequence of alternating human and machine moves, printing
        each move and the resulting board state for a fixed number of turns.
"""

import subprocess
import os
import csv
import sys
import argparse

test_board = '................................................................'
weight_file = 'weights.txt'

def load_weights_from_file(filename):
    """
    Load weight configurations from a CSV file.
    
    File format: name,weight_string
    Where weight_string is 25 space-separated integers.
    
    Returns:
        dict: Dictionary mapping weight names to weight strings
    """
    weights = {}
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row_num, row in enumerate(reader, 1):
                if len(row) != 2:
                    print(f"Warning: Line {row_num} in {filename} has {len(row)} columns, expected 2. Skipping.")
                    continue
                
                name, weight_string = row
                name = name.strip()
                weight_string = weight_string.strip().strip('"')
                
                # Validate that weight_string has exactly 25 integers
                weight_values = weight_string.split()
                if len(weight_values) != 25:
                    print(f"Warning: Weight '{name}' has {len(weight_values)} values, expected 25. Skipping.")
                    continue
                
                # Validate that all values are integers
                try:
                    [int(val) for val in weight_values]
                except ValueError:
                    print(f"Warning: Weight '{name}' contains non-integer values. Skipping.")
                    continue
                
                weights[name] = weight_string
                
    except FileNotFoundError:
        print(f"Warning: Weights file '{filename}' not found. Running without custom weights.")
    except Exception as e:
        print(f"Error reading weights file '{filename}': {e}")
    
    return weights

def run_tttt_tournament(player, board, weights=None):
    """
    Execute the 'tttt' engine with optional custom weights.
    
    Args:
        player: 'h' for human or 'm' for machine
        board: 64-character board string
        weights: Optional weight string (25 space-separated integers)
    
    Returns:
        str: Engine output
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tttt_path = os.path.join(script_dir, 'tttt')
    args = ['-t', player, board, '-q']
    
    # Add weights if provided (typically for human player)
    if weights and player == 'h':
        args.extend(['-w', weights])
    
    try:
        result = subprocess.run(
            [tttt_path] + args, 
            capture_output=True, 
            text=True
        )
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr

    return result.stdout

def check_game_over(output):
    """Check if the game is over based on tournament output"""
    return "game_over" in output.lower()

def extract_winner_from_output(output):
    """Extract winner information from tournament output"""
    lines = output.strip().split('\n')
    for line in lines:
        if "game over" in line.lower():
            if "machine wins" in line.lower():
                return "Machine"
            elif "human wins" in line.lower():
                return "Human"
            elif "draw" in line.lower() or "board is full" in line.lower():
                return "Draw"
    return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run a Tic Tac Toc Toe tournament')
    parser.add_argument('-w', '--weights', type=str, 
                        help='Name of weight configuration to use from weights file')
    parser.add_argument('-f', '--weights-file', type=str, default=weight_file,
                        help='Path to weights file (default: weights.txt)')
    args = parser.parse_args()
    
    # Load weights configuration from file
    weights_config = load_weights_from_file(args.weights_file)
    
    # Select weights to use
    selected_weights = None
    selected_name = None
    if weights_config:
        weight_names = list(weights_config.keys())
        print(f"Available weight configurations: {', '.join(weight_names)}")
        
        if args.weights:
            if args.weights in weights_config:
                selected_weights = weights_config[args.weights]
                selected_name = args.weights
            else:
                print(f"Warning: Weight configuration '{args.weights}' not found. Using default.")
                selected_weights = weights_config[weight_names[0]]
                selected_name = weight_names[0]
        else:
            selected_weights = weights_config[weight_names[0]]  # Use first one by default
            selected_name = weight_names[0]
            
        print(f"Using weights '{selected_name}': {selected_weights}")
        print()
    
    new_board = '................................................................'
    turn = 1
    game_over = False
    winner = None
    
    while not game_over:
        # Human move (with optional custom weights)
        human_move = run_tttt_tournament('h', new_board, selected_weights)
        
        # Check if game is over after human move
        if check_game_over(human_move):
            winner = extract_winner_from_output(human_move) or "Human"
            game_over = True
            # Still parse and display the final move
            try:
                move_str, new_board = human_move.strip().split(maxsplit=1)
                move = int(move_str)
                print(turn * 2 - 1, 'H:', move, new_board)
            except ValueError:
                print(f"Final human move output: {human_move.strip()}")
            break
        
        # Parse normal human move output
        move_str, new_board = human_move.strip().split(maxsplit=1)
        move = int(move_str)
        print(turn * 2 - 1, 'H:', move, new_board)
        print('')

        # Machine move
        machine_move = run_tttt_tournament('m', new_board)
        
        # Check if game is over after machine move
        if check_game_over(machine_move):
            winner = extract_winner_from_output(machine_move) or "Machine"
            game_over = True
            # Still parse and display the final move
            try:
                move_str, new_board = machine_move.strip().split(maxsplit=1)
                move = int(move_str)
                print(turn * 2, 'M:', move, new_board)
            except ValueError:
                print(f"Final machine move output: {machine_move.strip()}")
            break
        
        # Parse normal machine move output
        move_str, new_board = machine_move.strip().split(maxsplit=1)
        move = int(move_str)
        print(turn * 2, 'M:', move, new_board)
        print('')
        
        turn += 1
        
        # Safety check to prevent infinite loops (64 positions max)
        if turn > 32:  # 32 turns = 64 moves maximum
            winner = "Draw - Maximum moves reached"
            game_over = True
    
    # Display the final result
    print('=' * 50)
    print(f'GAME OVER - WINNER: {winner}')
    print('=' * 50)

if __name__ == '__main__':
    main()