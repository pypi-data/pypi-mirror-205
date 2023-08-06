class Cursor:
    def __init__(self, matrix):
        self.matrix = matrix
        self.row = 0
        self.col = 0
        try:
            self.shape = matrix.shape
        except Exception as e:
            raise ValueError(f"Matrix must be a NumPy matrix")

    def left(self, steps: int = 1) -> str:
        if steps < 1:
            raise ValueError(f"Cursor left step must be > 0, but obtained {steps}")
        new_col = self.col - steps
        if new_col < 0:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to go to ({self.row},{new_col})")
        self.col = new_col
        return str(self.matrix[self.row, self.col])

    def right(self, steps: int = 1) -> str:
        if steps < 1:
            raise ValueError(f"Cursor right step must be > 0, but obtained {steps}")
        new_col = self.col + steps
        if new_col > self.shape[1] - 1:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to go to ({self.row},{new_col})")
        self.col = new_col
        return str(self.matrix[self.row, self.col])

    def up(self, steps: int = 1) -> str:
        if steps < 1:
            raise ValueError(f"Cursor up step must be > 0, but obtained {steps}")
        new_row = self.row - steps
        if new_row < 0:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to go to ({new_row},{self.col})")
        self.row = new_row
        return str(self.matrix[self.row, self.col])

    def down(self, steps: int = 1) -> str:
        if steps < 1:
            raise ValueError(f"Cursor down step must be > 0, but obtained {steps}")
        new_row = self.row + steps
        if new_row > self.shape[0] - 1:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to go to ({new_row},{self.col})")
        self.row = new_row
        return str(self.matrix[self.row, self.col])

    def move(self, row_steps: int, col_steps: int) -> str:
        if row_steps == 0:
            raise ValueError(f"Cursor move row step must be != 0, but obtained {row_steps}")
        if col_steps == 0:
            raise ValueError(f"Cursor move col step must be != 0, but obtained {col_steps}")
        new_row = self.row + row_steps
        new_col = self.col + col_steps
        if new_row < 0 or new_row > self.shape[0] - 1 or new_col < 0 or new_col > self.shape[1] - 1:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to go to ({new_row},{new_col})")
        self.row = new_row
        self.col = new_col
        return str(self.matrix[self.row, self.col])

    def setItem(self, item) -> str:
        self.matrix[self.row, self.col] = item
        return str(self.matrix[self.row, self.col])

    def set(self, row: int, col: int) -> str:
        if row < 0:
            raise ValueError(f"Cursor set row must be > -1, but obtained {row}")
        if col < 0:
            raise ValueError(f"Cursor set col must be > -1, but obtained {row}")
        if row > self.shape[0] - 1 or col > self.shape[1] - 1:
            raise ValueError(
                f"Cursor try to out of bounds matrix, matrix limits is (0,0) ({self.shape[0] - 1},{self.shape[1] - 1}), but the cursor tried to set to ({row},{col})")
        self.row = row
        self.col = col
        return str(self.matrix[self.row, self.col])

    @property
    def coordinates(self):
        return self.row, self.col

    @property
    def isEmpty(self):
        return self.matrix[self.row, self.col] == 0

    def __repr__(self):
        return str(self.matrix[self.row, self.col])

    def __str__(self):
        return str(self.matrix[self.row, self.col])
