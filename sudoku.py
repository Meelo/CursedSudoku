#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

class InvalidBoard(object):
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
        all_chars = string.maketrans('', '')
        no_digits = all_chars.translate(all_chars, string.digits)
        board_data = board_data.translate(all_chars, no_digits)

        if len(board_data) != 81 and not board_data.isalnum():
            raise InvalidBoard('File contains invalid data')

        for i in range(len(board_data)):
            self.board[i] = ord(board_data[i]) - ord('0')
            

if __name__ == '__main__':
    board = Sudoku()
