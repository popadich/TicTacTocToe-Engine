"""
Text report formatter for tournament system.

Formats tournament results as human-readable text output.
"""

import os
from datetime import datetime
from typing import List
from ..models import TournamentReport, MatchupResult


class TextFormatter:
    """
    Formats tournament results as human-readable text output.
    
    Provides clear, formatted text reports for human consumption.
    """
    
    def __init__(self, width: int = 80):
        """
        Initialize text formatter.
        
        Args:
            width: Report width in characters (default: 80)
        """
        self.width = width
        
    def format_report(self, report: TournamentReport) -> str:
        """
        Format complete tournament report as text.
        
        Args:
            report: TournamentReport to format
            
        Returns:
            Formatted text string
        """
        lines = []
        
        # Header
        lines.extend(self._format_header(report))
        lines.append("")
        
        # Tournament summary
        lines.extend(self._format_tournament_summary(report))
        lines.append("")
        
        # Matrix rankings
        lines.extend(self._format_matrix_rankings(report))
        lines.append("")
        
        # Matchup details
        lines.extend(self._format_matchup_details(report))
        lines.append("")
        
        # Performance analysis
        lines.extend(self._format_performance_analysis(report))
        
        # Footer
        lines.append("")
        lines.extend(self._format_footer())
        
        return "\n".join(lines)
        
    def _format_header(self, report: TournamentReport) -> List[str]:
        """Format report header section."""
        title = "TOURNAMENT RESULTS REPORT"
        separator = "=" * self.width
        
        return [
            separator,
            title.center(self.width),
            separator
        ]
        
    def _format_tournament_summary(self, report: TournamentReport) -> List[str]:
        """Format tournament summary section."""
        config = report.tournament_config
        
        lines = [
            "TOURNAMENT SUMMARY",
            "-" * 20,
            f"Configuration File: {config.config_file_path or 'N/A'}",
            f"Number of Matrices: {len(config.matrices)}",
            f"Iterations per Matchup: {config.iterations_per_matchup}",
            f"Randomization Enabled: {'Yes' if config.randomization_enabled else 'No'}",
            "",
            f"Total Games Played: {report.total_games_played:,}",
            f"Expected Games: {config.total_games_count:,}",
            f"Tournament Duration: {report.tournament_duration:.1f} seconds",
            f"Games per Hour: {report.games_per_hour:.1f}",
        ]
        
        if report.execution_start_time:
            lines.extend([
                f"Start Time: {report.execution_start_time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"End Time: {report.execution_end_time.strftime('%Y-%m-%d %H:%M:%S') if report.execution_end_time else 'In Progress'}"
            ])
            
        return lines
        
    def _format_matrix_rankings(self, report: TournamentReport) -> List[str]:
        """Format matrix rankings section."""
        rankings = report.get_matrix_rankings()
        
        lines = [
            "MATRIX RANKINGS",
            "-" * 15,
            ""
        ]
        
        # Table header
        header = f"{'Rank':>4} {'Matrix Label':20} {'Win Rate':>10} {'Wins':>6} {'Losses':>6} {'Ties':>6} {'Total':>6}"
        lines.append(header)
        lines.append("-" * len(header))
        
        # Rankings data
        for ranking in rankings:
            line = (f"{ranking['rank']:4d} "
                   f"{ranking['label']:20s} "
                   f"{ranking['win_rate']:9.1%} "
                   f"{ranking['wins']:6d} "
                   f"{ranking['losses']:6d} "
                   f"{ranking['ties']:6d} "
                   f"{ranking['total_games']:6d}")
            lines.append(line)
            
        return lines
        
    def _format_matchup_details(self, report: TournamentReport) -> List[str]:
        """Format detailed matchup results."""
        lines = [
            "DETAILED MATCHUP RESULTS",
            "-" * 25,
            ""
        ]
        
        for matchup in report.matchup_results:
            lines.extend(self._format_single_matchup(matchup))
            lines.append("")
            
        return lines
        
    def _format_single_matchup(self, matchup: MatchupResult) -> List[str]:
        """Format a single matchup result."""
        lines = [
            f"{matchup.matrix1_label} vs {matchup.matrix2_label}",
            "-" * 40
        ]
        
        # Summary stats
        lines.extend([
            f"Total Games: {matchup.total_games}",
            f"  {matchup.matrix1_label} Wins: {matchup.matrix1_wins} ({matchup.matrix1_win_rate:.1%})",
            f"  {matchup.matrix2_label} Wins: {matchup.matrix2_wins} ({matchup.matrix2_win_rate:.1%})",
            f"  Ties: {matchup.ties} ({matchup.tie_rate:.1%})",
            "",
            f"Average Game Duration: {matchup.average_game_duration:.2f} seconds",
            f"Average Moves per Game: {matchup.average_move_count:.1f}",
            f"First Player Advantage: {matchup.first_player_advantage:+.3f}"
        ])
        
        return lines
        
    def _format_performance_analysis(self, report: TournamentReport) -> List[str]:
        """Format performance analysis section."""
        lines = [
            "PERFORMANCE ANALYSIS",
            "-" * 20,
            ""
        ]
        
        # Overall first player advantage
        overall_fpa = report.get_overall_first_player_advantage()
        lines.extend([
            f"Overall First Player Advantage: {overall_fpa:+.3f}",
            ""
        ])
        
        # Top performers
        rankings = report.get_matrix_rankings()
        if rankings:
            best = rankings[0]
            worst = rankings[-1] if len(rankings) > 1 else best
            
            lines.extend([
                "Best Performing Matrix:",
                f"  {best['label']} - {best['win_rate']:.1%} win rate ({best['wins']} wins)",
                "",
                "Lowest Performing Matrix:",
                f"  {worst['label']} - {worst['win_rate']:.1%} win rate ({worst['wins']} wins)",
            ])
            
        # Randomization analysis
        if report.tournament_config.randomization_enabled:
            rand_analysis = report.get_randomization_analysis()
            lines.extend([
                "",
                "Randomization Analysis:",
                f"  Randomization was {'enabled' if rand_analysis.get('enabled') else 'disabled'}",
                f"  Games with randomization: {rand_analysis.get('total_games_with_randomization', 0)}"
            ])
            
        return lines
        
    def _format_footer(self) -> List[str]:
        """Format report footer."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return [
            "=" * self.width,
            f"Report generated by Tournament System Enhancement at {timestamp}".center(self.width),
            "=" * self.width
        ]
        
    def format_summary_only(self, report: TournamentReport) -> str:
        """
        Format brief summary without detailed matchups.
        
        Args:
            report: TournamentReport to summarize
            
        Returns:
            Brief text summary
        """
        lines = []
        
        lines.extend(self._format_header(report))
        lines.append("")
        lines.extend(self._format_tournament_summary(report))
        lines.append("")
        lines.extend(self._format_matrix_rankings(report))
        lines.append("")
        lines.extend(self._format_footer())
        
        return "\n".join(lines)
        
    def save_report(self, report: TournamentReport, output_path: str, summary_only: bool = False):
        """
        Save tournament report as text file.
        
        Args:
            report: TournamentReport to save
            output_path: Path for output file
            summary_only: If True, save only summary without detailed matchups
            
        Raises:
            IOError: If file write fails
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            content = self.format_summary_only(report) if summary_only else self.format_report(report)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            raise IOError(f"Failed to save text report to {output_path}: {e}")
            
    def __str__(self) -> str:
        """String representation."""
        return f"TextFormatter(width={self.width})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"TextFormatter(width={self.width})"