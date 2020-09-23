import pytest

from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Knight


class TestKnights:

    @staticmethod
    @pytest.mark.parametrize("valid_destination", [[6, 5], [3, 6], [2, 3], [2, 5]])
    def test_knight_can_move_in_l_pattern(valid_destination):

        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        square = Square.at(4, 4)
        board.set_piece(square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert
        assert Square.at(valid_destination[0], valid_destination[1]) in moves
        assert Square.at(valid_destination[1], valid_destination[0]) in moves
