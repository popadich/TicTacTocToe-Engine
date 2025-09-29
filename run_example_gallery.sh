#!/bin/bash
# Run all example tournaments and generate comparative analysis

echo "🏆 Running Tournament Example Gallery"
echo "====================================="

# Create results directory
mkdir -p gallery_results

echo "⚡ Quick validation test..."
python3 tournament_runner.py -c examples/quick_test.csv -i 5 --output-dir gallery_results/quick_validation

if [ $? -ne 0 ]; then
    echo "❌ Quick test failed. Check engine and configuration."
    exit 1
fi

echo "✅ System validated. Running full gallery..."

# Run each example configuration
declare -a configs=("aggressive_strategies" "defensive_strategies" "positional_strategies" "randomization_test")

for config in "${configs[@]}"; do
    echo ""
    echo "🎯 Running: $config"
    echo "----------------------------------------"
    
    # Deterministic run
    echo "  📊 Deterministic tournament..."
    python3 tournament_runner.py \
        -c "examples/${config}.csv" \
        -i 15 \
        --output-dir "gallery_results/${config}_deterministic" \
        --formats json,text
    
    # Randomized run  
    echo "  🎲 Randomized tournament..."
    python3 tournament_runner.py \
        -c "examples/${config}.csv" \
        -i 15 \
        --randomization \
        --output-dir "gallery_results/${config}_randomized" \
        --formats json,text
        
    echo "  ✅ $config completed"
done

echo ""
echo "📊 Generating comparative analysis..."

# Generate summary report
cat > gallery_results/GALLERY_SUMMARY.txt << 'EOF'
Tournament Example Gallery Results
==================================

This directory contains results from running all example tournament configurations
in both deterministic and randomized modes.

Configuration Overview:
- aggressive_strategies: 4 matrices, conservative to very aggressive
- defensive_strategies: 4 matrices, various defensive approaches  
- positional_strategies: 4 matrices, center/edge/corner/layer focus
- randomization_test: 4 matrices, random baseline to structured strategies
- quick_test: 2 matrices, for rapid system validation

Each configuration was run with:
- 15 iterations per matchup (deterministic)
- 15 iterations per matchup (randomized)
- All output formats (JSON, text)

Compare Results:
================
EOF

# Add performance summary for each config
for config in "${configs[@]}"; do
    echo "" >> gallery_results/GALLERY_SUMMARY.txt
    echo "$config Results:" >> gallery_results/GALLERY_SUMMARY.txt
    echo "----------------------------------------" >> gallery_results/GALLERY_SUMMARY.txt
    echo "Deterministic:" >> gallery_results/GALLERY_SUMMARY.txt
    grep -E "(Games Completed|Total Duration|Games per Hour)" "gallery_results/${config}_deterministic/tournament_summary.txt" >> gallery_results/GALLERY_SUMMARY.txt
    echo "Randomized:" >> gallery_results/GALLERY_SUMMARY.txt  
    grep -E "(Games Completed|Total Duration|Games per Hour)" "gallery_results/${config}_randomized/tournament_summary.txt" >> gallery_results/GALLERY_SUMMARY.txt
done

echo ""
echo "🎉 Gallery generation complete!"
echo "📁 Results saved to: gallery_results/"
echo "📋 Summary report: gallery_results/GALLERY_SUMMARY.txt"
echo ""
echo "🔍 Quick analysis commands:"
echo "  View all summaries: find gallery_results -name tournament_summary.txt -exec echo '=== {} ===' \; -exec cat {} \;"
echo "  Compare performance: grep 'Games per Hour' gallery_results/*/tournament_summary.txt"
echo "  Check randomization: diff gallery_results/randomization_test_deterministic/tournament_summary.txt gallery_results/randomization_test_randomized/tournament_summary.txt"