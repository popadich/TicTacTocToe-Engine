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
        'expected_output': "...XX.........................................................OO",
    },
    {
        'args': ['--t', 'm', "......XX.....................................................OOX" ],
        'expected_output': "Machine move: 1  O.....XX.....................................................OOX"
    },
    {
        'args': ['--t', 'm', "......XX.....................................................OOX", '-q' ],
        'expected_output': "1 O.....XX.....................................................OOX"
    },
    {
        'args': ['-g', '-h', '4 5 6 7', '-m', '64 63'],
        'expected_output': 'Invalid number of moves. Human moves: 4, Machine moves: 2. The difference cannot be greater than 1.\n',
    },
    {
        'args': ['-t', 'm', "./tttt -t m O..O........O...XXXX.......................................XXXXX"],
        'expected_output': 'Invalid number of moves. Human moves: 3, Machine moves: 9. The difference cannot be greater than 1.'
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
    passed_count = 0
    failed_count = 0
    for idx, test in enumerate(test_cases):
        output = run_test(test['args'])
        print( '\n\n' + '-' * 40 )
        print(f"Test {idx + 1}: {' '.join(test['args'])}")
        print("Captured Output:")
        print(output)
        print("Expected Output:")
        print(test['expected_output'])
        passed = output.strip() == test['expected_output'].strip()
        if passed:
            # Print 'Test Passed: True' in green
            print(f"\033[92mTest {idx + 1}: {passed}\033[0m")
        else:
            # Print 'Test Passed: False' in red
            print(f"\033[91mTest {idx + 1}: {passed}\033[0m")
        if passed:
            passed_count += 1
        else:
            failed_count += 1
    print('\n' + '=' * 40)
    print(f"Total Passed: {passed_count}  ::  Total Failed: {failed_count}\n")


if __name__ == '__main__':
    main()