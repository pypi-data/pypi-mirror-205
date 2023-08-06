"""
Standards:

Internally, positions are a list, where index 0 is X and 1 is Y.
A-H are 1-8 respectively.
These are changed to algebraic notation when displayed to the user.
Example: [0,0]  = 'a1', [7,6]  = 'h7'

"""

##Either R-S, R-R, U-U, U-R, U-S
##R = random, S = stockfish, U = user
run = "U-U"

import os
import random

from stockfish import Stockfish
import board as boardM
from board import *
from chessman import *
from enums import *

os.chdir(__file__+"/../")

def main():
    board = Board()
    board.to_image().save("Boards/0.0.png")

    # stockfish = Stockfish(path="stockfish_15.1_win_x64_popcnt/stockfish-windows-2022-x86-64-modern.exe",depth=10,parameters={"Threads": 2,"Minimum Thinking Time":1,"Hash":2048})
    # stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 0")
    # for idx in range(1,100):
    #     bm = stockfish.get_best_move()

    #     st = convert_move(bm[:2],MoveNotation.internal)
    #     dt = convert_move(bm[2:],MoveNotation.internal)
    #     squares = board.squares
    #     piece:chessman.Chessman = squares[st[0]][st[1]].chessman
    #     try:
    #         piece.move(dt)
    #     except AttributeError:
    #         raise AttributeError(bm)

    #     stockfish.make_moves_from_current_position([bm])

    #     board.to_image(str(idx/2))

    def isValidMove(start:list[int,int],dest:list[int,int],board:Board,colour:Colour) -> bool:
        try:
            piece = board.squares[start[0]][start[1]].chessman
        except IndexError:
            return False
        if piece:
            if piece.colour == colour:
                if dest in piece.getavailablemoves():
                    return True

    if run == "U-U":
        idx = 0
        oppColour = Colour.black
        while True:
            idx += 1

            anyMoves = False
            for i in board.pieces[1 if ~oppColour == Colour.white else 0]:
                moves = i.getavailablemoves()
                if len(moves) > 0:
                    anyMoves = True
                    print(i.type)
                    convMoves = [boardM.convert_move((i.letter,i.position,mov),MoveNotation.longalgebraic) for mov in moves]
                    print(convMoves)
                    print()

            if not anyMoves:
                print("\n\n")
                if board.incheck:
                    print("Game ended by Checkmate!",f"{oppColour} wins.")
                    print("\n\n")
                    return GameResolution.victory,oppColour
                else:
                    print("Game ended by Stalemate!")
                    print("\n\n")
                    return GameResolution.draw,DrawCondition.stalemate

            move = input("Move: ")
            st = convert_move(move[:2],MoveNotation.internal)
            dt = convert_move(move[2:],MoveNotation.internal)
            if isValidMove(st,dt,board,~oppColour):
                oppColour = ~oppColour
                board.squares[st[0]][st[1]].chessman.move(dt)
                board.to_image().save(f"Boards/{str(idx)}.png")
                print(board.to_text(False))
            else:
                print("Invalid move!")

    if run == "R-R":
    
        for idx in range(1,100):
            pieces = []
            for i in board.squares:
                for j in i:
                    if getattr(j.chessman,"colour",None) == Colour.white and idx % 2 == 0:
                        pieces.append(j.chessman)
                    elif getattr(j.chessman,"colour",None) == Colour.black and idx % 2 == 1:
                        pieces.append(j.chessman)

            found = False
            for i in range(1,100):
                random.shuffle(pieces)
                piece = pieces[0]
                moves = piece.getavailablemoves()
                if len(moves) >= 1:
                    found = True
                    break
            
            if found:  
                random.shuffle(moves)
                piece.move(moves[0])
                #print(board.to_text(True))
                board.to_image().save(f"Boards/{str(idx/2)}.png")
            else:
                print("Failed to find a valid move, game aborted.")
                return -1

        print("Simulation finished!")

if __name__ == "__main__":
    main()
