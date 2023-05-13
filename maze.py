'''
Maze module.
'''
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        stack = Stack()
        start_cell = self._start_cell
        stack.push(start_cell)

        while not stack.is_empty():
            current_cell = stack.peek()
            row = current_cell.row
            col = current_cell.col

            if self._exit_found(row, col):
                return True

            if self._valid_move(row - 1, col):  # Check upward
                self._mark_path(row - 1, col)
                stack.push(_CellPosition(row - 1, col))
            elif self._valid_move(row + 1, col):  # Check downward
                self._mark_path(row + 1, col)
                stack.push(_CellPosition(row + 1, col))
            elif self._valid_move(row, col - 1):  # Check left
                self._mark_path(row, col - 1)
                stack.push(_CellPosition(row, col - 1))
            elif self._valid_move(row, col + 1):  # Check right
                self._mark_path(row, col + 1)
                stack.push(_CellPosition(row, col + 1))
            else:
                stack.pop()
                self._mark_tried(row, col)

        return False

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if (
                    self._maze_cells[row, col] == self.PATH_TOKEN
                    or self._maze_cells[row, col] or self._maze_cells[row, col] == self.TRIED_TOKEN
                ):
                    self._maze_cells[row, col] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        maze_str = ""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                cell = self._maze_cells[row, col]
                if cell is None:
                    maze_str += "_ "
                else:
                    maze_str += cell + " "
            maze_str = maze_str.rstrip() + "\n"
        return maze_str.rstrip()


    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return (
            row >= 0
            and row < self.num_rows()
            and col >= 0
            and col < self.num_cols()
            and self._maze_cells[row, col] is None
        )

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col


def build_maze(filename):
    """Builds a maze based on a text format in the given file."""
    infile = open(filename, "r")

    # Read the size of the maze.
    nrows, ncols = read_value_pair(infile)
    maze = Maze(nrows, ncols)

    # Read the starting and exit positions.
    row, col = read_value_pair(infile)
    maze.set_start(row, col)
    row, col = read_value_pair(infile)
    maze.set_exit(row, col)

    # Read the maze itself.
    for row in range(nrows):
        line = infile.readline()
        for col in range(len(line)):
            if line[col] == "*":
                maze.set_wall(row, col)

    # Close the maze file and return the newly constructed maze.
    infile.close()

    return maze


def read_value_pair(infile):
    """Extracts an integer value pair from the given input file."""
    line = infile.readline()
    valA, valB = line.split()
    return int(valA), int(valB)

maze = build_maze("mazefile.txt")
print(maze.find_path())
print(maze)
print(len(str(maze)))
print(str(maze) == '* * * * * \
* o * o * \
* x x x * \
* x * x x \
_ x * * * ')
# * * * * *
# * o * o *
# * x x x *
# * x * x x
# _ _ * * *

# * * * * * 
# * o * o * 
# * x x x * 
# * x * x x 
# _ x * * * 
