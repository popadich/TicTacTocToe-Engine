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


#ifndef TTTTAPI_H
#define TTTTAPI_H

#include "TTTTcommon.h"

#define kTTTT_StringRepMaxBufferLength		256
#define export_dll


// Error codes for the TicTacTocToe API
enum
{
	kTTTT_NoError = 0,
	kTTTT_InvalidMove = -1,
	kTTTT_InvalidArgument = -2,
	kTTTT_InvalidArgumentOutOfRange = -3
};

enum
{
	kTTTT_NOBODY		= 0,
	kTTTT_MACHINETOSH	= 1,
	kTTTT_HUMAN			= 2
};

typedef long TTTT_Return;

static const TTTT_Return	kTTTT_False = 0;
static const TTTT_Return	kTTTT_True = 1;
static const int			kTTTT_Positions = TTTT_BOARD_POSITIONS;

typedef char TTTT_GameBoardStringRep[kTTTT_StringRepMaxBufferLength];
typedef int TTTT_WinnerMovesArr[TTTT_WIN_PATH_SIZE];
typedef int TTTT_WeightsTable[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE];        // 0 based 0-4 we need 5 ok


#ifdef __cplusplus 
extern "C"
{
#endif	
	// TTTT interfaces
	export_dll void 		TTTT_Initialize(void);
	export_dll TTTT_Return 	TTTT_GetBoard(TTTT_GameBoardStringRep pszGameBoard);
	export_dll TTTT_Return	TTTT_GetWinner(long *aWinner);
	export_dll TTTT_Return	TTTT_GetWinnerPath(TTTT_WinnerMovesArr aWinnerPath);
	export_dll TTTT_Return	TTTT_GetWinnerStringRep(TTTT_GameBoardStringRep pszGameBoard);
    export_dll TTTT_Return  TTTT_SetHeuristicWeights(int matrix[TTTT_WEIGHT_MATRIX_SIZE][TTTT_WEIGHT_MATRIX_SIZE]);
	export_dll TTTT_Return 	TTTT_HumanMove(long aMove);
	export_dll TTTT_Return 	TTTT_MacMove(long *aMove);
	export_dll TTTT_Return	TTTT_StringRep(const char *humanMoves, const char *machineMoves, TTTT_GameBoardStringRep pszGameBoard);
	export_dll TTTT_Return	TTTT_EvaluateBoardValue(const TTTT_GameBoardStringRep pszGameBoard, long *pValue);
	
	// More exotic data interfaces
/*	export_dll TTTT_Return XS_TTTT_GetPositionAtIndex(long handleToData, long nIndex, long *plDataPosition);
	export_dll TTTT_Return XS_TTTT_GetRequiredEdit(long handleToData, long nIndex, char pszRequirededit[kXS_MaxStringLength]);
*/
#ifdef __cplusplus
}
#endif

#endif
