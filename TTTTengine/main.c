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
#include "TTTTapi.h"

// some local scoped globals
bool quiteflag = false;
bool verboseflag = false;
bool setweightsflag = false;
TTTT_WeightsTable new_weights;

void print_stringrep(char *theBoard) {
    int i = 0;
    for (i = 0; i < 64; i++) {
        printf("%c ", theBoard[i]);
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

void set_weightsmatrix(const char *weightsmatrix) {
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
        printf("Problem with weights!\n");
        printf("Matrix is: %d %d %d %d %d for first few numbers\n", r1c1, r1c2,
               r1c3, r1c4, r1c5);
        printf("Matrix is: %d %d %d %d %d for second few numbers\n", r2c1, r2c2,
               r2c3, r2c4, r2c5);
        printf("Matrix is: %d %d %d %d %d for third few numbers\n", r3c1, r3c2,
               r3c3, r3c4, r3c5);
        printf("Matrix is: %d %d %d %d %d for fourth few numbers\n", r4c1, r4c2,
               r4c3, r4c4, r4c5);
        printf("Matrix is: %d %d %d %d %d for fourth few numbers\n", r5c1, r5c2,
               r5c3, r5c4, r5c5);
    }

    if (verboseflag)
        printf("Matrix is: %d %d %d %d %d for first few numbers\n", r1c1, r1c2,
               r1c3, r1c4, r1c5);
    if (verboseflag)
        printf("Matrix is: %d %d %d %d %d for second few numbers\n", r2c1, r2c2,
               r2c3, r2c4, r2c5);
    if (verboseflag)
        printf("Matrix is: %d %d %d %d %d for third few numbers\n", r3c1, r3c2,
               r3c3, r3c4, r3c5);
    if (verboseflag)
        printf("Matrix is: %d %d %d %d %d for fourth few numbers\n", r4c1, r4c2,
               r4c3, r4c4, r4c5);
    if (verboseflag)
        printf("Matrix is: %d %d %d %d %d for fifth few numbers\n", r5c1, r5c2,
               r5c3, r5c4, r5c5);

    new_weights[0][0] = r1c1;
    new_weights[0][1] = r1c2;
    new_weights[0][2] = r1c3;
    new_weights[0][3] = r1c4;
    new_weights[0][4] = r1c5;

    new_weights[1][0] = r2c1;
    new_weights[1][1] = r2c2;
    new_weights[1][2] = r2c3;
    new_weights[1][3] = r2c4;
    new_weights[1][4] = r3c5;

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
        game_over = false;
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

void print_usage(void) {
    fprintf(stderr, "Usage:  \n");
    fprintf(stderr, "  Evaluate: tttt -e <stringrep>\n");
    fprintf(stderr, "  Generate: tttt -g <-h \"list\"> <-m \"list\">\n");
    fprintf(stderr,
            "  Play:     tttt -p <\"h\"|\"m\"> [-vq] [-w weights_matrix] \n");

    fprintf(stderr, "Examples: \n");
    fprintf(stderr, "  Play:     tttt -p \"h\" -w \"0 -2 -5 -11 -27 2 0 3 12 0 "
                    "5 -3 1 0 0 11 -12 0 0 0 23 0 0 0 0\" \n");
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
    int genflag = 0;
    int evalflag = 0;
    int playflag = 0;
    const char *whovalue = NULL;
    const char *mvalue = NULL;
    const char *hvalue = NULL;
    const char *weightsmatrix = NULL;
    const char *stringrep = NULL;
    int index;
    int c;
    opterr = 0;

    while ((c = getopt(argc, argv, "gvqp:w:e:m:h:")) != -1) {
        switch (c) {
            case 'e':
                evalflag = 1;
                stringrep = optarg;
                break;
            case 'g':
                genflag = 1;
                break;
            case 'v':
                verboseflag = true;
                break;
            case 'q':
                quiteflag = true;
                break;
            case 'p':
                playflag = 1;
                whovalue = optarg;
                break;
            case 'w':
                setweightsflag = true;
                weightsmatrix = optarg;
                set_weightsmatrix(weightsmatrix);
                break;
            case 'm':
                mvalue = optarg;
                break;
            case 'h':
                hvalue = optarg;
                break;
            case '?':
                if (optopt == 'p')
                    fprintf(stderr, "Option -%c requires an argument.\n", optopt);
                else if (optopt == 'w')
                    fprintf(stderr, "Option -%c requires an argument.\n", optopt);
                else if (optopt == 'e')
                    fprintf(stderr, "Option -%c requires an argument.\n", optopt);
                else if (isprint(optopt)) {
                    fprintf(stderr, "Unknown option `-%c'.\n", optopt);
                    print_usage();
                } else
                    fprintf(stderr, "Unknown option character `\\x%x'.\n", optopt);
                return 1;
            default:
                abort();
        }
    }

    // get verbose here for debugging
    if (verboseflag)
        printf("evalflag = %d, genflag = %d, playflag = %d quiteflag = %d \n",
               evalflag, genflag, playflag, quiteflag);
    if (verboseflag)
        printf("whovalue = %s, weightsmatrix = %s, mvalue = %s, hvalue = %s\n",
               whovalue, weightsmatrix, mvalue, hvalue);
    if (verboseflag) {
        for (index = optind; index < argc; index++)
            printf("Non-option argument %s\n\n\n", argv[index]);
    }

    if (playflag) {
        interactive_mode(whovalue);
    } else if (genflag) {
        if (hvalue == NULL) {
            printf("Human moves must be specified with '-h' option.\n");
            return 1;
        }
        if (mvalue == NULL) {
            printf("Machine moves must be specified with '-m' option.\n");
            return 1;
        }
        generate_stringrep(hvalue, mvalue);
    } else if (evalflag) {
        long myBoardValue = evaluate_stringrep(stringrep);
        printf("Board Value is: %ld\n\n", myBoardValue);
    }
    return 0;
}
