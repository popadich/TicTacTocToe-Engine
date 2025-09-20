/*
 *  TTTT.c
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
#include <stdlib.h>    // for random
#include "TTTT.h"

struct stack_structure{
    xs_played_move stack_array[64];
    xs_stackptr stack_pointer;
};

// LOCALS
xs_player the_winner_is;
xs_gameboard the_board;
xs_winpath the_winpath;
xs_pathcount the_path_counts_mac;
xs_pathcount the_path_counts_human;
xs_weighttab the_weights;
bool randomized = false;
struct stack_structure firstpass_stack;
struct stack_structure bestmoves_stack;
struct stack_structure *st;
struct stack_structure *bm;

// the lower the score the better it is for the machine.
xs_weighttab default_weights =
{
{0,-2,-4,-8,-16},
{2,0,0,0,0},
{4,0,1,0,0},
{8,0,0,0,0},
{16,0,0,0,0},
};

// the winning paths table is all 1 based at this time
xs_winstable        the_wins_path_ids_table =
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

#pragma mark  MOVE STACK

void push_into_movestack(struct stack_structure *s, xs_played_move playedMove){
    s->stack_pointer++;
    s->stack_array[s->stack_pointer] = playedMove;
}

bool pop_from_movestack(struct stack_structure *s, xs_played_move *no){
    if (s->stack_pointer >= 0) {
        *no = s->stack_array[s->stack_pointer];
        s->stack_pointer--;
        return true;
    }
    return false;
}

void clear_movestack(struct stack_structure *s){
    s->stack_pointer = -1;
}

xs_stackptr size_movestack(struct stack_structure *s){
    return (s->stack_pointer) + 1;
}

#pragma mark  -
#pragma mark LOCAL FUNCTIONS

void setwinpath(xs_stackptr pathwinner)
{
    xs_move i;
    xs_move k;
    xs_move tally = 0;
    
    for (i = 0; i < TTTT_BOARD_POSITIONS; i++) {
        for (k = 0; k < 7; k++) {
            if (pathwinner == the_wins_path_ids_table[i][k] ) {
                the_winpath[tally++] = i; // global array only good when there is a winner.
            }
        }
    }
}

// check by tallying the counts arrays
xs_player checkforwinners(void)
{
    xs_player aWinner = kXS_NOBODY_PLAYER;
    xs_stackptr j;

    boardeval(the_board); // this will populate the win path arrays

    for (j = 0; j < TTTT_WINNING_PATHS_COUNT; j++)
    {
        if (the_path_counts_mac[j] == TTTT_WIN_SIZE)
        {
            aWinner = kXS_MACHINE_PLAYER;
            setwinpath(j);
        }
        if (the_path_counts_human[j] == TTTT_WIN_SIZE)
        {
            aWinner = kXS_HUMAN_PLAYER;
            setwinpath(j);
        }
    }
    return aWinner;
}

// Blank out Count arrays which are 1's based
void clearpathcounts(void)
{
    xs_stackptr i;

    for (i = 0; i < TTTT_WINNING_PATHS_COUNT; i++ ) {
        the_path_counts_human[i] = 0;
        the_path_counts_mac[i] = 0;
    }
}

void clearwinpath(void)
{
    xs_stackptr i;

    for (i = 0; i < TTTT_WIN_SIZE; i++ ) {
        the_winpath[i] = 0;
    }
}

#pragma mark -
#pragma mark PUBLIC

void initboard(void) {
    xs_move the_move;
    for (the_move = 0; the_move < TTTT_BOARD_POSITIONS; the_move++) {
        the_board[the_move] = kXS_NOBODY_PLAYER;
    }
}

void initweights(void) {
    xs_stackptr i, j;

    for (i = 0; i < TTTT_WEIGHT_MATRIX_SIZE; i++) {
        for (j = 0; j < TTTT_WEIGHT_MATRIX_SIZE; j++) {
            the_weights[i][j] = default_weights[i][j];
        }
    }
}

void initialize(void) {
    the_winner_is = kXS_NOBODY_PLAYER;
    initboard();
    initweights();
    clearpathcounts();
    clearwinpath();
    st = &firstpass_stack;
    clear_movestack(st);
    bm = &bestmoves_stack;
    clear_movestack(bm);
}

// Gets a pointer to the board array, and fills a string representation of the board in a string.
// This should be split into two different functions.
xs_gameboard* getboard(char *pszBoard)
{
    xs_move the_move;

    for(the_move = 0; the_move < TTTT_BOARD_POSITIONS; the_move++)
    {
        if(the_board[the_move] == kXS_HUMAN_PLAYER)
            pszBoard[the_move] = 'X';
        else if(the_board[the_move] == kXS_MACHINE_PLAYER)
            pszBoard[the_move] = 'O';
        else if(the_board[the_move] == kXS_NOBODY_PLAYER)
            pszBoard[the_move] = '_';
    }
    pszBoard[TTTT_BOARD_POSITIONS] = '\0';

    return &the_board;
}

xs_player getwinner(void)
{
    return the_winner_is;
}

xs_winpath * getwinpath(void)
{
    return &the_winpath;
}

void setweights(xs_weighttab weights)
{
    xs_stackptr i, j;

    for (i = 0; i < TTTT_WEIGHT_MATRIX_SIZE; i++) {
        for (j = 0; j < TTTT_WEIGHT_MATRIX_SIZE; j++) {
            the_weights[i][j] = weights[i][j];
        }
    }
}

void setrandomize(bool randomize){
    randomized = randomize;
}

// this is currently 0 based
xs_move humanmove(xs_move aMove)
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

xs_move machinemoverote(void) {
    xs_move bestmove = kXS_UNDEFINED_MOVE;
    xs_move trymove = kXS_UNDEFINED_MOVE;
    long minscore;
    long boardvalue;

    if (the_winner_is == kXS_NOBODY_PLAYER) {
        minscore = TTTT_VERY_BIG_BOARDVALUE;
        for (trymove = 0; trymove < TTTT_BOARD_POSITIONS; trymove++) {
            if (the_board[trymove] == kXS_NOBODY_PLAYER) {
                boardvalue = futureboardscore(trymove, kXS_MACHINE_PLAYER);
                if (boardvalue < minscore) {
                    minscore = boardvalue;
                    bestmove = trymove;
                }
            }
        }

        the_board[bestmove] = kXS_MACHINE_PLAYER;
        the_winner_is = checkforwinners();
    }
    return bestmove;
}

xs_move undomove(xs_move aMove) {
    xs_move undomove = kXS_UNDEFINED_MOVE;

    if (the_board[aMove] != kXS_NOBODY_PLAYER) {
        the_board[aMove] = kXS_NOBODY_PLAYER;
        undomove = aMove;
    }

    return undomove;
}

xs_move machinemoverandomized(void) {
    xs_move bestmove = kXS_UNDEFINED_MOVE;
    xs_move trymove = kXS_UNDEFINED_MOVE;
    xs_played_move playedmove;
    long minscore;
    long boardvalue;

    if (the_winner_is == kXS_NOBODY_PLAYER) {
        minscore = TTTT_VERY_BIG_BOARDVALUE;
        for (trymove = 0; trymove < TTTT_BOARD_POSITIONS; trymove++) {
            if (the_board[trymove] == kXS_NOBODY_PLAYER) {
                boardvalue = futureboardscore(trymove, kXS_MACHINE_PLAYER);
                if (boardvalue <= minscore) {
                    minscore = boardvalue;
                    bestmove = trymove;
                    playedmove.theScore = boardvalue;
                    playedmove.theMove = trymove;
                    push_into_movestack(st, playedmove);
                }
            }
        }
        xs_played_move goodmove;
        xs_played_move evenmove;
        if (pop_from_movestack(st, &goodmove)) {
            push_into_movestack(bm, goodmove);
        }
        while (pop_from_movestack(st, &evenmove)) {
            if (evenmove.theScore == goodmove.theScore) {
                push_into_movestack(bm, evenmove);
            }
        }

        // this stack should always conatin at least one move
        // if the stack is empty it means big trouble
        // printf("size: %d\n", size_movestack(bm));
        xs_stackptr pickedmove = (arc4random() % size_movestack(bm)) + 1;
        // printf("random pick: %d\n",pickedmove);

        while (pop_from_movestack(bm, &goodmove) && pickedmove > 0) {
            bestmove = goodmove.theMove;
            pickedmove--;
        }
        //    printf("ERROR ERROR, This is a critical problem. No move can be
        //    chosen by machine");

        clear_movestack(bm);
        clear_movestack(st);
        the_board[bestmove] = kXS_MACHINE_PLAYER;
        the_winner_is = checkforwinners();
    }
    return bestmove;
}

xs_move machinemove(void) {
    xs_move themove;
    if (randomized) {
        themove = machinemoverandomized();
    } else {
        themove = machinemoverote();
    }
    return themove;
}

#pragma mark -
#pragma mark BOARD SCORING

// Move is 1 based
void count_human(xs_move aMove)
{
    xs_stackptr j;
    xs_stackptr win_path;

    for (j = 0; j < TTTT_PATHPARTICIPANT; j++)
    {
        win_path = the_wins_path_ids_table[aMove][j];
        if (win_path >= 0)
        {
            the_path_counts_human[win_path] = the_path_counts_human[win_path] + 1;
        }
    }
}

// Move is 0 based
void count_machine(xs_move aMove)
{
    xs_stackptr j;
    xs_stackptr win_path;

    for (j = 0; j < TTTT_PATHPARTICIPANT; j++)
    {
        win_path = the_wins_path_ids_table[aMove][j];
        if (win_path >= 0)
        {
            the_path_counts_mac[win_path] = the_path_counts_mac[win_path] + 1;
        }
    }
}

long boardeval(xs_gameboard aBoard) {
    xs_move pieceposition = kXS_UNDEFINED_MOVE;
    xs_stackptr i;
    long total_score = 0;

    clearpathcounts();

    for (pieceposition = 0; pieceposition < TTTT_BOARD_POSITIONS; pieceposition++) {
        if (aBoard[pieceposition] == kXS_MACHINE_PLAYER) {
            count_machine(pieceposition);
        }
        else if (aBoard[pieceposition] == kXS_HUMAN_PLAYER) {
            count_human(pieceposition);
        }
    }

    for (i = 0; i < TTTT_WINNING_PATHS_COUNT; i++)
    {
        long HumPieces = the_path_counts_human[i];
        long MacPieces = the_path_counts_mac[i];
        total_score = the_weights[HumPieces][MacPieces] + total_score;
    }
    //printf("Total score : %d\n",total_score);

    return total_score;
}

// This routine scores only the mac's moves it should be more general
// the move is 0 based
long futureboardscore(xs_move aMove, xs_player currentPlayer)
{
//    xs_move the_move;
    xs_gameboard dup_board_game;
    long sum = 0;

    // make a copy of the board
    TTTT_clone_board(dup_board_game, the_board);

    // add our move to the board
    dup_board_game[aMove] = kXS_MACHINE_PLAYER;

    sum = boardeval(dup_board_game);

    return sum;
}

// Allocate/copy a board for look-ahead operations
void TTTT_clone_board(xs_gameboard dest, const xs_gameboard src) {
    for (xs_move i = 0; i < TTTT_BOARD_POSITIONS; i++) {
        dest[i] = src[i];
    }
}

void setboard(xs_gameboard new_board) {
    TTTT_clone_board(the_board, new_board);
}

xs_move choosemove(xs_gameboard board, int player)
{
    xs_move bestMove = kXS_UNDEFINED_MOVE;
    long bestScore = (player == kXS_MACHINE_PLAYER) ? TTTT_VERY_BIG_BOARDVALUE : -TTTT_VERY_BIG_BOARDVALUE;

    for (xs_move i = 0; i < TTTT_BOARD_POSITIONS; i++) {
        if (board[i] == kXS_NOBODY_PLAYER) {
            board[i] = player;
            long score = boardeval(board);
            board[i] = kXS_NOBODY_PLAYER; // Undo the move

            if (player == kXS_MACHINE_PLAYER) {
                if (score < bestScore) {
                    bestScore = score;
                    bestMove = i;
                }
            } else { // kXS_HUMAN_PLAYER
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = i;
                }
            }
        }
    }
    return bestMove;
}
