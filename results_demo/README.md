# Tournament Results Demo

This directory contains sample tournament outputs demonstrating the various report formats and performance characteristics of the TicTacTocToe-Engine tournament system.

## Sample Configuration
- **Source Config**: `examples/aggressive_strategies.csv`
- **Matrices**: 4 different weight configurations  
- **Iterations**: 3 per matchup
- **Randomization**: Enabled
- **Total Games**: 36 games in 2.1 seconds

## Report Formats

| File | Format | Purpose |
|------|--------|---------|
| `tournament_report.json` | JSON | Machine-readable complete results |
| `tournament_report.txt` | Text | Human-readable summary |
| `tournament_summary.txt` | Text | Executive summary |
| `tournament_report_games.csv` | CSV | Individual game results |
| `tournament_report_matchups.csv` | CSV | Matchup statistics |
| `tournament_report_rankings.csv` | CSV | Matrix performance rankings |
| `tournament_report_summary.csv` | CSV | Tournament overview |

## Performance Metrics
- **Execution Speed**: ~62,907 games/hour
- **Throughput**: 17.4 games/second
- **Scalability**: Linear scaling with game count

These sample results demonstrate the tournament system's capabilities and serve as reference for expected outputs when running your own tournaments.