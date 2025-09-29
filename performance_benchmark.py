#!/usr/bin/env python3
"""
Performance Benchmarking Suite for TicTacToe Engine
Tests various scenarios to establish baseline performance and detect regressions.
"""

import subprocess
import time
import json
import sys
import os
from datetime import datetime
from pathlib import Path

class PerformanceBenchmark:
    def __init__(self, engine_path="./tttt"):
        self.engine_path = engine_path
        self.results = []
        
    def benchmark_single_move(self, board_state="." * 64, randomized=False, iterations=1000):
        """Benchmark single move generation performance."""
        print(f"Benchmarking single moves ({'randomized' if randomized else 'deterministic'})...")
        
        cmd = [self.engine_path, "-t", "m", board_state, "-q"]
        if randomized:
            cmd.append("-r")
            
        start_time = time.time()
        for i in range(iterations):
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Engine failed on iteration {i}: {result.stderr}")
                
        end_time = time.time()
        total_time = end_time - start_time
        moves_per_second = iterations / total_time
        
        return {
            "test": "single_move",
            "randomized": randomized,
            "iterations": iterations,
            "total_time": total_time,
            "moves_per_second": moves_per_second,
            "avg_time_per_move": total_time / iterations * 1000  # ms
        }
    
    def benchmark_tournament(self, config_file, iterations_per_matchup, randomized=False):
        """Benchmark full tournament performance."""
        print(f"Benchmarking tournament ({'randomized' if randomized else 'deterministic'}, {iterations_per_matchup} iterations)...")
        
        output_dir = f"benchmark_results_{int(time.time())}"
        cmd = [
            "python3", "tournament_runner.py",
            "--config", config_file,
            "--iterations", str(iterations_per_matchup),
            "--output-dir", output_dir,
            "--formats", "json"  # Only JSON for speed
        ]
        if randomized:
            cmd.append("--randomization")
            
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        end_time = time.time()
        
        if result.returncode != 0:
            raise RuntimeError(f"Tournament failed: {result.stderr}")
            
        # Parse tournament output to get game count
        lines = result.stdout.split('\n')
        games_played = 0
        for line in lines:
            if "Total games played:" in line:
                games_played = int(line.split(':')[1].strip())
                break
                
        total_time = end_time - start_time
        games_per_second = games_played / total_time if total_time > 0 else 0
        
        # Cleanup
        subprocess.run(["rm", "-rf", output_dir], capture_output=True)
        
        return {
            "test": "tournament",
            "randomized": randomized,
            "iterations_per_matchup": iterations_per_matchup,
            "total_games": games_played,
            "total_time": total_time,
            "games_per_second": games_per_second,
            "avg_time_per_game": total_time / games_played * 1000 if games_played > 0 else 0  # ms
        }
    
    def benchmark_board_evaluation(self, iterations=10000):
        """Benchmark board evaluation performance."""
        print("Benchmarking board evaluation...")
        
        # Test with a complex board state
        board_state = "X..O....O...X..OO...OXX..OX....XO....OX..OOX...OX..X.......XX..O"
        cmd = [self.engine_path, "-e", board_state, "-q"]
        
        start_time = time.time()
        for i in range(iterations):
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Evaluation failed on iteration {i}: {result.stderr}")
                
        end_time = time.time()
        total_time = end_time - start_time
        evaluations_per_second = iterations / total_time
        
        return {
            "test": "board_evaluation",
            "iterations": iterations,
            "total_time": total_time,
            "evaluations_per_second": evaluations_per_second,
            "avg_time_per_evaluation": total_time / iterations * 1000  # ms
        }
    
    def run_comprehensive_benchmark(self):
        """Run complete performance benchmark suite."""
        print("=== TicTacToe Engine Performance Benchmark Suite ===")
        print(f"Engine: {self.engine_path}")
        print(f"Date: {datetime.now().isoformat()}")
        print()
        
        try:
            # 1. Single Move Performance
            self.results.append(self.benchmark_single_move(randomized=False, iterations=1000))
            self.results.append(self.benchmark_single_move(randomized=True, iterations=1000))
            
            # 2. Board Evaluation Performance  
            self.results.append(self.benchmark_board_evaluation(iterations=5000))
            
            # 3. Small Tournament Performance
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 10, randomized=False))
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 10, randomized=True))
            
            # 4. Medium Tournament Performance
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 50, randomized=False))
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 50, randomized=True))
            
            # 5. Large Tournament Performance (if time permits)
            print("Running large tournament benchmark (this may take a while)...")
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 100, randomized=False))
            self.results.append(self.benchmark_tournament("sample_tournament_config.csv", 100, randomized=True))
            
        except Exception as e:
            print(f"Benchmark failed: {e}")
            return False
            
        return True
    
    def generate_report(self):
        """Generate performance benchmark report."""
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("="*60)
        
        # Single Move Performance
        single_move_det = next(r for r in self.results if r["test"] == "single_move" and not r["randomized"])
        single_move_rand = next(r for r in self.results if r["test"] == "single_move" and r["randomized"])
        
        print(f"\n📊 Single Move Performance:")
        print(f"  Deterministic: {single_move_det['moves_per_second']:.1f} moves/sec ({single_move_det['avg_time_per_move']:.2f}ms avg)")
        print(f"  Randomized:    {single_move_rand['moves_per_second']:.1f} moves/sec ({single_move_rand['avg_time_per_move']:.2f}ms avg)")
        
        overhead = ((single_move_rand['avg_time_per_move'] - single_move_det['avg_time_per_move']) / single_move_det['avg_time_per_move']) * 100
        print(f"  Randomization overhead: {overhead:+.1f}%")
        
        # Board Evaluation
        board_eval = next(r for r in self.results if r["test"] == "board_evaluation")
        print(f"\n🎯 Board Evaluation Performance:")
        print(f"  {board_eval['evaluations_per_second']:.1f} evaluations/sec ({board_eval['avg_time_per_evaluation']:.2f}ms avg)")
        
        # Tournament Performance
        print(f"\n🏆 Tournament Performance:")
        tournament_results = [r for r in self.results if r["test"] == "tournament"]
        
        for result in sorted(tournament_results, key=lambda x: (x["iterations_per_matchup"], x["randomized"])):
            mode = "randomized" if result["randomized"] else "deterministic"
            print(f"  {result['iterations_per_matchup']} iter/matchup ({mode}): {result['games_per_second']:.1f} games/sec ({result['total_games']} games in {result['total_time']:.1f}s)")
        
        # Performance Summary
        print(f"\n📈 Performance Summary:")
        max_games_per_sec = max(r['games_per_second'] for r in tournament_results)
        max_games_per_hour = max_games_per_sec * 3600
        print(f"  Peak Tournament Rate: {max_games_per_sec:.1f} games/sec ({max_games_per_hour:.0f} games/hour)")
        print(f"  Peak Single Move Rate: {max(single_move_det['moves_per_second'], single_move_rand['moves_per_second']):.1f} moves/sec")
        print(f"  Board Evaluation Rate: {board_eval['evaluations_per_second']:.1f} evaluations/sec")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"benchmark_report_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "engine_path": self.engine_path,
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            },
            "results": self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {report_file}")
        
        # Performance regression detection
        self.check_performance_regressions()
        
        return report_file
    
    def check_performance_regressions(self):
        """Check for potential performance issues."""
        print(f"\n🔍 Performance Analysis:")
        
        single_move_det = next(r for r in self.results if r["test"] == "single_move" and not r["randomized"])
        single_move_rand = next(r for r in self.results if r["test"] == "single_move" and r["randomized"])
        
        # Check for excessive randomization overhead
        overhead = ((single_move_rand['avg_time_per_move'] - single_move_det['avg_time_per_move']) / single_move_det['avg_time_per_move']) * 100
        if overhead > 50:
            print(f"  ⚠️  HIGH randomization overhead: {overhead:.1f}% (expected < 50%)")
        else:
            print(f"  ✅ Randomization overhead acceptable: {overhead:.1f}%")
        
        # Check minimum performance thresholds
        min_moves_per_sec = 1000  # Expect at least 1000 moves/sec
        if single_move_det['moves_per_second'] < min_moves_per_sec:
            print(f"  ⚠️  LOW single move performance: {single_move_det['moves_per_second']:.1f} moves/sec (expected > {min_moves_per_sec})")
        else:
            print(f"  ✅ Single move performance good: {single_move_det['moves_per_second']:.1f} moves/sec")
        
        # Check tournament performance
        tournament_results = [r for r in self.results if r["test"] == "tournament"]
        min_games_per_sec = 10  # Expect at least 10 games/sec for tournaments
        
        for result in tournament_results:
            if result['games_per_second'] < min_games_per_sec:
                mode = "randomized" if result["randomized"] else "deterministic"
                print(f"  ⚠️  LOW tournament performance ({mode}): {result['games_per_second']:.1f} games/sec (expected > {min_games_per_sec})")

def main():
    """Main benchmark execution."""
    if not os.path.exists("./tttt"):
        print("Error: Engine executable './tttt' not found. Please run 'make' first.")
        sys.exit(1)
        
    if not os.path.exists("sample_tournament_config.csv"):
        print("Error: 'sample_tournament_config.csv' not found.")
        sys.exit(1)
    
    benchmark = PerformanceBenchmark()
    
    print("Starting comprehensive performance benchmark...")
    print("This will take several minutes to complete.\n")
    
    if benchmark.run_comprehensive_benchmark():
        benchmark.generate_report()
        print("\n✅ Performance benchmark completed successfully!")
    else:
        print("\n❌ Performance benchmark failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()