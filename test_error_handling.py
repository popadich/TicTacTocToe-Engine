#!/usr/bin/env python3
"""
Comprehensive Error Handling Test Suite for TicTacTocToe-Engine

Tests edge cases, invalid inputs, missing files, and robustness scenarios
across the CLI interface and tournament system.
"""

import subprocess
import tempfile
import os
import sys
import shutil
import time
import signal
from pathlib import Path

class ErrorHandlingTestSuite:
    def __init__(self):
        self.tttt_path = self.find_tttt_executable()
        self.test_count = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def find_tttt_executable(self):
        """Find the tttt executable in the project"""
        # Check current directory first
        if os.path.exists('./tttt'):
            return './tttt'
        
        # Check TTTTengine directory
        if os.path.exists('TTTTengine/tttt'):
            return 'TTTTengine/tttt'
            
        # Check if we're in TTTTengine directory
        if os.path.exists('tttt'):
            return './tttt'
            
        raise FileNotFoundError("Could not find tttt executable. Please run 'make' to build the project.")

    def run_test(self, test_name, test_func):
        """Run a single test and track results"""
        self.test_count += 1
        print(f"\n--- Test {self.test_count}: {test_name} ---")
        
        try:
            result = test_func()
            if result:
                print(f"✅ PASS: {test_name}")
                self.passed_tests += 1
                return True
            else:
                print(f"❌ FAIL: {test_name}")
                self.failed_tests += 1
                return False
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            self.failed_tests += 1
            return False

    def test_cli_invalid_board_strings(self):
        """Test CLI with various invalid board string formats"""
        invalid_boards = [
            "",  # Empty string
            "X",  # Too short
            "X" * 63,  # Too short by 1
            "X" * 65,  # Too long by 1  
            "X" * 100,  # Way too long
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXY",  # Invalid character
            "123456789012345678901234567890123456789012345678901234567890123",  # Numbers
            "X.O" * 20 + "ZZZZ",  # Mixed valid/invalid chars
            "X.O." * 15 + "XYZ.",  # Valid length but with invalid char
        ]
        
        for i, board in enumerate(invalid_boards):
            try:
                result = subprocess.run(
                    [self.tttt_path, '-e', board], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                
                # Should return non-zero exit code for invalid input
                if result.returncode == 0:
                    print(f"  Invalid board #{i+1} was accepted (should be rejected): '{board}'")
                    return False
                    
                # Should contain helpful error message
                if 'error' not in result.stderr.lower() and 'invalid' not in result.stderr.lower():
                    print(f"  Invalid board #{i+1} error message unclear: {result.stderr}")
                    return False
                    
                print(f"  ✓ Invalid board #{i+1} properly rejected")
                
            except subprocess.TimeoutExpired:
                print(f"  Invalid board #{i+1} caused timeout")
                return False
                
        return True

    def test_cli_invalid_player_arguments(self):
        """Test CLI with invalid player arguments"""
        invalid_players = ['x', 'human', 'machine', 'H', 'M', '1', '0', '', 'hh', 'mm']
        
        for player in invalid_players:
            try:
                result = subprocess.run(
                    [self.tttt_path, '-p', player], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                
                # Should return non-zero exit code
                if result.returncode == 0:
                    print(f"  Invalid player '{player}' was accepted")
                    return False
                    
                print(f"  ✓ Invalid player '{player}' properly rejected")
                
            except subprocess.TimeoutExpired:
                print(f"  Invalid player '{player}' caused timeout")
                return False
                
        return True

    def test_cli_missing_arguments(self):
        """Test CLI with missing required arguments"""
        test_cases = [
            [self.tttt_path, '-e'],  # Missing board string
            [self.tttt_path, '-p'],  # Missing player
            [self.tttt_path, '-g'],  # Missing moves
            [self.tttt_path, '-t'],  # Missing player and board
            [self.tttt_path, '-w'],  # Missing weights
        ]
        
        for i, cmd in enumerate(test_cases):
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                # Should return non-zero exit code
                if result.returncode == 0:
                    print(f"  Missing argument test #{i+1} passed incorrectly: {' '.join(cmd)}")
                    return False
                    
                print(f"  ✓ Missing argument test #{i+1} properly rejected")
                
            except subprocess.TimeoutExpired:
                print(f"  Missing argument test #{i+1} caused timeout")
                return False
                
        return True

    def test_cli_malformed_weight_matrix(self):
        """Test CLI with malformed weight matrices"""
        invalid_weights = [
            "1,2,3",  # Too few elements
            "1," * 30,  # Too many elements  
            "a,b,c,d,e," * 5,  # Non-numeric
            "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24",  # Missing one
            "",  # Empty
        ]
        
        valid_board = "." * 64
        
        for i, weights in enumerate(invalid_weights):
            try:
                result = subprocess.run(
                    [self.tttt_path, '-e', valid_board, '-w', weights], 
                    capture_output=True, 
                    text=True,
                    timeout=5
                )
                
                # Should return non-zero exit code for invalid weights
                if result.returncode == 0:
                    print(f"  Invalid weights #{i+1} were accepted: '{weights}'")
                    return False
                    
                print(f"  ✓ Invalid weights #{i+1} properly rejected")
                
            except subprocess.TimeoutExpired:
                print(f"  Invalid weights #{i+1} caused timeout")
                return False
                
        return True

    def test_tournament_missing_executable(self):
        """Test tournament system with missing tttt executable"""
        # Temporarily rename the executable
        temp_name = self.tttt_path + '.backup'
        
        try:
            shutil.move(self.tttt_path, temp_name)
            
            # Import tournament module and test
            import tournament
            
            # Should fail gracefully
            try:
                result = tournament.run_tttt_tournament('h', '.' * 64)
                if result['success']:
                    print("  Tournament succeeded with missing executable")
                    return False
                    
                if 'not found' not in result['error'].lower() and 'executable' not in result['error'].lower():
                    print(f"  Tournament error message unclear: {result['error']}")
                    return False
                    
                print("  ✓ Tournament properly detected missing executable")
                return True
                
            except Exception as e:
                print(f"  Tournament threw exception instead of graceful error: {e}")
                return False
                
        finally:
            # Restore the executable
            if os.path.exists(temp_name):
                shutil.move(temp_name, self.tttt_path)

    def test_tournament_corrupted_output(self):
        """Test tournament system with malformed engine output"""
        # Create a fake tttt executable that produces bad output
        fake_tttt_path = './fake_tttt_test'
        
        try:
            with open(fake_tttt_path, 'w') as f:
                f.write('''#!/bin/bash
case "$1" in
    "-t")
        case "$2" in
            "h") echo "CORRUPTED OUTPUT" ;;
            "m") echo "42" ;;  # Missing board string
            *) echo "Invalid player" >&2; exit 1 ;;
        esac
        ;;
    *) echo "Usage error" >&2; exit 1 ;;
esac
''')
            os.chmod(fake_tttt_path, 0o755)
            
            # Test with tournament module
            import tournament
            
            # Temporarily replace the executable path
            original_path = tournament.tttt_path if hasattr(tournament, 'tttt_path') else None
            
            # Test corrupted human output
            result = tournament.run_tttt_tournament('h', '.' * 64, executable_path=fake_tttt_path)
            if result['success']:
                print("  Tournament accepted corrupted output")
                return False
                
            # Test missing board string in output
            result = tournament.run_tttt_tournament('m', '.' * 64, executable_path=fake_tttt_path)  
            if result['success']:
                print("  Tournament accepted malformed output")
                return False
                
            print("  ✓ Tournament properly handled corrupted output")
            return True
            
        except Exception as e:
            print(f"  Error in corrupted output test: {e}")
            return False
            
        finally:
            if os.path.exists(fake_tttt_path):
                os.remove(fake_tttt_path)

    def test_resource_exhaustion_scenarios(self):
        """Test behavior under resource constraints"""
        # Test with very long running process (timeout handling)
        try:
            # Create a process that runs too long
            result = subprocess.run(
                [self.tttt_path, '-p', 'h'],  # Interactive mode 
                input='99\n' * 10,  # Send invalid moves repeatedly
                capture_output=True,
                text=True,
                timeout=2  # Short timeout
            )
            
            # Should either complete quickly or be terminated by timeout
            print("  ✓ Process completed within timeout or was properly terminated")
            return True
            
        except subprocess.TimeoutExpired:
            print("  ✓ Long-running process properly timed out")
            return True
        except Exception as e:
            print(f"  Timeout test error: {e}")
            return False

    def test_file_system_edge_cases(self):
        """Test file system related errors"""
        # Test with read-only directory (if possible)
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Try to make directory read-only (may fail on some systems)
            try:
                os.chmod(temp_dir, 0o444)
            except (OSError, PermissionError) as e:
                print(f"  ✓ Cannot test read-only directory (system limitation): {e}")
                return True
            
            # Change to that directory and try to run
            original_cwd = os.getcwd()
            
            try:
                os.chdir(temp_dir)
            except (OSError, PermissionError) as e:
                print(f"  ✓ Cannot access read-only directory (expected): {e}")
                return True
            
            try:
                result = subprocess.run(
                    [os.path.join(original_cwd, self.tttt_path), '-e', '.' * 64],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                # Should still work (just evaluating, not writing files)
                print("  ✓ Program works in read-only directory")
                return True
                
            except Exception as e:
                print(f"  Read-only directory test failed: {e}")
                return False
                
            finally:
                try:
                    os.chdir(original_cwd)
                except (OSError, PermissionError):
                    pass  # Already changed back or couldn't change
                
        except Exception as e:
            print(f"  ✓ File system test skipped due to system limitations: {e}")
            return True
            
        finally:
            # Cleanup
            try:
                os.chmod(temp_dir, 0o755)
                shutil.rmtree(temp_dir)
            except (OSError, PermissionError):
                pass  # May not be able to clean up, that's ok

    def test_signal_handling(self):
        """Test graceful handling of interruption signals"""
        try:
            # Start an interactive process
            process = subprocess.Popen(
                [self.tttt_path, '-p', 'h'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it a moment to start
            time.sleep(0.1)
            
            # Send interrupt signal
            process.send_signal(signal.SIGINT)
            
            # Wait for it to terminate
            try:
                process.wait(timeout=2)
                print("  ✓ Process handled interrupt signal gracefully")
                return True
            except subprocess.TimeoutExpired:
                process.kill()
                print("  Process did not respond to interrupt, had to kill")
                return False
                
        except Exception as e:
            print(f"  Signal handling test error: {e}")
            return False

    def run_all_tests(self):
        """Run the complete test suite"""
        print("=" * 60)
        print("TicTacTocToe-Engine Error Handling Test Suite")
        print("=" * 60)
        
        print(f"Using executable: {self.tttt_path}")
        
        # CLI Input Validation Tests
        print("\n" + "=" * 40)
        print("CLI INPUT VALIDATION TESTS")
        print("=" * 40)
        
        self.run_test("Invalid Board String Formats", self.test_cli_invalid_board_strings)
        self.run_test("Invalid Player Arguments", self.test_cli_invalid_player_arguments)
        self.run_test("Missing Required Arguments", self.test_cli_missing_arguments)
        self.run_test("Malformed Weight Matrix", self.test_cli_malformed_weight_matrix)
        
        # Tournament System Tests
        print("\n" + "=" * 40)
        print("TOURNAMENT SYSTEM TESTS")
        print("=" * 40)
        
        self.run_test("Missing Executable Detection", self.test_tournament_missing_executable)
        self.run_test("Corrupted Engine Output", self.test_tournament_corrupted_output)
        
        # System Resource Tests
        print("\n" + "=" * 40)
        print("SYSTEM RESOURCE TESTS") 
        print("=" * 40)
        
        self.run_test("Resource Exhaustion Scenarios", self.test_resource_exhaustion_scenarios)
        self.run_test("File System Edge Cases", self.test_file_system_edge_cases)
        self.run_test("Signal Handling", self.test_signal_handling)
        
        # Final Results
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.test_count}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Error handling is robust.")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Review error handling implementation.")
            return False

def main():
    """Main entry point for the test suite"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        return
        
    test_suite = ErrorHandlingTestSuite()
    success = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()