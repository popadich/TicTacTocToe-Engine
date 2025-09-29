"""
Tournament System Enhancement for 3D Tic-Tac-Toe Engine

This package provides automated tournament functionality for testing
different heuristic weight matrices against each other.

Components:
- models: Core data structures (WeightMatrix, GameResult, etc.)
- reports: Output formatting (JSON, CSV, text)
- game_runner: Engine subprocess communication
- tournament_manager: Tournament orchestration
"""

__version__ = "1.0.0"
__author__ = "TicTacTocToe-Engine Project"

# Core exports
try:
    from .game_runner import GameRunner
    from .tournament_manager import TournamentManager
    __all__ = ["GameRunner", "TournamentManager"]
except ImportError:
    # During development, modules might not exist yet
    __all__ = []