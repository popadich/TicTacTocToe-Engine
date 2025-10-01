/*
 *  TTTTapi.h
 *  TTTTengine
 *
 *  Created by Alex Popadich on 4/5/10.
 *  Copyright (c) 2010 Alex Popadich.
 *
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include <ctype.h>
#include <getopt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "TTTTapi.h"

#define TTTT_VERSION "1.0"

typedef enum {
    MODE_NONE,
    MODE_PLAY,
    MODE_EVALUATE,
    MODE_GENERATE,
    MODE_TURN,
    MODE_HELP,
    MODE_VERSION
} tttt_mode;

typedef struct {
    tttt_mode mode;
    const char *who_moves;
    const char *machine_moves;
    const char *human_moves;
    const char *weights_matrix;
    const char *string_rep;
} tttt_args;

// some local scoped globals
bool quiteflag = false;
bool verboseflag = false;
bool setweightsflag = false;
bool randomizeflag = false;
TTTT_WeightsTable new_weights;

// Function declarations
int count_moves_from_board(const char *board_string, char player_char);

void print_stringrep(char *theBoard) {
    int i = 0;
    for (i = 0; i < 64; i++) {
        printf("%c", theBoard[i]);
    }
    printf("\n");
}

void print_board_stringrep(char *theBoard) {
    int i, j;
    if (quiteflag) {
        return;
    }
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 16; j++) {
            printf("%c ", theBoard[i * 16 + j]);
            if ((j + 1) % 4 == 0) {
                printf("\n");
            }
        }
        printf("\n");
    }
}

void print_board(bool game_over) {
    TTTT_GameBoardStringRep pszGameBoard;
    if (game_over) {
        TTTT_GetWinnerStringRep(pszGameBoard);
    } else {
        TTTT_GetBoard(pszGameBoard);
    }
    print_board_stringrep(pszGameBoard);
}

int set_weightsmatrix(const char *weightsmatrix) {
    int scanError;
    int r1c1, r1c2, r1c3, r1c4, r1c5;
    int r2c1, r2c2, r2c3, r2c4, r2c5;
    int r3c1, r3c2, r3c3, r3c4, r3c5;
    int r4c1, r4c2, r4c3, r4c4, r4c5;
    int r5c1, r5c2, r5c3, r5c4, r5c5;

    scanError = sscanf(
        weightsmatrix, "%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d",
        &r1c1, &r1c2, &r1c3, &r1c4, &r1c5, &r2c1, &r2c2, &r2c3, &r2c4, &r2c5,
        &r3c1, &r3c2, &r3c3, &r3c4, &r3c5, &r4c1, &r4c2, &r4c3, &r4c4, &r4c5,
        &r5c1, &r5c2, &r5c3, &r5c4, &r5c5);
    if (scanError != 25) {
        fprintf(stderr, "Error: Invalid weight matrix format.\n");
        fprintf(stderr, "Expected: 25 space-separated integers (5x5 matrix)\n");
        fprintf(stderr, "Example: '0 -2 -4 -8 -16 2 0 0 0 0 4 0 1 0 0 8 0 0 0 0 16 0 0 0 0'\n");
        fprintf(stderr, "Got %d values from: '%s'\n", scanError, weightsmatrix);
        return -1;  // Return error
    }

    if (verboseflag) {
        printf("Matrix is: %d %d %d %d %d for first row\n", r1c1, r1c2,
               r1c3, r1c4, r1c5);
        printf("Matrix is: %d %d %d %d %d for second row\n", r2c1, r2c2,
               r2c3, r2c4, r2c5);
        printf("Matrix is: %d %d %d %d %d for third row\n", r3c1, r3c2,
               r3c3, r3c4, r3c5);
        printf("Matrix is: %d %d %d %d %d for fourth row\n", r4c1, r4c2,
               r4c3, r4c4, r4c5);
        printf("Matrix is: %d %d %d %d %d for fifth row\n", r5c1, r5c2,
               r5c3, r5c4, r5c5);
    }

    new_weights[0][0] = r1c1;
    new_weights[0][1] = r1c2;
    new_weights[0][2] = r1c3;
    new_weights[0][3] = r1c4;
    new_weights[0][4] = r1c5;

    new_weights[1][0] = r2c1;
    new_weights[1][1] = r2c2;
    new_weights[1][2] = r2c3;
    new_weights[1][3] = r2c4;
    new_weights[1][4] = r2c5;

    new_weights[2][0] = r3c1;
    new_weights[2][1] = r3c2;
    new_weights[2][2] = r3c3;
    new_weights[2][3] = r3c4;
    new_weights[2][4] = r3c5;

    new_weights[3][0] = r4c1;
    new_weights[3][1] = r4c2;
    new_weights[3][2] = r4c3;
    new_weights[3][3] = r4c4;
    new_weights[3][4] = r4c5;

    new_weights[4][0] = r5c1;
    new_weights[4][1] = r5c2;
    new_weights[4][2] = r5c3;
    new_weights[4][3] = r5c4;
    new_weights[4][4] = r5c5;
    
    return 0;  // Success
}

long evaluate_stringrep(const TTTT_GameBoardStringRep pszGameBoard) {
    long value = 0;

    TTTT_Initialize();
    if (setweightsflag) {
        TTTT_SetHeuristicWeights(new_weights);
    }

    printf("Board StringRep is: %s\n\n", pszGameBoard);
    if (TTTT_EvaluateBoardValue(pszGameBoard, &value) == kTTTT_NoError)
        return value;
    return 0;
}

void generate_stringrep(const char *human_moves, const char *machine_moves) {
    TTTT_GameBoardStringRep pszGameBoard;

    TTTT_Initialize();
    TTTT_GetBoard(pszGameBoard);
    TTTT_StringRep(human_moves, machine_moves, pszGameBoard);

    print_stringrep(pszGameBoard);
}

void generative_mode(TTTT_GameBoardStringRep pszGameBoard, char *human_moves) {
    int scanError;
    // Game vars
    TTTT_Return aWinner;
    long theWinner;
    bool game_over = false;
    int aMove = -1;

    while (!game_over) {
        TTTT_GetBoard(pszGameBoard);

        print_board_stringrep(pszGameBoard);
        print_stringrep(pszGameBoard);

        do {
            printf("\n\nPlease enter move [1-64], or a [0] to quit!\n");
            scanError = scanf("%d", &aMove);

        } while (scanError != 1);

        if (aMove > 0 && aMove <= 64) {
            printf("\nyour move is:  %d\n", aMove);
            if (TTTT_HumanMove(aMove) == kTTTT_NoError) {
                aWinner = TTTT_GetWinner(&theWinner);
                if (aWinner == kTTTT_NOBODY) {
                    aWinner = TTTT_GetWinner(&theWinner);
                }
                switch (theWinner) {
                case kTTTT_MACHINE:
                    if (!quiteflag)
                        printf("\nGame Over:  Machine Wins\n");
                    else
                        printf("game_over");
                    game_over = true;
                    break;

                case kTTTT_HUMAN:
                    if (!quiteflag)
                        printf("\nGame Over:  Human Wins\n");
                    else
                        printf("game_over");
                    game_over = true;
                    break;

                case kTTTT_NOBODY:
                    break;
                }
            }

        } else {
            game_over = true;
            if (!quiteflag)
                printf("Game Over\n");
        }
        // gets(inbuf);
    }
}

bool is_board_full(void) {
    TTTT_GameBoardStringRep board_string;
    TTTT_GetBoard(board_string);
    
    int human_moves = count_moves_from_board(board_string, TTTT_HUMAN_MARKER);
    int machine_moves = count_moves_from_board(board_string, TTTT_MACHINE_MARKER);
    
    return (human_moves + machine_moves) >= TTTT_BOARD_POSITIONS;
}

bool announce_winner(TTTT_Return aWinner) {
    bool game_over = false;

    switch (aWinner) {
    case kTTTT_MACHINE:
        if (!quiteflag)
            printf("\nGame Over:  Machine Wins\n");
        else
            printf("game_over");
        game_over = true;
        break;

    case kTTTT_HUMAN:
        if (!quiteflag)
            printf("\nGame Over:  Human Wins\n");
        else
            printf("game_over");
        game_over = true;
        break;

    case kTTTT_NOBODY:
        // Check if board is full (draw condition)
        game_over = false;
        if (is_board_full()) {
            if (!quiteflag)
                printf("\nGame Over:  Draw - Board is Full\n");
            else
                printf("game_over");
            game_over = true;
        }
        break;
    }
    return game_over;
}

bool human_moves(void) {
    bool game_over = false;
    int scanError;
    long aMove = -1;
    long possibleWinner;

    if (!quiteflag)
        printf("\n\nPlease enter a move [1-64], or a [0] to quit!\n");

    while (1) {
        scanError = scanf("%ld", &aMove);
        if (scanError == 1 && aMove >= 0 && aMove <= 64) {
            break; // Valid input
        } else {
            printf("Invalid input. Please enter a number between 1 and 64.\n");
            // Clear the input buffer
            while (getchar() != '\n');
        }
    }

    if (aMove > 0 && aMove <= 64) {
        if (!quiteflag)
            printf("\nHuman move is:  %ld\n", aMove);
        if (TTTT_HumanMove(aMove - 1) == kTTTT_NoError) {
            TTTT_GetWinner(&possibleWinner);
            game_over = announce_winner(possibleWinner);
        }
        // display board
        print_board(game_over);
    } else {
        game_over = true;
        if (!quiteflag)
            printf("Game Over\n");
    }

    return game_over;
}

bool machine_moves(void) {
    bool game_over = false;

    long possibleWinner;
    long aMove;

    TTTT_MacMove(&aMove);
    if (!quiteflag)
        printf("\nMachine move is:  %ld\n", aMove + 1);
    else
        printf("%ld\n", aMove + 1);

    TTTT_GetWinner(&possibleWinner);
    game_over = announce_winner(possibleWinner);

    // display board
    print_board(game_over);

    return game_over;
}

void interactive_mode(const char *who_moves) {
    // Game vars
    bool is_game_over = false;
    int first_player = kTTTT_HUMAN;

    TTTT_Initialize();
    if (setweightsflag) {
        TTTT_SetHeuristicWeights(new_weights);
    }
    print_board(is_game_over);

    // figure out who goes first
    if (*who_moves == 'h') {
        if (verboseflag)
            printf("You Go First\n\n");
        first_player = kTTTT_HUMAN;
    } else if (*who_moves == 'm') {
        if (verboseflag)
            printf("I will go first, thank you very much.\n\n");
        first_player = kTTTT_MACHINE;
    }

    if (first_player == kTTTT_HUMAN) {
        while (!is_game_over) {
            // human moves
            if (!is_game_over) {
                is_game_over = human_moves();
            }

            // machine moves
            if (!is_game_over) {
                is_game_over = machine_moves();
            }
        }
    } else if (first_player == kTTTT_MACHINE) {
        while (!is_game_over) {
            // machine moves
            if (!is_game_over) {
                is_game_over = machine_moves();
            }

            // human moves
            if (!is_game_over) {
                is_game_over = human_moves();
            }
        }

    } else {
        printf("Please specify player to move first -p \"human\" or -p "
               "\"machine\".\n");
    }
}

void turn_mode(const char *who_moves, const char *string_rep) {
    TTTT_Initialize();
    if (setweightsflag) {
        TTTT_SetHeuristicWeights(new_weights);
    }
    TTTT_SetBoard(string_rep);

    // Do one move ahead based on who's turn it is
    long aMove = -1;
    TTTT_GameBoardStringRep newStringRep;
    
    if (*who_moves == 'm') {
        TTTT_MacMove(&aMove);
        TTTT_MakeStringRep(kTTTT_MACHINE, aMove, string_rep, newStringRep);
        if (!quiteflag)
            printf("Machine move: %ld  ", aMove + 1);
        else
            printf("%ld ", aMove + 1);
    } else if (*who_moves == 'h') {
        TTTT_GetBestMove(kTTTT_HUMAN, &aMove);
        TTTT_MakeStringRep(kTTTT_HUMAN, aMove, string_rep, newStringRep);
        if (!quiteflag)
            printf("Human move:  %ld  ", aMove + 1);
        else
            printf("%ld ", aMove + 1);
    }

    // Set the board to the new state after the move
    TTTT_SetBoard(newStringRep);

    // Check for winner after the move
    long winner = kTTTT_NOBODY;
    TTTT_GetWinner(&winner);

    if (winner == kTTTT_MACHINE) {
        if (!quiteflag)
            printf("\nGame Over:  Machine Wins\n");
        else
            printf("game_over\n");
    } else if (winner == kTTTT_HUMAN) {
        if (!quiteflag)
            printf("\nGame Over:  Human Wins\n");
        else
            printf("game_over\n");
    }

    print_stringrep(newStringRep);

}


void print_usage(void) {
    fprintf(stderr, "Usage: tttt [options]\n");
    fprintf(stderr, "Options:\n");
    fprintf(stderr, "  -e, --evaluate <stringrep>   Evaluate a board string representation.\n");
    fprintf(stderr, "  -g, --generate               Generate a board string representation.\n");
    fprintf(stderr, "  -p, --play <h|m>             Play an interactive game.\n");
    fprintf(stderr, "  -t, --turn <h|m> <stringrep> Get next move for a given board state.\n");
    fprintf(stderr, "  -w, --weights <matrix>       Set the heuristic weights.\n");
    fprintf(stderr, "  -m, --machine-moves <list>   List of machine moves for generation.\n");
    fprintf(stderr, "  -h, --human-moves <list>     List of human moves for generation.\n");
    fprintf(stderr, "  -r, --randomize              Enable randomized move selection.\n");
    fprintf(stderr, "  -v, --verbose                Enable verbose output.\n");
    fprintf(stderr, "  -q, --quiet                  Suppress all output.\n");
    fprintf(stderr, "      --help                   Display this help and exit.\n");
    fprintf(stderr, "      --version                Output version information and exit.\n");

    fprintf(stderr, "Examples:\n");
    fprintf(stderr, "  tttt -p \"h\" -w \"0 -2 -5 -11 -27 2 0 3 12 0 5 -3 1 0 0 11 -12 0 0 0 23 0 0 0 0\"\n");
    fprintf(stderr, "  tttt -p h\n");
    fprintf(stderr, "  tttt -g -h \"4 5\" -m \"64 63\"\n");
    fprintf(stderr, "  tttt -e \"......X......................................................OOX\"\n");

}

tttt_args parse_arguments(int argc, char *argv[]) {
    tttt_args args = { .mode = MODE_NONE };
    int c;

    static struct option long_options[] = {
        {"evaluate",      required_argument, 0, 'e'},
        {"generate",      no_argument,       0, 'g'},
        {"play",          required_argument, 0, 'p'},
        {"turn",          required_argument, 0, 't'},
        {"weights",       required_argument, 0, 'w'},
        {"machine-moves", required_argument, 0, 'm'},
        {"human-moves",   required_argument, 0, 'h'},
        {"randomize",     no_argument,       0, 'r'},
        {"verbose",       no_argument,       0, 'v'},
        {"quiet",         no_argument,       0, 'q'},
        {"help",          no_argument,       0, 0},
        {"version",       no_argument,       0, 0},
        {0, 0, 0, 0}
    };

    while (1) {
        int option_index = 0;
        c = getopt_long(argc, argv, "e:gp:t:w:m:h:rvq", long_options, &option_index);

        if (c == -1)
            break;

        switch (c) {
            case 0:
                if (strcmp(long_options[option_index].name, "help") == 0) {
                    args.mode = MODE_HELP;
                } else if (strcmp(long_options[option_index].name, "version") == 0) {
                    args.mode = MODE_VERSION;
                }
                break;
            case 'e':
                args.mode = MODE_EVALUATE;
                args.string_rep = optarg;
                break;
            case 'g':
                args.mode = MODE_GENERATE;
                break;
            case 'p':
                args.mode = MODE_PLAY;
                args.who_moves = optarg;
                break;
            case 't':
                args.mode = MODE_TURN;
                args.who_moves = optarg;
                if (optind < argc && argv[optind][0] != '-') {
                    args.string_rep = argv[optind];
                    optind++;
                } else {
                    fprintf(stderr, "Option -t requires two arguments: [whofirst] and [boardstringrep]\n");
                    print_usage();
                    exit(EXIT_FAILURE);
                }
                break;
            case 'w':
                setweightsflag = true;
                args.weights_matrix = optarg;
                break;
            case 'm':
                args.machine_moves = optarg;
                break;
            case 'h':
                args.human_moves = optarg;
                break;
            case 'r':
                randomizeflag = true;
                break;
            case 'v':
                verboseflag = true;
                break;
            case 'q':
                quiteflag = true;
                break;
            case '?':
                exit(EXIT_FAILURE);
            default:
                abort();
        }
    }
    return args;
}


int count_moves_from_string(const char *moves_string) {
    if (moves_string == NULL) {
        return 0;
    }
    int count = 0;
    const char *p = moves_string;
    while (*p) {
        if (isspace(*p)) {
            count++;
        }
        p++;
    }
    return count + 1;
}

int count_moves_from_board(const char *board_string, char player_char) {
    if (board_string == NULL) {
        return 0;
    }
    int count = 0;
    const char *p = board_string;
    while (*p) {
        if (*p == player_char) {
            count++;
        }
        p++;
    }
    return count;
}

bool validate_board_string(const char *board_string) {
    if (board_string == NULL) {
        fprintf(stderr, "Error: Board string cannot be NULL.\n");
        return false;
    }
    
    size_t length = strlen(board_string);
    if (length != TTTT_BOARD_POSITIONS) {
        fprintf(stderr, "Error: Board string must be exactly %d characters long, got %zu.\n", 
                TTTT_BOARD_POSITIONS, length);
        return false;
    }
    
    // Validate each character
    for (int i = 0; i < TTTT_BOARD_POSITIONS; i++) {
        char c = board_string[i];
        if (c != 'X' && c != 'O' && c != '.') {
            fprintf(stderr, "Error: Invalid character '%c' at position %d. "
                           "Only 'X', 'O', and '.' are allowed.\n", c, i);
            return false;
        }
    }
    
    return true;
}

bool validate_player_argument(const char *player) {
    if (player == NULL) {
        fprintf(stderr, "Error: Player argument cannot be NULL.\n");
        return false;
    }
    
    if (strlen(player) != 1) {
        fprintf(stderr, "Error: Player must be a single character ('h' or 'm'), got '%s'.\n", player);
        return false;
    }
    
    if (*player != 'h' && *player != 'm') {
        fprintf(stderr, "Error: Invalid player '%c'. Must be 'h' (human) or 'm' (machine).\n", *player);
        return false;
    }
    
    return true;
}

void sanity_check_moves(int human_moves, int machine_moves) {
    if (abs(human_moves - machine_moves) > 1) {
        fprintf(stderr, "Error: Invalid number of moves. Human moves: %d, Machine moves: %d. "
                       "The difference cannot be greater than 1.\n", human_moves, machine_moves);
        fprintf(stderr, "Hint: In 4x4x4 Tic-Tac-Toe, players alternate moves, so move counts "
                       "should be equal or differ by at most 1.\n");
        exit(EXIT_FAILURE);
    }
}

// PLAY INTERACTIVE GAME
//     tttt -p
//
// EVALUATE BOARD STRINGREP
//     tttt -e <stringrep>
//
// stringrep samples:
// ......X......................................................OOX
// X..X...........................................................O
// O..XXXX........O.....O....................O.....................
//
// GENERATE BOARD REPRESENTATION STRING
// ./tttt -g -h "4 5" -m "64 63"

int main(int argc, char *argv[]) {
    if (argc <= 1) {
        print_usage();
        exit(EXIT_FAILURE);
    }

    tttt_args args = parse_arguments(argc, argv);

    // get verbose here for debugging
     if (verboseflag) {
        printf("mode = %d, quiteflag = %d \n", args.mode, quiteflag);
        printf("who_moves = %s, weights_matrix = %s, machine_moves = %s, human_moves = %s\n",
               args.who_moves, args.weights_matrix, args.machine_moves, args.human_moves);

    }

    if (setweightsflag == true) {
        if (set_weightsmatrix(args.weights_matrix) != 0) {
            exit(EXIT_FAILURE);
        }
    }

    if (randomizeflag == true) {
        TTTT_SetRandomize(true);
    }

    switch (args.mode)
    {
    case MODE_PLAY:
        if (args.who_moves == NULL) {
            fprintf(stderr, "Error: Player must be specified with '-p' option ('h' or 'm').\n");
            exit(EXIT_FAILURE);
        }
        if (!validate_player_argument(args.who_moves)) {
            exit(EXIT_FAILURE);
        }
        interactive_mode(args.who_moves);
        break;

    case MODE_EVALUATE:
        if (args.string_rep == NULL) {
            fprintf(stderr, "Error: Board string representation must be specified with '-e' option.\n");
            exit(EXIT_FAILURE);
        }
        if (!validate_board_string(args.string_rep)) {
            exit(EXIT_FAILURE);
        }
        int human_moves_eval = count_moves_from_board(args.string_rep, TTTT_HUMAN_MARKER);
        int machine_moves_eval = count_moves_from_board(args.string_rep, TTTT_MACHINE_MARKER);
        sanity_check_moves(human_moves_eval, machine_moves_eval);
        long myBoardValue = evaluate_stringrep(args.string_rep);
        printf("Board Value is: %ld\n\n", myBoardValue);
        break;
    
    case MODE_GENERATE:
        if (args.human_moves == NULL) {
            fprintf(stderr, "Human moves must be specified with '-h' option.\n");
            exit(EXIT_FAILURE);
        }
        if (args.machine_moves == NULL) {
            fprintf(stderr, "Machine moves must be specified with '-m' option.\n");
            exit(EXIT_FAILURE);
        }
        int human_moves_gen = count_moves_from_string(args.human_moves);
        int machine_moves_gen = count_moves_from_string(args.machine_moves);
        sanity_check_moves(human_moves_gen, machine_moves_gen);
        generate_stringrep(args.human_moves, args.machine_moves);
        break;

    case MODE_TURN:
        if (args.who_moves == NULL || args.string_rep == NULL) {
            fprintf(stderr, "Error: Turn mode requires who moves and board string representation.\n");
            exit(EXIT_FAILURE);
        }
        if (!validate_player_argument(args.who_moves)) {
            exit(EXIT_FAILURE);
        }
        if (!validate_board_string(args.string_rep)) {
            exit(EXIT_FAILURE);
        }
        int human_moves_turn = count_moves_from_board(args.string_rep, TTTT_HUMAN_MARKER);
        int machine_moves_turn = count_moves_from_board(args.string_rep, TTTT_MACHINE_MARKER);
        sanity_check_moves(human_moves_turn, machine_moves_turn);
        turn_mode(args.who_moves, args.string_rep);
        break;

    case MODE_HELP:
        print_usage();
        break;

    case MODE_VERSION:
        printf("tttt version %s\n", TTTT_VERSION);
        break;

    case MODE_NONE:
        print_usage();
        break;

    default:
        break;
    }
    return 0;
}
