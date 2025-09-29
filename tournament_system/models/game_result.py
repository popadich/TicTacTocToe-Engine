"""
GameResult model for tournament system.

Records the outcome of a single game between two weight matrices.
"""

from typing import Optional
import time


class GameResult:
    """
    Records outcome of a single game between two weight matrices.
    
    Tracks winner, game statistics, and metadata for analysis.
    """
    
    VALID_WINNERS = {"player1", "player2", "tie"}
    
    def __init__(self, 
                 player1_matrix: str,
                 player2_matrix: str, 
                 winner: str,
                 move_count: int,
                 game_duration: float,
                 final_board: str):
        """
        Initialize game result.
        
        Args:
            player1_matrix: Label of first player's weight matrix
            player2_matrix: Label of second player's weight matrix
            winner: Game winner ("player1", "player2", "tie")
            move_count: Number of moves in the game
            game_duration: Seconds elapsed during game execution
            final_board: Final board state as string representation
            
        Raises:
            ValueError: If winner is invalid or counts are negative
        """
        if winner not in self.VALID_WINNERS:
            raise ValueError(f"Winner must be one of {self.VALID_WINNERS}, got '{winner}'")
            
        if move_count < 0:
            raise ValueError("Move count must be non-negative")
            
        if game_duration < 0:
            raise ValueError("Game duration must be non-negative")
            
        if not player1_matrix.strip() or not player2_matrix.strip():
            raise ValueError("Matrix labels cannot be empty")
            
        self.player1_matrix = player1_matrix
        self.player2_matrix = player2_matrix
        self.winner = winner
        self.move_count = move_count
        self.game_duration = game_duration
        self.final_board = final_board
        self.timestamp = time.time()
        
    @property
    def player1_won(self) -> bool:
        """True if player1 won the game."""
        return self.winner == "player1"
        
    @property  
    def player2_won(self) -> bool:
        """True if player2 won the game."""
        return self.winner == "player2"
        
    @property
    def was_tie(self) -> bool:
        """True if game was a tie."""
        return self.winner == "tie"
        
    def get_winner_matrix(self) -> Optional[str]:
        """
        Get the winning matrix label.
        
        Returns:
            Matrix label of winner, or None if tie
        """
        if self.player1_won:
            return self.player1_matrix
        elif self.player2_won:
            return self.player2_matrix
        return None
        
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "player1_matrix": self.player1_matrix,
            "player2_matrix": self.player2_matrix,
            "winner": self.winner,
            "move_count": self.move_count,
            "game_duration": self.game_duration,
            "final_board": self.final_board,
            "timestamp": self.timestamp
        }
        
    def __str__(self) -> str:
        """String representation."""
        return f"GameResult({self.player1_matrix} vs {self.player2_matrix} -> {self.winner})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"GameResult(player1='{self.player1_matrix}', "
                f"player2='{self.player2_matrix}', winner='{self.winner}', "
                f"moves={self.move_count}, duration={self.game_duration:.3f}s)")