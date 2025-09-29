# TTTTengine API Reference

## Overview

The TTTTengine provides a comprehensive C API for implementing 4x4x4 3D Tic-Tac-Toe game logic. This document describes all public functions, data types, and usage patterns.

## Table of Contents

- [Quick Start](#quick-start)
- [Data Types](#data-types)
- [Error Codes](#error-codes)
- [Core Functions](#core-functions)
- [Board Management](#board-management)
- [Game Logic](#game-logic)
- [AI and Move Generation](#ai-and-move-generation)
- [Configuration](#configuration)
- [Utility Functions](#utility-functions)
- [Usage Examples](#usage-examples)
- [Platform Compatibility](#platform-compatibility)

## Quick Start

```c
#include "TTTTapi.h"

int main() {
    TTTT_GameBoardStringRep board;
    long move, winner;
    
    // Initialize the engine
    TTTT_Initialize();
    
    // Get current board state
    TTTT_GetBoard(board);
    printf("Board: %s\n", board);
    
    // Make human move at position 5
    if (TTTT_HumanMove(5) == kTTTT_NoError) {
        // Get machine's response
        if (TTTT_MacMove(&move) == kTTTT_NoError) {
            printf("Machine plays position %ld\n", move);
        }
    }
    
    // Check for winner
    TTTT_GetWinner(&winner);
    if (winner != kTTTT_NOBODY) {
        printf("Game over! Winner: %s\n", 
               winner == kTTTT_HUMAN ? "Human" : "Machine");
    }
    
    return 0;
}
```

## Data Types

### Board Representation
```c
typedef char TTTT_GameBoardStringRep[kTTTT_StringRepMaxBufferLength];
```
64-character string representing the 4x4x4 game board:
- `'X'` = Human player piece
- `'O'` = Machine player piece  
- `'.'` = Empty position

**Position Mapping**: Position `i` maps to 3D coordinates:
```
Layer = i / 16     (0-3)
Row   = (i % 16) / 4   (0-3)  
Col   = i % 4          (0-3)
```

### Return Codes
```c
typedef long TTTT_Return;
```
All API functions return status codes for error handling.

### Weight Matrix
```c
typedef long TTTT_WeightsTable[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE];
```
5x5 matrix for customizing AI heuristics (see [Configuration](#configuration)).

### Winner Information
```c
typedef long TTTT_WinnerMovesArr[TTTT_WIN_SIZE];
```
Array of 4 positions representing the winning path when game ends.

### Player Constants
```c
enum {
    kTTTT_NOBODY = 0,   // No winner yet
    kTTTT_MACHINE = 1,  // Machine/AI player
    kTTTT_HUMAN = 2     // Human player
};
```

## Error Codes

```c
enum {
    kTTTT_NoError = 0,                    // Success
    kTTTT_InvalidMove = -1,               // Move to occupied position
    kTTTT_InvalidArgument = -2,           // NULL pointer or invalid parameter
    kTTTT_InvalidArgumentOutOfRange = -3  // Position outside 0-63 range
};
```

**Error Handling Pattern**:
```c
TTTT_Return result = TTTT_HumanMove(position);
if (result != kTTTT_NoError) {
    switch (result) {
        case kTTTT_InvalidMove:
            printf("Position %d already occupied\n", position);
            break;
        case kTTTT_InvalidArgumentOutOfRange:
            printf("Position must be 0-63\n");
            break;
        default:
            printf("Unexpected error: %ld\n", result);
    }
    return result;
}
```

## Core Functions

### TTTT_Initialize
```c
void TTTT_Initialize(void);
```
**Purpose**: Initialize the game engine and reset board to empty state.

**Usage**: Must be called before any other API functions.

**Example**:
```c
TTTT_Initialize();  // Engine ready for use
```

---

### TTTT_GetBoard
```c
TTTT_Return TTTT_GetBoard(TTTT_GameBoardStringRep pszGameBoard);
```
**Purpose**: Retrieve current board state as 64-character string.

**Parameters**:
- `pszGameBoard` - Buffer to receive board string (must be at least 256 chars)

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` if buffer is NULL

**Example**:
```c
TTTT_GameBoardStringRep board;
if (TTTT_GetBoard(board) == kTTTT_NoError) {
    printf("Current board: %s\n", board);
}
```

---

### TTTT_SetBoard
```c
TTTT_Return TTTT_SetBoard(const TTTT_GameBoardStringRep pszGameBoard);
```
**Purpose**: Set board state from 64-character string representation.

**Parameters**:
- `pszGameBoard` - 64-character string with 'X', 'O', '.' characters

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` for invalid input

**Example**:
```c
// Set up a specific board position
const char* board = "X...O...........................................................";
TTTT_SetBoard(board);
```

## Game Logic

### TTTT_HumanMove
```c
TTTT_Return TTTT_HumanMove(long aMove);
```
**Purpose**: Execute human player move at specified position.

**Parameters**:
- `aMove` - Position index (0-63)

**Returns**: 
- `kTTTT_NoError` - Move successful
- `kTTTT_InvalidMove` - Position already occupied
- `kTTTT_InvalidArgumentOutOfRange` - Position outside valid range

**Example**:
```c
int position = 32;  // Middle of board
TTTT_Return result = TTTT_HumanMove(position);
if (result == kTTTT_InvalidMove) {
    printf("Position %d is already taken!\n", position);
}
```

---

### TTTT_MacMove
```c
TTTT_Return TTTT_MacMove(long *aMove);
```
**Purpose**: Generate and execute optimal machine move.

**Parameters**:
- `aMove` - Pointer to receive the chosen move position

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` if pointer is NULL

**Side Effects**: Updates internal board state with machine's move

**Example**:
```c
long machine_move;
if (TTTT_MacMove(&machine_move) == kTTTT_NoError) {
    printf("Machine plays position %ld\n", machine_move);
}
```

---

### TTTT_UndoMove
```c
TTTT_Return TTTT_UndoMove(long aMove);
```
**Purpose**: Remove piece from specified position (undo a move).

**Parameters**:
- `aMove` - Position to clear (0-63)

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgumentOutOfRange` for invalid position

**Example**:
```c
// Undo last move at position 15
TTTT_UndoMove(15);
```

---

### TTTT_GetWinner
```c
TTTT_Return TTTT_GetWinner(long *aWinner);
```
**Purpose**: Check current game state for winner.

**Parameters**:
- `aWinner` - Pointer to receive winner status

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` if pointer is NULL

**Winner Values**:
- `kTTTT_NOBODY` - Game continues
- `kTTTT_HUMAN` - Human player won
- `kTTTT_MACHINE` - Machine player won

**Example**:
```c
long winner;
TTTT_GetWinner(&winner);
switch (winner) {
    case kTTTT_NOBODY:
        printf("Game continues...\n");
        break;
    case kTTTT_HUMAN:
        printf("Human wins!\n");
        break;
    case kTTTT_MACHINE:
        printf("Machine wins!\n");
        break;
}
```

---

### TTTT_GetWinnerPath
```c
TTTT_Return TTTT_GetWinnerPath(TTTT_WinnerMovesArr aWinnerPath);
```
**Purpose**: Get the four positions that form the winning line.

**Parameters**:
- `aWinnerPath` - Array to receive 4 winning positions

**Returns**: `kTTTT_NoError` on success, array undefined if no winner

**Example**:
```c
TTTT_WinnerMovesArr winning_positions;
long winner;

TTTT_GetWinner(&winner);
if (winner != kTTTT_NOBODY) {
    TTTT_GetWinnerPath(winning_positions);
    printf("Winning line: %ld %ld %ld %ld\n", 
           winning_positions[0], winning_positions[1],
           winning_positions[2], winning_positions[3]);
}
```

## AI and Move Generation

### TTTT_GetBestMove
```c
TTTT_Return TTTT_GetBestMove(int player, long *aMove);
```
**Purpose**: Calculate optimal move for specified player without executing it.

**Parameters**:
- `player` - Player type (`kTTTT_HUMAN` or `kTTTT_MACHINE`)
- `aMove` - Pointer to receive best move position

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` for invalid parameters

**Example**:
```c
long best_human_move, best_machine_move;

// Analyze best moves for both players
TTTT_GetBestMove(kTTTT_HUMAN, &best_human_move);
TTTT_GetBestMove(kTTTT_MACHINE, &best_machine_move);

printf("Best human move: %ld\n", best_human_move);
printf("Best machine move: %ld\n", best_machine_move);
```

---

### TTTT_EvaluateBoardValue
```c
TTTT_Return TTTT_EvaluateBoardValue(const TTTT_GameBoardStringRep pszGameBoard, long *pValue);
```
**Purpose**: Evaluate board position strength using current heuristic weights.

**Parameters**:
- `pszGameBoard` - Board string to evaluate
- `pValue` - Pointer to receive evaluation score

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` for invalid parameters

**Score Interpretation**:
- **Positive values** favor human player
- **Negative values** favor machine player  
- **Zero** indicates balanced position
- **Magnitude** indicates strength of advantage

**Example**:
```c
TTTT_GameBoardStringRep board;
long evaluation;

TTTT_GetBoard(board);
TTTT_EvaluateBoardValue(board, &evaluation);

if (evaluation > 0) {
    printf("Human advantage: +%ld\n", evaluation);
} else if (evaluation < 0) {
    printf("Machine advantage: %ld\n", evaluation);
} else {
    printf("Balanced position\n");
}
```

## Configuration

### TTTT_SetHeuristicWeights
```c
TTTT_Return TTTT_SetHeuristicWeights(long matrix[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE]);
```
**Purpose**: Customize AI evaluation using 5x5 weight matrix.

**Parameters**:
- `matrix` - 5x5 weight matrix (rows=human pieces, cols=machine pieces)

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` if matrix is NULL

**Matrix Structure**:
```c
// matrix[human_pieces][machine_pieces]
long weights[5][5] = {
    //Mac: 0   1   2   3    4    (Machine pieces in winning path)
    {   0, -2, -4, -8, -16},  // 0 Human pieces
    {   2,  0,  0,  0,   0},  // 1 Human piece  
    {   4,  0,  1,  0,   0},  // 2 Human pieces
    {   8,  0,  0,  0,   0},  // 3 Human pieces
    {  16,  0,  0,  0,   0},  // 4 Human pieces (win)
};
```

**Usage Example**:
```c
// Create aggressive strategy (higher penalties for machine threats)
long aggressive_weights[5][5] = {
    {   0, -5, -10, -20, -50},
    {   5,  0,   0,   0,   0},
    {  10,  0,   2,   0,   0},
    {  20,  0,   0,   0,   0},
    {  50,  0,   0,   0,   0},
};

TTTT_SetHeuristicWeights(aggressive_weights);
```

---

### TTTT_SetRandomize
```c
TTTT_Return TTTT_SetRandomize(bool randomize);
```
**Purpose**: Enable or disable randomized move selection among equal-value moves.

**Parameters**:
- `randomize` - `true` to enable randomization, `false` to use deterministic selection

**Returns**: `kTTTT_NoError` on success

**Behavior**:
- **Randomization OFF**: AI always selects first optimal move (deterministic)
- **Randomization ON**: AI randomly selects from all equally optimal moves

**Example**:
```c
#include <stdbool.h>

// Enable randomization for varied gameplay
TTTT_SetRandomize(true);

// Generate multiple moves from same position to see variety
long move1, move2, move3;
TTTT_SetBoard("................................................................");
TTTT_GetBestMove(kTTTT_MACHINE, &move1);
TTTT_GetBestMove(kTTTT_MACHINE, &move2);
TTTT_GetBestMove(kTTTT_MACHINE, &move3);
// move1, move2, move3 may be different

// Disable for consistent behavior
TTTT_SetRandomize(false);
```

## Utility Functions

### TTTT_StringRep
```c
TTTT_Return TTTT_StringRep(const char *humanMoves, const char *machineMoves, 
                          TTTT_GameBoardStringRep pszGameBoard);
```
**Purpose**: Generate board string from space-separated move sequences.

**Parameters**:
- `humanMoves` - Space-separated human move positions ("4 15 32")
- `machineMoves` - Space-separated machine move positions ("8 23 45")
- `pszGameBoard` - Buffer to receive resulting board string

**Returns**: `kTTTT_NoError` on success, `kTTTT_InvalidArgument` for invalid input

**Example**:
```c
TTTT_GameBoardStringRep board;

// Create board from move history
TTTT_StringRep("4 15 32", "8 23 45", board);
printf("Resulting board: %s\n", board);
// Output: ....X...O...............X.......O.......X.......O...........
```

---

### TTTT_MakeStringRep
```c
TTTT_Return TTTT_MakeStringRep(const int whoMoves, const long aMove, 
                              const TTTT_GameBoardStringRep pszOldRep,
                              TTTT_GameBoardStringRep pszNewRep);
```
**Purpose**: Apply single move to existing board representation.

**Parameters**:
- `whoMoves` - Player making move (`kTTTT_HUMAN` or `kTTTT_MACHINE`)
- `aMove` - Position for new move (0-63)
- `pszOldRep` - Current board state
- `pszNewRep` - Buffer to receive new board state

**Returns**: 
- `kTTTT_NoError` - Move applied successfully
- `kTTTT_InvalidMove` - Position already occupied
- `kTTTT_InvalidArgumentOutOfRange` - Invalid position

**Example**:
```c
TTTT_GameBoardStringRep old_board, new_board;

// Start with empty board
strcpy(old_board, "................................................................");

// Apply human move at position 30
TTTT_Return result = TTTT_MakeStringRep(kTTTT_HUMAN, 30, old_board, new_board);
if (result == kTTTT_NoError) {
    printf("After human move: %s\n", new_board);
    // Output: ..............................X.................................
}
```

---

### TTTT_GetWinnerStringRep
```c
TTTT_Return TTTT_GetWinnerStringRep(TTTT_GameBoardStringRep pszGameBoard);
```
**Purpose**: Get string representation highlighting winning positions.

**Parameters**:
- `pszGameBoard` - Buffer to receive winner-highlighted board

**Returns**: `kTTTT_NoError` on success

**Format**: Normal pieces shown as '.', winning pieces shown as original ('X' or 'O')

**Example**:
```c
TTTT_GameBoardStringRep winner_board;
long winner;

TTTT_GetWinner(&winner);
if (winner != kTTTT_NOBODY) {
    TTTT_GetWinnerStringRep(winner_board);
    printf("Winning positions highlighted: %s\n", winner_board);
}
```

## Usage Examples

### Complete Game Loop
```c
#include "TTTTapi.h"
#include <stdio.h>
#include <stdbool.h>

int play_game() {
    TTTT_GameBoardStringRep board;
    long winner, machine_move;
    int human_position;
    bool game_over = false;
    
    // Initialize engine
    TTTT_Initialize();
    
    // Optional: Enable randomization
    TTTT_SetRandomize(true);
    
    printf("Starting new game!\n");
    
    while (!game_over) {
        // Display current board
        TTTT_GetBoard(board);
        printf("Current board: %s\n", board);
        
        // Human move
        printf("Enter your move (0-63): ");
        scanf("%d", &human_position);
        
        TTTT_Return result = TTTT_HumanMove(human_position);
        if (result != kTTTT_NoError) {
            printf("Invalid move! Try again.\n");
            continue;
        }
        
        // Check for human win
        TTTT_GetWinner(&winner);
        if (winner == kTTTT_HUMAN) {
            printf("You win!\n");
            break;
        }
        
        // Machine move
        if (TTTT_MacMove(&machine_move) == kTTTT_NoError) {
            printf("Machine plays position %ld\n", machine_move);
        }
        
        // Check for machine win
        TTTT_GetWinner(&winner);
        if (winner == kTTTT_MACHINE) {
            printf("Machine wins!\n");
            break;
        }
        
        // Check for draw (board full)
        TTTT_GetBoard(board);
        bool board_full = true;
        for (int i = 0; i < 64; i++) {
            if (board[i] == '.') {
                board_full = false;
                break;
            }
        }
        
        if (board_full) {
            printf("Draw game!\n");
            break;
        }
    }
    
    return 0;
}
```

### Board Analysis Tool
```c
#include "TTTTapi.h"

void analyze_position(const char* position_string) {
    long evaluation, winner;
    TTTT_GameBoardStringRep board;
    
    TTTT_Initialize();
    TTTT_SetBoard(position_string);
    
    // Check if game is over
    TTTT_GetWinner(&winner);
    if (winner != kTTTT_NOBODY) {
        printf("Game Over - Winner: %s\n", 
               winner == kTTTT_HUMAN ? "Human" : "Machine");
        
        TTTT_WinnerMovesArr winning_path;
        TTTT_GetWinnerPath(winning_path);
        printf("Winning line: %ld %ld %ld %ld\n",
               winning_path[0], winning_path[1], 
               winning_path[2], winning_path[3]);
        return;
    }
    
    // Evaluate position
    TTTT_EvaluateBoardValue(position_string, &evaluation);
    printf("Position evaluation: %ld\n", evaluation);
    
    // Get best moves for both players
    long best_human, best_machine;
    TTTT_GetBestMove(kTTTT_HUMAN, &best_human);
    TTTT_GetBestMove(kTTTT_MACHINE, &best_machine);
    
    printf("Best human move: %ld\n", best_human);
    printf("Best machine move: %ld\n", best_machine);
}
```

### Custom Strategy Implementation
```c
void setup_defensive_strategy() {
    // Defensive weights - heavily penalize machine threats
    long defensive_matrix[5][5] = {
        //Mac: 0   1   2    3    4
        {   0, -1, -3, -15, -100},  // 0 Human pieces
        {   1,  0,  0,   0,    0},  // 1 Human piece  
        {   3,  0,  1,   0,    0},  // 2 Human pieces
        {  15,  0,  0,   0,    0},  // 3 Human pieces
        { 100,  0,  0,   0,    0},  // 4 Human pieces (win)
    };
    
    TTTT_SetHeuristicWeights(defensive_matrix);
    printf("Defensive strategy activated\n");
}

void setup_aggressive_strategy() {
    // Aggressive weights - prioritize own winning chances
    long aggressive_matrix[5][5] = {
        //Mac: 0   1   2   3    4
        {   0, -2, -4, -8, -16},    // 0 Human pieces
        {   3,  0,  0,  0,   0},    // 1 Human piece  
        {   6,  0,  2,  0,   0},    // 2 Human pieces
        {  12,  0,  0,  0,   0},    // 3 Human pieces
        {  25,  0,  0,  0,   0},    // 4 Human pieces (win)
    };
    
    TTTT_SetHeuristicWeights(aggressive_matrix);
    printf("Aggressive strategy activated\n");
}
```

## Platform Compatibility

The TTTTengine API is designed for cross-platform compatibility with specific considerations for randomization:

### Supported Platforms
- **macOS, FreeBSD, OpenBSD, NetBSD**: Native `arc4random()` support
- **Linux**: Conditional `arc4random()` (with libbsd) or `rand()` fallback
- **Windows**: Standard `rand()` implementation
- **Other Unix**: Standard `rand()` with `time()` seeding

### Build Requirements
- **C99 compatible compiler** (GCC, Clang, MSVC)
- **Standard C library**
- **Optional**: `libbsd-dev` for Linux `arc4random()` support

### Thread Safety
- **Engine state**: Not thread-safe, requires external synchronization
- **API functions**: Operate on shared global state
- **Randomization**: Platform random functions may have different thread safety guarantees

### Performance Characteristics
- **Move generation**: ~160-200 moves/second
- **Game simulation**: ~67,000 games/hour  
- **Memory usage**: Minimal (< 1KB working set)
- **Randomization overhead**: Zero measurable impact

---

## Constants Reference

```c
#define TTTT_BOARD_POSITIONS     64    // Total positions in 4x4x4 cube
#define TTTT_WINNING_PATHS_COUNT 76    // Number of possible winning lines
#define TTTT_WIN_SIZE           4     // Positions needed to win
#define TTTT_WEIGHT_MATRIX_SIZE  5     // Heuristic matrix dimensions
#define kTTTT_StringRepMaxBufferLength 256  // Buffer size for board strings
```

---

*This API documentation covers TTTTengine version with randomization support. For usage examples and integration guides, see the project's README.md and examples/ directory.*