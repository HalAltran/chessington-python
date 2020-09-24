"""
A module providing a representation of a chess board. The rules of chess are not implemented - 
this is just a "dumb" board that will let you move pieces around as you like.
"""
from copy import deepcopy
from chessington.engine.data import Player, Square, Move
from chessington.engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King

BOARD_SIZE = 8


class Board:
    """
    A representation of the chess board, and the pieces on it.
    """

    def __init__(self, player, board_state):
        self.current_player = Player.WHITE
        self.board = board_state
        self.move_list = []

    @staticmethod
    def empty():
        return Board(Player.WHITE, Board._create_empty_board())

    @staticmethod
    def at_starting_position():
        return Board(Player.WHITE, Board._create_starting_board())

    @staticmethod
    def _create_empty_board():
        return [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    @staticmethod
    def _create_starting_board():

        # Create an empty board
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Setup the rows of pawns
        board[1] = [Pawn(Player.WHITE) for _ in range(BOARD_SIZE)]
        board[6] = [Pawn(Player.BLACK) for _ in range(BOARD_SIZE)]

        # Setup the rows of pieces
        piece_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board[0] = list(map(lambda piece: piece(Player.WHITE), piece_row))
        board[7] = list(map(lambda piece: piece(Player.BLACK), piece_row))

        return board

    def set_piece(self, square, piece):
        """
        Places the piece at the given position on the board.
        """
        self.board[square.row][square.col] = piece

    def get_piece(self, square):
        """
        Retrieves the piece from the given square of the board.
        """
        return self.board[square.row][square.col]

    def find_piece(self, piece_to_find):
        """
        Searches for the given piece on the board and returns its square.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is piece_to_find:
                    return Square.at(row, col)
        raise Exception('The supplied piece is not on the board')

    def move_piece(self, from_square, to_square):
        """
        Moves the piece from the given starting square to the given destination square.
        """
        moving_piece = self.get_piece(from_square)
        if moving_piece is not None and moving_piece.player == self.current_player:
            piece_under_attack = deepcopy(self.get_piece(to_square))
            self.set_piece(to_square, moving_piece)
            self.set_piece(from_square, None)

            self.move_list.append(Move(deepcopy(moving_piece), piece_under_attack, from_square, to_square))

            self.remove_en_passant_pawn()
            self.castle_rook()
            self.promote_pawn()

            self.current_player = self.current_player.opponent()

    def remove_en_passant_pawn(self):
        if self.move_list[-1].is_en_passant():
            self.set_piece(self.move_list[-2].square_to, None)

    def castle_rook(self):
        last_move = self.move_list[-1]
        if last_move.is_castle():
            if last_move.horizontal_distance_moved() > 0:
                rook_square_from = Square.at(last_move.square_to.row, last_move.square_to.col + 1)
                rook_square_to = Square.at(last_move.square_to.row, last_move.square_to.col - 1)
            else:
                rook_square_from = Square.at(last_move.square_to.row, last_move.square_to.col - 2)
                rook_square_to = Square.at(last_move.square_to.row, last_move.square_to.col + 1)

            self.set_piece(rook_square_to, self.get_piece(rook_square_from))
            self.set_piece(rook_square_from, None)

    def promote_pawn(self):
        last_move = self.move_list[-1]
        if last_move.is_pawn_promotion():
            self.set_piece(last_move.square_to, Queen(self.current_player))

    def square_contains_opponent(self, square, player):
        piece_on_square = self.get_piece(square)
        return piece_on_square is not None and piece_on_square.player != player

    def square_is_empty(self, square):
        return self.get_piece(square) is None

    def king_is_in_check(self):
        pass
