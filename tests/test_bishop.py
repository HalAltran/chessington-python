from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Bishop


class TestBishops:

    @staticmethod
    def test_bishop_can_move_diagonally():

        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, bishop)

        # Act
        moves = bishop.get_available_moves(board)

        # Assert
        assert Square.at(6, 6) in moves

    @staticmethod
    def test_bishop_can_move_until_blocked_by_teammate():

        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, bishop)
        board.set_piece(Square.at(6, 6), Bishop(Player.WHITE))

        # Act
        moves = bishop.get_available_moves(board)

        # Assert
        assert Square.at(6, 6) not in moves

    @staticmethod
    def test_bishop_can_take_opponent():
        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, bishop)
        board.set_piece(Square.at(6, 6), Bishop(Player.BLACK))

        # Act
        moves = bishop.get_available_moves(board)

        # Assert
        assert Square.at(6, 6) in moves

    @staticmethod
    def test_bishop_can_not_move_beyond_opponent():

        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.BLACK)
        square = Square.at(4, 4)
        board.set_piece(square, bishop)
        board.set_piece(Square.at(6, 6), Bishop(Player.WHITE))

        # Act
        moves = bishop.get_available_moves(board)

        # Assert
        assert Square.at(7, 7) not in moves
