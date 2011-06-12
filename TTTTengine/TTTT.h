/*
 *  TTTT.h
 *  TTTTengine
 *
 *
 *  Purpose:    Engine for playing a 4x4x4 3D tic tac toe game.
 *
 *  Created by Alex Popadich on 4/5/10.
 *  Copyright (c) 2010 Alex Popadich
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

#ifndef TTTT_H
#define TTTT_H

#include "TTTTcommon.h"


enum xs_player {
	kXS_NOBODY_PLAYER = 0,
	kXS_MACINTOSH_PLAYER,
	kXS_HUMAN_PLAYER
};

typedef enum xs_player xs_player;

typedef		 int xs_move;
static const xs_move kXS_UNDEFINED_MOVE = -1;


typedef int	xs_winstable[TTTT_BOARD_POSITIONS][TTTT_WINPATHSMAX];				// 0 based 0-63,0-6
typedef int xs_weighttab[TTTT_FOUR_IN_A_ROW+1][TTTT_FOUR_IN_A_ROW+1];			// 0 based 0-4 we need 5 ok


typedef xs_player	xs_gameboard[TTTT_BOARD_POSITIONS];							// 0 based 1-63
typedef int			xs_pathcount[TTTT_WINNING_POSITIONS_COUNT];					// 0 based 1-75 
typedef xs_move		xs_winpath[TTTT_WIN_PATH_SIZE];

//typedef xs_move *XSWinPath;



// P R O T O T Y P E S
void			initialize(void);
void			initall(void);
void			initboard(void);


void			count_human (xs_move aMove);
void			count_machine (xs_move aMove);
xs_move			humanmove (xs_move aMove);
xs_move			machinemove(void);
xs_gameboard* 	getboard(char *pszBoard);
xs_player		getwinner(void);
xs_move*		getwinpath(void);

long			boardscore(xs_move aMove, xs_player currentPlayer);
long			boardeval(xs_gameboard aBoard);

#endif
