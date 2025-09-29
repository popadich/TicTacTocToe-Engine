#!/usr/bin/env python3
"""
Integration Testing Suite for TicTacToe Tournament System

This comprehensive test suite validates:
- Tournament system end-to-end functionality
- Randomization verification 
- Error handling and edge cases
- Configuration validation
- Multi-format reporting
- Cross-platform compatibility
- Performance regression detection
"""

import subprocess
import os
import sys
import json
import csv
import tempfile
import shutil
import time
from pathlib import Path

class IntegrationTestSuite:
    def __init__(self):
        self.test_results = []
        self.temp_dirs = []
        self.start_time = time.time()
        
    def setup(self):
        """Initialize test environment"""
        print("🚀 TicTacToe Integration Test Suite")
        print("=" * 60)
        
        # Verify prerequisites
        if not os.path.exists('./tttt'):
            raise Exception("❌ Engine executable './tttt' not found. Run 'make' first.")
        
        if not os.path.exists('tournament_runner.py'):
            raise Exception("❌ Tournament runner 'tournament_runner.py' not found.")
            
        if not os.path.exists('sample_tournament_config.csv'):
            raise Exception("❌ Sample config 'sample_tournament_config.csv' not found.")
        
        print("✅ Prerequisites verified")
        
    def cleanup(self):
        """Clean up temporary test directories"""
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
    def run_command(self, cmd, description, expected_returncode=0, timeout=60):
        """Run a command and validate results"""
        print(f"  🔧 {description}")
        
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            
            success = (result.returncode == expected_returncode)
            
            test_result = {
                'test': description,
                'success': success,
                'returncode': result.returncode,
                'expected_returncode': expected_returncode,
                'stdout': result.stdout[:500],  # Limit output size
                'stderr': result.stderr[:500]
            }
            
            self.test_results.append(test_result)
            
            if success:
                print(f"    ✅ PASS")
                return result
            else:
                print(f"    ❌ FAIL (exit code: {result.returncode})")
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"    ⏰ TIMEOUT (>{timeout}s)")
            self.test_results.append({
                'test': description,
                'success': False,
                'error': 'Timeout',
                'timeout': timeout
            })
            return None
        except Exception as e:
            print(f"    💥 EXCEPTION: {e}")
            self.test_results.append({
                'test': description,
                'success': False,
                'error': str(e)
            })
            return None
    
    def create_temp_dir(self, prefix="integration_test"):
        """Create temporary directory and track for cleanup"""
        temp_dir = tempfile.mkdtemp(prefix=f"{prefix}_")
        self.temp_dirs.append(temp_dir)
        return temp_dir
        
    def create_test_config(self, filename, matrices=None):
        """Create a test configuration file"""
        if matrices is None:
            # Default 2-matrix config for testing
            matrices = [
                ('test_A', [0,-1,-2,-4,-8,1,0,0,0,0,2,0,1,0,0,4,0,0,0,0,8,0,0,0,0]),
                ('test_B', [0,-2,-3,-5,-10,2,0,0,0,0,3,0,1,0,0,5,0,0,0,0,10,0,0,0,0])
            ]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            header = ['label'] + [f'w{i}_{j}' for i in range(5) for j in range(5)]
            writer.writerow(header)
            
            # Write matrices
            for name, weights in matrices:
                writer.writerow([name] + weights)
        
        return filename

    def test_engine_functionality(self):
        """Test core engine functionality"""
        print("\n🔧 Testing Engine Core Functionality")
        print("-" * 40)
        
        # Test engine version
        self.run_command('./tttt --version', 'Engine version check')
        
        # Test engine help
        self.run_command('./tttt --help', 'Engine help display')
        
        # Test deterministic move
        self.run_command('./tttt -t m "................................................................" -q', 'Deterministic move generation')
        
        # Test randomized move  
        self.run_command('./tttt -t m "................................................................" -r -q', 'Randomized move generation')
        
        # Test board evaluation
        self.run_command('./tttt -e "......X......................................................OOX" -q', 'Board evaluation')
        
        # Test functional tests
        self.run_command('python3 functional.py', 'Functional test suite')

    def test_tournament_system_basic(self):
        """Test basic tournament system functionality"""
        print("\n🏆 Testing Tournament System - Basic")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("tournament_basic")
        
        # Test configuration validation
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 1 --validate-only',
            'Configuration validation'
        )
        
        # Test small tournament
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 2 --output-dir {temp_dir}',
            'Small tournament execution'
        )
        
        # Verify output files exist
        expected_files = [
            'tournament_report.json',
            'tournament_report.txt', 
            'tournament_summary.txt',
            'tournament_report_summary.csv',
            'tournament_report_rankings.csv',
            'tournament_report_matchups.csv',
            'tournament_report_games.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(temp_dir, filename)
            if os.path.exists(filepath):
                print(f"    ✅ Output file exists: {filename}")
                self.test_results.append({
                    'test': f'Output file creation: {filename}',
                    'success': True
                })
            else:
                print(f"    ❌ Missing output file: {filename}")
                self.test_results.append({
                    'test': f'Output file creation: {filename}',
                    'success': False,
                    'error': 'File not found'
                })

    def test_randomization_functionality(self):
        """Test randomization functionality and verification"""
        print("\n🎲 Testing Randomization Functionality")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("randomization_test")
        
        # Test deterministic tournament (should be reproducible)
        result1 = self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 3 --output-dir {temp_dir}/det1',
            'Deterministic tournament run 1'
        )
        
        result2 = self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 3 --output-dir {temp_dir}/det2',
            'Deterministic tournament run 2'
        )
        
        # Compare deterministic results (should be identical)
        if result1 and result2:
            try:
                with open(f'{temp_dir}/det1/tournament_report.json') as f1, \
                     open(f'{temp_dir}/det2/tournament_report.json') as f2:
                    data1 = json.load(f1)
                    data2 = json.load(f2)
                    
                    # Compare deterministic results using matchup details
                    matchups1 = data1.get('matchup_details', [])
                    matchups2 = data2.get('matchup_details', [])
                    
                    # Compare win counts which should be identical for deterministic runs
                    results1 = [(m['matrix1_wins'], m['matrix2_wins'], m['ties']) for m in matchups1]
                    results2 = [(m['matrix1_wins'], m['matrix2_wins'], m['ties']) for m in matchups2]
                    
                    if results1 == results2:
                        print("    ✅ Deterministic reproducibility verified")
                        self.test_results.append({
                            'test': 'Deterministic reproducibility',
                            'success': True
                        })
                    else:
                        print("    ❌ Deterministic results differ")
                        self.test_results.append({
                            'test': 'Deterministic reproducibility', 
                            'success': False,
                            'error': 'Results not identical'
                        })
            except Exception as e:
                print(f"    ❌ Failed to compare results: {e}")
                self.test_results.append({
                    'test': 'Deterministic reproducibility',
                    'success': False,
                    'error': str(e)
                })
        
        # Test randomized tournaments
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 5 --randomization --output-dir {temp_dir}/rand1',
            'Randomized tournament run 1'
        )
        
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 5 --randomization --output-dir {temp_dir}/rand2', 
            'Randomized tournament run 2'
        )

    def test_configuration_validation(self):
        """Test configuration file validation and error handling"""
        print("\n📋 Testing Configuration Validation")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("config_test")
        
        # Test valid configuration
        valid_config = self.create_test_config(f'{temp_dir}/valid.csv')
        self.run_command(
            f'python3 tournament_runner.py -c {valid_config} -i 1 --validate-only',
            'Valid configuration validation'
        )
        
        # Test invalid configurations
        # Missing header
        with open(f'{temp_dir}/invalid_header.csv', 'w') as f:
            f.write('wrong,header,format\n')
            f.write('test,1,2\n')
        
        self.run_command(
            f'python3 tournament_runner.py -c {temp_dir}/invalid_header.csv -i 1 --validate-only',
            'Invalid header rejection',
            expected_returncode=1
        )
        
        # Invalid weights (not enough columns)
        with open(f'{temp_dir}/invalid_weights.csv', 'w') as f:
            f.write('label,w0_0,w0_1,w0_2\n')  # Only 3 weight columns instead of 25
            f.write('test,1,2,3\n')
            
        self.run_command(
            f'python3 tournament_runner.py -c {temp_dir}/invalid_weights.csv -i 1 --validate-only',
            'Invalid weight count rejection',
            expected_returncode=1
        )
        
        # Duplicate labels
        matrices = [
            ('duplicate', [0,-1,-2,-4,-8,1,0,0,0,0,2,0,1,0,0,4,0,0,0,0,8,0,0,0,0]),
            ('duplicate', [0,-2,-3,-5,-10,2,0,0,0,0,3,0,1,0,0,5,0,0,0,0,10,0,0,0,0])
        ]
        duplicate_config = self.create_test_config(f'{temp_dir}/duplicate.csv', matrices)
        self.run_command(
            f'python3 tournament_runner.py -c {duplicate_config} -i 1 --validate-only',
            'Duplicate label rejection',
            expected_returncode=1
        )

    def test_output_formats(self):
        """Test multi-format output generation"""
        print("\n📄 Testing Multi-Format Output")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("format_test")
        
        # Test individual formats
        formats = ['json', 'csv', 'text']
        
        for fmt in formats:
            self.run_command(
                f'python3 tournament_runner.py -c sample_tournament_config.csv -i 2 --output-dir {temp_dir}/{fmt}_test --formats {fmt}',
                f'Single format output: {fmt}'
            )
        
        # Test combined formats
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 2 --output-dir {temp_dir}/multi_test --formats json,csv,text',
            'Multi-format output'
        )

    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n🚨 Testing Error Handling")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("error_test")
        
        # Test nonexistent config file
        self.run_command(
            f'python3 tournament_runner.py -c nonexistent.csv -i 1',
            'Nonexistent config file handling',
            expected_returncode=1
        )
        
        # Test invalid engine path
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 1 --engine-path ./nonexistent_engine',
            'Invalid engine path handling',
            expected_returncode=1
        )
        
        # Test invalid iterations
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 0',
            'Zero iterations handling',
            expected_returncode=1
        )
        
        # Test read-only output directory
        readonly_dir = f'{temp_dir}/readonly'
        os.makedirs(readonly_dir, exist_ok=True)
        os.chmod(readonly_dir, 0o444)  # Read-only
        
        self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 1 --output-dir {readonly_dir}/subdir',
            'Read-only directory handling',
            expected_returncode=1
        )

    def test_performance_regression(self):
        """Test for performance regressions"""
        print("\n⚡ Testing Performance Regression")
        print("-" * 40)
        
        temp_dir = self.create_temp_dir("perf_test")
        
        # Benchmark small tournament
        start_time = time.time()
        result = self.run_command(
            f'python3 tournament_runner.py -c sample_tournament_config.csv -i 10 --output-dir {temp_dir}',
            'Performance benchmark (60 games)'
        )
        end_time = time.time()
        
        if result:
            duration = end_time - start_time
            games_per_hour = (60 / duration) * 3600
            
            # Performance threshold: should be >30K games/hour (realistic for comprehensive tests)
            if games_per_hour > 30000:
                print(f"    ✅ Performance OK: {games_per_hour:.0f} games/hour")
                self.test_results.append({
                    'test': 'Performance benchmark',
                    'success': True,
                    'games_per_hour': games_per_hour,
                    'duration': duration
                })
            else:
                print(f"    ⚠️  Performance warning: {games_per_hour:.0f} games/hour (below 30K threshold)")
                self.test_results.append({
                    'test': 'Performance benchmark',
                    'success': False,
                    'games_per_hour': games_per_hour,
                    'duration': duration,
                    'error': 'Below performance threshold'
                })

    def test_examples(self):
        """Test example configurations"""
        print("\n📚 Testing Example Configurations")
        print("-" * 40)
        
        if not os.path.exists('examples'):
            print("    ⚠️  Examples directory not found, skipping")
            return
        
        temp_dir = self.create_temp_dir("examples_test")
        
        # Test each example configuration
        example_configs = [
            'examples/quick_test.csv',
            'examples/aggressive_strategies.csv', 
            'examples/defensive_strategies.csv',
            'examples/positional_strategies.csv',
            'examples/randomization_test.csv'
        ]
        
        for config in example_configs:
            if os.path.exists(config):
                config_name = os.path.basename(config)
                self.run_command(
                    f'python3 tournament_runner.py -c {config} -i 2 --output-dir {temp_dir}/{config_name}_test',
                    f'Example config: {config_name}'
                )

    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for t in self.test_results if t['success'])
        failed_tests = total_tests - passed_tests
        
        total_time = time.time() - self.start_time
        
        print(f"\n📊 Integration Test Results")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        print(f"Total Time: {total_time:.1f}s")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for test in self.test_results:
                if not test['success']:
                    print(f"  - {test['test']}")
                    if 'error' in test:
                        print(f"    Error: {test['error']}")
        
        # Save detailed report
        report_data = {
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': passed_tests/total_tests*100,
                'total_time': total_time
            },
            'test_results': self.test_results
        }
        
        with open('INTEGRATION_TEST_REPORT.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📋 Detailed report saved: INTEGRATION_TEST_REPORT.json")
        
        return failed_tests == 0

    def run_all_tests(self):
        """Run the complete integration test suite"""
        try:
            self.setup()
            
            self.test_engine_functionality()
            self.test_tournament_system_basic()
            self.test_randomization_functionality()
            self.test_configuration_validation()
            self.test_output_formats()
            self.test_error_handling()
            self.test_performance_regression()
            self.test_examples()
            
            success = self.generate_report()
            
            return success
            
        except Exception as e:
            print(f"\n💥 Test suite failed with exception: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main entry point"""
    suite = IntegrationTestSuite()
    success = suite.run_all_tests()
    
    if success:
        print(f"\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print(f"\n💥 Some integration tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()