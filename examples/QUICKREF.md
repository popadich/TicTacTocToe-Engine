# Tournament Examples Quick Reference

## 🚀 Quick Start Commands

```bash
# Quick system test (5 seconds)
python3 tournament_runner.py -c examples/quick_test.csv -i 5

# Aggressive strategies comparison (15 seconds)
python3 tournament_runner.py -c examples/aggressive_strategies.csv -i 10

# Test randomization effects (10 seconds each)
python3 tournament_runner.py -c examples/randomization_test.csv -i 8
python3 tournament_runner.py -c examples/randomization_test.csv -i 8 --randomization

# Run complete gallery (2-3 minutes)
./run_example_gallery.sh
```

## 📁 Example Files

| File | Matrices | Purpose | Runtime (10 iter) |
|------|----------|---------|-------------------|
| `quick_test.csv` | 2 | System validation | ~3 seconds |
| `aggressive_strategies.csv` | 4 | Strategy comparison | ~15 seconds |
| `defensive_strategies.csv` | 4 | Defensive analysis | ~15 seconds |
| `positional_strategies.csv` | 4 | Position preferences | ~15 seconds |
| `randomization_test.csv` | 4 | Randomization testing | ~15 seconds |

## 🎯 Use Cases

**Development Testing**: Use `quick_test.csv` for CI/CD and rapid validation
**Strategy Research**: Use `aggressive_strategies.csv` and `defensive_strategies.csv` 
**Algorithm Testing**: Use `randomization_test.csv` to verify randomization
**Performance Testing**: Use any 4-matrix config to benchmark system performance
**Demo/Teaching**: Use `run_example_gallery.sh` for comprehensive demonstration

## 📊 Expected Performance

- **2-matrix tournaments**: ~50K games/hour
- **4-matrix tournaments**: ~65K games/hour  
- **All examples should maintain**: >60K games/hour baseline

## 🔧 Customization Template

```csv
label,w0_0,w0_1,w0_2,w0_3,w0_4,w1_0,w1_1,w1_2,w1_3,w1_4,w2_0,w2_1,w2_2,w2_3,w2_4,w3_0,w3_1,w3_2,w3_3,w3_4,w4_0,w4_1,w4_2,w4_3,w4_4
my_strategy,0,-2,-4,-8,-16,2,0,0,0,0,4,0,1,0,0,8,0,0,0,0,16,0,0,0,0
```

Replace `my_strategy` with your name and adjust the 25 weight values as needed.