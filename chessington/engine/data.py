"""
Data classes for easy representation of concepts such as a square on the board or a player.
"""
import chessington.engine.board as board_module

from dataclasses import dataclass
from enum import Enum, auto


class Player(Enum):
    """
    The two players in a game of chess.
    """
    WHITE = auto()
    BLACK = auto()

    def opponent(self):
        if self == Player.WHITE:
            return Player.BLACK
        else:
            return Player.WHITE


@dataclass(frozen=True)
class Square:
    row: int
    col: int

    @classmethod
    def at(cls, row: int, col: int):
        """
        Provides backward compatibility with previous namedtuple implementation.

        Square.at(...) is equivalent to Square(...).
        """

        return cls(row=row, col=col)

    def is_on_board(self):
        return 0 <= self.row < board_module.BOARD_SIZE and 0 <= self.col < board_module.BOARD_SIZE


class Move:

    def __init__(self, piece, square_from, square_to):
        self.piece = piece
        self.square_from = square_from
        self.square_to = square_to

    def vertical_distance_moved(self):
        return abs(self.square_to.row - self.square_from.row)
