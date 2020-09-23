from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Queen
from chessington.engine.pieces import King


class TestKings:

    @staticmethod
    def test_king_can_move_diagonally():
        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, king)

        # Act
        moves = king.get_available_moves(board)

        # Assert
        assert Square.at(5, 5) in moves

    @staticmethod
    def test_king_can_move_straight():

        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, king)

        # Act
        moves = king.get_available_moves(board)

        # Assert
        assert Square.at(5, 4) in moves

    @staticmethod
    def test_king_can_take_opponent():
        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, king)
        board.set_piece(Square.at(5, 4), Queen(Player.BLACK))

        # Act
        moves = king.get_available_moves(board)

        # Assert
        assert Square.at(5, 4) in moves

    @staticmethod
    def test_king_is_blocked_by_friend():

        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, king)
        board.set_piece(Square.at(5, 4), Queen(Player.WHITE))

        # Act
        moves = king.get_available_moves(board)

        # Assert
        assert Square.at(5, 4) not in moves
