from copy import deepcopy
import os

from enums import *
import board

os.chdir(__file__+"/../")
__all__ = (
    "Chessman",
)

class Chessman:
    """Base class for a Chessman (Piece, Pawn, King).
    Movement rules and traits defined in sub-classes.

    Properties
    -----------
    type: :class:`ChessmanType`
        What Chessman is this?
    colour: :class:`Colour`
        Who does this Chessman belong to?
    king: :class:`bool`
        Is this Chessman type a King (will lose if this Chessman is checkmated)?
    
    state: :class:`ChessmanState`
        Alive or Captured?
    position: :class:`List[int,int]`
        Where on the board is this Chessman?

    canmove: :class:`bool`
        Can this Chessman move, or is it blocked or pinned to the King?
    hasmoved: :class:`bool`
        Has this Chessman moved already? Used for castling rights and pawns.
    
    availablemovement: :class:`List[List[int,int]]`
        Where can this Chessman move to? 'a_castle' and 'h_castle' used to denote castling, respectively.
    controlledsquares: :class:`List[List[int,int]]
        Which squares is this Chessman controlling?

    availablepromotions: :class:`List[Chessman]`
        Who can this Chessman promote to? Empty until can promote, i.e. Pawn reaching final Rank.
    promotedfrom: :class:`List[Chessman]`
        Who was this Chessman before promoting?
    

    """

    king = False
    letter = "-"
    type = ChessmanType.none

    def checkforcheck(self,possibleMoves:list[list[int,int]]):
        "Returns a list of possible moves that would not put the King in check. Helper function for getavailablemoves()."
        b:board.Board = self.board

        if not self.king:
            kingPos = None
            for piece in b.pieces[1 if self.colour == Colour.white else 0]:
                if piece.type == ChessmanType.king:
                    kingPos = piece.position
                    break
        
        originalMoves = deepcopy(possibleMoves)
        for move in originalMoves:
            newBoard = deepcopy(b)
            curSquare = newBoard.squares[self.position[0]][self.position[1]]
            newChessman = curSquare.chessman
            if not newChessman:
                continue
            curSquare.chessman = None

            newSquare = newBoard.squares[move[0]][move[1]]
            del(newSquare.chessman)
            newChessman.square = newSquare
            newSquare.chessman = newChessman

            if self.king:
                kingPos = move
            
            for enemy in newBoard.pieces[1 if self.colour == Colour.black else 0]:
                enemy:Chessman
                if kingPos in enemy.getattackedpositions(b=newBoard,skipCheckCheck=True):
                    possibleMoves.remove(move)
                    break
            del(newBoard)

        return possibleMoves

    def getavailablemoves(self,b=None,skipCheckCheck=False) -> list[list[int,int]]:
        "Returns a list of available moves."
        return []
    
    def getattackedpositions(self,b=None,skipCheckCheck=False) -> list[list[int,int]]:
        "Returns positions that are being attacked by this Chessman. Identical to getavailablemoves for all pieces but not pawns."
        return self.getavailablemoves(b=b,skipCheckCheck=skipCheckCheck)
    
    def capture(self,square):
        "Capture a Chessman on a Square."
        square.chessman.state = ChessmanState.captured
        del(square.chessman)

    def move(self,pos:list[int]):
        "Move to a square, and capture if needed."
        self.hasmoved = True
        self.square.chessman = None
        newSquare = self.board.squares[pos[0]][pos[1]]
        if newSquare.chessman:
            self.capture(newSquare)
        newSquare.chessman = self
        self.square = newSquare
        self.position = pos

        kingPos = None
        for piece in self.board.pieces[1 if self.colour == Colour.black else 0]:
            if piece.king:
                kingPos = piece.position
                break

        for move in self.getavailablemoves(skipCheckCheck=True):
            if move == kingPos:
                self.board.incheck = True
                break
        else:
            self.board.incheck = False

    def __init__(self,colour:Colour,b=None,square=None,pos=[0,0]):
        self.board = b
        self.square = square
        self.colour = colour

        self.state = ChessmanState.alive
        self.position = pos

        self.incheck = False
        self.canmove = True
        self.hasmoved = False

        self.availablemovement = []
        self.controlledsquares = []

        self.availablepromotions = []
        self.promotedfrom = []


    def __str__(self):
        return f"Type: {self.type}\nColour: {self.colour}\nState: {self.state}\nPosition: {self.position}\nCanMove: {self.canmove}\nHasMoved: {self.hasmoved}\nAvailablePromotions: {str(self.availablepromotions)}\nPromotedFrom: {str(self.promotedfrom)}"

