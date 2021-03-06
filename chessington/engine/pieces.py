"""
Definitions of each of the different chess pieces.
"""
import chessington.engine.board as board_module

from abc import ABC, abstractmethod
from copy import deepcopy

from chessington.engine.data import Player, Square


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player
        self.has_moved = False

    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        available_moves = self.get_piece_specific_moves(board)

        if board.primary_board:
            return self.remove_moves_that_leave_self_in_check(board, board.find_piece(self), available_moves)
        return available_moves

    @abstractmethod
    def get_piece_specific_moves(self, board):
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

    @staticmethod
    def remove_moves_that_leave_self_in_check(board, current_square, available_moves):
        for move in list(available_moves):
            board_copy = deepcopy(board)
            board_copy.primary_board = False
            board_copy.move_piece(current_square, move)
            if board_copy.king_is_in_check():
                available_moves.remove(move)
        return available_moves


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_piece_specific_moves(self, board):

        available_moves = []

        direction = self.reverse_direction_if_black(1)

        current_square = board.find_piece(self)

        available_moves.extend(self.get_pawn_straight_moves(board, current_square, direction))
        available_moves.extend(self.get_pawn_diagonal_moves(board, current_square, direction))

        return available_moves

    def get_pawn_straight_moves(self, board, current_square, direction):
        straight_moves = []

        square_in_front = Square.at(current_square.row + direction, current_square.col)
        if square_in_front.is_on_board() and board.square_is_empty(square_in_front):
            straight_moves.append(square_in_front)
            square_two_in_front = Square.at(current_square.row + direction * 2, current_square.col)
            if not self.has_moved and board.square_is_empty(square_two_in_front):
                straight_moves.append(square_two_in_front)

        return straight_moves

    def get_pawn_diagonal_moves(self, board, current_square, direction):
        diagonal_moves = []

        diagonal_moves.extend(self.get_moves_in_direction(board, current_square, 1, direction, 1))
        diagonal_moves.extend(self.get_moves_in_direction(board, current_square, -1, direction, 1))

        attacking_diagonal_moves = []

        for square in diagonal_moves:
            if board.square_contains_opponent(square, self.player):
                attacking_diagonal_moves.append(square)
            elif len(board.move_list) > 0 and self.en_passant_possible(board, current_square, square):
                attacking_diagonal_moves.append(square)
        return attacking_diagonal_moves

    @staticmethod
    def en_passant_possible(board, current_square, diagonal_square):
        last_move = board.move_list[-1]
        is_pawn = isinstance(last_move.attacking_piece, Pawn)
        same_col = last_move.square_to.col == diagonal_square.col
        same_row = last_move.square_to.row == current_square.row

        return is_pawn and same_col and same_row and abs(last_move.vertical_distance_moved()) == 2


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_piece_specific_moves(self, board):

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

    def get_piece_specific_moves(self, board):
        return self.get_diagonal_moves(board, board.find_piece(self), board_module.BOARD_SIZE)


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_piece_specific_moves(self, board):
        return self.get_straight_moves(board, board.find_piece(self), board_module.BOARD_SIZE)


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_piece_specific_moves(self, board):
        current_square = board.find_piece(self)

        available_moves = self.get_straight_moves(board, current_square, board_module.BOARD_SIZE)
        available_moves.extend(self.get_diagonal_moves(board, current_square, board_module.BOARD_SIZE))

        return available_moves


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_piece_specific_moves(self, board):
        current_square = board.find_piece(self)

        available_moves = self.get_straight_moves(board, current_square, 1)
        available_moves.extend(self.get_diagonal_moves(board, current_square, 1))
        available_moves.extend(self.get_castle_moves(board, current_square))

        return available_moves

    def get_castle_moves(self, board, current_square):
        castle_moves = []

        if self.can_castle_king_side(board, current_square):
            castle_moves.append(Square.at(current_square.row, current_square.col + 2))
        if self.can_castle_queen_side(board, current_square):
            castle_moves.append(Square.at(current_square.row, current_square.col - 2))

        return castle_moves

    def can_castle_king_side(self, board, current_square):
        return self.can_castle(board, current_square, 3)

    def can_castle_queen_side(self, board, current_square):
        return self.can_castle(board, current_square, -4)

    def can_castle(self, board, current_square, distance_to_rook):
        if self.has_moved:
            return False
        direction = 1
        if distance_to_rook < 0:
            direction = - 1
        rook_column = current_square.col + distance_to_rook
        rook_square = Square.at(current_square.row, rook_column)
        rook = board.get_piece(rook_square)
        if not isinstance(rook, Rook):
            return False
        castle_squares = self.get_moves_in_direction(board, current_square, 1 * direction, 0, abs(distance_to_rook))
        castle_squares_are_empty = len(castle_squares) == abs(distance_to_rook) - 1
        return not rook.has_moved and castle_squares_are_empty
