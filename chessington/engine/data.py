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

    def __init__(self, attacking_piece, defending_piece, square_from, square_to):
        self.attacking_piece = attacking_piece
        self.defending_piece = defending_piece
        self.square_from = square_from
        self.square_to = square_to

    def vertical_distance_moved(self):
        return abs(self.square_to.row - self.square_from.row)

    def horizontal_distance_moved(self):
        return self.square_to.col - self.square_from.col

    def is_en_passant(self):
        import chessington.engine.pieces as pieces
        return isinstance(self.attacking_piece, pieces.Pawn) and self.defending_piece is None \
               and self.horizontal_distance_moved() != 0

    def is_castle(self):
        import chessington.engine.pieces as pieces
        return isinstance(self.attacking_piece, pieces.King) and abs(self.horizontal_distance_moved()) == 2