class Pawn(Chessman):
    "The Pawn."

    king = False
    type = ChessmanType.pawn

    letter = "p"
    unicode = ["♟︎","♙"]

    def getattackedpositions(self,b=None,skipCheckCheck=False) -> list[list[int]]:
        b:board.Board = b if b else self.board
        sq = b.squares

        pos = self.position
        col = self.colour

        yDir = 1 if col == Colour.white else -1
        moves = []
        try:
            Cman = sq[pos[0]+1][pos[1]+yDir].chessman
            if Cman != None and pos[0] < 7 and pos[1]+yDir <= 7 and pos[1]+yDir >= 0:
                if Cman.colour != col:
                    moves.append([pos[0]+1,pos[1]+yDir])
        except IndexError:
            pass
            ##Apparantely negative index underflows are fine but positive overflows are not. I retract my statement about python being a nice language

        try:
            Cman = sq[pos[0]-1][pos[1]+yDir].chessman
            if Cman != None and pos[0] > 0 and pos[1]+yDir <= 7 and pos[1]+yDir >= 0:
                if Cman.colour != col:
                    moves.append([pos[0]-1,pos[1]+yDir])
        except IndexError:
            pass

        if not skipCheckCheck:
            moves = self.checkforcheck(moves)

        return moves


    def getavailablemoves(self,b=None,skipCheckCheck=False) -> list[list[int]]:
        ## Fake boards are used to determine check or not
        b:board.Board = b if b else self.board
        sq = b.squares

        pos = self.position
        mov = self.hasmoved
        col = self.colour

        moves = self.getattackedpositions(b=b,skipCheckCheck=skipCheckCheck)

        yDir = 1 if col == Colour.white else -1
        forwardBlocked = False
        try:
            if sq[pos[0]][pos[1]+yDir].chessman == None and pos[1]+yDir <= 7 and pos[1]+yDir >= 0:
                moves.append([pos[0],pos[1]+yDir])
            else:
                forwardBlocked = True
        except IndexError:
            pass

        if not mov and not forwardBlocked:
            try:
                if sq[pos[0]][pos[1]+(yDir*2)].chessman == None and pos[1]+(yDir*2) <= 7 and pos[1]+(yDir*2) >= 0:
                    moves.append([pos[0],pos[1]+(yDir*2)])
            except IndexError:
                pass

        if not skipCheckCheck:
            moves = self.checkforcheck(moves)

        return moves
    
class Knight(Chessman):
    "The Knight Chess Piece."

    king = False
    type = ChessmanType.knight

    letter = "n"
    unicode = ["♞","♘"]

    def getavailablemoves(self,b=None,skipCheckCheck=False) -> list[list[int]]:
        ## Fake boards are used to determine check or not
        b:board.Board = b if b else self.board
        sq = b.squares

        pos = self.position
        col = self.colour

        moves = []

        for x,l in enumerate(sq):
            for y,square in enumerate(l):
                if square.distance(pos) > 2:
                    continue
                if (abs(x-pos[0]) == 2 and abs(y-pos[1]) == 1) or (abs(x-pos[0]) == 1 and abs(y-pos[1]) == 2):
                    if not square.chessman:
                        moves.append(square.position)
                    elif square.chessman.colour != col:
                        moves.append(square.position)

        if not skipCheckCheck:
            moves = self.checkforcheck(moves)

        return moves
    
def rookMoves(self,b=None,skipCheckCheck=False) -> list[list[int]]:
    "Returns available moves for Rook-like pieces."

    b:board.Board = b if b else self.board
    sq = b.squares

    pos = self.position
    mov = self.hasmoved
    col = self.colour

    moves = []

    for y in range(pos[1]+1,8):
        square = sq[pos[0]][y]
        if square.chessman == None:
            moves.append(square.position)
        else:
            if square.chessman.colour != col:
                moves.append(square.position)
            break

    for y in range(pos[1]-1,-1,-1):
        square = sq[pos[0]][y]
        if square.chessman == None:
            moves.append(square.position)
        else:
            if square.chessman.colour != col:
                moves.append(square.position)
            break

    for x in range(pos[0]+1,8):
        square = sq[x][pos[1]]
        if square.chessman == None:
            moves.append(square.position)
        else:
            if square.chessman.colour != col:
                moves.append(square.position)
            break

    for x in range(pos[0]-1,-1,-1):
        square = sq[x][pos[1]]
        if square.chessman == None:
            moves.append(square.position)
        else:
            if square.chessman.colour != col:
                moves.append(square.position)
            break

    if not skipCheckCheck:
        moves = self.checkforcheck(moves)
    
    return moves

