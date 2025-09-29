"""
MatchupResult model for tournament system.

Aggregates statistics for all games between two specific weight matrices.
"""

from typing import List
from .game_result import GameResult


class MatchupResult:
    """
    Aggregates statistics for all games between two specific weight matrices.
    
    Provides win/loss statistics and derived analytics for matchup analysis.
    """
    
    def __init__(self, matrix1_label: str, matrix2_label: str):
        """
        Initialize matchup result for two matrices.
        
        Args:
            matrix1_label: Label of first matrix
            matrix2_label: Label of second matrix
        """
        self.matrix1_label = matrix1_label
        self.matrix2_label = matrix2_label
        
        # Game statistics
        self.total_games = 0
        self.matrix1_wins = 0
        self.matrix2_wins = 0
        self.ties = 0
        
        # Role-based statistics
        self.matrix1_as_first_wins = 0
        self.matrix2_as_first_wins = 0
        
        # Performance metrics
        self.total_duration = 0.0
        self.total_moves = 0
        
        # Game history
        self._game_results: List[GameResult] = []
        
    def add_game_result(self, game_result: GameResult, matrix1_played_first: bool):
        """
        Add a game result to this matchup.
        
        Args:
            game_result: The completed game result
            matrix1_played_first: True if matrix1 was the first player
            
        Raises:
            ValueError: If game result doesn't match this matchup
        """
        # Validate that this game belongs to this matchup
        matrices = {game_result.player1_matrix, game_result.player2_matrix}
        expected = {self.matrix1_label, self.matrix2_label}
        
        if matrices != expected:
            raise ValueError(f"Game result matrices {matrices} don't match matchup {expected}")
            
        # Update statistics
        self.total_games += 1
        self.total_duration += game_result.game_duration
        self.total_moves += game_result.move_count
        
        # Determine which matrix won and update counts
        if game_result.was_tie:
            self.ties += 1
        elif game_result.get_winner_matrix() == self.matrix1_label:
            self.matrix1_wins += 1
            if matrix1_played_first:
                self.matrix1_as_first_wins += 1
        elif game_result.get_winner_matrix() == self.matrix2_label:
            self.matrix2_wins += 1  
            if not matrix1_played_first:
                self.matrix2_as_first_wins += 1
                
        self._game_results.append(game_result)
        
    @property
    def matrix1_win_rate(self) -> float:
        """Win rate for matrix1 (0.0 to 1.0)."""
        return self.matrix1_wins / self.total_games if self.total_games > 0 else 0.0
        
    @property
    def matrix2_win_rate(self) -> float:
        """Win rate for matrix2 (0.0 to 1.0)."""
        return self.matrix2_wins / self.total_games if self.total_games > 0 else 0.0
        
    @property
    def tie_rate(self) -> float:
        """Tie rate (0.0 to 1.0)."""
        return self.ties / self.total_games if self.total_games > 0 else 0.0
        
    @property
    def average_game_duration(self) -> float:
        """Average seconds per game."""
        return self.total_duration / self.total_games if self.total_games > 0 else 0.0
        
    @property
    def average_move_count(self) -> float:
        """Average moves per game."""
        return self.total_moves / self.total_games if self.total_games > 0 else 0.0
        
    @property
    def first_player_advantage(self) -> float:
        """
        Calculate first player advantage statistic.
        
        Returns:
            Positive value indicates first player advantage
        """
        if self.total_games == 0:
            return 0.0
            
        # Calculate win rate when each matrix plays first
        matrix1_first_games = sum(1 for gr in self._game_results 
                                 if gr.player1_matrix == self.matrix1_label)
        matrix2_first_games = self.total_games - matrix1_first_games
        
        if matrix1_first_games == 0 or matrix2_first_games == 0:
            return 0.0
            
        matrix1_first_win_rate = self.matrix1_as_first_wins / matrix1_first_games
        matrix2_first_win_rate = self.matrix2_as_first_wins / matrix2_first_games
        
        return (matrix1_first_win_rate + matrix2_first_win_rate) / 2 - 0.5
        
    def get_game_results(self) -> List[GameResult]:
        """Get all game results for this matchup."""
        return self._game_results.copy()
        
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "matrix1_label": self.matrix1_label,
            "matrix2_label": self.matrix2_label,
            "total_games": self.total_games,
            "matrix1_wins": self.matrix1_wins,
            "matrix2_wins": self.matrix2_wins,
            "ties": self.ties,
            "matrix1_win_rate": self.matrix1_win_rate,
            "matrix2_win_rate": self.matrix2_win_rate,
            "tie_rate": self.tie_rate,
            "matrix1_as_first_wins": self.matrix1_as_first_wins,
            "matrix2_as_first_wins": self.matrix2_as_first_wins,
            "average_game_duration": self.average_game_duration,
            "average_move_count": self.average_move_count,
            "first_player_advantage": self.first_player_advantage
        }
        
    def __str__(self) -> str:
        """String representation."""
        return f"MatchupResult({self.matrix1_label} vs {self.matrix2_label}: {self.total_games} games)"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"MatchupResult(matrix1='{self.matrix1_label}', matrix2='{self.matrix2_label}', "
                f"games={self.total_games}, m1_wins={self.matrix1_wins}, m2_wins={self.matrix2_wins})")