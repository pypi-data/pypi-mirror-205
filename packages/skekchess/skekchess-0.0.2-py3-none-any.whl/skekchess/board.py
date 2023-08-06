from copy import deepcopy
import os
from PIL import Image, ImageDraw

import chessman
from enums import *

os.chdir(__file__+"/../")

# default_layout = """
# 8 | r n b q k b n r
# 7 | p p p p p p p p
# 6 | . . . . . . . .
# 5 | . . . . . . . .
# 4 | . . . . . . . .
# 3 | . . . . . . . .
# 2 | P P P P P P P P
# 1 | R N B Q K B N R
#     ― ― ― ― ― ― ― ―
#     A B C D E F G H
# """

default_layout = {
    0: [chessman.Rook(Colour.white),chessman.Knight(Colour.white),chessman.Bishop(Colour.white),chessman.Queen(Colour.white),
        chessman.King(Colour.white),chessman.Bishop(Colour.white),chessman.Knight(Colour.white),chessman.Rook(Colour.white)],
    1: [chessman.Pawn(Colour.white) for _ in range(0,8)],
    6: [chessman.Pawn(Colour.black) for _ in range(0,8)],
    7: [chessman.Rook(Colour.black),chessman.Knight(Colour.black),chessman.Bishop(Colour.black),chessman.Queen(Colour.black),
        chessman.King(Colour.black),chessman.Bishop(Colour.black),chessman.Knight(Colour.black),chessman.Rook(Colour.black)],
}

# __all__ = (
#     "Square",
#     "Board",
# )

class Square:
    """Represents a Square on a Board.

    Properties
    -----------
    chessman: :class:`Chessman`
        A chessman instance to place on this Square. Can be None.

    position: :class:`List[int]`
        The position of this Square.

    Methods
    -----------
    distance(position :class:`List[int]`):
        Returns the integer diagonal distance between two squares.
    """

    def __init__(self,position:list[int],chessman:chessman.Chessman=None):
        self.position = position
        self.chessman = chessman
        self.colour = Colour.black if (position[0]+position[1])%2 == 1 else Colour.white

    def __str__(self):
        self.chessman = getattr(self,"chessman","")
        return f"Position: {self.position[0]},{self.position[1]}\nChessman: {self.chessman}\nColour: {self.colour}"


    def distance(self,p:list[int]):
        "Returns the integer diagonal distance between two squares."
        p1 = self.position

        distX = abs(p[0]-p1[0])
        distY = abs(p[1]-p1[1])
        diagCut = min(distX,distY)

        return distX + distY - diagCut
    
    def isatdiagonal(self,pos:list[int]):
        "Returns whether this square is at a diagonal to another square."
        sPos = self.position
        if abs(sPos[0] - pos[0]) == (sPos[1] - pos[1]):
            return True
        
class Board:
    """Represents a chess Board.
    """
    
    def __init__(self,ruleset=Rulesets.standard):
        
        squares = [[Square([j,i]) for i in range(0,8)] for j in range(0,8)] ##I love that this works, python is such a nice language
        pieces = [[],[]]
        for x,l in enumerate(squares,start=0):
            for y,square in enumerate(l,start=0):
                if y not in [0,1,6,7]:
                    continue
                Cman = deepcopy(default_layout[y][x])
                Cman.board = self
                Cman.square = square
                Cman.position = [x,y]
                pieces[1 if Cman.colour == Colour.white else 0].append(Cman)
                square.chessman = Cman

        self.pieces = pieces
        self.squares = squares
        self.incheck = False

    def to_text(self,unicode:bool):
        text = ""
        for x in reversed(self.squares):
            for square in x:
                Cman = square.chessman
                if Cman:
                    if Cman.colour == Colour.black:
                        text += " "+ (Cman.letter.lower() if not unicode else Cman.unicode[0])
                    else:
                        text += " "+ (Cman.letter.upper() if not unicode else Cman.unicode[1])
                else:
                    text += " ."
            text += "\n"
        return text
    

    def to_image(self):
        background = Image.open(__file__+"/../"+"Images/board.png").convert("RGBA")
        for x,l in enumerate(self.squares):
            for y,square in enumerate(l):
                if square.chessman:
                    img = Image.open(__file__+"/../"+"Images/"+str("b" if square.chessman.colour == Colour.black else "w")+str(square.chessman.letter)+".png").convert("RGBA")
                    background.paste(img,(x*150,1050-(y*150)),img)
        return background
    

letters_numbers = {
    "a":0,
    "b":1,
    "c":2,
    "d":3,
    "e":4,
    "f":5,
    "g":6,
    "h":7
}
    

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
    

def convert_coordinate(position:list[int,int]|str) -> list[int,int]|str:
    "Converts a coordinate to the alternative format."
    if type(position) == str:
        pass
    elif type(position) == list:
        return f"{baseN(position[0]+10,18)}{position[1]+1}"
    

def convert_move(move:str|tuple[str,list[int,int],list[int,int]],newFormat:MoveNotation) -> str:
    """Converts a move to another notation.
    To convert to Long Algebraic, move must be a tuple of the Chessman's letter, the Chessman's starting position and the destination.
    """
    if type(move) == tuple and len(move) == 3:
        if newFormat == MoveNotation.longalgebraic:
            _,start,dest = move
            return convert_coordinate(start)+convert_coordinate(dest)
    elif type(move) == str and len(move) == 2:
        if newFormat == MoveNotation.internal:
            return [letters_numbers[move[0]],int(move[1])-1]
