# TTTTengine - 4x4x4 3D Tic-Tac-Toe Engine

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#building-and-running)
[![Platform Support](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Unix-blue.svg)](#platform-compatibility)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A high-performance 3D Tic-Tac-Toe game engine written in C for the 4x4x4 game variant. Features a clean API, advanced AI with configurable heuristics, randomization support, and comprehensive tournament system.

## Quick Start

```bash
# Clone and build
git clone <repository-url>
cd TicTacTocToe-Engine
make

# Play interactively
./tttt -p h

# Run tournament
python3 tournament.py human machine 10 results.csv
```

## Features

- **🎯 Advanced AI**: Configurable heuristic weights and randomization
- **🚀 High Performance**: ~67,000 games/hour, ~200 moves/second
- **🔧 Cross Platform**: Native builds for macOS, Linux, Unix systems
- **📊 Tournament System**: Python-based automation with CSV output
- **🎲 Randomization**: Optional random selection among optimal moves
- **📚 Complete API**: Well-documented C API for integration
- **✅ Comprehensive Testing**: 39-test integration suite with performance validation

**Key Technologies:**

* Language: C
* Build System: Make

**Architecture:**

* `TTTT.c`, `TTTT.h`: Core game engine logic.
* `TTTTapi.c`, `TTTTapi.h`: API for interacting with the game engine.
* `main.c`: Command-line interface for playing the game and utilizing the engine.
* `makefile`: Defines the build process.

# Building and Running

## Prerequisites

**Required:**
- C99-compatible compiler (GCC 4.8+, Clang 3.5+, or equivalent)
- Make utility
- Python 3.6+ (for tournament system)

**Optional:**
- `libbsd-dev` (Ubuntu/Debian) for enhanced randomization on Linux
- Xcode (macOS) for IDE-based development

**Installation:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3 libbsd-dev

# macOS (Homebrew)
brew install python3
# Xcode Command Line Tools:
xcode-select --install

# CentOS/RHEL/Fedora
sudo dnf install gcc make python3-devel  # Fedora
sudo yum install gcc make python3-devel  # CentOS 7
```

## Building the Project

### Quick Build (Recommended)

```bash
cd TicTacTocToe-Engine
make clean && make
```

**Platform-Specific Builds** (for optimal performance):
```bash
make                     # Auto-detects platform, recommended
make linux-bsd          # Linux with libbsd (superior randomization)
make linux              # Standard Linux (fallback randomization)
make standard           # Generic Unix/POSIX build
```

**Build Outputs:**
- `tttt` - Main executable (command-line interface)
- `TTTTengine/*.o` - Object files
- Compiler optimization: `-O2` for performance

**Verification:**
```bash
./tttt --help           # Verify build success
./tttt -e "..."          # Test basic functionality
```

**Testing & Validation:**
```bash
make test                    # Run functional tests (7 tests)
make quick-test             # Essential integration tests (30s)
make integration-test       # Full test suite (39 tests, ~30s)
```

## Performance Benchmarks

**Engine Performance:**
- **Move Generation**: ~160-200 moves/second
- **Game Simulation**: ~67,000 complete games/hour
- **Memory Usage**: <1KB working set
- **Randomization Overhead**: Zero measurable impact

**Benchmark Commands:**
```bash
# Engine speed test
time ./tttt -e "................................................................"
# Expected: <0.01 seconds

# Tournament throughput test  
time python3 tournament.py human machine 100 benchmark.csv
# Expected: <10 seconds for 100 games
```

See `PERFORMANCE_RESULTS.md` for detailed benchmarks across platforms.

### Xcode (macOS IDE)

**Project Setup:**
1. Open `TTTTengine/TTTTengine.xcodeproj`
2. Configure run arguments:
   - Product → Scheme → Edit Scheme → Arguments
   - Add `-p h` for interactive human-first play
   - Add `-r` to enable randomization

**Development Workflow:**
- **Build**: ⌘+B
- **Run**: ⌘+R (output in Debug Console)
- **Debug**: Set breakpoints, use LLDB debugger

**Alternative**: Use command-line for faster iteration:
```bash
cd TTTTengine
make clean && make
./tttt -p h
```

## Running the Game

To play the game in interactive mode, use the `-p` flag and specify who moves first ('h' for human, 'm' for machine):

```bash
./tttt -p h
```

Or play with different heurisitic weights:

```bash
./tttt -p "h" -w "0 -2 -5 -11 -27 2 0 3 12 0 5 -3 1 0 0 11 -12 0 0 0 23 0 0 0 0"
```

### Other Modes

* **Generate Board String Representation:**

    ```bash
    ./tttt -g -h "4 5" -m "64 63"
    ```

* **Evaluate Board State:**

    ```bash
    ./tttt -e "......X......................................................OOX"
    ```

* **Tournament Mode, Next Move Generator:**

    ```bash
    ./tttt  -t m  "......XX.....................................................OOX"
    ```

* **Randomized Move Selection** (New!):

    ```bash
    # Enable randomization in any mode
    ./tttt -p h -r                    # Interactive play with randomization
    ./tttt -t m "..." -r              # Tournament mode with randomized moves
    ```
    
    The `-r`/`--randomize` flag enables random selection among equally optimal moves, useful for tournament analysis and strategic variety testing.

* **Tournament System Examples**:

    ```bash
    # Quick system test
    python3 tournament_runner.py -c examples/quick_test.csv -i 5
    
    # Strategy comparison 
    python3 tournament_runner.py -c examples/aggressive_strategies.csv -i 15 --randomization
    
    # Run complete example gallery
    ./run_example_gallery.sh
    ```
    
    See `examples/` directory for ready-to-use tournament configurations and comprehensive documentation.

## Documentation

### Core Documentation
- **[Build Guide](BUILD_GUIDE.md)** 📋 - Comprehensive cross-platform build instructions
- **[API Reference](API_REFERENCE.md)** 📚 - Complete C API documentation with examples  
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** 🔧 - Common issues and solutions
- **[Integration Testing](INTEGRATION_TESTING.md)** ✅ - Test suite documentation
- **[Performance Results](PERFORMANCE_RESULTS.md)** ⚡ - Detailed benchmark data

### Developer Resources
- **[Examples Gallery](examples/README.md)** 🎯 - Ready-to-use tournament configurations
- **[Tournament System](tournament.py)** 🤖 - Python automation framework
- **[Build System](makefile)** ⚙️ - Multi-platform compilation targets
- **[Project Specification](spec.md)** 📖 - Complete technical specification

### Quick References
- **[Documentation Index](DOCUMENTATION_INDEX.md)** 🗂️ - Complete documentation navigation
- **[Examples Quickref](examples/QUICKREF.md)** ⚡ - Fast example lookup  
- **[GitHub Copilot Instructions](.github/copilot-instructions.md)** 🤖 - AI development context

## Platform Compatibility

| Platform | Build Command | Random Function | Status |
|----------|---------------|-----------------|--------|
| **macOS** | `make` | `arc4random()` (native) | ✅ Fully Supported |
| **Linux + libbsd** | `make linux-bsd` | `arc4random()` (libbsd) | ✅ Recommended |
| **Linux Standard** | `make linux` | `rand()` + `time()` | ✅ Supported |
| **FreeBSD/OpenBSD** | `make` | `arc4random()` (native) | ✅ Supported |
| **Other Unix** | `make standard` | `rand()` + `time()` | ✅ Supported |
| **Windows** | Manual/MinGW | `rand()` + `time()` | ⚠️ Community Support |

**Notes:**
- `arc4random()` provides superior randomization (no seeding required)
- All builds produce identical game logic behavior
- Cross-platform compatibility tested and verified

# Development Conventions

## Code Architecture

**Layered Design:**
- **Core Engine** (`TTTT.c/.h`) - Game logic, AI algorithms, board evaluation
- **API Layer** (`TTTTapi.c/.h`) - Clean C interface with error handling
- **CLI Interface** (`main.c`) - Command-line tool with multiple operation modes
- **Common Definitions** (`TTTTcommon.h`) - Shared constants and types

**Key Principles:**
- **Separation of Concerns**: Engine logic independent of UI
- **Error Handling**: All API functions return status codes
- **Platform Abstraction**: Conditional compilation for cross-platform support
- **Performance**: Optimized algorithms with minimal memory footprint
- **Testability**: Comprehensive test coverage with automation

## Contributing Guidelines

**Code Style:**
- C99 standard compliance
- Consistent indentation and naming
- Comprehensive error checking
- Documentation for public APIs

**Testing Requirements:**
- All changes must pass integration test suite: `make integration-test`
- Performance regression testing: verify sustained 60K+ games/hour
- Cross-platform validation when possible

**Quality Assurance:**
```bash
# Full validation workflow
make clean && make
make integration-test        # 39 tests, expect 100% pass rate
make test                   # 7 functional tests
python3 integration_test_suite.py  # System-level validation
```

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| **Build fails** | `make clean && make`, check [prerequisites](#prerequisites) |
| **"Command not found"** | Install build tools: `xcode-select --install` (macOS) |
| **Random errors on Linux** | Try `make linux-bsd` or install `libbsd-dev` |
| **Segmentation fault** | Ensure `TTTT_Initialize()` called before API use |
| **Tournament fails** | Verify `./tttt --help` works, check Python 3.6+ |
| **Performance issues** | Use optimized build: `CFLAGS="-O2" make` |

**Full troubleshooting guide** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

# License

Licensed under the [MIT License](http://www.opensource.org/licenses/mit-licenses.php)

Copyright (c) 2010 Alex Popadich. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.