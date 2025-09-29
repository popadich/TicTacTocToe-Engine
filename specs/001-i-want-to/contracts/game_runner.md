# Game Runner Interface Contract

## Overview
The GameRunner executes individual games between two weight matrices using subprocess communication with the tttt engine.

## Interface Definition

### Constructor
```python
def __init__(self, engine_path: str = "./tttt"):
    """
    Initialize game runner with engine executable path.
    
    Args:
        engine_path: Path to tttt executable
        
    Raises:
        EngineNotFoundError: If executable doesn't exist or isn't executable
    """
```

### Core Methods

#### play_game()
```python
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
```

#### validate_engine()
```python
def validate_engine(self) -> bool:
    """
    Verify engine executable is functional.
    
    Returns:
        True if engine passes basic functionality test
        
    Raises:
        EngineValidationError: If engine fails validation
    """
```

## Engine Communication Protocol

### Command Format
```bash
# Tournament mode with weight matrix
./tttt -t m "board_string" -w "w1 w2 w3 ... w25" [-r]

# Expected output format:
"move_number new_board_string"
```

### Game Flow Sequence
1. Initialize empty board: 64 '.' characters
2. Player 1 (matrix1) makes first move using tournament mode
3. Player 2 (matrix2) responds to updated board state  
4. Continue alternating until win condition or board full
5. Determine winner based on final game state

### Error Handling
- Invalid board state → GameStateError
- Engine timeout → EngineTimeoutError  
- Malformed engine output → ProtocolError
- Process execution failure → EngineExecutionError

## Input/Output Specifications

### WeightMatrix Input Format
- 25 space-separated integers for -w flag
- Values passed as: "w0_0 w0_1 w0_2 ... w4_3 w4_4"
- Engine expects row-major flattened 5x5 matrix

### GameResult Output Fields
```python
@dataclass
class GameResult:
    player1_matrix: str        # Matrix label for first player
    player2_matrix: str        # Matrix label for second player
    winner: str               # "player1", "player2", or "tie"
    move_count: int           # Total moves in game
    game_duration: float      # Seconds elapsed
    final_board: str          # 64-character board representation
```

## Performance Requirements

### Timing Constraints
- Maximum game duration: 60 seconds per game
- Engine response timeout: 5 seconds per move
- Process cleanup within 1 second of completion

### Resource Management
- One subprocess per game (no persistent processes)
- Automatic cleanup of zombie processes
- Memory usage <10MB per concurrent game

## Validation Requirements

### Pre-game Validation
- Verify weight matrices have exactly 25 values
- Confirm all weights are valid integers
- Check engine executable permissions and accessibility

### Post-game Validation  
- Verify winner determination is consistent with board state
- Validate move count matches actual game progression
- Confirm final board state represents valid game end condition

## Integration Contracts

### Dependency Requirements
- tttt executable compiled and accessible
- Python subprocess module available  
- Sufficient system resources for process spawning

### Thread Safety
- GameRunner instances are NOT thread-safe
- Create separate instances for concurrent game execution
- No shared state between GameRunner instances