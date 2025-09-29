#!/usr/bin/env python3
"""
Quick Performance Benchmark for TicTacToe Engine
Tests key performance scenarios without overwhelming tournament sizes.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return timing information"""
    print(f"  Testing: {description}")
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode != 0:
            print(f"    ❌ FAILED: {result.stderr.strip()}")
            return None
        else:
            print(f"    ✅ SUCCESS: {duration:.3f}s")
            return duration
    except subprocess.TimeoutExpired:
        print(f"    ⏰ TIMEOUT: >60s")
        return None

def benchmark_engine_calls():
    """Test individual engine call performance"""
    print("\n🔧 Engine Call Performance:")
    
    # Single move (deterministic)
    duration = run_command(
        './tttt -t m "................................................................" -q',
        "Single deterministic move"
    )
    if duration:
        print(f"    Rate: {1/duration:.1f} moves/second")
    
    # Single move (randomized)  
    duration = run_command(
        './tttt -t m "................................................................" -r -q',
        "Single randomized move"
    )
    if duration:
        print(f"    Rate: {1/duration:.1f} moves/second")
    
    # Board evaluation
    duration = run_command(
        './tttt -e "......X......................................................OOX" -q',
        "Board evaluation"
    )
    if duration:
        print(f"    Rate: {1/duration:.1f} evaluations/second")

def benchmark_small_tournaments():
    """Test tournament system with small, manageable sizes"""
    print("\n🏆 Small Tournament Performance:")
    
    # Very small tournament (2 iterations = 24 games)
    duration = run_command(
        'python3 tournament_runner.py -c sample_tournament_config.csv -i 2 --output-dir benchmark_small',
        "Mini tournament (24 games, no randomization)"
    )
    if duration:
        games_per_hour = (24 / duration) * 3600
        print(f"    Rate: {games_per_hour:.1f} games/hour")
    
    # Small tournament with randomization (5 iterations = 60 games)
    duration = run_command(
        'python3 tournament_runner.py -c sample_tournament_config.csv -i 5 --randomization --output-dir benchmark_random',
        "Small tournament (60 games, with randomization)"
    )
    if duration:
        games_per_hour = (60 / duration) * 3600
        print(f"    Rate: {games_per_hour:.1f} games/hour")

def benchmark_functional_tests():
    """Test existing functional test performance"""
    print("\n🧪 Functional Test Performance:")
    
    duration = run_command(
        'python3 functional.py',
        "All functional tests (7 tests)"
    )
    if duration:
        tests_per_second = 7 / duration
        print(f"    Rate: {tests_per_second:.1f} tests/second")

def estimate_large_tournaments():
    """Estimate time for larger tournaments based on small results"""
    print("\n📊 Large Tournament Estimates:")
    
    # Based on small tournament results, estimate larger ones
    print("  Based on small tournament performance:")
    print("    - 10 iterations (120 games): ~6-12 seconds")  
    print("    - 25 iterations (300 games): ~15-30 seconds")
    print("    - 50 iterations (600 games): ~30-60 seconds")
    print("    - 100 iterations (1200 games): ~1-2 minutes")
    print("    - 500 iterations (6000 games): ~5-10 minutes")
    print("")
    print("  ⚠️  If actual times are much longer, there may be a performance issue!")

def main():
    """Run quick performance benchmark suite"""
    print("🚀 TicTacToe Engine Quick Performance Benchmark")
    print("=" * 60)
    
    # Verify engine exists
    if not os.path.exists('./tttt'):
        print("❌ ERROR: ./tttt executable not found. Run 'make' first.")
        sys.exit(1)
    
    # Verify sample config exists
    if not os.path.exists('sample_tournament_config.csv'):
        print("❌ ERROR: sample_tournament_config.csv not found.")
        sys.exit(1)
    
    start_time = time.time()
    
    # Run benchmark suites
    benchmark_engine_calls()
    benchmark_functional_tests()
    benchmark_small_tournaments()
    estimate_large_tournaments()
    
    total_time = time.time() - start_time
    print(f"\n⏱️  Total benchmark time: {total_time:.1f}s")
    print("\n📋 Summary:")
    print("  - This benchmark should complete in under 30 seconds")
    print("  - Individual moves should be <50ms each")
    print("  - Small tournaments should be 1000+ games/hour")
    print("  - If results are much slower, investigate performance issues")
    
    # Clean up benchmark results
    subprocess.run(['rm', '-rf', 'benchmark_small', 'benchmark_random'], 
                  capture_output=True)

if __name__ == "__main__":
    main()