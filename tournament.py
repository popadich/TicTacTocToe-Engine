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

def validate_tournament_inputs(player, board, weights=None):
    """
    Validate inputs for tournament execution with detailed error reporting.
    
    Args:
        player: Player identifier to validate
        board: Board string to validate  
        weights: Optional weight string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Validate player
    if not isinstance(player, str):
        return False, f"Player must be string, got {type(player).__name__}"
    
    if player not in ['h', 'm', 'human', 'machine']:
        return False, f"Player must be 'h', 'm', 'human', or 'machine', got '{player}'"
    
    # Validate board
    if not isinstance(board, str):
        return False, f"Board must be string, got {type(board).__name__}"
    
    if len(board) != 64:
        return False, f"Board must be exactly 64 characters, got {len(board)}"
    
    valid_chars = set('XO.')
    for i, char in enumerate(board):
        if char not in valid_chars:
            return False, f"Invalid character '{char}' at position {i}. Only 'X', 'O', '.' allowed"
    
    # Check move balance
    x_count = board.count('X')
    o_count = board.count('O')
    if abs(x_count - o_count) > 1:
        return False, f"Invalid move counts: X={x_count}, O={o_count} (difference > 1)"
    
    # Validate weights if provided
    if weights is not None:
        if not isinstance(weights, str):
            return False, f"Weights must be string, got {type(weights).__name__}"
        
        weight_values = weights.split()
        if len(weight_values) != 25:
            return False, f"Weights must have 25 values, got {len(weight_values)}"
        
        for i, val in enumerate(weight_values):
            try:
                int(val)
            except ValueError:
                return False, f"Weight {i} is not an integer: '{val}'"
    
    return True, ""

def find_tttt_executable():
    """
    Locate tttt executable with multiple fallback locations.
    
    Returns:
        str: Path to executable if found, None otherwise
    """
    candidates = ['./tttt', './TTTTengine/tttt', 'tttt']
    
    for candidate in candidates:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            # Test executable works
            try:
                result = subprocess.run(
                    [candidate, '--version'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    return candidate
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
    
    return None

def run_tttt_tournament(player, board, weights=None, executable_path=None):
    """
    Execute the 'tttt' engine with comprehensive error handling.
    
    Args:
        player: 'h' for human or 'm' for machine
        board: 64-character board string
        weights: Optional weight string (25 space-separated integers)
        executable_path: Optional path to tttt executable (for testing)
    
    Returns:
        dict: {'success': bool, 'output': str, 'error': str, 'returncode': int}
    """
    # Input validation
    valid, error_msg = validate_tournament_inputs(player, board, weights)
    if not valid:
        return {
            'success': False,
            'output': None,
            'error': f"Input validation failed: {error_msg}",
            'returncode': -1
        }
    
    # Find executable (use provided path or search for it)
    if executable_path:
        tttt_path = executable_path
        if not os.path.exists(tttt_path):
            return {
                'success': False,
                'output': None,
                'error': f"Specified tttt executable not found: {tttt_path}",
                'returncode': -1
            }
    else:
        tttt_path = find_tttt_executable()
        if not tttt_path:
            return {
                'success': False,
                'output': None,
                'error': "tttt executable not found. Please run 'make clean && make' to build it.",
                'returncode': -1
            }
    
    # Normalize player argument
    player_arg = 'h' if player in ['h', 'human'] else 'm'
    
    # Build command
    args = [tttt_path, '-t', player_arg, board, '-q']
    
    # Add weights if provided
    if weights:
        args.extend(['-w', weights])
    
    try:
        # Execute with timeout and comprehensive error capture
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,  # Generous timeout
            check=False   # Don't raise on non-zero exit
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode != 0:
            error_detail = error if error else "Unknown error (no stderr output)"
            return {
                'success': False,
                'output': output,
                'error': f"Engine failed (exit code {result.returncode}): {error_detail}",
                'returncode': result.returncode
            }
        
        if not output:
            return {
                'success': False,
                'output': output,
                'error': "Engine produced no output",
                'returncode': result.returncode
            }
        
        # Validate output format (should be "<move> <board>" or "<move> game_over\n<board>")
        lines = output.split('\n')
        if len(lines) >= 1:
            first_line_parts = lines[0].split()
            if len(first_line_parts) < 2:
                return {
                    'success': False,
                    'output': output,
                    'error': f"Malformed engine output (expected '<move> <board>'): '{output}'",
                    'returncode': result.returncode
                }
            
            try:
                move_num = int(first_line_parts[0])
            except ValueError:
                return {
                    'success': False,
                    'output': output,
                    'error': f"Invalid move number in output: '{first_line_parts[0]}'",
                    'returncode': result.returncode
                }
                
            # Validate board string (should be 64 characters of X, O, .)
            board_part = first_line_parts[1] if len(first_line_parts) > 1 else ""
            if not board_part or len(board_part) != 64:
                return {
                    'success': False,
                    'output': output,
                    'error': f"Invalid board string in output (expected 64 chars): '{board_part}'",
                    'returncode': result.returncode
                }
            
            # Check board contains only valid characters
            if not all(c in 'XO.' for c in board_part):
                return {
                    'success': False,
                    'output': output,
                    'error': f"Board contains invalid characters: '{board_part}'",
                    'returncode': result.returncode
                }
        
        return {
            'success': True,
            'output': output,
            'error': None,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': None,
            'error': "Engine command timed out after 30 seconds",
            'returncode': -1
        }
    except FileNotFoundError:
        return {
            'success': False,
            'output': None,
            'error': f"Executable not found: {tttt_path}",
            'returncode': -1
        }
    except PermissionError:
        return {
            'success': False,
            'output': None,
            'error': f"Permission denied executing: {tttt_path}",
            'returncode': -1
        }
    except MemoryError:
        return {
            'success': False,
            'output': None,
            'error': "Insufficient memory to run engine",
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'output': None,
            'error': f"Unexpected error: {str(e)}",
            'returncode': -1
        }

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
        human_result = run_tttt_tournament('h', new_board, selected_weights)
        
        if not human_result['success']:
            print(f"Error in human move: {human_result['error']}")
            winner = "Error - Tournament stopped"
            game_over = True
            break
        
        human_move = human_result['output']
        
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
        try:
            move_str, new_board = human_move.strip().split(maxsplit=1)
            move = int(move_str)
            print(turn * 2 - 1, 'H:', move, new_board)
            print('')
        except (ValueError, IndexError) as e:
            print(f"Error parsing human move output '{human_move}': {e}")
            winner = "Error - Invalid move output"
            game_over = True
            break

        # Machine move
        machine_result = run_tttt_tournament('m', new_board)
        
        if not machine_result['success']:
            print(f"Error in machine move: {machine_result['error']}")
            winner = "Error - Tournament stopped"
            game_over = True
            break
        
        machine_move = machine_result['output']
        
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
        try:
            move_str, new_board = machine_move.strip().split(maxsplit=1)
            move = int(move_str)
            print(turn * 2, 'M:', move, new_board)
            print('')
        except (ValueError, IndexError) as e:
            print(f"Error parsing machine move output '{machine_move}': {e}")
            winner = "Error - Invalid move output"
            game_over = True
            break
        
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