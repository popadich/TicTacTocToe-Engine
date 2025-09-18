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
#include <stdbool.h>

typedef enum xs_player {
    kXS_NOBODY_PLAYER = 0,
    kXS_MACINTOSH_PLAYER,
    kXS_HUMAN_PLAYER
} xs_player;

typedef long xs_move;
static const xs_move kXS_UNDEFINED_MOVE = -1;

typedef long xs_stackptr;  // NEW: type for stack pointers and indices

typedef long xs_winstable[TTTT_BOARD_POSITIONS][TTTT_PATHPARTICIPANT];   // 0 based 0-63,0-6
typedef long xs_weighttab[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE];   // 0 based 0-4 we need 5 ok

typedef char        xs_gameboard[TTTT_BOARD_POSITIONS]; // 0 based 0-63 = 64 positions
typedef long            xs_pathcount[TTTT_WINNING_PATHS_COUNT]; // 0 based 0-75 = 76 winning paths
typedef xs_move        xs_winpath[TTTT_WIN_SIZE];

struct xs_played_move {
    xs_move theMove;
    long theScore;
};
typedef struct xs_played_move xs_played_move;

// P R O T O T Y P E S
void initialize(void);

void count_human(xs_move aMove);
void count_machine(xs_move aMove);
xs_move humanmove(xs_move aMove);
xs_move machinemove(void);
xs_move undomove(xs_move aMove);
xs_move machinemoverandomized(void);
xs_gameboard *getboard(char *pszBoard);
xs_player getwinner(void);
xs_winpath *getwinpath(void);
void setweights(xs_weighttab weights);
void setrandomize(bool randomize);
void setboard(xs_gameboard new_board);
long futureboardscore(xs_move aMove, xs_player currentPlayer);
long boardeval(xs_gameboard aBoard);

// Board copy utility for look-ahead
void TTTT_clone_board(xs_gameboard dest, const xs_gameboard src);

#endif
