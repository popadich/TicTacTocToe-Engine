"""
Tic Tac Toc Toe Tournament Runner

This script automates a series of games between a human and a machine player
for the Tic Tac Toc Toe engine. It is designed to test the playability of the
game and to facilitate the adjustment of heuristic weights for an improved
user experience. The script interacts with an external executable ('tttt')
to simulate moves for both human and machine players, parses the results,
and prints the sequence of moves for analysis.

Functions:
    run_tttt_tournament(player, board):
        Executes the 'tttt' engine with the specified player and board state,
        returning the engine's output.

    main():
        Runs a sequence of alternating human and machine moves, printing
        each move and the resulting board state for a fixed number of turns.
"""

import subprocess
import os

def run_tttt_tournament(player, board):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tttt_path = os.path.join(script_dir, 'tttt')
    args = ['-t', player, board, '-q']
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
    new_board = '................................................................'
    turn = 1
    game_over = False
    winner = None
    
    while not game_over:
        # Human move
        human_move = run_tttt_tournament('h', new_board)
        
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