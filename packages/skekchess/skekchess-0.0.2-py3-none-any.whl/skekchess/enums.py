from enum import Enum

__all__ = (
    "ChessmanType",
    "ChessmanState",
    "GameResolution",
    "MoveNotation",
    "VictoryCondition",
    "DrawCondition",
    "Rulesets",
    "Colour",
)

class ChessmanType(Enum):
    """Denotes a Chessman type.

    Values are 40-49, where 49 is none.
    """
    pawn = 40
    knight = 41
    bishop = 42
    rook = 43
    queen = 44
    king = 45
    none = 49

    def __str__(self) -> str:
        return self.name
    
    def __int__(self) -> int:
        return self.value
    
class ChessmanState(Enum):
    """Denotes a State for a Chessman, either Alive or Dead.

    Dead should not generally be used.

    Values are 50-59.
    """

    dead = 50
    alive = 51
    captured = 52

class Colour(Enum):
    """Denotes a Colour.
    Does not denote an RGB value for these.

    Values are 10-19.
    """
    black = 10
    white = 11

    def __str__(self) -> str:
        return self.name
    
    def __invert__(self):
        if self.value == 10:
            return Colour.white
        else:
            return Colour.black

class Rulesets(Enum):
    """Denotes a Ruleset for Skek-Chess.

    Standard - the standard rules of Chess, as clarified by FIDE (https://www.fide.com/FIDE/handbook/LawsOfChess.pdf).

    Values are 0-9.
    """
    standard = 0

    def __str__(self) -> str:
        return self.name
    

class GameResolution(Enum):
    """Denotes the basic game ending, either victory for either party or a draw.

    Values are 20-21.
    """
    victory = 20
    draw = 21

    def __str__(self) -> str:
        return self.name

class VictoryCondition(Enum):
    """Denotes the Condition that resulted in a Victory for either party.

    A Timeout can be either a Victory or a Draw depending on the game state.
    https://www.chess.com/article/view/how-chess-games-can-end-8-ways-explained Should explain these.

    Values are 22-23.
    """
    checkmate = 22
    timeout = 23

    def __str__(self) -> str:
        return self.name

class DrawCondition(Enum):
    """Denotes the Condition that resulted in a Draw.

    A Timeout can be either a Victory or a Draw depending on the game state.
    https://www.chess.com/article/view/how-chess-games-can-end-8-ways-explained Should explain these.
    Values are 24-29.

    """
    stalemate = 24
    material = 25
    fiftymoverule = 26
    repetition = 27
    agreement = 28
    timeout = 29

    def __str__(self) -> str:
        return self.name
    
class PlayerType(Enum):
    """Denotes a Type of Player that the user is playing against.

    Engine refers to any Engine run in Skek-Chess.
    Other refers to any Other Player Type, such as an External Engine or AI.

    Values are 60-69.
    """
    human = 60
    engine = 61
    other = 69

    def __str__(self) -> str:
        return self.name
    
class MoveNotation(Enum):
    """Denotes a move notation.

    LongAlgebraic uses the starting position followed by the destination position. A piece letter is appended if promoting.
    Algebraic - https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
    Internal is a list of 2 base 10 integers starting from 0.

    Values are 70-75.
    """

    longalgebraic = 70
    algebraic = 71
    internal = 75
