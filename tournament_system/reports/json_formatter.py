"""
JSON report formatter for tournament system.

Formats tournament results as structured JSON output.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from ..models import TournamentReport


class JSONFormatter:
    """
    Formats tournament results as structured JSON output.
    
    Provides comprehensive tournament data in machine-readable format.
    """
    
    def __init__(self, indent: int = 2):
        """
        Initialize JSON formatter.
        
        Args:
            indent: JSON indentation level (default: 2)
        """
        self.indent = indent
        
    def format_report(self, report: TournamentReport) -> str:
        """
        Format tournament report as JSON string.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            Formatted JSON string
        """
        data = report.to_dict()
        
        # Add generation metadata
        data["generation_info"] = {
            "generated_at": datetime.now().isoformat(),
            "generator": "Tournament System Enhancement",
            "format_version": "1.0.0"
        }
        
        return json.dumps(data, indent=self.indent, ensure_ascii=False)
        
    def save_report(self, report: TournamentReport, output_path: str):
        """
        Save tournament report as JSON file.
        
        Args:
            report: TournamentReport to save
            output_path: Path for output file
            
        Raises:
            IOError: If file write fails
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(self.format_report(report))
                
        except Exception as e:
            raise IOError(f"Failed to save JSON report to {output_path}: {e}")
            
    def format_matchup_details(self, report: TournamentReport) -> str:
        """
        Format only matchup details as JSON.
        
        Args:
            report: TournamentReport to extract matchups from
            
        Returns:
            JSON string with matchup details only
        """
        matchups_data = {
            "matchups": [mr.to_dict() for mr in report.matchup_results],
            "summary": {
                "total_matchups": len(report.matchup_results),
                "total_games": report.total_games_played,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        return json.dumps(matchups_data, indent=self.indent, ensure_ascii=False)
        
    def format_rankings_only(self, report: TournamentReport) -> str:
        """
        Format only matrix rankings as JSON.
        
        Args:
            report: TournamentReport to extract rankings from
            
        Returns:
            JSON string with rankings only
        """
        rankings_data = {
            "matrix_rankings": report.get_matrix_rankings(),
            "tournament_info": {
                "total_games": report.total_games_played,
                "duration_seconds": report.tournament_duration,
                "matrices_count": len(report.tournament_config.matrices)
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(rankings_data, indent=self.indent, ensure_ascii=False)
        
    @staticmethod
    def load_report(file_path: str) -> Dict[str, Any]:
        """
        Load tournament report from JSON file.
        
        Args:
            file_path: Path to JSON report file
            
        Returns:
            Dictionary with tournament data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON report file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in report file: {e}")
        except Exception as e:
            raise IOError(f"Failed to load JSON report: {e}")
            
    def __str__(self) -> str:
        """String representation."""
        return f"JSONFormatter(indent={self.indent})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"JSONFormatter(indent={self.indent})"