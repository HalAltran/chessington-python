from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Knight


class TestKnights:

    @staticmethod
    def test_knight_can_move_forward_two_and_right_one():

        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert
        assert Square.at(6, 5) in moves

    @staticmethod
    def test_knight_can_move_back_one_and_right_two():
        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert
        assert Square.at(3, 6) in moves

    @staticmethod
    def test_knight_can_move_back_two_and_left_one():
        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert
        assert Square.at(2, 3) in moves
