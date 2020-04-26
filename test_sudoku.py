import unittest

from solver import Solver
from sudoku import Sudoku


class TestSudoku(unittest.TestCase):

    def test_block_ids(self):
        expected = [0, 1, 2, 9, 10, 11, 18, 19, 20]
        self.assertEqual(Sudoku.get_block_ids(0), expected)
        self.assertEqual(Sudoku.get_block_ids(1), expected)
        self.assertEqual(Sudoku.get_block_ids(10), expected)
        self.assertEqual(Sudoku.get_block_ids(11), expected)
        self.assertEqual(Sudoku.get_block_ids(18), expected)
        self.assertEqual(Sudoku.get_block_ids(20), expected)

        expected = [3, 4, 5, 12, 13, 14, 21, 22, 23]
        self.assertEqual(Sudoku.get_block_ids(4), expected)
        self.assertEqual(Sudoku.get_block_ids(5), expected)
        self.assertEqual(Sudoku.get_block_ids(12), expected)
        self.assertEqual(Sudoku.get_block_ids(14), expected)
        self.assertEqual(Sudoku.get_block_ids(22), expected)

        expected = [27, 28, 29, 36, 37, 38, 45, 46, 47]
        self.assertEqual(Sudoku.get_block_ids(27), expected)
        self.assertEqual(Sudoku.get_block_ids(28), expected)
        self.assertEqual(Sudoku.get_block_ids(29), expected)
        self.assertEqual(Sudoku.get_block_ids(38), expected)
        self.assertEqual(Sudoku.get_block_ids(47), expected)

        expected = [30, 31, 32, 39, 40, 41, 48, 49, 50]
        self.assertEqual(Sudoku.get_block_ids(31), expected)
        self.assertEqual(Sudoku.get_block_ids(32), expected)
        self.assertEqual(Sudoku.get_block_ids(39), expected)
        self.assertEqual(Sudoku.get_block_ids(40), expected)
        self.assertEqual(Sudoku.get_block_ids(49), expected)

        expected = [60, 61, 62, 69, 70, 71, 78, 79, 80]
        self.assertEqual(Sudoku.get_block_ids(80), expected)
        self.assertEqual(Sudoku.get_block_ids(60), expected)
        self.assertEqual(Sudoku.get_block_ids(62), expected)
        self.assertEqual(Sudoku.get_block_ids(70), expected)

    def test_units(self):
        sudoku = Solver.deserialize_from_str(
            '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
        self.assertEqual(len(sudoku.units), 27)
        nrs = [[c.cell_id for c in unit] for unit in sudoku.units]
        print('nrs:', nrs)

        # rows
        self.assertTrue([0, 1, 2, 3, 4, 5, 6, 7, 8] in nrs)
        self.assertTrue([9, 10, 11, 12, 13, 14, 15, 16, 17] in nrs)
        self.assertTrue([18, 19, 20, 21, 22, 23, 24, 25, 26] in nrs)
        self.assertTrue([27, 28, 29, 30, 31, 32, 33, 34, 35] in nrs)
        self.assertTrue([36, 37, 38, 39, 40, 41, 42, 43, 44] in nrs)
        self.assertTrue([45, 46, 47, 48, 49, 50, 51, 52, 53] in nrs)
        self.assertTrue([54, 55, 56, 57, 58, 59, 60, 61, 62] in nrs)
        self.assertTrue([63, 64, 65, 66, 67, 68, 69, 70, 71] in nrs)
        self.assertTrue([72, 73, 74, 75, 76, 77, 78, 79, 80] in nrs)

        # cols
        self.assertTrue([0, 9, 18, 27, 36, 45, 54, 63, 72] in nrs)
        self.assertTrue([1, 10, 19, 28, 37, 46, 55, 64, 73] in nrs)
        self.assertTrue([2, 11, 20, 29, 38, 47, 56, 65, 74] in nrs)
        self.assertTrue([3, 12, 21, 30, 39, 48, 57, 66, 75] in nrs)
        self.assertTrue([4, 13, 22, 31, 40, 49, 58, 67, 76] in nrs)
        self.assertTrue([5, 14, 23, 32, 41, 50, 59, 68, 77] in nrs)
        self.assertTrue([6, 15, 24, 33, 42, 51, 60, 69, 78] in nrs)
        self.assertTrue([7, 16, 25, 34, 43, 52, 61, 70, 79] in nrs)
        self.assertTrue([8, 17, 26, 35, 44, 53, 62, 71, 80] in nrs)

        # 3x3 blocks
        self.assertTrue([0, 1, 2, 9, 10, 11, 18, 19, 20] in nrs)
        self.assertTrue([3, 4, 5, 12, 13, 14, 21, 22, 23] in nrs)
        self.assertTrue([6, 7, 8, 15, 16, 17, 24, 25, 26] in nrs)
        self.assertTrue([27, 28, 29, 36, 37, 38, 45, 46, 47] in nrs)
        self.assertTrue([30, 31, 32, 39, 40, 41, 48, 49, 50] in nrs)
        self.assertTrue([33, 34, 35, 42, 43, 44, 51, 52, 53] in nrs)
        self.assertTrue([54, 55, 56, 63, 64, 65, 72, 73, 74] in nrs)
        self.assertTrue([57, 58, 59, 66, 67, 68, 75, 76, 77] in nrs)
        self.assertTrue([60, 61, 62, 69, 70, 71, 78, 79, 80] in nrs)


if __name__ == '__main__':
    unittest.main()
