"""
TournamentManager for tournament system.

Main orchestrator for running automated tournaments between different
weight matrix configurations.
"""

import os
import time
from typing import Dict, Any, List, Optional
from .models import (TournamentConfiguration, TournamentReport, MatchupResult, 
                    WeightMatrix)
from .game_runner import GameRunner, EngineError
from .reports import JSONFormatter, TextFormatter, CSVFormatter


class ValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class TournamentManager:
    """
    Main orchestrator for running automated tournaments between different
    weight matrix configurations.
    
    Handles tournament execution, progress tracking, and result coordination.
    """
    
    def __init__(self, config_path: str, output_dir: str = "./tournament_results"):
        """
        Initialize tournament manager with configuration.
        
        Args:
            config_path: Path to CSV configuration file
            output_dir: Directory for output report files (default: "./tournament_results")
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValidationError: If config format is invalid
        """
        self.config_path = config_path
        self.output_dir = output_dir
        
        # Load and validate configuration
        try:
            self.config = TournamentConfiguration.from_csv_file(config_path)
        except (FileNotFoundError, ValueError) as e:
            if isinstance(e, FileNotFoundError):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            else:
                raise ValidationError(f"Invalid configuration: {e}")
        
        # Initialize game runner
        self.game_runner = GameRunner()
        
        # Tournament state
        self.current_report: Optional[TournamentReport] = None
        self._progress = {
            "games_completed": 0,
            "games_total": 0,
            "current_matchup": None,
            "start_time": None,
            "estimated_completion": None
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
    def _validate_configuration(self):
        """
        Validate tournament configuration and engine.
        
        Raises:
            ValidationError: If configuration or engine validation fails
        """
        try:
            # Validate engine functionality
            self.game_runner.validate_engine()
        except Exception as e:
            raise ValidationError(f"Engine validation failed: {e}")
            
        # Validate configuration requirements
        if len(self.config.matrices) < 2:
            raise ValidationError("Tournament requires at least 2 weight matrices")
            
        if self.config.iterations_per_matchup <= 0:
            raise ValidationError("Iterations per matchup must be positive")
            
    def _execute_matchup(self, matrix1: WeightMatrix, matrix2: WeightMatrix, 
                        iterations: int, randomization: bool = False) -> MatchupResult:
        """
        Execute all games for a single matchup between two matrices.
        
        Args:
            matrix1: First weight matrix
            matrix2: Second weight matrix  
            iterations: Number of games to play
            randomization: Enable engine randomization
            
        Returns:
            MatchupResult with all game statistics
            
        Raises:
            EngineError: If game execution fails
        """
        matchup = MatchupResult(matrix1.label, matrix2.label)
        
        # Play games with both matrices as first/second player
        for i in range(iterations):
            # Matrix1 as first player
            try:
                game_result = self.game_runner.play_game(matrix1, matrix2, randomization)
                matchup.add_game_result(game_result, matrix1_played_first=True)
                self._progress["games_completed"] += 1
                
            except Exception as e:
                raise EngineError(f"Game failed (matrix1 first, iteration {i+1}): {e}")
                
            # Matrix2 as first player (reverse order)
            try:
                game_result = self.game_runner.play_game(matrix2, matrix1, randomization)
                matchup.add_game_result(game_result, matrix1_played_first=False)
                self._progress["games_completed"] += 1
                
            except Exception as e:
                raise EngineError(f"Game failed (matrix2 first, iteration {i+1}): {e}")
                
        return matchup
        
    def _calculate_estimated_completion(self):
        """Calculate estimated completion time based on progress."""
        if not self._progress["start_time"] or self._progress["games_completed"] == 0:
            return None
            
        elapsed = time.time() - self._progress["start_time"]
        games_per_second = self._progress["games_completed"] / elapsed
        
        remaining_games = self._progress["games_total"] - self._progress["games_completed"]
        if games_per_second > 0:
            remaining_seconds = remaining_games / games_per_second
            return time.time() + remaining_seconds
        return None
        
    def run_tournament(self, iterations: int, randomization: bool = False) -> TournamentReport:
        """
        Execute complete tournament with all matrix combinations.
        
        Args:
            iterations: Number of games per matchup
            randomization: Enable engine randomization flag
            
        Returns:
            TournamentReport with complete statistics
            
        Raises:
            ValidationError: If configuration is invalid
            EngineError: If tttt executable fails
            IOError: If report generation fails
        """
        # Validate everything before starting
        self._validate_configuration()
        
        # Update configuration with runtime parameters
        self.config.iterations_per_matchup = iterations
        self.config.randomization_enabled = randomization
        
        # Initialize tournament report
        self.current_report = TournamentReport(self.config)
        self.current_report.start_tournament()
        
        # Initialize progress tracking
        matchups = self.config.get_all_matchups()
        self._progress.update({
            "games_completed": 0,
            "games_total": len(matchups) * 2 * iterations,  # 2 games per iteration (role switching)
            "start_time": time.time(),
            "current_matchup": None
        })
        
        print(f"Starting tournament with {len(matchups)} matchups, {iterations} iterations each")
        print(f"Total games to play: {self._progress['games_total']}")
        print()
        
        # Execute all matchups
        try:
            for i, (matrix1, matrix2) in enumerate(matchups):
                self._progress["current_matchup"] = f"{matrix1.label} vs {matrix2.label}"
                
                print(f"Matchup {i+1}/{len(matchups)}: {self._progress['current_matchup']}")
                
                # Execute matchup
                matchup_result = self._execute_matchup(
                    matrix1, matrix2, iterations, randomization)
                
                # Add to report
                self.current_report.add_matchup_result(matchup_result)
                
                # Update progress estimate
                self._progress["estimated_completion"] = self._calculate_estimated_completion()
                
                # Progress update
                progress_pct = (self._progress["games_completed"] / 
                              self._progress["games_total"]) * 100
                print(f"  Completed: {progress_pct:.1f}% "
                      f"({self._progress['games_completed']}/{self._progress['games_total']} games)")
                
        except Exception as e:
            # Mark tournament as completed even if failed
            self.current_report.complete_tournament()
            raise e
            
        # Mark tournament completion
        self.current_report.complete_tournament()
        
        print()
        print(f"Tournament completed in {self.current_report.tournament_duration:.1f} seconds")
        print(f"Total games played: {self.current_report.total_games_played}")
        
        # Generate reports in configured formats
        self._generate_reports(self.current_report)
        
        return self.current_report
        
    def _generate_reports(self, report: TournamentReport):
        """
        Generate tournament reports in all configured formats.
        
        Args:
            report: TournamentReport to generate output from
        """
        output_formats = self.config.output_formats
        base_name = "tournament_report"
        
        try:
            # Generate JSON report
            if "json" in output_formats:
                json_formatter = JSONFormatter()
                json_path = os.path.join(self.output_dir, f"{base_name}.json")
                json_formatter.save_report(report, json_path)
                print(f"JSON report saved: {json_path}")
                
            # Generate text report
            if "text" in output_formats:
                text_formatter = TextFormatter()
                text_path = os.path.join(self.output_dir, f"{base_name}.txt")
                text_formatter.save_report(report, text_path)
                print(f"Text report saved: {text_path}")
                
                # Also save summary
                summary_path = os.path.join(self.output_dir, "tournament_summary.txt")
                text_formatter.save_report(report, summary_path, summary_only=True)
                print(f"Summary report saved: {summary_path}")
                
            # Generate CSV reports
            if "csv" in output_formats:
                csv_formatter = CSVFormatter()
                csv_files = csv_formatter.save_all_reports(report, self.output_dir, base_name)
                print("CSV reports saved:")
                for file_type, path in csv_files.items():
                    print(f"  {file_type}: {path}")
                    
        except Exception as e:
            print(f"Warning: Report generation failed: {e}")
            # Don't raise exception - tournament completed successfully
        
    def get_progress(self) -> Dict[str, Any]:
        """
        Get current tournament progress information.
        
        Returns:
            Dictionary with completed/total games, estimated time remaining
        """
        progress = self._progress.copy()
        
        # Add derived metrics
        if progress["games_total"] > 0:
            progress["completion_percentage"] = (
                progress["games_completed"] / progress["games_total"]) * 100
        else:
            progress["completion_percentage"] = 0.0
            
        # Add time estimates
        if progress["start_time"]:
            progress["elapsed_seconds"] = time.time() - progress["start_time"]
            
            if progress["estimated_completion"]:
                progress["remaining_seconds"] = max(0, progress["estimated_completion"] - time.time())
            else:
                progress["remaining_seconds"] = None
        else:
            progress["elapsed_seconds"] = 0
            progress["remaining_seconds"] = None
            
        return progress
        
    def load_configuration(self, config_path: str):
        """
        Load new tournament configuration.
        
        Args:
            config_path: Path to CSV configuration file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValidationError: If config format is invalid
        """
        try:
            self.config = TournamentConfiguration.from_csv_file(config_path)
            self.config_path = config_path
        except (FileNotFoundError, ValueError) as e:
            if isinstance(e, FileNotFoundError):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            else:
                raise ValidationError(f"Invalid configuration: {e}")
                
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get summary of current tournament configuration.
        
        Returns:
            Dictionary with configuration details
        """
        return {
            "config_file": self.config_path,
            "output_directory": self.output_dir,
            "matrices_count": len(self.config.matrices),
            "matrix_labels": self.config.matrix_labels,
            "default_iterations": self.config.iterations_per_matchup,
            "randomization_enabled": self.config.randomization_enabled,
            "output_formats": self.config.output_formats,
            "estimated_total_games": self.config.total_games_count
        }
        
    def __str__(self) -> str:
        """String representation."""
        return f"TournamentManager({len(self.config.matrices)} matrices, {self.output_dir})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"TournamentManager(config_path='{self.config_path}', "
                f"output_dir='{self.output_dir}', "
                f"matrices={len(self.config.matrices)})")