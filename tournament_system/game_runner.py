"""
GameRunner for tournament system.

Executes individual games between two weight matrices using subprocess
communication with the tttt engine.
"""

import os
import subprocess
import subprocess
import time
from typing import Optional
from .models.weight_matrix import WeightMatrix
from .models.game_result import GameResult


class EngineError(Exception):
    """Raised when engine execution fails."""
    pass


class EngineNotFoundError(Exception):
    """Raised when engine executable is not found or not executable."""
    pass


class EngineValidationError(Exception):
    """Raised when engine fails validation tests."""
    pass


class GameRunner:
    """
    Executes individual games between two weight matrices using subprocess
    communication with the tttt engine.
    
    Handles engine validation, game execution, and result parsing.
    """
    
    # Empty board string (64 dots for 4x4x4 cube)
    EMPTY_BOARD = "." * 64
    
    # Maximum game duration before timeout (seconds)
    MAX_GAME_DURATION = 300  # 5 minutes
    
    def __init__(self, engine_path: str = "./tttt"):
        """
        Initialize game runner with engine executable path.
        
        Args:
            engine_path: Path to tttt executable (default: "./tttt")
            
        Raises:
            EngineNotFoundError: If executable doesn't exist or isn't executable
        """
        self.engine_path = engine_path
        self._validate_engine_exists()
        
    def _validate_engine_exists(self):
        """
        Check if engine executable exists and is executable.
        
        Raises:
            EngineNotFoundError: If engine is not found or not executable
        """
        if not os.path.exists(self.engine_path):
            raise EngineNotFoundError(f"Engine executable not found: {self.engine_path}")
            
        if not os.access(self.engine_path, os.X_OK):
            raise EngineNotFoundError(f"Engine executable is not executable: {self.engine_path}")
            
    def validate_engine(self) -> bool:
        """
        Verify engine executable is functional with basic test.
        
        Returns:
            True if engine passes basic functionality test
            
        Raises:
            EngineValidationError: If engine fails validation
        """
        try:
            # Test basic engine functionality with help flag
            result = subprocess.run(
                [self.engine_path, "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Engine should return help text and exit with code 0 or 1
            if result.returncode not in [0, 1]:
                raise EngineValidationError(f"Engine help command failed with code {result.returncode}")
                
            # Test tournament mode with empty board
            test_weights = "0 -2 -4 -8 -16 2 0 0 0 0 4 0 1 0 0 8 0 0 0 0 16 0 0 0 0"
            result = subprocess.run(
                [self.engine_path, "-t", "m", self.EMPTY_BOARD, "-w", test_weights, "-q"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise EngineValidationError(f"Engine tournament mode test failed: {result.stderr}")
                
            # Parse output to ensure it's valid move format
            output = result.stdout.strip()
            if not output:
                raise EngineValidationError("Engine returned empty output")
                
            # Parse engine output - same logic as _execute_move
            lines = output.split('\n')
            first_line_parts = lines[0].split()
            
            if len(first_line_parts) < 1:
                raise EngineValidationError(f"No move number found in output: '{output}'")
                
            try:
                move_num = int(first_line_parts[0])
            except ValueError:
                raise EngineValidationError(f"Invalid move number in output: '{first_line_parts[0]}'")
                
            game_over = "game_over" in first_line_parts
            
            if game_over and len(lines) >= 2:
                new_board = lines[1].strip()
            elif not game_over and len(first_line_parts) >= 2:
                new_board = lines[0].split(maxsplit=1)[1]
            else:
                raise EngineValidationError(f"Could not parse board state from output: '{output}'")
            
            # Validate board state
            if len(new_board) != 64:
                raise EngineValidationError(f"Invalid board state length: {len(new_board)}, expected 64")
                
            # Ensure the move was actually applied (move numbers are 1-based, positions 0-based)
            position = move_num - 1
            if position < 0 or position >= 64:
                raise EngineValidationError(f"Move number {move_num} out of range (1-64)")
            if new_board[position] == '.':
                raise EngineValidationError(f"Move {move_num} (position {position}) was not applied to board")
                
            if move_num < 0 or move_num >= 64:
                raise EngineValidationError(f"Invalid move number from engine: {move_num}")
                
            return True
            
        except subprocess.TimeoutExpired:
            raise EngineValidationError("Engine validation timed out")
        except subprocess.SubprocessError as e:
            raise EngineValidationError(f"Engine subprocess error: {e}")
        except Exception as e:
            raise EngineValidationError(f"Unexpected validation error: {e}")
            
    def _format_weights_for_command(self, matrix: WeightMatrix) -> str:
        """
        Format weight matrix for command line.
        
        Args:
            matrix: WeightMatrix to format
            
        Returns:
            Space-separated string of 25 weight values
        """
        return matrix.to_command_string()
        
    def _execute_move(self, board_state: str, player: str, weights: str, 
                     randomization: bool = False) -> tuple:
        """
        Execute a single move using the engine.
        
        Args:
            board_state: Current board state as 64-character string
            player: Player type ("m" for machine, "h" for human)
            weights: Weight matrix as space-separated string
            randomization: Enable randomization flag
            
        Returns:
            Tuple of (move_number, new_board_state)
            
        Raises:
            EngineError: If engine execution fails
        """
        # Build command
        cmd = [self.engine_path, "-t", player, board_state, "-w", weights, "-q"]
        # Note: Randomization flag is not supported by the engine CLI
        # The randomization parameter is accepted but ignored for now
            
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout per move
            )
            
            if result.returncode != 0:
                raise EngineError(f"Engine move failed: {result.stderr.strip()}")
                
            output = result.stdout.strip()
            if not output:
                raise EngineError("Engine returned empty output")
                
            # Parse engine output format with -q flag: 
            # Normal: "NUMBER BOARD_STATE"
            # Game over: "NUMBER game_over\nBOARD_STATE"
            lines = output.split('\n')
            
            # First line contains move number (and possibly "game_over")
            first_line_parts = lines[0].split()
            if len(first_line_parts) < 1:
                raise EngineError(f"No move number found in output: '{output}'")
                
            try:
                move_number = int(first_line_parts[0])
            except ValueError:
                raise EngineError(f"Invalid move number in output: '{first_line_parts[0]}'")
                
            # Determine if this is a game over condition
            game_over = "game_over" in first_line_parts
            
            # Board state is either in the first line (normal) or second line (game over)
            if game_over and len(lines) >= 2:
                # Game over: board is on second line
                new_board_state = lines[1].strip()
            elif not game_over and len(first_line_parts) >= 2:
                # Normal: board is rest of first line
                new_board_state = lines[0].split(maxsplit=1)[1]
            else:
                raise EngineError(f"Could not parse board state from output: '{output}'")
            
            # Validate board state length
            if len(new_board_state) != 64:
                raise EngineError(f"Invalid board state length: {len(new_board_state)}, expected 64")
                
            return move_number, new_board_state, game_over
            
        except subprocess.TimeoutExpired:
            raise EngineError("Engine move timed out")
        except ValueError as e:
            raise EngineError(f"Invalid engine output format: {output}")
        except Exception as e:
            raise EngineError(f"Unexpected engine error: {e}")
            
    def _check_game_over(self, board_state: str) -> Optional[str]:
        """
        Check if game is over by examining board state.
        
        For now, this only detects full board (tie).
        TODO: Implement proper win detection using engine analysis.
        
        Args:
            board_state: Current board state
            
        Returns:
            "tie" if board is full, None if game continues
        """
        # Simple check: if no empty positions, it's a tie
        if "." not in board_state:
            return "tie"
        return None
        
    def play_game(self, matrix1: WeightMatrix, matrix2: WeightMatrix, 
                  randomization: bool = False) -> GameResult:
        """
        Execute single game between two weight matrices.
        
        Args:
            matrix1: First player's weight configuration
            matrix2: Second player's weight configuration
            randomization: Enable random move selection for tied scores
            
        Returns:
            GameResult with winner, moves, and game metadata
            
        Raises:
            EngineError: If game execution fails
            TimeoutError: If game exceeds maximum duration
        """
        start_time = time.time()
        board_state = self.EMPTY_BOARD
        move_count = 0
        
        # Format weights for both matrices
        weights1 = self._format_weights_for_command(matrix1)
        weights2 = self._format_weights_for_command(matrix2)
        
        try:
            while True:
                # Check timeout
                if time.time() - start_time > self.MAX_GAME_DURATION:
                    raise TimeoutError(f"Game exceeded maximum duration of {self.MAX_GAME_DURATION} seconds")
                
                # Check if game is over
                game_over = self._check_game_over(board_state)
                if game_over:
                    break
                    
                # Count current pieces to determine whose turn it is
                x_count = board_state.count('X')
                o_count = board_state.count('O')
                
                # Validate board state consistency
                if abs(x_count - o_count) > 1:
                    raise EngineError(f"Invalid board state: X={x_count}, O={o_count}, difference too large")
                
                # Determine current player based on board state
                # X (human/matrix1) goes first, so if counts are equal, it's X's turn
                # If X has one more, it's O's turn
                if x_count == o_count:
                    # Matrix1's turn (plays as human 'X')
                    move_num, new_board, engine_game_over = self._execute_move(
                        board_state, "h", weights1, randomization)
                elif x_count == o_count + 1:
                    # Matrix2's turn (plays as machine 'O')
                    move_num, new_board, engine_game_over = self._execute_move(
                        board_state, "m", weights2, randomization)
                else:
                    # This should not happen given the validation above
                    raise EngineError(f"Unexpected board state: X={x_count}, O={o_count}")
                
                # Update board state and move count
                board_state = new_board
                move_count += 1
                
                # Check if engine detected game over
                if engine_game_over:
                    game_over = "engine_detected"
                    break
                        
                # Validate the move was properly applied
                new_x_count = new_board.count('X')
                new_o_count = new_board.count('O')
                
                # Exactly one piece should have been added
                if (new_x_count + new_o_count) != (x_count + o_count + 1):
                    raise EngineError(f"Move did not add exactly one piece: before X={x_count}, O={o_count}, after X={new_x_count}, O={new_o_count}")
                
                # Safety check for infinite games
                if move_count > 100:  # 4x4x4 has 64 positions max
                    game_over = "tie"
                    break
                    
        except Exception as e:
            game_duration = time.time() - start_time
            raise EngineError(f"Game execution failed after {move_count} moves "
                            f"in {game_duration:.2f}s: {e}")
        
        game_duration = time.time() - start_time
        
        # Determine winner - this is simplified logic
        # In a real implementation, we'd need proper win detection
        if game_over == "tie" or move_count >= 64:
            winner = "tie"
        elif move_count % 2 == 1:
            # Odd number of moves means first player (matrix1) made last move
            winner = "player1"
        else:
            # Even number of moves means second player (matrix2) made last move  
            winner = "player2"
            
        return GameResult(
            player1_matrix=matrix1.label,
            player2_matrix=matrix2.label,
            winner=winner,
            move_count=move_count,
            game_duration=game_duration,
            final_board=board_state
        )
        
    def __str__(self) -> str:
        """String representation."""
        return f"GameRunner(engine_path='{self.engine_path}')"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"GameRunner(engine_path='{self.engine_path}')"