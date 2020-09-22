"""
Definitions of each of the different chess pieces.
"""
from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player
        self.has_moved = False

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)
        self.has_moved = True

    def reverse_direction_if_black(self, distance):
        if self.player == Player.BLACK:
            return distance * - 1
        return distance

    def square_contains_opponent(self, board, square):
        piece_on_square = board.get_piece(square)
        if piece_on_square is not None:
            if piece_on_square.player != self.player:
                return True


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):

        available_moves = []

        available_moves.extend(self.get_straight_moves(board))
        available_moves.extend(self.get_diagonal_moves(board))

        return available_moves

    def at_end_of_board(self, current_square):
        if self.player == Player.WHITE:
            return current_square.row == 7
        return current_square.row == 0

    def piece_in_front(self, board, offset):
        current_square = board.find_piece(self)
        return not board.board[current_square.row + offset][current_square.col] is None

    def get_straight_moves(self, board):
        straight_moves = []

        current_square = board.find_piece(self)
        offset = self.reverse_direction_if_black(1)
        if not self.at_end_of_board(current_square) and not self.piece_in_front(board, offset):
            straight_moves.append(Square.at(current_square.row + offset, current_square.col))
            if not self.has_moved and not self.piece_in_front(board, offset * 2):
                straight_moves.append(Square.at(current_square.row + offset * 2, current_square.col))
        return straight_moves

    def get_diagonal_moves(self, board):
        diagonal_moves = []

        current_square = board.find_piece(self)

        offset = self.reverse_direction_if_black(1)

        if not self.at_end_of_board(current_square):
            diagonal_in_front_squares = [Square.at(current_square.row + offset, current_square.col + 1),
                                         Square.at(current_square.row + offset, current_square.col - 1)]

            for square in diagonal_in_front_squares:
                if square.is_on_board() and self.square_contains_opponent(board, square):
                    diagonal_moves.append(square)
        return diagonal_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):

        available_moves = []

        current_square = board.find_piece(self)

        minus_two_to_two_excluding_zero = [-2, -1, 1, 2]

        for i in minus_two_to_two_excluding_zero:
            for j in minus_two_to_two_excluding_zero:
                if self.abs_diff_one(i, j):
                    square = Square.at(current_square.row + i, current_square.col + j)
                    if square.is_on_board() and (self.square_contains_opponent(board, square)
                                                 or board.get_piece(square) is None):
                        available_moves.append(square)

        return available_moves

    @staticmethod
    def abs_diff_one(i, j):
        return abs(abs(i) - abs(j)) == 1


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []