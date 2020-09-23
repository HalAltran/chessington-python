"""
Definitions of each of the different chess pieces.
"""
import chessington.engine.board as board_module

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

    def get_straight_moves(self, board, current_square, max_step_count):
        straight_moves = []

        direction_array = [-1, 1]

        for i in direction_array:
            straight_moves.extend(self.get_moves_in_direction(board, current_square, i, 0, max_step_count))
            straight_moves.extend(self.get_moves_in_direction(board, current_square, 0, i, max_step_count))

        return straight_moves

    def get_diagonal_moves(self, board, current_square, max_step_count):

        diagonal_moves = []

        direction_array = [-1, 1]

        for i in direction_array:
            for j in direction_array:
                diagonal_moves.extend(self.get_moves_in_direction(board, current_square, i, j, max_step_count))

        return diagonal_moves

    def get_moves_in_direction(self, board, current_square, horizontal_step, vertical_step, max_step_count):
        directional_squares = []

        horizontal_offset = horizontal_step
        vertical_offset = vertical_step

        do_next_step = True

        step_count = 0

        while do_next_step:
            square = Square.at(current_square.row + vertical_offset, current_square.col + horizontal_offset)
            if square.is_on_board():
                if board.square_is_empty(square):
                    directional_squares.append(square)
                elif board.square_contains_opponent(square, self.player):
                    directional_squares.append(square)
                    do_next_step = False
                else:
                    do_next_step = False
            else:
                do_next_step = False
            vertical_offset += vertical_step
            horizontal_offset += horizontal_step
            step_count += 1

            if step_count == max_step_count:
                do_next_step = False

        return directional_squares


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):

        available_moves = []

        direction = self.reverse_direction_if_black(1)

        available_moves.extend(self.get_pawn_straight_moves(board, direction))
        available_moves.extend(self.get_pawn_diagonal_moves(board, direction))

        return available_moves

    def get_pawn_straight_moves(self, board, direction):
        straight_moves = []

        current_square = board.find_piece(self)

        square_in_front = Square.at(current_square.row + direction, current_square.col)
        if square_in_front.is_on_board() and board.get_piece(square_in_front) is None:
            straight_moves.append(square_in_front)
            square_two_in_front = Square.at(current_square.row + direction * 2, current_square.col)
            if not self.has_moved and board.get_piece(square_two_in_front) is None:
                straight_moves.append(square_two_in_front)

        return straight_moves

    def get_pawn_diagonal_moves(self, board, direction):
        current_square = board.find_piece(self)

        diagonal_moves = []

        diagonal_moves.extend(self.get_moves_in_direction(board, current_square, 1, direction, 1))
        diagonal_moves.extend(self.get_moves_in_direction(board, current_square, -1, direction, 1))

        attacking_diagonal_moves = []

        for square in diagonal_moves:
            if board.square_contains_opponent(square, self.player):
                attacking_diagonal_moves.append(square)
        return attacking_diagonal_moves


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
                if self.abs_not_equal(i, j):
                    available_moves.extend(self.get_moves_in_direction(board, current_square, i, j, 1))

        return available_moves

    @staticmethod
    def abs_not_equal(i, j):
        return abs(i) != abs(j)


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return self.get_diagonal_moves(board, board.find_piece(self), board_module.BOARD_SIZE)


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return self.get_straight_moves(board, board.find_piece(self), board_module.BOARD_SIZE)


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        current_square = board.find_piece(self)

        available_moves = self.get_straight_moves(board, current_square, board_module.BOARD_SIZE)
        available_moves.extend(self.get_diagonal_moves(board, current_square, board_module.BOARD_SIZE))

        return available_moves


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        current_square = board.find_piece(self)

        available_moves = self.get_straight_moves(board, current_square, 1)
        available_moves.extend(self.get_diagonal_moves(board, current_square, 1))

        return available_moves
