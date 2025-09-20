/*
 *  TTTTapi.cpp
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

#include "TTTTapi.h"
#include "TTTT.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// Implements TTTT_MakeStringRep
// whoMoves: which player (kTTTT_HUMAN or kTTTT_MACHINE)
// aMove: move index (0-based)
// pszOldRep: input board string representation (length >= TTTT_BOARD_POSITIONS)
// pszNewRep: output board string representation (buffer must be large enough)
TTTT_Return TTTT_MakeStringRep(const int whoMoves, const long aMove, const TTTT_GameBoardStringRep pszOldRep, TTTT_GameBoardStringRep pszNewRep)
{
	// Validate arguments
	if (!pszOldRep || !pszNewRep) {
		return kTTTT_InvalidArgument;
	}
	if (aMove < 0 || aMove >= kTTTT_Positions) {
		return kTTTT_InvalidArgumentOutOfRange;
	}

	// Copy old rep to new rep
	size_t len = strlen(pszOldRep);
	// Defensive: ensure we copy at least kTTTT_Positions chars, but not more than buffer
	size_t copylen = (len > kTTTT_Positions) ? kTTTT_Positions : len;
	memcpy(pszNewRep, pszOldRep, copylen);
	// If pszOldRep is shorter, fill the rest with '_'
	for (size_t i = copylen; i < kTTTT_Positions; ++i) {
		pszNewRep[i] = '.';
	}
	pszNewRep[kTTTT_Positions] = '\0';

	// Set the move for the player
	char mark = '.';
	if (whoMoves == kTTTT_HUMAN) {
		mark = 'X';
	} else if (whoMoves == kTTTT_MACHINE) {
		mark = 'O';
	} else {
		return kTTTT_InvalidArgument;
	}

	// Only allow move if position is empty
	if (pszNewRep[aMove] != '.') {
		return kTTTT_InvalidMove;
	}
	pszNewRep[aMove] = mark;

	return kTTTT_NoError;
}

//const char                     *const kDateTimeFormat = "%m/%d/%y %I:%M%p";


// Our Exported Function Wrappers

void TTTT_Initialize(void)
{
	initialize();
}


// Getting properties

TTTT_Return TTTT_GetBoard(TTTT_GameBoardStringRep pszGameBoard) {
    xs_gameboard *gameBoard;
    TTTT_GameBoardStringRep qszBoard;
    long i;

    qszBoard[0] = '\0';
    gameBoard = getboard(qszBoard);

    char *charPointer = (char *)gameBoard;

    for (i = 0; i < TTTT_BOARD_POSITIONS; i++) {
        // printf("gameboard[%d] : %d\n",i, charPointer[i]);
        if (charPointer[i] < kXS_NOBODY_PLAYER ||
            charPointer[i] > kXS_HUMAN_PLAYER) {
            printf("error: gameboard[%ld] : %c", i, charPointer[i]);
            return kTTTT_InvalidMove;
        }
    }

    strncpy(pszGameBoard, qszBoard, kTTTT_StringRepMaxBufferLength);

    return kTTTT_NoError;
}

TTTT_Return TTTT_GetWinner(long *aWinner)
{
	long winner;
	
	winner = getwinner();
	*aWinner = winner;
	
	return kTTTT_NoError;
}

TTTT_Return TTTT_GetWinnerPath(TTTT_WinnerMovesArr aWinnerPath) {
    long i;
    xs_winpath *winpath;
    xs_move *winarray;

    winpath = getwinpath();
    winarray = *winpath;

    for (i = 0; i < TTTT_WIN_SIZE; i++) {
        aWinnerPath[i] = winarray[i];
    }

    return kTTTT_NoError;
}

TTTT_Return TTTT_GetWinnerStringRep(TTTT_GameBoardStringRep pszGameBoard) {
    long i;
    long aSpace;
    xs_winpath *winpath;
    xs_move *winarray;

    if (getwinner()) {

        winpath = getwinpath();
        winarray = *winpath;

        TTTT_GetBoard(pszGameBoard);
        for (i = 0; i < TTTT_WIN_SIZE; i++) {
            aSpace = winarray[i];
            pszGameBoard[aSpace] = '*';
        }

        return kTTTT_NoError;
    }
    return kTTTT_NoError;
}

TTTT_Return TTTT_SetHeuristicWeights(long matrix[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE]) {
    setweights(matrix);
    return kTTTT_NoError;
}

TTTT_Return TTTT_SetRandomize(bool randomize) {
    setrandomize(randomize);
    return kTTTT_NoError;
}

TTTT_Return TTTT_UndoMove(long aMove)
{
    undomove(aMove);
    return kTTTT_NoError;
}

TTTT_Return TTTT_HumanMove(long aMove)
{
	 if (humanmove(aMove) == aMove)
	 	return kTTTT_NoError;
	
	return kTTTT_InvalidMove;
}



TTTT_Return TTTT_MacMove(long *aMove)
{
	long	theMove;
	
	theMove =  machinemove();
    //theMove = machinemoverandomized();
	*aMove = theMove;
	 
	return kTTTT_NoError;
}

// this is a convenience function and does not involve an actual game play it is just a representation conversion
TTTT_Return	TTTT_StringRep(const char *humanMoves, const char *machineMoves, TTTT_GameBoardStringRep pszGameBoard)
{
	long j;
	char *ptr, *buf;
	long tokens_count;

	long h_arr[32];
	long m_arr[32];

    long len = 0;
	
	if (pszGameBoard == NULL)
		return kTTTT_InvalidArgument;
	
	// Parse the moves and if there are errors report back
	len = strlen( humanMoves );
	if (len<1024) {
		buf = (char *)malloc(4096);
		strncpy(buf, humanMoves, len);
		buf[len]='\0';
		printf("\nhuman moves len: %ld \nmoves: %s\n", len, humanMoves);
		
		
		tokens_count=0;
		if( (ptr = strtok(buf, " ")) != NULL ) {
			h_arr[tokens_count] = strtol(ptr, NULL, 10);
			tokens_count++;
			while ( (ptr = strtok(NULL, " ")) != NULL ) {
				h_arr[tokens_count] = strtol(ptr, NULL, 10);
				tokens_count++;
			}
		}
		
		for (j=0; j<tokens_count; j++) {
			printf("h_arr is: %ld \n", h_arr[j]);
			pszGameBoard[h_arr[j]-1] = 'X';
		}
		if (buf) {
			free(buf);
			buf=NULL;
		}
	}
	
	len = strlen( machineMoves );
	if (len<1024) {
		buf = (char *)malloc(4096);
		strncpy(buf, machineMoves, len);
		buf[len]='\0';
		printf("\nmachine moves len: %ld \nmoves: %s\n", len, machineMoves);
		
		tokens_count=0;
		if( (ptr = strtok(buf, " ")) != NULL ) {
			m_arr[tokens_count] = strtol(ptr, NULL, 10);
			tokens_count++;
			while ( (ptr = strtok(NULL, " ")) != NULL ) {
				m_arr[tokens_count] = strtol(ptr, NULL, 10);
				tokens_count++;
			}
		}
		
		for (j=0; j<tokens_count; j++) {
			printf("m_arr is: %ld \n", m_arr[j]);
			pszGameBoard[m_arr[j]-1] = 'O';
		}
		
		if (buf) {
			free(buf);
			buf = NULL;
		}
	}
	
	return kTTTT_NoError;
}

TTTT_Return	TTTT_EvaluateBoardValue(const TTTT_GameBoardStringRep pszGameBoard, long *pValue)
{
	xs_gameboard aBoard;
	long i;
	long score;
	
	for (i=0; i<TTTT_BOARD_POSITIONS; i++) {
		if (pszGameBoard[i] == 'X') {
			aBoard[i] = kXS_HUMAN_PLAYER;
		}
		else if (pszGameBoard[i] == 'O') {
			aBoard[i] = kXS_MACHINE_PLAYER;
		}
		else {
			aBoard[i] = kXS_NOBODY_PLAYER;
		}

	}
	
	score = boardeval(aBoard);
	*pValue = score;
	return kTTTT_NoError;
}


TTTT_Return TTTT_SetBoard(const TTTT_GameBoardStringRep pszGameBoard)
{
    xs_gameboard aBoard;
    long i;

    for (i=0; i<TTTT_BOARD_POSITIONS; i++) {
        if (pszGameBoard[i] == 'X') {
            aBoard[i] = kXS_HUMAN_PLAYER;
        }
        else if (pszGameBoard[i] == 'O') {
            aBoard[i] = kXS_MACHINE_PLAYER;
        }
        else {
            aBoard[i] = kXS_NOBODY_PLAYER;
        }
    }
    setboard(aBoard);
    return kTTTT_NoError;
}

// Sets a zero based index for best location on the board
// to place a piece.
TTTT_Return TTTT_GetBestMove(int player, long *aMove)
{
    xs_gameboard *aBoard;
	TTTT_GameBoardStringRep pszGameBoard;
    long best_move_idx = -1;

    aBoard = getboard(pszGameBoard);
    best_move_idx = choosemove(*aBoard, player);
    *aMove = best_move_idx;
    return kTTTT_NoError;
}
