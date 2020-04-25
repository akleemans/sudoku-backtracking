import unittest

from sudoku import Sudoku


class TestSudoku(unittest.TestCase):

    def test_block_ids(self):
        expected = {0, 1, 2, 9, 10, 11, 18, 19, 20}
        self.assertEqual(Sudoku.get_block_ids(0), expected)
        self.assertEqual(Sudoku.get_block_ids(1), expected)
        self.assertEqual(Sudoku.get_block_ids(10), expected)
        self.assertEqual(Sudoku.get_block_ids(11), expected)
        self.assertEqual(Sudoku.get_block_ids(18), expected)
        self.assertEqual(Sudoku.get_block_ids(20), expected)

        expected = {3, 4, 5, 12, 13, 14, 21, 22, 23}
        self.assertEqual(Sudoku.get_block_ids(4), expected)
        self.assertEqual(Sudoku.get_block_ids(5), expected)
        self.assertEqual(Sudoku.get_block_ids(12), expected)
        self.assertEqual(Sudoku.get_block_ids(14), expected)
        self.assertEqual(Sudoku.get_block_ids(22), expected)

        expected = {30, 31, 32, 39, 40, 41, 48, 49, 50}
        self.assertEqual(Sudoku.get_block_ids(31), expected)
        self.assertEqual(Sudoku.get_block_ids(32), expected)
        self.assertEqual(Sudoku.get_block_ids(39), expected)
        self.assertEqual(Sudoku.get_block_ids(40), expected)
        self.assertEqual(Sudoku.get_block_ids(49), expected)

        expected = {60, 61, 62, 69, 70, 71, 78, 79, 80}
        self.assertEqual(Sudoku.get_block_ids(80), expected)
        self.assertEqual(Sudoku.get_block_ids(60), expected)
        self.assertEqual(Sudoku.get_block_ids(62), expected)
        self.assertEqual(Sudoku.get_block_ids(70), expected)


if __name__ == '__main__':
    unittest.main()
