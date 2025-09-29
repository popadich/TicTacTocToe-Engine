# Data Model: Tournament System Enhancement

## Core Entities

### WeightMatrix

**Purpose**: Represents a labeled heuristic weight configuration for the game engine

**Attributes**:
- `label`: String identifier (e.g., "alpha", "beta", "aggressive")  
- `weights`: List of 25 integers representing 5x5 matrix flattened row-major
- `description`: Optional human-readable description of the strategy

**Constraints**:
- Label must be unique within configuration
- Weights array must contain exactly 25 integer values
- Label must not contain commas (CSV compatibility)

**Example**:
```
WeightMatrix(
    label="default",
    weights=[0, -2, -4, -8, -16, 2, 0, 0, 0, 0, 4, 0, 1, 0, 0, 8, 0, 0, 0, 0, 16, 0, 0, 0, 0],
    description="Default engine weights"
)
```

### GameResult

**Purpose**: Records outcome of a single game between two weight matrices

**Attributes**:
- `player1_matrix`: String label of first player's weight matrix
- `player2_matrix`: String label of second player's weight matrix  
- `winner`: String indicating winner ("player1", "player2", "tie")
- `move_count`: Integer number of moves in the game
- `game_duration`: Float seconds elapsed for game execution
- `final_board`: String representation of final board state

**Constraints**:
- Matrix labels must reference valid WeightMatrix entries
- Winner must be one of three valid values
- Move count must be positive integer
- Duration must be non-negative float

### MatchupResult

**Purpose**: Aggregates statistics for all games between two specific weight matrices

**Attributes**:
- `matrix1_label`: String identifier for first matrix
- `matrix2_label`: String identifier for second matrix
- `total_games`: Integer count of games played between these matrices
- `matrix1_wins`: Integer count of wins for matrix1
- `matrix2_wins`: Integer count of wins for matrix2  
- `ties`: Integer count of tied games
- `matrix1_as_first_wins`: Integer wins when matrix1 plays first
- `matrix2_as_first_wins`: Integer wins when matrix2 plays first
- `average_game_duration`: Float average seconds per game
- `average_move_count`: Float average moves per game

**Derived Properties**:
- `matrix1_win_rate`: matrix1_wins / total_games
- `matrix2_win_rate`: matrix2_wins / total_games  
- `first_player_advantage`: Statistical analysis of first-move advantage

### TournamentConfiguration

**Purpose**: Complete tournament setup including all weight matrices and parameters

**Attributes**:
- `matrices`: List of WeightMatrix objects
- `iterations_per_matchup`: Integer games to play per matrix pair
- `randomization_enabled`: Boolean flag for engine randomization
- `output_formats`: List of strings ("json", "csv", "text")
- `config_file_path`: String path to source CSV file

**Constraints**:
- Must contain at least 2 weight matrices for meaningful tournament
- Iterations must be positive integer
- Output formats must be valid supported types

### TournamentReport

**Purpose**: Complete statistical analysis and results of tournament execution

**Attributes**:
- `tournament_config`: Reference to TournamentConfiguration used
- `execution_start_time`: Datetime when tournament began
- `execution_end_time`: Datetime when tournament completed
- `total_games_played`: Integer count of all completed games
- `matchup_results`: List of MatchupResult objects for all matrix pairs
- `individual_games`: List of GameResult objects for detailed analysis
- `matrix_rankings`: Ordered list of matrices by overall win rate
- `randomization_analysis`: Statistics on randomized move selection (if enabled)

**Derived Analytics**:
- Overall tournament duration
- Games per hour execution rate
- Matrix performance correlation analysis
- First player advantage across all matchups

## Data Relationships

### Hierarchy
```
TournamentConfiguration
├── WeightMatrix (multiple)
└── TournamentReport
    ├── MatchupResult (multiple, one per matrix pair)
    └── GameResult (multiple, detailed game history)
```

### Key Relationships
- Each MatchupResult references exactly 2 WeightMatrix objects
- Each GameResult contributes to exactly 1 MatchupResult
- TournamentReport aggregates all MatchupResults and GameResults
- WeightMatrix objects can participate in multiple MatchupResults

## File Format Specifications

### CSV Configuration File Schema

**Filename**: `tournament_config.csv`

**Header Row**: `label,w0_0,w0_1,w0_2,w0_3,w0_4,w1_0,w1_1,w1_2,w1_3,w1_4,w2_0,w2_1,w2_2,w2_3,w2_4,w3_0,w3_1,w3_2,w3_3,w3_4,w4_0,w4_1,w4_2,w4_3,w4_4`

**Data Rows**: Each row contains matrix label + 25 weight values

**Example**:
```csv
label,w0_0,w0_1,w0_2,w0_3,w0_4,w1_0,w1_1,w1_2,w1_3,w1_4,w2_0,w2_1,w2_2,w2_3,w2_4,w3_0,w3_1,w3_2,w3_3,w3_4,w4_0,w4_1,w4_2,w4_3,w4_4
default,0,-2,-4,-8,-16,2,0,0,0,0,4,0,1,0,0,8,0,0,0,0,16,0,0,0,0
aggressive,-5,-10,-15,-25,-50,5,0,0,0,0,10,0,2,0,0,20,0,0,0,0,40,0,0,0,0
defensive,5,2,1,-2,-8,8,0,0,0,0,12,0,1,0,0,16,0,0,0,0,24,0,0,0,0
```

### JSON Report Output Schema

**Tournament Summary Structure**:
```json
{
  "tournament_info": {
    "start_time": "2025-09-28T10:30:00Z",
    "end_time": "2025-09-28T11:45:00Z", 
    "total_duration_seconds": 4500,
    "total_games": 1800,
    "matrices_count": 5,
    "iterations_per_matchup": 100
  },
  "matrix_rankings": [
    {
      "label": "aggressive",
      "total_wins": 856,
      "total_games": 1800,
      "win_rate": 0.476,
      "rank": 1
    }
  ],
  "matchup_details": [
    {
      "matrix1": "default", 
      "matrix2": "aggressive",
      "matrix1_wins": 45,
      "matrix2_wins": 155,
      "ties": 0,
      "first_player_advantage": 0.12
    }
  ]
}
```

## Validation Rules

### Configuration Validation
- All weight matrices must have unique labels
- Weight values must be valid integers (negative allowed)
- CSV file must have correct number of columns (26 total)
- No empty or null values in required fields

### Runtime Validation  
- Tournament must have at least 2 matrices for meaningful competition
- Engine executable must be accessible and functional
- Sufficient disk space for report generation
- Valid write permissions for output directory

### Data Integrity
- GameResult matrix labels must match TournamentConfiguration matrices
- MatchupResult statistics must sum correctly from individual GameResults  
- Tournament totals must match sum of all matchup statistics
- Timestamps must be chronologically consistent

## Performance Considerations

### Memory Usage
- Store individual GameResults in batches to manage memory with large tournaments
- Stream CSV parsing for large configuration files
- Lazy loading of detailed game history for report generation

### Storage Requirements
- Estimated 200 bytes per GameResult record
- 10,000 game tournament ≈ 2MB detailed data
- Report files typically 10-50KB depending on format and detail level

### Scalability Limits
- Recommended maximum: 20 weight matrices (380 unique matchups)
- Practical limit: 10,000 total games per tournament session
- Report generation time scales linearly with game count