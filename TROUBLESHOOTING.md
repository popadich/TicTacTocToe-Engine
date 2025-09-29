# TTTTengine Troubleshooting Guide

## Table of Contents

- [Build Issues](#build-issues)
- [Runtime Problems](#runtime-problems)
- [Platform-Specific Issues](#platform-specific-issues)
- [Performance Issues](#performance-issues)
- [API Integration Problems](#api-integration-problems)
- [Tournament System Issues](#tournament-system-issues)
- [Common Error Messages](#common-error-messages)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

## Build Issues

### "Command not found: make"

**Symptoms**: `make: command not found` or `make` not available

**Solutions**:
```bash
# macOS - Install Xcode Command Line Tools
xcode-select --install

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential

# CentOS/RHEL/Fedora
sudo yum install gcc make   # CentOS 7
sudo dnf install gcc make   # Fedora/CentOS 8+

# Verify installation
make --version
gcc --version
```

---

### Compilation Errors: "error: 'arc4random' was not declared"

**Symptoms**: Linux build fails with `arc4random` undefined

**Root Cause**: Missing `libbsd` development headers

**Solutions**:
```bash
# Option 1: Install libbsd and use BSD build
sudo apt-get install libbsd-dev
make clean && make linux-bsd

# Option 2: Use standard build (falls back to rand())
make clean && make linux

# Option 3: Force standard build
make clean && make standard
```

**Verification**:
```bash
# Check if libbsd is available
pkg-config --exists libbsd && echo "libbsd available" || echo "libbsd not found"

# Test randomization works
./tttt -t m "................................................................" -r -q
./tttt -t m "................................................................" -r -q
# Should show different moves
```

---

### "warning: unused variable" or Other Warnings

**Symptoms**: Compilation succeeds but shows warnings

**Impact**: Generally harmless but indicates code quality issues

**Solutions**:
```bash
# Clean build to ensure fresh compilation
make clean && make

# Check if warnings persist across platforms
make clean && make linux      # Standard Linux build
make clean && make linux-bsd  # Linux with libbsd
```

**Ignore List** (Known acceptable warnings):
- Unused variables in debug builds
- Signed/unsigned comparison in legacy code sections

---

### Xcode Build Issues

**Symptoms**: Xcode project won't build or run correctly

**Solutions**:
1. **Set up arguments in Xcode**:
   - Product → Scheme → Edit Scheme
   - Arguments tab → Arguments Passed On Launch
   - Add: `-p h` (for human-first interactive play)

2. **Console output**:
   - View → Debug Area → Activate Console
   - All output appears in debug console

3. **Build errors**:
   - Ensure all source files are in project
   - Check header search paths
   - Verify deployment target compatibility

**Alternative**: Use command-line build instead:
```bash
cd TTTTengine
make clean && make
./tttt -p h
```

## Runtime Problems

### "Segmentation fault" or Crashes

**Symptoms**: Program crashes with segfault

**Common Causes**:
1. **Uninitialized engine**: Must call `TTTT_Initialize()` first
2. **NULL pointer**: Passing NULL to API functions expecting valid pointers
3. **Buffer overflow**: Using insufficient buffer sizes

**Debugging Steps**:
```bash
# Enable core dumps
ulimit -c unlimited

# Run with debugger
gdb ./tttt
(gdb) run -p h
# When it crashes:
(gdb) bt
(gdb) print variable_name

# Or use lldb on macOS
lldb ./tttt
(lldb) run -p h
# When it crashes:
(lldb) bt
(lldb) print variable_name
```

**Prevention**:
```c
// Always initialize first
TTTT_Initialize();

// Check return values
TTTT_Return result = TTTT_GetBoard(board);
if (result != kTTTT_NoError) {
    fprintf(stderr, "Failed to get board: %ld\n", result);
    return -1;
}

// Use proper buffer sizes
TTTT_GameBoardStringRep board;  // Correctly sized buffer
// NOT: char board[64];          // Too small!
```

---

### Invalid Move Errors

**Symptoms**: `kTTTT_InvalidMove` returned from move functions

**Root Causes**:
1. **Position already occupied**
2. **Position out of range** (not 0-63)
3. **Game already over**

**Debugging**:
```c
// Check position validity
if (position < 0 || position > 63) {
    printf("Invalid position %d, must be 0-63\n", position);
    return kTTTT_InvalidArgumentOutOfRange;
}

// Check if position is empty
TTTT_GameBoardStringRep board;
TTTT_GetBoard(board);
if (board[position] != '.') {
    printf("Position %d already occupied by '%c'\n", position, board[position]);
    return kTTTT_InvalidMove;
}

// Check for winner before moving
long winner;
TTTT_GetWinner(&winner);
if (winner != kTTTT_NOBODY) {
    printf("Game over, winner is %ld\n", winner);
    return kTTTT_InvalidMove;
}
```

---

### No Output in Interactive Mode

**Symptoms**: Program runs but shows no output or prompts

**Common Causes**:
1. **Output buffering**: Printf output not flushed
2. **Wrong mode**: Program expecting different arguments
3. **Redirected output**: Output going to file instead of terminal

**Solutions**:
```bash
# Ensure unbuffered output
./tttt -p h | cat

# Force line buffering
stdbuf -oL ./tttt -p h

# Check if output is redirected
./tttt -p h 2>&1

# Verify correct arguments
./tttt --help
```

**Code Fix**:
```c
// Add after printf statements
printf("Enter move: ");
fflush(stdout);  // Force output

// Or use stderr for immediate output
fprintf(stderr, "Debug: position = %d\n", pos);
```

## Platform-Specific Issues

### macOS: "Developer cannot be verified" Error

**Symptoms**: macOS blocks execution of locally built binary

**Solution**:
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine ./tttt

# Or allow in Security & Privacy settings:
# System Preferences → Security & Privacy → General → "Allow anyway"
```

---

### Linux: "Permission denied" When Running

**Symptoms**: `./tttt: Permission denied` despite file existing

**Solutions**:
```bash
# Check permissions
ls -l tttt

# Add execute permission
chmod +x tttt

# Verify it's executable
file tttt
# Should show: tttt: ELF 64-bit LSB executable...
```

---

### Windows: Build or Execution Issues

**Note**: Primary development targets Unix/Linux systems. Windows support may require additional setup.

**MinGW/MSYS2 Setup**:
```bash
# Install MSYS2, then:
pacman -S mingw-w64-x86_64-gcc make

# Build
make clean && make standard

# Windows-specific random number generation
# The engine automatically uses rand() on Windows
```

**Visual Studio**: Create new console application project and add all `.c` files to project.

## Performance Issues

### Slow Move Generation

**Expected Performance**: ~160-200 moves/second, ~67K games/hour

**Symptoms**: Significantly slower performance

**Diagnostic**:
```bash
# Test engine performance
time ./tttt -e "................................................................"
# Should complete in < 0.01 seconds

# Test tournament performance  
time python3 tournament.py human machine 100 quick_perf_test.csv
# Should complete ~100 games in < 10 seconds
```

**Common Causes**:
1. **Debug build**: Ensure optimized compilation
2. **Memory issues**: Check for memory leaks or excessive allocation
3. **I/O bottleneck**: Reduce disk writes during performance testing

**Solutions**:
```bash
# Rebuild with optimizations
make clean
CFLAGS="-O2 -DNDEBUG" make

# Profile execution
# macOS:
time ./tttt -t m "................................................................" -q

# Linux:
perf stat ./tttt -t m "................................................................" -q
```

---

### Memory Usage Concerns

**Expected Usage**: < 1KB working set for engine state

**Monitoring**:
```bash
# macOS
/usr/bin/time -l ./tttt -p h

# Linux
/usr/bin/time -v ./tttt -p h

# During tournament
ps aux | grep python3  # Check tournament script memory
```

## API Integration Problems

### Linking Errors

**Symptoms**: `undefined reference` errors when linking with TTTTapi

**Solutions**:
```bash
# Ensure all object files are included
gcc -o my_program my_program.c TTTTapi.o TTTT.o

# Or use makefile approach
# Add to your makefile:
TTTT_OBJECTS = TTTTapi.o TTTT.o
my_program: my_program.c $(TTTT_OBJECTS)
	gcc -o $@ $^ 
```

**CMake Integration**:
```cmake
add_executable(my_program my_program.c)
target_sources(my_program PRIVATE TTTTapi.c TTTT.c)
target_include_directories(my_program PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
```

---

### Header Include Issues

**Symptoms**: Compile errors about missing types or functions

**Solution**:
```c
// Correct include order:
#include "TTTTapi.h"      // Main API
// TTTTapi.h automatically includes TTTTcommon.h

// NOT:
#include "TTTT.h"         // Internal header, don't use directly
#include "TTTTcommon.h"   // Included automatically
```

---

### Type Compatibility Issues

**Symptoms**: Compiler warnings about type mismatches

**Common Issues**:
```c
// WRONG - int vs long mismatch
int move = 5;
TTTT_HumanMove(move);  // May cause warnings

// CORRECT - explicit long type
long move = 5L;
TTTT_HumanMove(move);

// WRONG - incorrect buffer type
char board[64];
TTTT_GetBoard(board);  // Buffer too small!

// CORRECT - use typedef
TTTT_GameBoardStringRep board;
TTTT_GetBoard(board);
```

## Tournament System Issues

### Python Script Errors

**Symptoms**: Tournament scripts fail with import or execution errors

**Prerequisites Check**:
```bash
# Verify Python version (3.6+ required)
python3 --version

# Check if tttt executable exists and works
./tttt --help
./tttt -t m "................................................................" -q

# Verify subprocess communication
python3 -c "
import subprocess
result = subprocess.run(['./tttt', '--help'], capture_output=True, text=True)
print('Return code:', result.returncode)
print('Output length:', len(result.stdout))
"
```

**Common Fixes**:
```bash
# Ensure executable is built
make clean && make

# Check PATH and permissions
which python3
ls -l ./tttt
chmod +x ./tttt

# Test minimal tournament
python3 tournament.py human machine 1 test_output.csv
```

---

### CSV Output Problems

**Symptoms**: Malformed or empty CSV files from tournaments

**Debugging**:
```bash
# Check if engine produces expected output format
./tttt -t m "................................................................" -q
# Should output: "<move_number> <64_char_board>"

# Verify CSV structure
head -5 tournament_output.csv
# Should show proper CSV headers and data

# Check for file permission issues
touch test.csv && rm test.csv  # Test write permissions
```

**Manual Verification**:
```bash
# Run single tournament iteration manually
echo "Testing single move..."
RESULT=$(./tttt -t m "................................................................" -q)
echo "Engine output: '$RESULT'"
echo "$RESULT" | wc -w  # Should be 2 words: move_number board_string
```

### Performance Regression in Tournaments

**Symptoms**: Tournament system runs slower than expected ~67K games/hour

**Diagnostic Steps**:
```bash
# Benchmark engine alone
time for i in {1..1000}; do ./tttt -t m "................................................................" -q >/dev/null; done
# Should complete 1000 moves in ~5-6 seconds

# Benchmark tournament system
time python3 tournament.py human machine 100 benchmark.csv >/dev/null
# Should complete in < 10 seconds

# Profile tournament script
python3 -m cProfile tournament.py human machine 10 profile_test.csv
```

## Common Error Messages

### "tttt: No such file or directory"

**Meaning**: Executable not found or not built

**Solutions**:
```bash
# Build the executable
make clean && make

# Check if it exists
ls -l tttt

# Ensure you're in correct directory
pwd
# Should end with /TicTacTocToe-Engine
```

---

### "invalid option" or "unrecognized arguments"

**Meaning**: Incorrect command-line arguments

**Solutions**:
```bash
# Check help
./tttt --help

# Common valid invocations
./tttt -p h                    # Interactive, human first
./tttt -t m "board_string" -q  # Tournament mode, quiet
./tttt -e "board_string"       # Evaluate board
```

---

### "Invalid move" or "Invalid argument"

**Meaning**: API function called with bad parameters

**Debugging**:
```c
// Check return values
TTTT_Return result = TTTT_HumanMove(position);
switch (result) {
    case kTTTT_NoError:
        printf("Move successful\n");
        break;
    case kTTTT_InvalidMove:
        printf("Position %ld already occupied\n", position);
        break;
    case kTTTT_InvalidArgumentOutOfRange:
        printf("Position %ld out of range (0-63)\n", position);
        break;
    default:
        printf("Unexpected error: %ld\n", result);
}
```

## Debugging Tools

### Verbose Output Mode

**Enable detailed logging** in your code:
```c
#define DEBUG_VERBOSE 1

#if DEBUG_VERBOSE
    #define DEBUG_PRINT(fmt, ...) fprintf(stderr, "DEBUG: " fmt "\n", ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...) do {} while(0)
#endif

// Usage:
DEBUG_PRINT("Making move at position %ld", position);
```

### Memory Debugging

**Valgrind** (Linux):
```bash
# Check for memory errors
valgrind --leak-check=full --track-origins=yes ./tttt -p h

# Quick check
valgrind --error-exitcode=1 ./tttt -e "................................................................"
```

**AddressSanitizer** (GCC/Clang):
```bash
# Compile with sanitizer
gcc -fsanitize=address -g -o tttt_debug *.c
./tttt_debug -p h
```

### API State Inspection

**Board state dumper**:
```c
void debug_print_board(void) {
    TTTT_GameBoardStringRep board;
    if (TTTT_GetBoard(board) == kTTTT_NoError) {
        printf("Current board state:\n");
        for (int layer = 0; layer < 4; layer++) {
            printf("Layer %d:\n", layer);
            for (int row = 0; row < 4; row++) {
                for (int col = 0; col < 4; col++) {
                    int pos = layer * 16 + row * 4 + col;
                    printf("%c ", board[pos]);
                }
                printf("\n");
            }
            printf("\n");
        }
    }
}
```

## Getting Help

### Self-Diagnosis Checklist

Before seeking help, try this checklist:

- [ ] **Build successful**: `make clean && make` completes without errors
- [ ] **Basic functionality**: `./tttt --help` shows usage information  
- [ ] **API initialization**: Code calls `TTTT_Initialize()` before other functions
- [ ] **Return value checking**: All API calls check return values
- [ ] **Buffer sizes**: Using `TTTT_GameBoardStringRep` for board strings
- [ ] **Position ranges**: All positions are 0-63
- [ ] **Platform compatibility**: Using appropriate build target for your system

### Reporting Issues

**Include this information** when reporting problems:

```bash
# System information
uname -a
gcc --version
make --version

# Build information
make clean && make 2>&1 | head -20

# Runtime test
./tttt --help
./tttt -e "................................................................"
```

**Error reproduction steps**:
1. Exact command that fails
2. Expected vs actual output
3. Any error messages
4. Minimal code example (for API issues)

### Community Resources

- **GitHub Issues**: Primary support channel for bug reports
- **Code Examples**: See `examples/` directory for working integrations
- **API Reference**: See `API_REFERENCE.md` for complete function documentation
- **Performance Benchmarks**: See `PERFORMANCE_RESULTS.md` for expected performance metrics

---

*This troubleshooting guide covers common issues with TTTTengine. For additional help, consult the API documentation and example code in the project repository.*