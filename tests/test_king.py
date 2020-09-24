from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Queen, Rook
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

    @staticmethod
    def test_king_can_castle_king_side_if_not_blocked():

        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        king_square = Square.at(0, 4)
        board.set_piece(king_square, king)

        rook = Rook(Player.WHITE)
        rook_square = Square.at(0, 7)
        board.set_piece(rook_square, rook)

        # Act
        moves = king.get_available_moves(board)

        king_castle_square = Square.at(0, 6)

        # Assert
        assert king_castle_square in moves

        board.move_piece(king_square, king_castle_square)

        rook_castle_square = Square.at(0, 5)

        assert isinstance(board.get_piece(rook_castle_square), Rook)

    @staticmethod
    def king_can_not_castle_king_side_if_blocked():

        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        square = Square.at(0, 4)
        board.set_piece(square, king)

        # Act
        moves = king.get_available_moves(board)

        # Assert
        assert Square.at(0, 6) not in moves