def bishopMoves(self,b=None,skipCheckCheck=False):
    "Returns available moves for Bishop-like pieces."

    b:board.Board = b if b else self.board
    sq = b.squares

    pos = self.position
    col = self.colour

    moves = []

    for i in range(1,8):
        if pos[0] + i < 8 and pos[1] + i < 8:
            square = sq[pos[0]+i][pos[1]+i]
            if square.chessman == None:
                moves.append(square.position)
            else:
                if square.chessman.colour != col:
                    moves.append(square.position)
                break
        else:
            break

    for i in range(1,8):
        if pos[0] - i > -1 and pos[1] + i < 8:
            square = sq[pos[0]-i][pos[1]+i]
            if square.chessman == None:
                moves.append(square.position)
            else:
                if square.chessman.colour != col:
                    moves.append(square.position)
                break
        else:
            break

    for i in range(1,8):
        if pos[0] - i > -1 and pos[1] - i > -1:
            square = sq[pos[0]-i][pos[1]-i]
            if square.chessman == None:
                moves.append(square.position)
            else:
                if square.chessman.colour != col:
                    moves.append(square.position)
                break
        else:
            break

    for i in range(1,8):
        if pos[0] + i < 8 and pos[1] - i > -1:
            square = sq[pos[0]+i][pos[1]-i]
            if square.chessman == None:
                moves.append(square.position)
            else:
                if square.chessman.colour != col:
                    moves.append(square.position)
                break
        else:
            break

    if not skipCheckCheck:
        moves = self.checkforcheck(moves)
    return moves

def kingMoves(self,b=None,skipCheckCheck=False):
    "Returns available moves for King-like pieces."

    b:board.Board = b if b else self.board
    sq = b.squares

    pos = self.position
    mov = self.hasmoved
    col = self.colour

    moves = []

    idx = 0
    for l in sq:
        for square in l:
            if idx >= 8:
                break
            if square.distance(pos) == 1:
                if getattr(square.chessman,"colour",None) != col:
                    moves.append(square.position)
                idx += 1
                
    for piece in b.pieces[1 if col == Colour.white else 0]:
        if piece.type == ChessmanType.rook and not piece.hasmoved:
            ##castle
            pass

    if not skipCheckCheck:
        moves = self.checkforcheck(moves)

    return moves

def castleMoves(self:Chessman):
    "Returns available castling moves from this piece. Returns an empty list if none are available, either due to temporary or permenant reasons."

    b:board.Board = self.board
    sq = b.squares

    pos = self.position
    mov = self.hasmoved
    col = self.colour

    moves = []

    if not mov:
        king = self if self.type == ChessmanType.king else None

        idx = 0
        rooks = []
        for p in b.pieces:
            if p.type == ChessmanType.king and not king:
                idx += 1
                king = p
            elif p.type == ChessmanType.rook and not p.hasmoved:
                idx += 1
                rooks.append(p)

        if king.hasmoved or len(rooks) <= 0:
            return []
        else:
            pass
            
        

    return moves
    
class Rook(Chessman):
    "The Rook Chess Piece."

    king = False
    type = ChessmanType.rook

    letter = "r"
    unicode = ["♜","♖"]

    def getavailablemoves(self,b=None,skipCheckCheck=False):
        return rookMoves(self,b=b,skipCheckCheck=skipCheckCheck)
    
class Bishop(Chessman):
    "The Bishop Chess Piece."

    king = False
    type = ChessmanType.bishop

    letter = "b"
    unicode = ["♝","♗"]

    def getavailablemoves(self,b=None,skipCheckCheck=False) -> list[list[int]]:
        return bishopMoves(self,b=b,skipCheckCheck=skipCheckCheck)
    
class Queen(Chessman):
    "The Queen Chess Piece."

    king = False
    type = ChessmanType.queen

    letter = "q"
    unicode = ["♛","♕"]

    def getavailablemoves(self,b=None,skipCheckCheck=False):
        return rookMoves(self,b=b,skipCheckCheck=skipCheckCheck) + bishopMoves(self,b=b,skipCheckCheck=skipCheckCheck)

class King(Chessman):
    "The King."

    king = True
    type = ChessmanType.king

    letter = "k"
    unicode = ["♚","♔"]

    def getavailablemoves(self,b=None,skipCheckCheck=False) -> list[list[int]]:
        return kingMoves(self,b=b,skipCheckCheck=skipCheckCheck)