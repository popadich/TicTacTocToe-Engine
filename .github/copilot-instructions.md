# TicTacTocToe-Engine AI Instructions

## Architecture Overview

This is a **4x4x4 3D Tic-Tac-Toe engine** written in C with Python test harnesses. The codebase follows a layered architecture:

- **Core Engine** (`TTTTengine/TTTT.c/.h`) - Game logic, AI, and board evaluation
- **API Layer** (`TTTTengine/TTTTapi.c/.h`) - Clean C API with error handling and string representations
- **CLI Interface** (`TTTTengine/main.c`) - Command-line tool with multiple operation modes
- **Python Wrappers** (`functional.py`, `tournament.py`) - Test automation and tournament simulation

## Critical Constants & Data Structures

The game uses **64 positions** (4x4x4 cube) with **76 winning paths**. Key types defined in `TTTTcommon.h`:
```c
#define TTTT_BOARD_POSITIONS     64    // 4x4x4 = 64 positions
#define TTTT_WINNING_PATHS_COUNT 76    // Total winning combinations
#define TTTT_WIN_SIZE           4     // 4-in-a-row to win

typedef char xs_gameboard[64];        // Board as 64-char array
typedef long xs_pathcount[76];        // Win path evaluation
```

Board positions are **0-based indices** (0-63). String representation uses `'X'` (human), `'O'` (machine), `'.'` (empty).

## Build System Patterns

**Multi-platform builds** supported:
- **Linux/Unix**: `make` → produces `tttt` executable
- **macOS/Xcode**: Use `.xcodeproj` with manual argument setup (`-p` flag in scheme)
- **VS Code**: Use `C/C++: g++ build active file` task for individual files

Always build with: `make clean && make` to ensure clean compilation.

## Command-Line Interface Modes

The `tttt` executable has **5 distinct operation modes**:

1. **Interactive Play**: `./tttt -p h` (human first) or `./tttt -p m` (machine first)
2. **Board Evaluation**: `./tttt -e "64-char-board-string"`
3. **Board Generation**: `./tttt -g -h "moves" -m "moves"`
4. **Tournament/AI Move**: `./tttt -t m "board-string"` (returns best move + new board)
5. **Custom Weights**: `./tttt -p h -w "25-element-matrix"`

**Critical**: Tournament mode (`-t`) outputs `<move_number> <new_board_string>` - this is the primary API for external programs.

## Python Integration Patterns

Python scripts communicate with C engine via **subprocess calls**:

```python
# Pattern for tournament mode (machine learning/simulation)
result = subprocess.run([tttt_path, '-t', player, board_string, '-q'], 
                       capture_output=True, text=True)
move_num, new_board = result.stdout.strip().split(maxsplit=1)
```

- `functional.py` - Regression testing with expected output validation
- `tournament.py` - Automated game simulation (human vs machine alternating moves)

## AI & Heuristic System

The engine uses **configurable heuristic weights** (5x5 matrix) for board evaluation:
- Default weights optimized for competitive play
- Custom weights via `-w` flag or `TTTT_SetHeuristicWeights()` API
- Randomization option (`TTTT_SetRandomize()`) for varied gameplay

**5x5 Scoring Matrix Structure**:
```c
// Rows = Human pieces count (0-4), Columns = Machine pieces count (0-4)
// Lower scores favor machine, higher scores favor human
xs_weighttab default_weights = {
  // Mac:  0   1   2   3    4    (Machine pieces in path)
  {   0, -2, -4, -8, -16},  // 0 Human pieces
  {   2,  0,  0,  0,   0},  // 1 Human piece  
  {   4,  0,  1,  0,   0},  // 2 Human pieces
  {   8,  0,  0,  0,   0},  // 3 Human pieces
  {  16,  0,  0,  0,   0},  // 4 Human pieces
};
```

**Scoring Algorithm**: For each of the 76 winning paths, count human vs machine pieces, then lookup `weights[human_count][machine_count]` and sum all path scores. Negative scores favor machine (AI), positive scores favor human.

**Win Detection**: Uses precomputed winning path analysis across all 76 possible 4-in-a-row combinations (horizontal, vertical, diagonal, spatial).

## String Representation Format

Board state is encoded as **64-character string** where position `i` maps to 3D coordinates:
- Position 0 = (0,0,0), Position 15 = (0,3,3)
- Position 16 = (1,0,0), Position 63 = (3,3,3)
- Layer-major ordering: `layer * 16 + row * 4 + col`

## Development Workflow

1. **Code Changes**: Edit in `TTTTengine/` directory
2. **Build**: Run `make clean && make`
3. **Test**: Run `python3 functional.py` for regression tests
4. **Tournament**: Run `python3 tournament.py` for gameplay simulation
5. **Manual Test**: `./tttt -p h` for interactive verification

## Error Handling Conventions

API functions return `TTTT_Return` codes:
- `kTTTT_NoError = 0`
- `kTTTT_InvalidMove = -1` 
- `kTTTT_InvalidArgument = -2`

Always check return values when calling `TTTT_*` functions. CLI uses `getopt` for argument parsing with comprehensive help (`--help`).

## Key Files for Common Tasks

- **Add new CLI feature**: Modify `TTTTengine/main.c` argument parsing
- **Change AI behavior**: Edit weights/evaluation in `TTTTengine/TTTT.c`
- **Add new API**: Extend `TTTTengine/TTTTapi.h/.c`
- **Add tests**: Update `functional.py` test cases array
- **Cross-platform**: Check both `makefile` and `.xcodeproj` compatibility