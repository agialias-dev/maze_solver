from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
    ):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)
    
    def __break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        exit = self.__num_cols - 1,self.__num_rows - 1
        entrance.has_top_wall = False
        self.__cells[exit[0]][exit[1]].has_bottom_wall = False
        if self.__win is not None:
            self.__draw_cell(0, 0)
            self.__draw_cell(exit[0], exit[1])
    
    def __break_walls(self, col, row):
        self.__cells[col][row]._Cell__visited = True
        while True:
            adjacent_cells = {"west": (col - 1, row), "east": (col + 1, row), "north": (col, row - 1), "south": (col, row + 1)}
            unvisited_neighbors = [direction for direction, (c, r) in adjacent_cells.items() if 0 <= c < self.__num_cols and 0 <= r < self.__num_rows and not self.__cells[c][r]._Cell__visited]
            if unvisited_neighbors:
                direction = random.choice(unvisited_neighbors)
                if direction == "west":
                    self.__cells[col][row].has_left_wall = False
                    self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]].has_right_wall = False
                elif direction == "east":
                    self.__cells[col][row].has_right_wall = False
                    self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]].has_left_wall = False
                elif direction == "north":
                    self.__cells[col][row].has_top_wall = False
                    self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]].has_bottom_wall = False
                elif direction == "south":
                    self.__cells[col][row].has_bottom_wall = False
                    self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]].has_top_wall = False
                self.__break_walls(adjacent_cells[direction][0], adjacent_cells[direction][1])
            else:
                self.__draw_cell(col, row)
                return
            
    def __reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j]._Cell__visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, col, row):
        self.__animate()
        self.__cells[col][row]._Cell__visited = True
        if col == self.__num_cols - 1 and row == self.__num_rows - 1:
            return True
        adjacent_cells = {"west": (col - 1, row), "east": (col + 1, row), "north": (col, row - 1), "south": (col, row + 1)}
        unvisited_neighbors = [direction for direction, (c, r) in adjacent_cells.items() if 0 <= c < self.__num_cols and 0 <= r < self.__num_rows and not self.__cells[c][r]._Cell__visited]
        for direction in unvisited_neighbors:
            if direction == "west" and not self.__cells[col][row].has_left_wall and not self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]]._Cell__visited:
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]])
                if self._solve_r(adjacent_cells[direction][0], adjacent_cells[direction][1]):
                    return True
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]], undo=True)
            elif direction == "east" and not self.__cells[col][row].has_right_wall and not self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]]._Cell__visited:
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]])
                if self._solve_r(adjacent_cells[direction][0], adjacent_cells[direction][1]):
                    return True
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]], undo=True)
            elif direction == "north" and not self.__cells[col][row].has_top_wall and not self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]]._Cell__visited:
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]])
                if self._solve_r(adjacent_cells[direction][0], adjacent_cells[direction][1]):
                    return True
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]], undo=True)
            elif direction == "south" and not self.__cells[col][row].has_bottom_wall and not self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]]._Cell__visited:
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]])
                if self._solve_r(adjacent_cells[direction][0], adjacent_cells[direction][1]):
                    return True
                self.__cells[col][row].draw_move(self.__cells[adjacent_cells[direction][0]][adjacent_cells[direction][1]], undo=True)
        return False

        

    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        if self.__win is not None:
            self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.01)
