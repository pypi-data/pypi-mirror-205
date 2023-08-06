NumPy Cursor
============

This repository contains a Python implementation of a cursor for NumPy matrices. The cursor allows you to conveniently move through a matrix and read or modify its values.

The cursor class has the following methods:

*   `__init__(self, matrix)`: Initializes the cursor with a NumPy matrix.
*   `left(self, steps=1)`: Moves the cursor left by `steps` columns.
*   `right(self, steps=1)`: Moves the cursor right by `steps` columns.
*   `up(self, steps=1)`: Moves the cursor up by `steps` rows.
*   `down(self, steps=1)`: Moves the cursor down by `steps` rows.
*   `move(self, row_steps, col_steps)`: Moves the cursor by `row_steps` rows and `col_steps` columns.
*   `set(self, row, col)`: Set the cursor by `row` rows and `col` columns.
*   `coordinates`: Returns the current row and column coordinates of the cursor.
*   `isEmpty`: Returns `True` if the value of the matrix at the current cursor position is zero, and `False` otherwise.
*   `setItem(self, item)`: Setting the value of the cursor cell by `item`.
*   `__repr__(self)`: Returns a string representation of the value of the matrix at the current cursor position.
*   `__str__(self)`: Returns a string representation of the value of the matrix at the current cursor position.

The implementation also includes error checking to prevent moving the cursor beyond the boundaries of the matrix.