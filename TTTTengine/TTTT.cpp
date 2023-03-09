/*
 *  TTTT.cpp
 *  TTTTengine
 *
 *
 *  Purpose:    Engine for playing a 4x4x4 3D tic tac toe game.
 *
 *  Created by Alex Popadich on 4/5/10.
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

#include <stdio.h>
#include "TTTT.h"

// LOCALS 
xs_player		the_winner_is;
xs_gameboard	the_board;
xs_winpath		the_winpath;
//xs_move			the_winpath[TTTT_WIN_PATH_SIZE];
xs_pathcount	the_path_counts_mac;
xs_pathcount	the_path_counts_human;


// the lower the score the better it is for the machine. 
xs_weighttab		the_weights =
{
{0,-2,-4,-8,-16},		 
{2,0,0,0,0},
{4,0,1,0,0},
{8,0,0,0,0},
{16,0,0,0,0},
};

// the winning paths table is all 1 based at this time
xs_winstable		the_wins_path_ids_table = 
{
{0,4,8,40,56,60,64},
{0,5,-1,41,-1,-1,68},
{0,6,-1,42,-1,-1,69},
{0,7,9,43,57,61,65},
{1,4,-1,44,-1,-1,70},
{1,5,8,45,-1,-1,-1},
{1,6,9,46,-1,-1,-1},
{1,7,-1,47,-1,-1,72},
{2,4,-1,48,-1,-1,71},
{2,5,9,49,-1,-1,-1},
{2,6,8,50,-1,-1,-1},
{2,7,-1,51,-1,-1,73},
{3,4,9,52,58,62,66},
{3,5,-1,53,-1,-1,74},
{3,6,-1,54,-1,-1,75},
{3,7,8,55,59,63,67},
{10,14,18,40,-1,-1,-1},
{10,15,-1,41,56,-1,-1},
{10,16,-1,42,57,-1,-1},
{10,17,19,43,-1,-1,-1},
{11,14,-1,44,60,-1,-1},
{11,15,18,45,64,68,70},
{11,16,19,46,65,69,72},
{11,17,-1,47,61,-1,-1},
{12,14,-1,48,62,-1,-1},
{12,15,19,49,66,71,74},
{12,16,18,50,67,73,75},
{12,17,-1,51,63,-1,-1},
{13,14,19,52,-1,-1,-1},
{13,15,-1,53,58,-1,-1},
{13,16,-1,54,59,-1,-1},
{13,17,18,55,-1,-1,-1},
{20,24,28,40,-1,-1,-1},
{20,25,-1,41,57,-1,-1},
{20,26,-1,42,56,-1,-1},
{20,27,29,43,-1,-1,-1},
{21,24,-1,44,62,-1,-1},
{21,25,28,45,67,72,74},
{21,26,29,46,66,70,75},
{21,27,-1,47,63,-1,-1},
{22,24,-1,48,60,-1,-1},
{22,25,29,49,65,68,73},
{22,26,28,50,64,69,71},
{22,27,-1,51,61,-1,-1},
{23,24,29,52,-1,-1,-1},
{23,25,-1,53,59,-1,-1},
{23,26,-1,54,58,-1,-1},
{23,27,28,55,-1,-1,-1},
{30,34,38,40,57,62,67},
{30,35,-1,41,-1,-1,74},
{30,36,-1,42,-1,-1,75},
{30,37,39,43,56,63,66},
{31,34,-1,44,-1,-1,72},
{31,35,38,45,-1,-1,-1},
{31,36,39,46,-1,-1,-1},
{31,37,-1,47,-1,-1,70},
{32,34,-1,48,-1,-1,73},
{32,35,39,49,-1,-1,-1},
{32,36,38,50,-1,-1,-1},
{32,37,-1,51,-1,-1,71},
{33,34,39,52,59,60,65},
{33,35,-1,53,-1,-1,68},
{33,36,-1,54,-1,-1,69},
{33,37,38,55,58,61,64}
};



#pragma mark LOCAL FUNCTIONS
void setwinpath(int pathwinner)
{
	int	i;
	int k;
	
	int tally = 0;
	
	for (i=0; i<TTTT_BOARD_POSITIONS; i++) {
		for (k=0; k<7; k++) {
			if (pathwinner == the_wins_path_ids_table[i][k] ) {
				the_winpath[tally++] = i;							// global array only good when there is a winner.
			}			
		}
	}
}

// check by tallying the counts arrays 
xs_player checkforwinners(void)
{
	xs_player aWinner = kXS_NOBODY_PLAYER;
	int j;

	boardeval (the_board);		// this will populate the win path arrays
	
	for (j=0; j<TTTT_WINNING_POSITIONS_COUNT; j++)
	{			
		if (the_path_counts_mac[j] == TTTT_FOUR_IN_A_ROW)
		{
			aWinner = kXS_MACINTOSH_PLAYER;
			setwinpath(j);
		}
		if (the_path_counts_human[j] == TTTT_FOUR_IN_A_ROW)
		{
			aWinner = kXS_HUMAN_PLAYER;
			setwinpath(j);
		}
	}
	return aWinner;
}



// Blank out Count arrays which are 1's based
void clearpathcounts()
{
	int i;
	
	for (i=0; i<TTTT_WINNING_POSITIONS_COUNT; i++ )	{
		
		the_path_counts_human[i] = 0;	
		the_path_counts_mac[i] = 0;	
	}
}

void clearwinpath()
{
	int i;
	
	for (i=0; i<TTTT_WIN_PATH_SIZE; i++ )	{
		the_winpath[i] = 0;	
	}
}



#pragma mark -
#pragma mark PUBLIC

void initialize()
{
	initall();
}


void initall()
{
	the_winner_is = kXS_NOBODY_PLAYER;
	initboard();
	clearpathcounts();
	clearwinpath();
}

void initboard()
{
	xs_move the_move;
	for (the_move=0; the_move<TTTT_BOARD_POSITIONS; the_move++)	{
		the_board[the_move] = kXS_NOBODY_PLAYER;
	}
}


xs_gameboard* getboard(char *pszBoard)
{
	xs_move the_move;
	
	for(the_move=0; the_move<TTTT_BOARD_POSITIONS; the_move++)
	{
		if(the_board[the_move]==kXS_HUMAN_PLAYER)
			pszBoard[the_move]='X';
		else if(the_board[the_move]==kXS_MACINTOSH_PLAYER)
			pszBoard[the_move]='O';
		else if(the_board[the_move]==kXS_NOBODY_PLAYER)
			pszBoard[the_move]='_';
	}
	pszBoard[TTTT_BOARD_POSITIONS]='\0';
	
	return &the_board;
}


xs_player getwinner(void)
{
	return the_winner_is;
}

xs_move* getwinpath(void)
{
	return the_winpath;
}


// this is currently 0 based 
xs_move humanmove (xs_move aMove)
{
	xs_move move_made = kXS_UNDEFINED_MOVE;	

	if (the_board[aMove] == kXS_NOBODY_PLAYER && the_winner_is == kXS_NOBODY_PLAYER)
	{
		move_made = aMove;
		the_board[move_made] = kXS_HUMAN_PLAYER;
		the_winner_is = checkforwinners();
	}	
	return move_made;		
}



xs_move machinemove(void)
{
	xs_move bestmove = kXS_UNDEFINED_MOVE;
	xs_move trymove = kXS_UNDEFINED_MOVE;
	long minscore;
	long boardvalue;

	if ( the_winner_is == kXS_NOBODY_PLAYER)
	{
		minscore = TTTT_VERY_BIG_BOARDVALUE;
		for (trymove=0; trymove<TTTT_BOARD_POSITIONS; trymove++)
		{
			if (the_board[trymove] == kXS_NOBODY_PLAYER)
			{
				boardvalue = boardscore(trymove, kXS_MACINTOSH_PLAYER);
				if (boardvalue < minscore)
				{
					minscore = boardvalue;
					bestmove = trymove;
				}
			}
		}

		the_board[bestmove] = kXS_MACINTOSH_PLAYER;
		the_winner_is = checkforwinners();
	}
	return bestmove;
}

#pragma mark -
#pragma mark BOARD SCORING

// Move is 1 based 
void count_human (xs_move aMove)
{
	int j;
	int win_path;	
	
	for (j=0; j<TTTT_WINPATHSMAX; j++)
	{
		win_path = the_wins_path_ids_table[aMove][j];
		if (win_path >= 0)
		{
			the_path_counts_human[win_path] = the_path_counts_human[win_path] + 1;			
		}
	}
}

// Move is 0 based 
void count_machine (xs_move aMove)
{
	int	j;
	int win_path;
	
	for (j=0; j<TTTT_WINPATHSMAX; j++)
	{
		win_path = the_wins_path_ids_table[aMove][j];
		if (win_path >= 0)
		{
			the_path_counts_mac[win_path] = the_path_counts_mac[win_path] + 1;
		}
	}
}


long boardeval (xs_gameboard aBoard) {
	xs_move trymove = kXS_UNDEFINED_MOVE;
	int i;
	long total_score = 0;
	
		
	clearpathcounts();
	
	for (trymove=0; trymove<TTTT_BOARD_POSITIONS; trymove++) {
		if (aBoard[trymove] == kXS_MACINTOSH_PLAYER) {
			count_machine(trymove);
		}
		else if (aBoard[trymove] == kXS_HUMAN_PLAYER) {
			count_human(trymove);
		}
	}
	
	for (i=0; i<TTTT_WINNING_POSITIONS_COUNT; i++)
	{
		int HumPieces = the_path_counts_human[i];
		int MacPieces = the_path_counts_mac[i];
		total_score = the_weights[HumPieces][MacPieces] + total_score;
	}
	
	return total_score;
}


// This routine scores only the mac's moves it should be more general 
// the move is 0 based 
long boardscore(xs_move aMove, xs_player currentPlayer)
{
	xs_move			the_move;
	xs_gameboard	dup_board_game;
	long			sum = 0;
	
	// make a copy of the board
	for (the_move=0; the_move<TTTT_BOARD_POSITIONS; the_move++)
	{
		dup_board_game[the_move] = the_board[the_move];
	}
	// add our move to the board
	dup_board_game[aMove] = kXS_MACINTOSH_PLAYER;
	
	sum = boardeval(dup_board_game);
	
	return sum;
}








