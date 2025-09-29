# Research: Tournament System Enhancement

## Technical Investigation

### Existing Engine Capabilities Analysis

**Current Tournament Mode**:
- Command: `./tttt -t m "board_string"` - Returns best move for machine
- Command: `./tttt -t h "board_string"` - Returns best move for human  
- Weight support: `-w "matrix"` flag accepts 25-element weight matrix
- Randomization: `-r` flag enables randomized move selection for tied scores
- Output format: `"move_number new_board_string"` or `"move_number"` with `-q` flag

**Current Tournament.py Analysis**:
- Uses subprocess to communicate with tttt executable
- Basic game loop implementation
- Single game execution between fixed opponents
- No weight matrix management or statistical reporting

### Weight Matrix Format Research

**Current Weight Matrix Structure**:
- 5x5 matrix (Human pieces 0-4 vs Machine pieces 0-4)
- Passed as 25 space-separated integers to `-w` flag
- Example: `"0 -2 -4 -8 -16 2 0 0 0 0 4 0 1 0 0 8 0 0 0 0 16 0 0 0 0"`
- Lower scores favor machine, higher scores favor human

**CSV Configuration Design Decision**:
- Row format: `label,w1,w2,w3,...,w25` (26 columns total)
- Header row: `label,w0_0,w0_1,w0_2,w0_3,w0_4,w1_0,w1_1,...,w4_4`
- Sample matrices: Default, Aggressive, Defensive, Balanced configurations

### Game Execution Strategy

**Tournament Structure**:
- Round-robin: Each matrix vs every other matrix
- Role switching: Each pair plays with both matrices as first/second player  
- Game iterations: User-specified number of games per matchup
- Total games = N*(N-1)*iterations where N = number of matrices

**Randomization Testing**:
- Validate `-r` flag functionality through repeated identical board positions
- Measure randomness distribution in move selection
- Compare deterministic vs randomized outcomes

### Statistical Requirements

**Per-Matrix Statistics**:
- Total games played
- Win count and percentage
- Loss count and percentage  
- Games as first player vs second player
- Performance against specific opponents

**Matchup Analysis**:
- Head-to-head win rates between specific matrix pairs
- Advantage statistics for first/second player roles
- Tie game handling (if applicable)

**Report Format Options**:
- JSON for programmatic analysis
- CSV for spreadsheet import
- Human-readable text summary
- Optional: HTML report with charts

### Implementation Architecture

**Component Structure**:
1. **ConfigLoader**: Parse CSV weight matrix configurations
2. **GameRunner**: Execute individual games via subprocess 
3. **TournamentManager**: Coordinate all matchups and iterations
4. **StatisticsCollector**: Accumulate and analyze results
5. **ReportGenerator**: Output results in multiple formats

**Error Handling Requirements**:
- Invalid weight matrices in configuration
- tttt executable not found or compilation issues  
- Interrupted tournaments (partial completion)
- Invalid game states or engine errors
- File I/O errors for config/report files

### Dependencies and Constraints

**Python Standard Library Usage**:
- `subprocess`: Engine communication
- `csv`: Configuration file parsing
- `json`: Report generation  
- `itertools`: Combination generation for matchups
- `argparse`: Command-line interface
- `pathlib`: File path handling
- `time`: Performance measurement

**No External Dependencies**: Maintains constitutional engine isolation

### Performance Considerations

**Scalability Estimates**:
- 5 matrices × 100 iterations = 2,000 total games
- 10 matrices × 100 iterations = 9,000 total games  
- Average game duration: ~1-2 seconds per game
- Expected tournament duration: 30 minutes to 5 hours depending on scale

**Optimization Opportunities**:
- Parallel game execution (future enhancement)
- Progress reporting and resumption capability
- Incremental statistics updates during execution

## Decision Points Resolved

1. **Configuration Format**: CSV selected for simplicity and spreadsheet compatibility
2. **Communication Method**: Subprocess only, no library integration (constitutional requirement)
3. **Weight Matrix Storage**: Flattened 25-element arrays matching existing engine format
4. **Tournament Structure**: Full round-robin with role switching for comprehensive analysis
5. **Report Generation**: Multiple formats (JSON, CSV, text) for different use cases
6. **Randomization Testing**: Integrated validation of engine randomization functionality

## Next Phase Requirements

Phase 1 will need to design:
- CSV configuration file schema and sample data
- Tournament execution contracts and interfaces  
- Statistical data models and report structures
- Integration testing approach with existing test framework
- Command-line interface matching project conventions