# Sudoku-Solver

Python program to solve sudoku puzzles.
 Author: Aravind Raghunathan.
 The program attempts to solve a standard 9x9 Sudoku puzzle by using AI constrain propagation & search
 techniques ( Specifically,  Naked Twins, Elimination, Only-Choice & Search).
 Code developed as part of the requirement for Udacity AI degree program.

 The program accepts a string representation of a starting sudoku puzzle in the following format.

 Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'.

 Values in the string represents the starting values in individual squares and '.' represents empty square.

 The values in the string representation are ordered from (row A, column 1) to (row I, column 9)

 The board layout is defined as follows.

 Rows labeled from A - I & Columns labeled from 1 - 9.

        1 2 3 4 5 6 7 9
       A
       B
       C
       D
       E
       F
       G
       H
       I