# TTTTengine Build Guide

## Overview

This guide provides comprehensive instructions for building TTTTengine across all supported platforms. The engine uses a cross-platform makefile system with automatic platform detection and optimized builds.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Build](#quick-build)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Build Targets](#build-targets)
- [Troubleshooting](#troubleshooting)
- [Development Builds](#development-builds)
- [CI/CD Integration](#cicd-integration)

## Prerequisites

### All Platforms

**Required:**
- C99-compatible compiler (GCC 4.8+, Clang 3.5+, MSVC 2015+)
- Make utility (GNU Make recommended)
- Python 3.6+ (for tournament system and testing)

**Optional:**
- Git (for source code management)
- Debugger (GDB, LLDB, or platform equivalent)

### Platform-Specific Dependencies

#### macOS
```bash
# Install Xcode Command Line Tools (includes GCC/Clang + Make)
xcode-select --install

# Verify installation
gcc --version    # Should show Apple clang or GCC
make --version   # Should show GNU Make

# Optional: Homebrew for additional tools
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

#### Ubuntu/Debian Linux
```bash
# Install build essentials
sudo apt-get update
sudo apt-get install build-essential python3 python3-pip

# Enhanced randomization support (recommended)
sudo apt-get install libbsd-dev

# Verify installation
gcc --version    # Should show GCC 4.8+
make --version   # Should show GNU Make
python3 --version  # Should show Python 3.6+

# Optional: Development tools
sudo apt-get install gdb valgrind git
```

#### CentOS/RHEL/Fedora Linux
```bash
# CentOS 7 / RHEL 7
sudo yum groupinstall "Development Tools"
sudo yum install python3 python3-devel

# Fedora / CentOS 8+
sudo dnf groupinstall "Development Tools"  
sudo dnf install python3 python3-devel

# Enhanced randomization (if available)
sudo dnf install libbsd-devel  # Fedora
# Note: libbsd may not be available on all RHEL versions
```

#### Windows (MinGW/MSYS2)
```bash
# Install MSYS2 from https://www.msys2.org/
# Then in MSYS2 terminal:
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make python3

# Add to PATH (adjust paths for your installation):
export PATH="/mingw64/bin:$PATH"

# Verify installation
gcc --version
make --version
python3 --version
```

## Quick Build

### Standard Build (Recommended)
```bash
# Clone repository
git clone <repository-url>
cd TicTacTocToe-Engine

# Clean build (recommended)
make clean && make

# Verify build success
./tttt --help
./tttt -e "................................................................"
```

### Build with Testing
```bash
# Build and run all tests
make clean && make && make test

# Quick verification (essential tests)
make quick-test

# Comprehensive testing (39-test suite)
make integration-test
```

## Platform-Specific Instructions

### macOS

**Automatic Build** (Recommended):
```bash
make clean && make
# Automatically detects macOS and uses native arc4random()
```

**Xcode Project**:
1. Open `TTTTengine/TTTTengine.xcodeproj`
2. Product → Build (⌘+B)
3. Set up scheme arguments:
   - Product → Scheme → Edit Scheme → Arguments
   - Add `-p h` for interactive play

**Manual Compilation**:
```bash
cd TTTTengine
gcc -g -O2 -Wall -c TTTT.c TTTTapi.c main.c
gcc -o tttt TTTT.o TTTTapi.o main.o
```

---

### Linux with Enhanced Randomization

**Ubuntu/Debian** (Recommended):
```bash
# Install libbsd for superior randomization
sudo apt-get install libbsd-dev

# Build with BSD support
make clean && make linux-bsd

# Verify BSD functionality
./tttt -t m "................................................................" -r -q
# Should show varied outputs on repeated runs
```

**Manual BSD Build**:
```bash
cd TTTTengine  
gcc -g -O2 -Wall -DHAVE_ARC4RANDOM -c TTTT.c TTTTapi.c main.c
gcc -o tttt TTTT.o TTTTapi.o main.o -lbsd
```

---

### Standard Linux

**Any Distribution**:
```bash
# Standard build (uses rand() + time() seeding)
make clean && make linux

# Or use generic target
make clean && make standard
```

**Manual Standard Build**:
```bash
cd TTTTengine
gcc -g -O2 -Wall -c TTTT.c TTTTapi.c main.c  
gcc -o tttt TTTT.o TTTTapi.o main.o
```

---

### FreeBSD/OpenBSD/NetBSD

**Native BSD**:
```bash
# Uses native arc4random() automatically
make clean && make

# Alternative: explicit BSD target
gmake clean && gmake  # Use GNU make if available
```

---

### Windows

**MinGW/MSYS2**:
```bash
# Standard build (uses rand())
make clean && make standard

# Manual compilation
gcc -g -O2 -Wall -c TTTT.c TTTTapi.c main.c
gcc -o tttt.exe TTTT.o TTTTapi.o main.o
```

**Visual Studio**:
1. Create new Console Application project
2. Add source files: `TTTT.c`, `TTTTapi.c`, `main.c`
3. Add headers: `TTTT.h`, `TTTTapi.h`, `TTTTcommon.h`
4. Build → Build Solution

## Build Targets

### Primary Targets

| Target | Description | Platforms | Random Function |
|--------|-------------|-----------|-----------------|
| `make` | **Auto-detect build** | All | Platform optimal |
| `make linux-bsd` | **Linux + libbsd** | Linux | `arc4random()` |
| `make linux` | **Standard Linux** | Linux | `rand()` |
| `make standard` | **Generic Unix** | All | `rand()` |

### Testing Targets

| Target | Description | Duration | Tests |
|--------|-------------|----------|-------|
| `make test` | **Functional tests** | ~5s | 7 core tests |
| `make quick-test` | **Essential integration** | ~30s | Key functionality |
| `make integration-test` | **Full test suite** | ~30s | 39 comprehensive tests |

### Maintenance Targets

```bash
make clean          # Remove object files and executable
make clean-all      # Remove all generated files including test outputs
make rebuild        # Clean + build in one command
make help          # Show all available targets
```

## Build Verification

### Basic Functionality Test
```bash
# Test command-line interface
./tttt --help

# Test board evaluation
./tttt -e "................................................................"

# Test interactive mode (Ctrl+C to exit)
./tttt -p h

# Test tournament mode
./tttt -t m "................................................................" -q
```

### Performance Verification
```bash
# Engine speed test (should complete in <0.01s)
time ./tttt -e "................................................................"

# Tournament throughput test (should achieve 60K+ games/hour)
time python3 tournament.py human machine 100 benchmark.csv
```

### Randomization Verification
```bash
# Test randomization (outputs should vary)
./tttt -t m "................................................................" -r -q
./tttt -t m "................................................................" -r -q
./tttt -t m "................................................................" -r -q

# Test deterministic (outputs should be identical)
./tttt -t m "................................................................" -q
./tttt -t m "................................................................" -q
```

## Development Builds

### Debug Build
```bash
# Build with debug symbols and no optimization
CFLAGS="-g -O0 -DDEBUG" make clean && make

# Run with debugger
gdb ./tttt
(gdb) run -p h
```

### Optimized Build
```bash
# Maximum optimization
CFLAGS="-O3 -DNDEBUG -march=native" make clean && make

# Benchmark optimized build
time python3 tournament.py human machine 500 optimized_test.csv
```

### Memory Debugging
```bash
# AddressSanitizer build (GCC/Clang)
CFLAGS="-fsanitize=address -g" make clean && make
./tttt -p h

# Valgrind testing (Linux)
make clean && make
valgrind --leak-check=full ./tttt -e "................................................................"
```

### Static Analysis
```bash
# Enable all warnings
CFLAGS="-Wall -Wextra -Wpedantic" make clean && make

# Static analysis with Clang
clang-static-analyzer make clean && make
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Cross-Platform Build
on: [push, pull_request]

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install dependencies (Ubuntu)
      if: matrix.os == 'ubuntu-latest'
      run: sudo apt-get install libbsd-dev
      
    - name: Build
      run: make clean && make
      
    - name: Test
      run: make test && make integration-test
      
    - name: Performance benchmark
      run: python3 tournament.py human machine 100 ci_benchmark.csv
```

### Docker Build
```dockerfile
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    build-essential \
    libbsd-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN make clean && make linux-bsd && make integration-test

CMD ["./tttt", "--help"]
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make clean && make'
            }
        }
        stage('Test') {
            steps {
                sh 'make integration-test'
            }
        }
        stage('Performance') {
            steps {
                sh 'python3 tournament.py human machine 200 jenkins_bench.csv'
                archiveArtifacts 'jenkins_bench.csv'
            }
        }
    }
}
```

## Advanced Configuration

### Compiler Selection
```bash
# Use specific compiler
CC=clang make clean && make
CC=gcc-9 make clean && make

