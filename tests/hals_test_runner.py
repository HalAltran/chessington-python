from tests.test_bishop import TestBishops
from tests.test_knight import TestKnights
from tests.test_pawn import TestPawns

if __name__ == "__main__":
    # TestPawns.test_white_pawns_can_move_up_one_square()
    # TestPawns.test_white_pawn_cannot_move_at_top_of_board()
    # TestKnights.test_knight_can_move_in_l_pattern([6, 5])
    TestBishops.test_bishop_can_not_move_beyond_opponent()
