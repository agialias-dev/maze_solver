import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    
    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._Maze__cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_maze_break_walls_recursive(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__break_walls(0, 0)
        self.assertEqual(
            m1._Maze__cells[5][5].has_top_wall and m1._Maze__cells[5][5].has_bottom_wall and m1._Maze__cells[5][5].has_left_wall and m1._Maze__cells[5][5].has_right_wall,
            False,
        )
        self.assertEqual(
            m1._Maze__cells[6][6].has_top_wall and m1._Maze__cells[6][6].has_bottom_wall and m1._Maze__cells[6][6].has_left_wall and m1._Maze__cells[6][6].has_right_wall,
            False,
        )

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__break_walls(0, 0)
        m1._Maze__reset_cells_visited()
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(
                    m1._Maze__cells[i][j]._Cell__visited,
                    False,
                )


if __name__ == "__main__":
    unittest.main()
