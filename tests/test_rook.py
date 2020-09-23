from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Rook


class TestRooks:

    @staticmethod
    def test_rook_can_move_straight():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) in moves

    @staticmethod
    def test_rook_can_move_until_blocked_by_teammate():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, rook)
        board.set_piece(Square.at(6, 4), Rook(Player.WHITE))

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) not in moves

    @staticmethod
    def test_rook_can_take_opponent():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, rook)
        board.set_piece(Square.at(6, 4), Rook(Player.BLACK))

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) in moves

    @staticmethod
    def test_rook_can_not_move_beyond_opponent():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        square = Square.at(4, 4)
        board.set_piece(square, rook)
        board.set_piece(Square.at(6, 4), Rook(Player.WHITE))

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(7, 4) not in moves
