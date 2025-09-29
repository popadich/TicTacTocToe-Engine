# Tournament System Quickstart Guide

## Overview
The Tournament System Enhancement allows you to run automated competitions between different heuristic weight matrices to optimize the 3D tic-tac-toe engine performance.

## Prerequisites
- Compiled `tttt` executable in project root
- Python 3.8+ installed
- CSV configuration file with weight matrices

## Basic Usage

### 1. Create Configuration File
Create `tournament_config.csv` with your weight matrices:

```csv
label,w0_0,w0_1,w0_2,w0_3,w0_4,w1_0,w1_1,w1_2,w1_3,w1_4,w2_0,w2_1,w2_2,w2_3,w2_4,w3_0,w3_1,w3_2,w3_3,w3_4,w4_0,w4_1,w4_2,w4_3,w4_4
default,0,-2,-4,-8,-16,2,0,0,0,0,4,0,1,0,0,8,0,0,0,0,16,0,0,0,0
aggressive,-5,-10,-15,-25,-50,5,0,0,0,0,10,0,2,0,0,20,0,0,0,0,40,0,0,0,0
defensive,5,2,1,-2,-8,8,0,0,0,0,12,0,1,0,0,16,0,0,0,0,24,0,0,0,0
```

### 2. Run Basic Tournament
```bash
python tournament_runner.py --config tournament_config.csv --iterations 50
```

### 3. View Results
Results are saved to `tournament_results/` directory:
- `tournament_report.json` - Complete statistical analysis
- `tournament_summary.txt` - Human-readable summary  
- `matchup_details.csv` - Detailed matchup statistics

## Command Line Options

```bash
python tournament_runner.py [OPTIONS]

Required:
  --config PATH          Path to CSV configuration file
  --iterations INT       Number of games per matchup pair

Optional:
  --output-dir PATH      Output directory (default: ./tournament_results)
  --randomization        Enable randomized move selection
  --formats LIST         Output formats: json,csv,text (default: all)
  --engine-path PATH     Path to tttt executable (default: ./tttt)
  --verbose             Enable detailed progress output
  --parallel INT        Number of parallel games (future enhancement)
```

## Configuration File Format

### CSV Structure
- **Header Row**: `label` + 25 weight columns (`w0_0` through `w4_4`)
- **Data Rows**: Matrix label + 25 integer weight values
- **Requirements**: Unique labels, valid integers, no empty cells

### Weight Matrix Layout
The 25 weight values represent a 5×5 matrix in row-major order:
```
    Mac: 0   1   2   3   4    (Machine pieces in winning path)
Hum: 0  [w0_0 w0_1 w0_2 w0_3 w0_4]
     1  [w1_0 w1_1 w1_2 w1_3 w1_4] 
     2  [w2_0 w2_1 w2_2 w2_3 w2_4]
     3  [w3_0 w3_1 w3_2 w3_3 w3_4]
     4  [w4_0 w4_1 w4_2 w4_3 w4_4]
```

### Sample Matrix Strategies

**Default Engine Weights**:
```csv
default,0,-2,-4,-8,-16,2,0,0,0,0,4,0,1,0,0,8,0,0,0,0,16,0,0,0,0
```

**Aggressive Strategy** (favors offensive play):
```csv
aggressive,-5,-10,-15,-25,-50,5,0,0,0,0,10,0,2,0,0,20,0,0,0,0,40,0,0,0,0
```

**Defensive Strategy** (emphasizes blocking):
```csv
defensive,5,2,1,-2,-8,8,0,0,0,0,12,0,1,0,0,16,0,0,0,0,24,0,0,0,0
```

## Understanding Results

### Tournament Report Structure
- **Matrix Rankings**: Overall win rates across all matchups
- **Head-to-Head Analysis**: Win rates between specific matrix pairs  
- **First Player Advantage**: Statistical analysis of move order impact
- **Performance Metrics**: Game duration and move count statistics

### Key Statistics
- **Win Rate**: Percentage of games won by each matrix
- **Matchup Performance**: How each matrix performs against specific opponents
- **Consistency**: Variance in performance across different matchups
- **Efficiency**: Average moves and time per game

## Best Practices

### Tournament Design
- **Start Small**: Begin with 3-5 matrices and 50-100 iterations
- **Balanced Testing**: Include diverse strategy types in your configuration
- **Iterative Refinement**: Use results to guide creation of new matrices

### Performance Optimization
- **Reasonable Scale**: 10 matrices × 100 iterations ≈ 9,000 games (30-60 minutes)
- **Progress Monitoring**: Use `--verbose` flag for long tournaments
- **Resource Planning**: Ensure sufficient disk space for result files

### Analysis Workflow
1. Run initial tournament with baseline matrices
2. Identify top-performing strategies from results
3. Create variations of successful matrices
4. Run focused tournaments between promising candidates
5. Iterate until optimal weights are discovered

## Troubleshooting

### Common Issues

**"Engine not found" error**:
```bash
# Verify tttt executable exists and is executable
ls -la ./tttt
make clean && make  # Rebuild if necessary
```

**"Invalid CSV format" error**:
- Check CSV has exactly 26 columns (label + 25 weights)
- Verify no empty cells or non-integer values
- Ensure unique matrix labels

**Tournament hangs or times out**:
- Reduce iterations or number of matrices
- Check system resources (CPU, memory)
- Verify engine responds to manual test commands

### Validation Tests
```bash
# Test engine functionality
./tttt --version
./tttt -t m "................................................................" -w "0 -2 -4 -8 -16 2 0 0 0 0 4 0 1 0 0 8 0 0 0 0 16 0 0 0 0"

# Validate configuration file
python -c "import csv; print(len(list(csv.reader(open('tournament_config.csv')))))"
```

## Next Steps
- Analyze tournament results to identify successful weight patterns
- Create focused tournaments between top-performing matrices
- Experiment with randomization to test strategy robustness
- Scale up to larger tournaments once optimal parameters are identified