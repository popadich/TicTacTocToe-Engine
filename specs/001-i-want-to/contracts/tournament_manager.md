# Tournament Manager Interface Contract

## Overview
The TournamentManager serves as the main orchestrator for running automated tournaments between different weight matrix configurations.

## Interface Definition

### Constructor
```python
def __init__(self, config_path: str, output_dir: str = "./tournament_results"):
    """
    Initialize tournament manager with configuration.
    
    Args:
        config_path: Path to CSV configuration file
        output_dir: Directory for output report files
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValidationError: If config format is invalid
    """
```

### Primary Methods

#### run_tournament()
```python
def run_tournament(self, iterations: int, randomization: bool = False) -> TournamentReport:
    """
    Execute complete tournament with all matrix combinations.
    
    Args:
        iterations: Number of games per matchup
        randomization: Enable engine randomization flag
        
    Returns:
        TournamentReport with complete statistics
        
    Raises:
        EngineError: If tttt executable fails
        IOError: If report generation fails
    """
```

#### get_progress()
```python
def get_progress(self) -> Dict[str, Any]:
    """
    Get current tournament progress information.
    
    Returns:
        Dictionary with completed/total games, estimated time remaining
    """
```

## Input/Output Contracts

### Expected CSV Configuration Format
- Header: `label,w0_0,w0_1,...,w4_4` (26 columns)
- Data rows: String label + 25 integer weight values
- No empty rows or invalid data types
- Unique labels required

### Output Report Formats

#### JSON Report Structure
```json
{
    "tournament_info": {...},
    "matrix_rankings": [...],
    "matchup_details": [...],
    "execution_metadata": {...}
}
```

#### CSV Results Format
- Headers: matrix1,matrix2,total_games,matrix1_wins,matrix2_wins,win_rate
- One row per matrix matchup combination

## Error Handling Requirements

### Configuration Errors
- Invalid CSV format → ValidationError with specific line/column
- Duplicate matrix labels → DuplicateLabelError
- Invalid weight values → WeightValidationError

### Runtime Errors  
- Engine executable not found → EngineNotFoundError
- Game execution timeout → GameTimeoutError
- Insufficient disk space → StorageError

## Performance Guarantees

### Execution Time
- Must complete within 2x theoretical minimum (based on average game duration)
- Progress reporting every 10 completed games minimum
- Graceful handling of interruption signals

### Memory Usage
- Maximum 100MB RAM usage regardless of tournament size
- Streaming processing for large result sets
- Automatic cleanup of temporary files

## Integration Points

### Engine Communication
- Uses subprocess calls to tttt executable
- Parses standard output for move and board state
- Handles engine error conditions gracefully

### File System Dependencies
- Read access to configuration files
- Write access to output directory
- Temporary file creation for intermediate results