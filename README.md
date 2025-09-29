# Project Overview

This project is a 3D Tic-Tac-Toe (4x4x4) game engine written in C. It provides a command-line interface for playing against the computer, generating board representations, and evaluating board states. The engine's logic is separated from the command-line interface, with a clear API defined in `TTTTapi.h`.

This is the Tic Tac Toc Toe playing engine or just TTTTengine for short.

A simple 3 dimensional tic-tac-toe like game which is played on a 4x4x4 grid and requires you to get four in a row to win.

**Key Technologies:**

* Language: C
* Build System: Make

**Architecture:**

* `TTTT.c`, `TTTT.h`: Core game engine logic.
* `TTTTapi.c`, `TTTTapi.h`: API for interacting with the game engine.
* `main.c`: Command-line interface for playing the game and utilizing the engine.
* `makefile`: Defines the build process.

# Building and Running

This code is meant to compile both on a Mac as an XCode project and on a Linux/Unix system with the unix make utility.

## Building the Project

### Linux/Unix:

Assuming you have the proper development tools installed, you should be able to cd to the project directory and type make.

```bash
% cd TicTacTocToe-Engine
% make                    # Standard build (works on all platforms)
```

**Platform-Specific Builds** (for optimal randomization):
```bash
% make linux-bsd         # Linux with libbsd (requires: apt install libbsd-dev)
% make linux             # Standard Linux build  
% make standard          # Generic build for any platform
```

This will compile the source files and create an executable named `tttt`.

**Testing the Build:**
```bash
% make test                    # Run functional tests
% make quick-test             # Run essential integration tests (30s)
% make integration-test       # Run full integration test suite (30s)
```

### Xcode:

You have to set the argument on the executable otherwise there won't be much to see. 

In the Xcode project select the application under the "Executables" Group and then perform a Get Info. In the dialog presented choose the Arguments Tab and add a new "-p" argument telling the application you want to play a game.

All the output is sent to the "Console"

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

# Development Conventions

The code follows a consistent style, with clear separation of concerns between the engine and the UI. Header files are used to define public interfaces for the different modules. The code is well-commented, and the license is included in the header of each source file.

# License:

Licensed under the [MIT License](http://www.opensource.org/licenses/mit-licenses.php)