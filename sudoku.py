#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

class InvalidBoardException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return repr(self.reason)

class Sudoku(object):
    def __init__(self):
        self.board = [0 for x in range(81)]

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            board_data = f.read()
        board_data = [int(c) for c in board_data if c in '0123456789']
       
        if len(board_data) != 81:
            raise InvalidBoardException('File contains invalid data')

        self.board = board_data

if __name__ == '__main__':
    board = Sudoku()
