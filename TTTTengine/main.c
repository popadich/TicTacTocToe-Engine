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


void print_stringrep(char *theBoard)
{
	int	i=0;
	
	for(i=0; i<64; i++)
	{
		printf("%c",theBoard[i]);		
	}
	
	printf("\n");
}

void print_board_string(char *theBoard)
{
	int	i;
	
	
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
	
}

void print_board(bool game_over)
{
	TTTT_GameBoardStringRep		pszGameBoard;
	if (game_over) {
		TTTT_GetWinnerStringRep(pszGameBoard);
	} else {
		TTTT_GetBoard(pszGameBoard);
	}
	print_board_string(pszGameBoard);
}

long evaluate_stringrep(const TTTT_GameBoardStringRep pszGameBoard)
{
	long		value = 0;
	
	
	TTTT_Initialize();
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
		
		print_board_string(pszGameBoard);
		print_stringrep(pszGameBoard);
		
		do
		{
			printf("\n\nEnter move (1-64), or any other char to quit!\n");
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


// play game
//     tttt -p
//
// evaluate board stringrep
//     tttt -e <stringrep>
//
// stringrep samples:
// ......X......................................................OOX
// X..X...........................................................O

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
	
	while ((c = getopt (argc, argv, "pge:m:h:")) != -1)
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
			case '?':
				if (isprint (optopt))
					fprintf (stderr, "Unknown option `-%c'.\n", optopt);
				else
					fprintf (stderr, "Unknown option character `\\x%x'.\n", optopt);
				return 1;
			default:
				abort ();
		}

	}	
	
	printf ("evalflag = %d, genflag = %d, gameflag = %d, mvalue = %s, hvalue = %s\n", evalflag, genflag, gameflag, mvalue, hvalue);
	
	for (index = optind; index < argc; index++)
		printf ("Non-option argument %s\n\n\n", argv[index]);

	
	if (gameflag) {
		interactive_mode();
	}
	else if (genflag) {
		generate_stringrep( hvalue, mvalue );
	}
	else if (evalflag) {
		long myBoardValue = evaluate_stringrep(stringrep);
		printf("Board Value is: %ld\n\n", myBoardValue);
	}
	return 0;
}
