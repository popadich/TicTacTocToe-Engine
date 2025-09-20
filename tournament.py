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
    output = run_tttt_tournament('h', 'O.....XX.....................................................OOX')
    print(output)

if __name__ == '__main__':
    main()