#!/usr/bin/env python3
"""
Tournament Runner CLI for 3D Tic-Tac-Toe Engine

Command-line interface for running automated tournaments between different
heuristic weight matrices.

Usage:
    python tournament_runner.py --config config.csv --iterations 100
"""

import argparse
import sys
import os
import time
from pathlib import Path

# Add tournament_system to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tournament_system import TournamentManager
from tournament_system.game_runner import EngineError, EngineNotFoundError, EngineValidationError
from tournament_system.tournament_manager import ValidationError


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure command-line argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Run automated tournaments between weight matrix configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic tournament with 50 games per matchup
    python tournament_runner.py --config tournament_config.csv --iterations 50
    
    # Tournament with randomization enabled
    python tournament_runner.py --config config.csv --iterations 100 --randomization
    
    # Custom output directory and engine path
    python tournament_runner.py --config config.csv --iterations 25 \\
        --output-dir results/ --engine-path ./TTTTengine/tttt
    
    # Generate only JSON and text reports
    python tournament_runner.py --config config.csv --iterations 10 \\
        --formats json,text
        """
    )
    
    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '--config', '-c',
        type=str,
        required=True,
        help='Path to CSV configuration file with weight matrices'
    )
    required.add_argument(
        '--iterations', '-i',
        type=int,
        required=True,
        help='Number of games per matchup pair'
    )
    
    # Optional arguments
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='./tournament_results',
        help='Output directory for results (default: ./tournament_results)'
    )
    parser.add_argument(
        '--randomization', '-r',
        action='store_true',
        help='Enable randomized move selection when scores are tied'
    )
    parser.add_argument(
        '--formats', '-f',
        type=str,
        default='json,csv,text',
        help='Comma-separated output formats: json,csv,text (default: all)'
    )
    parser.add_argument(
        '--engine-path', '-e',
        type=str,
        default='./tttt',
        help='Path to tttt executable (default: ./tttt)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable detailed progress output'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate configuration and engine, do not run tournament'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show tournament plan without executing games'
    )
    
    return parser


def validate_arguments(args) -> None:
    """
    Validate command-line arguments.
    
    Args:
        args: Parsed arguments from argparse
        
    Raises:
        SystemExit: If validation fails
    """
    # Validate iterations
    if args.iterations <= 0:
        print("Error: Iterations must be a positive integer", file=sys.stderr)
        sys.exit(1)
        
    # Validate config file exists
    if not os.path.exists(args.config):
        print(f"Error: Configuration file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
        
    # Validate engine path exists
    if not os.path.exists(args.engine_path):
        print(f"Error: Engine executable not found: {args.engine_path}", file=sys.stderr)
        sys.exit(1)
        
    # Validate output formats
    valid_formats = {'json', 'csv', 'text'}
    requested_formats = set(f.strip().lower() for f in args.formats.split(','))
    invalid_formats = requested_formats - valid_formats
    if invalid_formats:
        print(f"Error: Invalid output formats: {invalid_formats}", file=sys.stderr)
        print(f"Valid formats are: {', '.join(valid_formats)}", file=sys.stderr)
        sys.exit(1)
        
    args.formats = list(requested_formats)


def print_configuration_summary(manager: TournamentManager, args) -> None:
    """
    Print tournament configuration summary.
    
    Args:
        manager: TournamentManager instance
        args: Command-line arguments
    """
    config_summary = manager.get_configuration_summary()
    
    print("Tournament Configuration:")
    print("=" * 50)
    print(f"Configuration File: {config_summary['config_file']}")
    print(f"Engine Path: {args.engine_path}")
    print(f"Output Directory: {config_summary['output_directory']}")
    print()
    
    print(f"Weight Matrices ({config_summary['matrices_count']}):")
    for i, label in enumerate(config_summary['matrix_labels'], 1):
        print(f"  {i:2d}. {label}")
    print()
    
    print(f"Tournament Parameters:")
    print(f"  Iterations per Matchup: {args.iterations}")
    print(f"  Randomization: {'Enabled' if args.randomization else 'Disabled'}")
    print(f"  Output Formats: {', '.join(args.formats)}")
    print(f"  Expected Total Games: {config_summary['matrices_count'] * (config_summary['matrices_count'] - 1) * args.iterations:,}")
    print()


def show_progress_updates(manager: TournamentManager, verbose: bool = False) -> None:
    """
    Show periodic progress updates during tournament execution.
    
    Args:
        manager: TournamentManager instance
        verbose: Enable detailed progress information
    """
    last_update = 0
    update_interval = 5  # seconds
    
    while True:
        progress = manager.get_progress()
        
        # Check if tournament is still running
        if progress['games_completed'] >= progress['games_total']:
            break
            
        current_time = time.time()
        if current_time - last_update >= update_interval:
            completion_pct = progress.get('completion_percentage', 0)
            
            print(f"\rProgress: {completion_pct:5.1f}% "
                  f"({progress['games_completed']:,}/{progress['games_total']:,} games)", 
                  end='', flush=True)
                  
            if verbose and progress.get('current_matchup'):
                print(f" | Current: {progress['current_matchup']}")
            elif not verbose:
                print("", end='', flush=True)
                
            last_update = current_time
            
        time.sleep(0.5)
        
    print()  # Final newline


def run_tournament(args) -> int:
    """
    Run the tournament with given arguments.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Initialize tournament manager with enhanced error handling
        print("Initializing tournament manager...")
        
        try:
            manager = TournamentManager(args.config, args.output_dir)
        except FileNotFoundError as e:
            print(f"✗ Configuration file error: {e}", file=sys.stderr)
            print(f"  Please check that the file exists: {args.config}", file=sys.stderr)
            return 1
        except PermissionError as e:
            print(f"✗ Permission error: {e}", file=sys.stderr)
            print(f"  Please check file permissions for: {args.config}", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"✗ Configuration validation error:", file=sys.stderr)
            print(f"  {e}", file=sys.stderr)
            print(f"\n  Please check the CSV format and data values in: {args.config}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"✗ Unexpected error loading configuration: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
        
        # Update engine path if specified
        if args.engine_path != './tttt':
            try:
                manager.game_runner.engine_path = args.engine_path
                manager.game_runner._validate_engine_exists()
            except EngineNotFoundError as e:
                print(f"✗ Engine not found: {e}", file=sys.stderr)
                print(f"  Please check the engine path: {args.engine_path}", file=sys.stderr)
                return 1
            
        # Update output formats
        try:
            manager.config.output_formats = args.formats
        except ValueError as e:
            print(f"✗ Invalid output format: {e}", file=sys.stderr)
            return 1
        
        print("Configuration loaded successfully.")
        print()
        
        # Print configuration summary
        print_configuration_summary(manager, args)
        
        # Validate configuration and engine
        print("Validating configuration and engine...")
        try:
            manager._validate_configuration()
            print("✓ Configuration validation passed")
            print("✓ Engine validation passed")
        except (ValidationError, EngineValidationError) as e:
            print(f"✗ Validation failed: {e}", file=sys.stderr)
            return 1
            
        print()
        
        # Handle validate-only mode
        if args.validate_only:
            print("Validation complete. Use --iterations to run tournament.")
            return 0
            
        # Handle dry-run mode  
        if args.dry_run:
            print("DRY RUN - Tournament plan:")
            matchups = manager.config.get_all_matchups()
            for i, (m1, m2) in enumerate(matchups, 1):
                print(f"  {i:2d}. {m1.label} vs {m2.label} ({args.iterations * 2} games)")
            print(f"\nTotal: {len(matchups)} matchups, {len(matchups) * args.iterations * 2:,} games")
            return 0
            
        # Confirm before starting large tournaments
        total_games = len(manager.config.get_all_matchups()) * args.iterations * 2
        if total_games > 1000:
            response = input(f"About to run {total_games:,} games. Continue? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Tournament cancelled.")
                return 0
                
        # Run tournament
        print(f"Starting tournament...")
        start_time = time.time()
        
        # TODO: In a full implementation, we'd run progress updates in a separate thread
        # For now, the tournament manager handles progress internally
        report = manager.run_tournament(args.iterations, args.randomization)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print()
        print("Tournament Summary:")
        print("-" * 30)
        print(f"Games Completed: {report.total_games_played:,}")
        print(f"Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print(f"Games per Hour: {report.games_per_hour:.1f}")
        
        # Show top performers
        rankings = report.get_matrix_rankings()
        if rankings:
            print()
            print("Top Performers:")
            for i, ranking in enumerate(rankings[:3], 1):
                print(f"  {i}. {ranking['label']:15s} {ranking['win_rate']:6.1%} "
                      f"({ranking['wins']} wins)")
                      
        print()
        print(f"Reports saved to: {args.output_dir}")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nTournament interrupted by user.")
        return 1
    except EngineNotFoundError as e:
        print(f"Engine Error: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        return 1
    except EngineError as e:
        print(f"Game Execution Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """
    Main entry point for tournament runner.
    
    Returns:
        Exit code
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Validate arguments
    try:
        validate_arguments(args)
    except SystemExit as e:
        return e.code
        
    # Run tournament
    return run_tournament(args)


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)