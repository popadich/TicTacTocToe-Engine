# Tournament Example Gallery

This directory contains ready-to-use tournament configurations demonstrating different aspects of the 3D TicTacToe engine and tournament system.

## 📁 Configuration Files

### 🎯 **Strategy Comparison Examples**

#### `aggressive_strategies.csv`
**Purpose**: Compare different levels of aggressive play
**Matrices**: 4 strategies from conservative to very aggressive
**Use Case**: Analyze how aggressive vs defensive strategies perform

```bash
# Run aggressive strategy tournament
python3 tournament_runner.py -c examples/aggressive_strategies.csv -i 20 --output-dir results_aggressive
```

**Expected Insights**: Very aggressive strategies may win quickly or lose quickly, moderate strategies may be more consistent.

#### `defensive_strategies.csv` 
**Purpose**: Compare defensive playing styles
**Matrices**: 4 defensive approaches with different blocking priorities
**Use Case**: Test various defensive weight configurations

```bash
# Run defensive strategy tournament  
python3 tournament_runner.py -c examples/defensive_strategies.csv -i 25 --output-dir results_defensive
```

**Expected Insights**: Defensive strategies may have longer games, fewer decisive wins.

#### `positional_strategies.csv`
**Purpose**: Compare positional preferences (center, edge, corner, layer control)
**Matrices**: 4 strategies focusing on different board positions
**Use Case**: Understand how positional preferences affect outcomes

```bash
# Run positional strategy tournament
python3 tournament_runner.py -c examples/positional_strategies.csv -i 15 --output-dir results_positional
```

**Expected Insights**: Center control may be stronger, but edge/corner strategies could surprise.

### 🎲 **Randomization Testing**

#### `randomization_test.csv`
**Purpose**: Test randomization effects with varying strategy strengths
**Matrices**: From random baseline to structured strategies
**Use Case**: Validate randomization produces statistical variance

```bash
# Test without randomization (deterministic)
python3 tournament_runner.py -c examples/randomization_test.csv -i 50 --output-dir results_deterministic

# Test with randomization (statistical variance)  
python3 tournament_runner.py -c examples/randomization_test.csv -i 50 --randomization --output-dir results_randomized

# Compare results
echo "=== Deterministic Results ==="
cat results_deterministic/tournament_summary.txt
echo "=== Randomized Results ==="
cat results_randomized/tournament_summary.txt
```

**Expected Insights**: Randomized tournaments should show more outcome variance, especially for similarly-skilled strategies.

### ⚡ **Quick Testing**

#### `quick_test.csv`
**Purpose**: Fast 2-matrix tournament for quick validation
**Matrices**: 2 simple strategies for rapid testing
**Use Case**: Verify system functionality, debug issues

```bash
# Quick system test (only 2 games per iteration)
python3 tournament_runner.py -c examples/quick_test.csv -i 5 --output-dir quick_validation
```

**Expected Results**: Should complete in <5 seconds, useful for CI/CD or quick checks.

## 🚀 **Usage Examples**

### Performance Testing
```bash
# Test engine performance with different configurations
for config in examples/*.csv; do
    echo "Testing $(basename "$config")..."
    time python3 tournament_runner.py -c "$config" -i 10 --output-dir "perf_$(basename "$config" .csv)"
done
```

### Randomization Comparison
```bash
# Compare randomized vs deterministic outcomes
python3 tournament_runner.py -c examples/aggressive_strategies.csv -i 25 --output-dir det_aggressive
python3 tournament_runner.py -c examples/aggressive_strategies.csv -i 25 --randomization --output-dir rand_aggressive

# Analyze variance
echo "Deterministic win rates:" && grep "wins" det_aggressive/tournament_summary.txt
echo "Randomized win rates:" && grep "wins" rand_aggressive/tournament_summary.txt
```

### Comprehensive Analysis
```bash
# Run all example configurations with randomization
for config in examples/*.csv; do
    name=$(basename "$config" .csv)
    echo "Running tournament: $name"
    python3 tournament_runner.py \
        -c "$config" \
        -i 30 \
        --randomization \
        --output-dir "gallery_$name" \
        --formats json,csv,text
done
```

## 📊 **Expected Results Guide**

### **Strategy Performance Patterns**

1. **Aggressive Strategies**: 
   - Shorter games (fewer moves)
   - Higher variance in outcomes
   - May dominate weaker strategies quickly

2. **Defensive Strategies**:
   - Longer games (more moves)  
   - More consistent outcomes
   - Better against aggressive players

3. **Positional Strategies**:
   - Varies by 3D board control effectiveness
   - Center control typically stronger
   - Layer control may show unique patterns

### **Randomization Effects**

- **Without `-r`**: 100% reproducible results, same outcomes every run
- **With `-r`**: Statistical variance in outcomes, different game sequences
- **Comparison**: Similar overall win rates, but individual game variation

### **Performance Characteristics**

- **quick_test.csv**: <5 seconds for 10 iterations
- **4-matrix configs**: ~15-30 seconds for 25 iterations
- **All examples**: Should maintain ~67K games/hour rate

## 🔧 **Customization Guide**

### Creating Your Own Configurations

1. **Copy existing file**: `cp examples/aggressive_strategies.csv my_config.csv`
2. **Edit labels**: Change strategy names in first column
3. **Adjust weights**: Modify the 25 weight values (w0_0 through w4_4)
4. **Test configuration**: `python3 tournament_runner.py -c my_config.csv -i 5 --validate-only`
5. **Run tournament**: `python3 tournament_runner.py -c my_config.csv -i 20`

### Weight Matrix Meaning

The 5x5 weight matrix represents preferences for board positions with different piece counts:
- **Rows**: Human pieces in winning path (0-4)  
- **Columns**: Machine pieces in winning path (0-4)
- **Negative values**: Favor machine (AI)
- **Positive values**: Favor human
- **Zero values**: Neutral

### Example Weight Interpretations

```csv
# Very aggressive machine (large negative values)
very_aggressive,-10,-20,-30,-50,-100,2,0,0,0,0,12,0,3,0,0,25,0,0,0,0,50,0,0,0,0

# Very defensive (large positive values when human has pieces)
very_defensive,15,10,8,5,0,20,0,0,0,0,25,0,0,0,0,30,0,0,0,0,35,0,0,0,0

# Balanced (moderate values)
balanced,2,-1,-2,-4,-8,4,0,0,0,0,6,0,1,0,0,10,0,0,0,0,18,0,0,0,0
```

## 📋 **Validation Checklist**

Before running tournaments, verify:
- [ ] Engine built: `make && ./tttt --version`
- [ ] Config valid: `python3 tournament_runner.py -c your_config.csv -i 1 --validate-only`
- [ ] Output directory accessible: `ls -la output_directory`
- [ ] Sufficient disk space for results
- [ ] Expected runtime reasonable for iteration count

## 🆘 **Troubleshooting**

**Config errors**: Check CSV format, ensure 25 weight columns, unique labels
**Engine errors**: Verify `./tttt` executable exists and works
**Performance issues**: Use `examples/quick_test.csv` first
**Randomization issues**: Compare with/without `-r` flag on same config