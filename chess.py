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

board = [TOWER, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, TOWER,
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
            
            if board[(row+1)*8+col]==EMPTY:
                moves.append( (idx, (row+1)*8+col))
            if row==1 and board[3*8+col]==EMPTY:
                moves.append( (idx, 3*8+col))
            if col>0 and board[(row+1)*8+col-1] < EMPTY:
                moves.append( (idx, (row+1)*8+col-1))
            if col<8 and board[(row+1)*8+col+1] < EMPTY:
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
    return False

def make_move(board, move):
    
    from_, to_ = move
    print("%s from %s to %s" % (piece_name[abs(board[from_])],
                                from_, to_))
    piece = board[from_]
    board[from_] = EMPTY
    destiny = board[to_]
    board[to_] = piece
    
    if destiny != EMPTY:
        print("Taken: ", piece_name[abs(destiny)])
        
    return board
   
def print_board(board):

    print(" ",*list(range(8)), sep="\t")
    
    for row in range(8):
        
        print(row, *[piece_name[abs(board[idx])
                                ][0]+("" if board[idx]>=0 else "." )
                           for idx in range(row*8,row*8+8)],sep="\t")
     
    print(" ", *list(range(8)), sep="\t")
    print("-"*40)   
    
import random

if __name__ == "__main__":

    you = False
    
    while not game_over(board):
        
        print_board(board)
        
        if not you:
            moves = possible_moves(board)
            pick = random.choice(moves) 
            board = make_move(board, pick)
        else:
            move = input("Your move:")
            
    
        you = not you
        
    