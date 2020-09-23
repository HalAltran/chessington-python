from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Queen


class TestQueens:

    @staticmethod
    def test_queen_can_move_diagonally():
        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, queen)

        # Act
        moves = queen.get_available_moves(board)

        # Assert
        assert Square.at(6, 6) in moves

    @staticmethod
    def test_queen_can_move_straight():

        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, queen)

        # Act
        moves = queen.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) in moves

    @staticmethod
    def test_queen_can_move_until_blocked_by_teammate():

        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, queen)
        board.set_piece(Square.at(6, 4), Queen(Player.WHITE))

        # Act
        moves = queen.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) not in moves

    @staticmethod
    def test_queen_can_take_opponent():
        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, queen)
        board.set_piece(Square.at(6, 4), Queen(Player.BLACK))

        # Act
        moves = queen.get_available_moves(board)

        # Assert
        assert Square.at(6, 4) in moves

    @staticmethod
    def test_queen_can_not_move_beyond_opponent():

        # Arrange
        board = Board.empty()
        queen = Queen(Player.BLACK)
        square = Square.at(4, 4)
        board.set_piece(square, queen)
        board.set_piece(Square.at(6, 4), Queen(Player.WHITE))

        # Act
        moves = queen.get_available_moves(board)

        # Assert
        assert Square.at(7, 4) not in moves
