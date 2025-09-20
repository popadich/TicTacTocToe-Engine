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

def main():
    new_board = '................................................................'
    for turn in range(1, 5):
        human_move = run_tttt_tournament('h', new_board)  
        # parse output which should look like <int> <string>
        move_str, new_board = human_move.strip().split(maxsplit=1)
        move = int(move_str)
        print(turn * 2 - 1, 'H:', move, new_board)
        print('')

        machine_move = run_tttt_tournament('m', new_board)
        # parse output which should look like <int> <string>
        move_str, new_board = machine_move.strip().split(maxsplit=1)
        move = int(move_str)
        print(turn * 2, 'M:', move, new_board)
        print('')

if __name__ == '__main__':
    main()