"""
CSV report formatter for tournament system.

Formats tournament results as CSV files for spreadsheet analysis.
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from ..models import TournamentReport


class CSVFormatter:
    """
    Formats tournament results as CSV files for spreadsheet analysis.
    
    Provides structured data export suitable for further analysis.
    """
    
    def __init__(self, delimiter: str = ',', quoting: int = csv.QUOTE_MINIMAL):
        """
        Initialize CSV formatter.
        
        Args:
            delimiter: CSV field delimiter (default: ',')
            quoting: CSV quoting mode (default: QUOTE_MINIMAL)
        """
        self.delimiter = delimiter
        self.quoting = quoting
        
    def format_matchup_results(self, report: TournamentReport) -> str:
        """
        Format matchup results as CSV string.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            CSV string with matchup data
        """
        output = []
        
        # Header
        headers = [
            'matrix1_label', 'matrix2_label', 'total_games',
            'matrix1_wins', 'matrix2_wins', 'ties',
            'matrix1_win_rate', 'matrix2_win_rate', 'tie_rate',
            'matrix1_as_first_wins', 'matrix2_as_first_wins',
            'average_game_duration', 'average_move_count', 'first_player_advantage'
        ]
        
        # Convert to CSV format
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer, delimiter=self.delimiter, quoting=self.quoting)
        
        writer.writerow(headers)
        
        for matchup in report.matchup_results:
            row = [
                matchup.matrix1_label,
                matchup.matrix2_label, 
                matchup.total_games,
                matchup.matrix1_wins,
                matchup.matrix2_wins,
                matchup.ties,
                f"{matchup.matrix1_win_rate:.4f}",
                f"{matchup.matrix2_win_rate:.4f}",
                f"{matchup.tie_rate:.4f}",
                matchup.matrix1_as_first_wins,
                matchup.matrix2_as_first_wins,
                f"{matchup.average_game_duration:.3f}",
                f"{matchup.average_move_count:.2f}",
                f"{matchup.first_player_advantage:.6f}"
            ]
            writer.writerow(row)
            
        return csv_buffer.getvalue()
        
    def format_matrix_rankings(self, report: TournamentReport) -> str:
        """
        Format matrix rankings as CSV string.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            CSV string with rankings data
        """
        rankings = report.get_matrix_rankings()
        
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer, delimiter=self.delimiter, quoting=self.quoting)
        
        # Header
        headers = ['rank', 'matrix_label', 'win_rate', 'total_wins', 'total_losses', 
                  'total_ties', 'total_games', 'description']
        writer.writerow(headers)
        
        # Data rows
        for ranking in rankings:
            row = [
                ranking['rank'],
                ranking['label'],
                f"{ranking['win_rate']:.4f}",
                ranking['wins'],
                ranking['losses'],
                ranking['ties'], 
                ranking['total_games'],
                ranking.get('description', '')
            ]
            writer.writerow(row)
            
        return csv_buffer.getvalue()
        
    def format_individual_games(self, report: TournamentReport) -> str:
        """
        Format individual game results as CSV string.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            CSV string with individual game data
        """
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer, delimiter=self.delimiter, quoting=self.quoting)
        
        # Header
        headers = [
            'game_id', 'player1_matrix', 'player2_matrix', 'winner',
            'move_count', 'game_duration', 'timestamp', 'final_board'
        ]
        writer.writerow(headers)
        
        # Data rows
        for i, game in enumerate(report.individual_games):
            row = [
                i + 1,  # game_id
                game.player1_matrix,
                game.player2_matrix,
                game.winner,
                game.move_count,
                f"{game.game_duration:.3f}",
                datetime.fromtimestamp(game.timestamp).isoformat(),
                game.final_board
            ]
            writer.writerow(row)
            
        return csv_buffer.getvalue()
        
    def format_tournament_summary(self, report: TournamentReport) -> str:
        """
        Format tournament summary as CSV string.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            CSV string with tournament summary
        """
        config = report.tournament_config
        
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer, delimiter=self.delimiter, quoting=self.quoting)
        
        # Summary as key-value pairs
        summary_data = [
            ['metric', 'value'],
            ['config_file', config.config_file_path or ''],
            ['matrices_count', len(config.matrices)],
            ['iterations_per_matchup', config.iterations_per_matchup],
            ['randomization_enabled', config.randomization_enabled],
            ['total_games_played', report.total_games_played],
            ['expected_games', config.total_games_count],
            ['tournament_duration_seconds', f"{report.tournament_duration:.3f}"],
            ['games_per_hour', f"{report.games_per_hour:.2f}"],
            ['start_time', report.execution_start_time.isoformat() if report.execution_start_time else ''],
            ['end_time', report.execution_end_time.isoformat() if report.execution_end_time else ''],
            ['overall_first_player_advantage', f"{report.get_overall_first_player_advantage():.6f}"]
        ]
        
        for row in summary_data:
            writer.writerow(row)
            
        return csv_buffer.getvalue()
        
    def save_matchup_results(self, report: TournamentReport, output_path: str):
        """
        Save matchup results as CSV file.
        
        Args:
            report: TournamentReport to save
            output_path: Path for output file
            
        Raises:
            IOError: If file write fails
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write(self.format_matchup_results(report))
                
        except Exception as e:
            raise IOError(f"Failed to save matchup CSV to {output_path}: {e}")
            
    def save_matrix_rankings(self, report: TournamentReport, output_path: str):
        """
        Save matrix rankings as CSV file.
        
        Args:
            report: TournamentReport to save
            output_path: Path for output file
            
        Raises:
            IOError: If file write fails
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write(self.format_matrix_rankings(report))
                
        except Exception as e:
            raise IOError(f"Failed to save rankings CSV to {output_path}: {e}")
            
    def save_individual_games(self, report: TournamentReport, output_path: str):
        """
        Save individual game results as CSV file.
        
        Args:
            report: TournamentReport to save
            output_path: Path for output file
            
        Raises:
            IOError: If file write fails
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write(self.format_individual_games(report))
                
        except Exception as e:
            raise IOError(f"Failed to save games CSV to {output_path}: {e}")
            
    def save_tournament_summary(self, report: TournamentReport, output_path: str):
        """
        Save tournament summary as CSV file.
        
        Args:
            report: TournamentReport to save  
            output_path: Path for output file
            
        Raises:
            IOError: If file write fails
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write(self.format_tournament_summary(report))
                
        except Exception as e:
            raise IOError(f"Failed to save summary CSV to {output_path}: {e}")
            
    def save_all_reports(self, report: TournamentReport, output_dir: str, base_name: str = "tournament"):
        """
        Save all CSV reports to specified directory.
        
        Args:
            report: TournamentReport to save
            output_dir: Directory for output files
            base_name: Base name for output files (default: "tournament")
            
        Returns:
            Dictionary with paths to created files
            
        Raises:
            IOError: If any file write fails
        """
        file_paths = {}
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Save each report type
            files_to_create = [
                ('summary', self.save_tournament_summary),
                ('rankings', self.save_matrix_rankings), 
                ('matchups', self.save_matchup_results),
                ('games', self.save_individual_games)
            ]
            
            for file_type, save_func in files_to_create:
                file_path = os.path.join(output_dir, f"{base_name}_{file_type}.csv")
                save_func(report, file_path)
                file_paths[file_type] = file_path
                
            return file_paths
            
        except Exception as e:
            raise IOError(f"Failed to save CSV reports to {output_dir}: {e}")
            
    def __str__(self) -> str:
        """String representation."""
        return f"CSVFormatter(delimiter='{self.delimiter}')"
        
    def __repr__(self) -> str:
        """Detailed representation.""" 
        return f"CSVFormatter(delimiter='{self.delimiter}', quoting={self.quoting})"