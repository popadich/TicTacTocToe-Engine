/*
 *  TTTTapi.h
 *  TTTTengine
 *
 *  Created by Alex Popadich on 4/5/10.
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


#include <unistd.h>
#include <getopt.h>
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include "TTTTapi.h"

// some local scoped globals
bool quiteflag = false;
bool verboseflag = false;
bool setweightsflag = false;
TTTT_WeightsTable new_weights;

void print_stringrep(char *theBoard)
{
    int	i=0;
    for(i=0; i<64; i++)
    {
        printf("%c",theBoard[i]);
    }
    printf("\n");
}

void print_board_stringrep(char *theBoard)
{
    int	i;
    if (quiteflag) {
        return;
    }
    for(i=0; i<4; i++)
    {
        printf("%c ",theBoard[i*16 + 0]);
        printf("%c ",theBoard[i*16 + 1]);
        printf("%c ",theBoard[i*16 + 2]);
        printf("%c \n",theBoard[i*16 + 3]);

        printf("%c ",theBoard[i*16 + 4]);
        printf("%c ",theBoard[i*16 + 5]);
        printf("%c ",theBoard[i*16 + 6]);
        printf("%c \n",theBoard[i*16 + 7]);

        printf("%c ",theBoard[i*16 + 8]);
        printf("%c ",theBoard[i*16 + 9]);
        printf("%c ",theBoard[i*16 + 10]);
        printf("%c \n",theBoard[i*16 + 11]);

        printf("%c ",theBoard[i*16 + 12]);
        printf("%c ",theBoard[i*16 + 13]);
        printf("%c ",theBoard[i*16 + 14]);
        printf("%c \n\n",theBoard[i*16 + 15]);

    }
    printf("\n");
}

void print_board(bool game_over)
{
    TTTT_GameBoardStringRep		pszGameBoard;
    if (game_over) {
        TTTT_GetWinnerStringRep(pszGameBoard);
    } else {
        TTTT_GetBoard(pszGameBoard);
    }
    print_board_stringrep(pszGameBoard);
}

void set_weightsmatrix(const char* weightsmatrix)
{
    int scanError;
    int r1c1, r1c2, r1c3, r1c4, r1c5;
    int r2c1, r2c2, r2c3, r2c4, r2c5;
    int r3c1, r3c2, r3c3, r3c4, r3c5;
    int r4c1, r4c2, r4c3, r4c4, r4c5;
    int r5c1, r5c2, r5c3, r5c4, r5c5;
    
    
    scanError = sscanf ( weightsmatrix, "%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d",
                        &r1c1, &r1c2, &r1c3, &r1c4, &r1c5 ,
                        &r2c1, &r2c2, &r2c3, &r2c4, &r2c5 ,
                        &r3c1, &r3c2, &r3c3, &r3c4, &r3c5 ,
                        &r4c1, &r4c2, &r4c3, &r4c4, &r4c5 ,
                        &r5c1, &r5c2, &r5c3, &r5c4, &r5c5
                        );
    if (scanError != 25) {
        printf("Problem with weights!\n");
        printf("Matrix is: %d %d %d %d %d for first few numbers\n",
               r1c1,
               r1c2,
               r1c3,
               r1c4,
               r1c5);
        printf("Matrix is: %d %d %d %d %d for second few numbers\n",
               r2c1,
               r2c2,
               r2c3,
               r2c4,
               r2c5);
        printf("Matrix is: %d %d %d %d %d for third few numbers\n",
               r3c1,
               r3c2,
               r3c3,
               r3c4,
               r3c5);
        printf("Matrix is: %d %d %d %d %d for fourth few numbers\n",
               r4c1,
               r4c2,
               r4c3,
               r4c4,
               r4c5);
        printf("Matrix is: %d %d %d %d %d for fourth few numbers\n",
               r5c1,
               r5c2,
               r5c3,
               r5c4,
               r5c5);
    }
    
    if (verboseflag) printf("Matrix is: %d %d %d %d %d for first few numbers\n",
                            r1c1,
                            r1c2,
                            r1c3,
                            r1c4,
                            r1c5);
    if (verboseflag) printf("Matrix is: %d %d %d %d %d for second few numbers\n",
                            r2c1,
                            r2c2,
                            r2c3,
                            r2c4,
                            r2c5);
    if (verboseflag) printf("Matrix is: %d %d %d %d %d for third few numbers\n",
                            r3c1,
                            r3c2,
                            r3c3,
                            r3c4,
                            r3c5);
    if (verboseflag) printf("Matrix is: %d %d %d %d %d for fourth few numbers\n",
                            r4c1,
                            r4c2,
                            r4c3,
                            r4c4,
                            r4c5);
    if (verboseflag) printf("Matrix is: %d %d %d %d %d for fifth few numbers\n",
                            r5c1,
                            r5c2,
                            r5c3,
                            r5c4,
                            r5c5);
    
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


long evaluate_stringrep(const TTTT_GameBoardStringRep pszGameBoard)
{
    long		value = 0;

    TTTT_Initialize();
    if (setweightsflag) {
        TTTT_SetHeuristicWeights(new_weights);
    }

    printf("Board StringRep is: %s\n\n", pszGameBoard);
    if (TTTT_EvaluateBoardValue(pszGameBoard, &value) == kTTTT_NoError)
        return value;
    return 0;
}

void generate_stringrep(const char *human_moves, const char *machine_moves)
{
    TTTT_GameBoardStringRep pszGameBoard;

    TTTT_Initialize();
    TTTT_GetBoard(pszGameBoard);
    TTTT_StringRep(human_moves, machine_moves,  pszGameBoard);

    print_stringrep(pszGameBoard);
}


void generative_mode(TTTT_GameBoardStringRep pszGameBoard, char *human_moves)
{
    int			scanError;
    // Game vars
    TTTT_Return	aWinner;
    long		theWinner;
    bool		game_over = false;
    int			aMove = -1;


    while( !game_over )
    {
        TTTT_GetBoard(pszGameBoard);

        print_board_stringrep(pszGameBoard);
        print_stringrep(pszGameBoard);

        do
        {
            printf("\n\nPlease enter move (1-64), or a [0] to quit!\n");
            scanError = scanf ("%d",&aMove);

        } while (scanError != 1);

        if (aMove>0 && aMove <=64)
        {
            printf("\nyour move is:  %d\n", aMove);
            if (TTTT_HumanMove(aMove)==kTTTT_NoError)
            {
                aWinner = TTTT_GetWinner(&theWinner);
                if (aWinner == kTTTT_NOBODY)
                {
                    aWinner = TTTT_GetWinner(&theWinner);
                }
                switch (aWinner)
                {
                    case kTTTT_MACHINETOSH:
                        printf("\nGame Over:  Mac Wins\n");
                        game_over = true;
                        break;

                    case kTTTT_HUMAN:
                        printf("\nGame Over:  You Win\n");
                        game_over = true;
                        break;

                    case kTTTT_NOBODY:
                        break;

                }
            }

        }
        else
        {
            game_over = true;
            printf("Quitting...\n");
        }
        // gets(inbuf);	
    }
}


bool announce_winner(TTTT_Return aWinner)
{
    bool	game_over;

    switch (aWinner)
    {
        case kTTTT_MACHINETOSH:
            printf("\nGame Over:  Mac Wins\n");
            game_over = true;
            break;

        case kTTTT_HUMAN:
            printf("\nGame Over:  You Win\n");
            game_over = true;
            break;

        case kTTTT_NOBODY:
            game_over = false;
            break;

    }
    return game_over;
}



void interactive_mode(void)
{
    int							scan_error;
    // Game vars
    long						possibleWinner;
    long						aMove;
    bool						is_game_over = false;

    TTTT_Initialize();
    print_board(is_game_over);


    while( !is_game_over )
    {
        // human moves
        if ( !is_game_over ) {

            printf("\n\nEnter move (1-64), or any other char to quit.\n");
            scan_error = scanf ("%ld",&aMove);
            if (scan_error != 1) {
                is_game_over = true;
                aMove = -1;
            }

            if (aMove>0 && aMove<=64)
            {
                printf("\nyour move is:  %ld\n", aMove);
                if ( TTTT_HumanMove(aMove-1) == kTTTT_NoError )
                {
                    TTTT_GetWinner(&possibleWinner);
                    is_game_over = announce_winner(possibleWinner);

                }			
                // display board
                print_board(is_game_over);
            }
            else
            {
                is_game_over = true;
                printf("Quitting...\n");
            }
        }


        // machine moves
        if ( !is_game_over )
        {
            TTTT_MacMove(&aMove);
            printf("\ncomputer move is:  %ld\n", aMove+1);
            TTTT_GetWinner(&possibleWinner);
            is_game_over = announce_winner(possibleWinner);

            // display board
            print_board(is_game_over);
        }
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

int main(int argc, char* argv[])
{
    int genflag = 0;
    int evalflag = 0;
    int gameflag = 0;
    const char *mvalue = NULL;
    const char *hvalue = NULL;
    const char *stringrep = NULL;
    int index;
    int c;


    opterr = 0;

    while ((c = getopt (argc, argv, ":pge:m:h:")) != -1)
    {
        switch (c)
        {
            case 'e':
                evalflag= 1;
                stringrep = optarg;
                break;
            case 'g':
                genflag= 1;
                break;
            case 'p':
                gameflag = 1;
                break;
            case 'm':
                mvalue = optarg;
                break;
            case 'h':
                hvalue = optarg;
                break;
            case ':':
                printf("Option '-%c' needs a value\n", optopt);
                break;
            case '?':
                if (isprint (optopt))
                    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
                else
                    fprintf (stderr,
                             "Unknown option character `\\x%x'.\n",
                             optopt);
                return 1;
            default:
                abort ();
        }

    }	
	
    printf ("evalflag = %d, genflag = %d, gameflag = %d, mvalue = %s, hvalue = %s\n",
            evalflag,
            genflag,
            gameflag,
            mvalue,
            hvalue);

    for (index = optind; index < argc; index++)
        printf ("Non-option argument %s\n\n\n", argv[index]);


    if (gameflag) {
        interactive_mode();
    }
    else if (genflag) {
        if (hvalue == NULL) {
            printf("Human moves must be specified with '-h' option.\n");
            return 1;
        }
        if (mvalue == NULL) {
            printf("Machine moves must be specified with '-m' option.\n");
            return 1;
        }
        generate_stringrep( hvalue, mvalue );
    }
    else if (evalflag) {
        long myBoardValue = evaluate_stringrep(stringrep);
        printf("Board Value is: %ld\n\n", myBoardValue);
    }
    return 0;
}