# Cross-compilation example
CC=arm-linux-gnueabihf-gcc make clean && make
```

### Custom Optimization
```bash
# Size optimization
CFLAGS="-Os" make clean && make

# Speed optimization with profiling
CFLAGS="-O3 -fprofile-generate" make clean && make
./tttt -p h  # Generate profile data
CFLAGS="-O3 -fprofile-use" make clean && make
```

### Feature Flags
```bash
# Disable randomization support
CFLAGS="-DNO_RANDOMIZATION" make clean && make

# Enable verbose debugging  
CFLAGS="-DVERBOSE_DEBUG" make clean && make
```

## Troubleshooting

### Common Issues

**"make: command not found"**
```bash
# macOS: Install Xcode Command Line Tools
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# CentOS/RHEL  
sudo yum groupinstall "Development Tools"
```

**"gcc: command not found"**
```bash
# Install compiler toolchain (see Prerequisites section above)
# Verify installation:
which gcc
gcc --version
```

**"arc4random not declared" (Linux)**
```bash
# Option 1: Install libbsd and use BSD build
sudo apt-get install libbsd-dev
make clean && make linux-bsd

# Option 2: Use standard build
make clean && make linux
```

**Build succeeds but executable crashes**
```bash
# Check for proper initialization
gdb ./tttt
(gdb) run -p h
# Look for segmentation faults

# Verify basic functionality
./tttt --help
```

**Performance issues**
```bash
# Ensure optimized build
CFLAGS="-O2" make clean && make

# Check system resources
top
iostat 1
```

### Build Environment Debugging
```bash
# Check build environment
echo "CC: $CC"
echo "CFLAGS: $CFLAGS"
make --version
gcc --version

# Verbose build output
make clean && make V=1

# Show all variables
make --print-data-base | grep -E '^[a-zA-Z_]+ ='
```

### Platform Detection Issues
```bash
# Check platform detection
uname -a
gcc -dumpmachine

# Force specific build target
make clean && make standard  # Generic build
```

---

**For additional help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive problem-solving guidance.**