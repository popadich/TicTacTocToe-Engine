import subprocess
import os

# Path to the C program "tttt" (assumed to be in the same directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TTTT_PATH = os.path.join(SCRIPT_DIR, 'tttt')

# Define test cases as a list of dictionaries for easy modification
test_cases = [
    {
        'args': ['--version'],
        'expected_output': 'tttt version 1.0\n',  # Example expected output
    },
    {
        'args': ['-e', "......X......................................................OOX"],
        'expected_output': """Board StringRep is: ......X......................................................OOX

Board Value is: 8


""",
    },
    {
        'args': ['--generate', '-h', "4 5", '-m', "64 63" ],
        'expected_output': """
human moves len: 3 
moves: 4 5
h_arr is: 4 
h_arr is: 5 

machine moves len: 5 
moves: 64 63
m_arr is: 64 
m_arr is: 63 
...XX.........................................................OO
""",
    },
    {
        'args': ['--t', 'm', "......XX.....................................................OOX" ],
        'expected_output': """
Machine's best move is:  1
O.....XX.....................................................OOX
"""
    }
]

def run_test(args):
    """Run the tttt program with the given arguments and capture output."""
    try:
        result = subprocess.run(
            [TTTT_PATH] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr

def main():
    for idx, test in enumerate(test_cases):
        output = run_test(test['args'])
        print(f"Test {idx + 1}: {' '.join(test['args'])}")
        print("Captured Output:")
        print(output)
        print("Expected Output:")
        print(test['expected_output'])
        print("Test Passed:", output.strip() == test['expected_output'].strip())
        print('-' * 40)

if __name__ == '__main__':
    main()