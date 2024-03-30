#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:26:58 2024

@author: egon
"""
PAWN = 1
TOWER = 4
KNIGHT = 2
BISHOP = 3
QUEEN = 100
KING = 1000
EMPTY = 0 

piece_name = { PAWN : "pawn", TOWER : "tower",
               KNIGHT : "knight", BISHOP : "bishop", QUEEN : "queen",
               KING : "King", EMPTY : " "}

import random

def new_board():
    
    return [TOWER, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, TOWER,
         PAWN,  PAWN,   PAWN,   PAWN,  PAWN, PAWN,   PAWN,   PAWN,
         EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,  EMPTY,    EMPTY,
         EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,  EMPTY,    EMPTY,
         EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,  EMPTY,    EMPTY,
         EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,  EMPTY,    EMPTY,
         -PAWN, -PAWN, -PAWN, -PAWN, -PAWN, -PAWN,  -PAWN,   -PAWN,
         -TOWER,-KNIGHT,-BISHOP,-QUEEN,-KING,-BISHOP,-KNIGHT, -TOWER]

def possible_moves(board):
    
    moves = []
    
    for idx in range(64):
        
        if (piece := board[idx]) <= EMPTY: continue
    
        row = idx // 8 
        col = idx % 8
        
        #print(idx, row, col, piece)
        
        if piece==PAWN:
            
            if row<7 and board[(row+1)*8+col]==EMPTY:
                moves.append( (idx, (row+1)*8+col))
            if row==1 and board[3*8+col]==EMPTY:
                moves.append( (idx, 3*8+col))
            if row<7 and col>0 and board[(row+1)*8+col-1] < EMPTY:
                moves.append( (idx, (row+1)*8+col-1))
            if row<7 and col<7 and board[(row+1)*8+col+1] < EMPTY:
                moves.append( (idx, (row+1)*8+col+1))
            continue
        
        if piece==KNIGHT:
            
            for _row, _col in  [ (row+2, col-1), (row+2,col+1),
                          (row-2, col-1), (row-2, col+1),
                          (row+1, col+2), (row+1, col-2),
                          (row-1, col+2), (row-1, col-2)]:
                
                if _row<0 or _row>7 or _col<0 or _col>7: continue
            
                if board[_row*8+_col]<= EMPTY: 
                    moves.append( (idx, _row*8+_col))
            continue
        
        if piece==KING:
            
            for _row, _col in [ (row,col-1), (row,col+1), (row-1, col-1),
                               (row-1,col), (row-1, col+1), 
                               (row+1,col-1), (row+1,col), (row+1,col+1)]:
                
                if _row<0 or _row>7 or _col<0 or _col>7: continue
            
                if board[_row*8+_col]<= EMPTY:
                    moves.append( (idx, _row*8+_col))
                    
            continue
            
        if piece==BISHOP or piece==QUEEN:
            
            for incr, incc in [ (-1,-1), (-1,1), (1,-1), (1,1)]:
                
                newr = row + incr
                newc = col + incc 
                
                for r in range(8):
                
                    if newr<0 or newr>7 or newc<0 or newc>7:
                        break
                    
                    if board[newr*8+newc]>EMPTY:
                        break
                    
                    moves.append( (idx, newr*8+newc))
                    
                    if board[newr*8+newc]<EMPTY: 
      
                        break
                
                    newr, newc = newr+incr, newc+incc 
                    
        if piece==TOWER or piece==QUEEN:
            
            for incr, incc in [ (-1, 0), (1,0), (0,-1), (0,1)]:
                
                newr = row + incr
                newc = col + incc 
                
                for r in range(8):
                
                    if newr<0 or newr>7 or newc<0 or newc>7:
                        break
                    
                    if board[newr*8+newc]>EMPTY:
                        break
                    
                    moves.append( (idx, newr*8+newc))
                    
                    if board[newr*8+newc]<EMPTY: 
                        break
                
                    newr, newc = newr+incr, newc+incc 
            
           
    return moves

def game_over(board):
    return sum(abs(piece) for piece in board)< 2*KING

def make_move(board, move, offset=0):
    
    reward = 0
    from_, to_ = move
    # print("%s from %s to %s" % (piece_name[abs(board[from_])],
    #                             abs(offset-from_),
    #                             abs(offset-to_)))
    piece = board[from_]
    board[from_] = EMPTY
    destiny = board[to_]
    board[to_] = piece
    
    if destiny != EMPTY:
        reward = abs(destiny)
       # print("Taken: ", piece_name[reward])
    
    if piece==PAWN and (to_ // 8)==7: # pawn to queen
        #print("Pawn into queen")
        reward += 100
        board[to_] = QUEEN
     
    if reward != 0: 
        #print("Reward:", reward)
        pass
    
    return board, reward
   
def print_board(board):

    print(" ",*list(range(8)), sep="\t")
    
    for row in range(8):
        
        print(row, *[piece_name[abs(board[idx])
                                ][0]+("" if board[idx]>=0 else "." )
                           for idx in range(row*8,row*8+8)],sep="\t")
     
    print(" ", *list(range(8)), sep="\t")
    print("-"*40)   
    
    
def best_move(Q, board, moves, epslon):
    
    best = 0
    
    if epslon and random.random() < epslon:
        return random.choice(moves)
            
    for move in moves:
        
        state = tuple(board), move
        
        if state in Q:
            
            if Q[state]>best:
                best = Q[state]
                best_move = move
                
    if best>0:
        return best_move 
    
    return random.choice(moves)
        
def play(Q, board, epslon, gamma=0.9, teta=0.1):
    
    moves = possible_moves(board)
    pick = best_move(Q, board, moves, epslon) 
    _board, reward = make_move(board[:], pick)
    state = tuple(board), pick
   
    
    f_pick = best_move(Q, _board, possible_moves(_board), 0)
    _, future = make_move(_board[:], f_pick)
    
    if state in Q:
        Q[state] += gamma*(reward + future)-teta*Q[state]  
    else:
        Q[state] = reward + future
    return Q, _board
    
    
def play_a_game(Q, board, you, auto,
                   epslon=0.2, ep_step=0.001):
    
    steps = 0 
    while not game_over(board):
        
        #print_board(board)
        
        if you:
            
            if auto:
                Q, board = play(Q, board, epslon)            
            else:
                move = input("Your move:")
                _from,_to = move.split()
                make_move(board, ( int(_from), int(_to)))
                
        else: # reverse board, so we can use the same function play
            #move = input("Your move:")
            board = [piece*-1 for piece in board[::-1]] # rotate the board
            
            Q, board = play(Q, board, epslon)
            
            board = [piece*-1 for piece in board[::-1]] # rotate the board
            
        you = not you
        steps += 1
        if epslon>0: epslon -= ep_step

    return steps

        
def main(Q, max=200000, auto=True):
    
    you = True

    while True:
        
        board = new_board()
        steps = play_a_game(Q, board, you, auto)
        you = not you    
        print("*****", len(Q), steps)
        if len(Q)>max: break
        


if __name__ == "__main__":

    Q = {}
        
    main(Q)