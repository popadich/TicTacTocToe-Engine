"""
TournamentReport model for tournament system.

Complete statistical analysis and results of tournament execution.
"""

import time
from typing import List, Dict, Any
from datetime import datetime
from .tournament_config import TournamentConfiguration
from .matchup_result import MatchupResult
from .game_result import GameResult


class TournamentReport:
    """
    Complete statistical analysis and results of tournament execution.
    
    Aggregates all matchup results and provides tournament-wide analytics.
    """
    
    def __init__(self, tournament_config: TournamentConfiguration):
        """
        Initialize tournament report.
        
        Args:
            tournament_config: Configuration used for this tournament
        """
        self.tournament_config = tournament_config
        self.execution_start_time = None
        self.execution_end_time = None
        
        # Results storage
        self.matchup_results: List[MatchupResult] = []
        self.individual_games: List[GameResult] = []
        
        # Progress tracking
        self._games_completed = 0
        
    def start_tournament(self):
        """Mark tournament start time."""
        self.execution_start_time = datetime.now()
        
    def complete_tournament(self):
        """Mark tournament completion time."""
        self.execution_end_time = datetime.now()
        
    def add_matchup_result(self, matchup_result: MatchupResult):
        """
        Add a completed matchup result.
        
        Args:
            matchup_result: Completed matchup with all games
        """
        self.matchup_results.append(matchup_result)
        self.individual_games.extend(matchup_result.get_game_results())
        self._games_completed += matchup_result.total_games
        
    @property
    def total_games_played(self) -> int:
        """Total number of games completed."""
        return len(self.individual_games)
        
    @property
    def tournament_duration(self) -> float:
        """
        Tournament duration in seconds.
        
        Returns:
            Duration in seconds, or 0 if not completed
        """
        if not self.execution_start_time or not self.execution_end_time:
            return 0.0
        return (self.execution_end_time - self.execution_start_time).total_seconds()
        
    @property
    def games_per_hour(self) -> float:
        """Games completed per hour execution rate."""
        duration_hours = self.tournament_duration / 3600
        if duration_hours == 0:
            return 0.0
        return self.total_games_played / duration_hours
        
    def get_matrix_rankings(self) -> List[Dict[str, Any]]:
        """
        Calculate overall matrix rankings by win rate.
        
        Returns:
            List of dictionaries with matrix statistics, sorted by win rate
        """
        # Aggregate statistics for each matrix
        matrix_stats = {}
        
        for matrix in self.tournament_config.matrices:
            label = matrix.label
            matrix_stats[label] = {
                "label": label,
                "total_games": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "description": matrix.description
            }
            
        # Process all game results
        for game in self.individual_games:
            # Update stats for both players
            for player_matrix in [game.player1_matrix, game.player2_matrix]:
                if player_matrix in matrix_stats:
                    matrix_stats[player_matrix]["total_games"] += 1
                    
                    if game.was_tie:
                        matrix_stats[player_matrix]["ties"] += 1
                    elif game.get_winner_matrix() == player_matrix:
                        matrix_stats[player_matrix]["wins"] += 1
                    else:
                        matrix_stats[player_matrix]["losses"] += 1
                        
        # Calculate win rates and rank
        rankings = []
        for stats in matrix_stats.values():
            total_games = stats["total_games"]
            if total_games > 0:
                win_rate = stats["wins"] / total_games
            else:
                win_rate = 0.0
                
            rankings.append({
                **stats,
                "win_rate": win_rate
            })
            
        # Sort by win rate (descending)
        rankings.sort(key=lambda x: x["win_rate"], reverse=True)
        
        # Add rank positions
        for i, ranking in enumerate(rankings):
            ranking["rank"] = i + 1
            
        return rankings
        
    def get_randomization_analysis(self) -> Dict[str, Any]:
        """
        Analyze randomization statistics if enabled.
        
        Returns:
            Dictionary with randomization analysis or empty if disabled
        """
        if not self.tournament_config.randomization_enabled:
            return {"enabled": False}
            
        # For randomization analysis, we'd need to track move selections
        # This is a placeholder for future enhancement
        return {
            "enabled": True,
            "total_games_with_randomization": self.total_games_played,
            "note": "Detailed randomization analysis requires move tracking"
        }
        
    def get_overall_first_player_advantage(self) -> float:
        """
        Calculate overall first player advantage across all matchups.
        
        Returns:
            Average first player advantage (0.0 = no advantage)
        """
        if not self.matchup_results:
            return 0.0
            
        advantages = [mr.first_player_advantage for mr in self.matchup_results]
        return sum(advantages) / len(advantages)
        
    def to_dict(self) -> dict:
        """Convert to complete dictionary representation."""
        return {
            "tournament_info": {
                "start_time": self.execution_start_time.isoformat() if self.execution_start_time else None,
                "end_time": self.execution_end_time.isoformat() if self.execution_end_time else None,
                "total_duration_seconds": self.tournament_duration,
                "total_games": self.total_games_played,
                "expected_games": self.tournament_config.total_games_count,
                "games_per_hour": self.games_per_hour,
                "matrices_count": len(self.tournament_config.matrices),
                "iterations_per_matchup": self.tournament_config.iterations_per_matchup,
                "randomization_enabled": self.tournament_config.randomization_enabled
            },
            "matrix_rankings": self.get_matrix_rankings(),
            "matchup_details": [mr.to_dict() for mr in self.matchup_results],
            "randomization_analysis": self.get_randomization_analysis(),
            "overall_first_player_advantage": self.get_overall_first_player_advantage(),
            "configuration": self.tournament_config.to_dict()
        }
        
    def get_summary_text(self) -> str:
        """
        Generate human-readable tournament summary.
        
        Returns:
            Multi-line string with tournament results summary
        """
        rankings = self.get_matrix_rankings()
        
        lines = [
            "Tournament Results Summary",
            "=" * 50,
            f"Total Games Played: {self.total_games_played}",
            f"Tournament Duration: {self.tournament_duration:.1f} seconds",
            f"Games per Hour: {self.games_per_hour:.1f}",
            "",
            "Matrix Rankings:",
            "-" * 20
        ]
        
        for ranking in rankings:
            lines.append(f"{ranking['rank']:2d}. {ranking['label']:15s} "
                        f"Win Rate: {ranking['win_rate']:6.1%} "
                        f"({ranking['wins']:3d}W/{ranking['losses']:3d}L/{ranking['ties']:3d}T)")
                        
        if self.tournament_config.randomization_enabled:
            lines.extend([
                "",
                f"First Player Advantage: {self.get_overall_first_player_advantage():+.3f}"
            ])
            
        return "\n".join(lines)
        
    def __str__(self) -> str:
        """String representation."""
        status = "completed" if self.execution_end_time else "in-progress"
        return f"TournamentReport({self.total_games_played} games, {status})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"TournamentReport(games={self.total_games_played}, "
                f"matchups={len(self.matchup_results)}, "
                f"duration={self.tournament_duration:.1f}s)")