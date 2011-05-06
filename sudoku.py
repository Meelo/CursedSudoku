#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index groups for each row, column and 3x3 box
ROW_GROUP_INDICES = [range(9 * r, 9 * r + 9) for r in range(9)]
COL_GROUP_INDICES = [range(c, c + 81, 9) for c in range(9)]
__BOX_INC = (0, 1, 2, 9, 10, 11, 18, 19, 20)
__BOX_START = (0, 3, 6, 27, 30, 33, 54, 57, 60)
BOX_GROUP_INDICES = [[s + i for i in __BOX_INC] for s in __BOX_START]

class InvalidBoardException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return repr(self.reason)

# every 9 tile group (of indices) on board
def _board_groups():
    for g in ROW_GROUP_INDICES:
        yield g
    for g in COL_GROUP_INDICES:
        yield g
    for g in BOX_GROUP_INDICES:
        yield g

# dictionary of index -> groups (of indices) where tile index is found
_in_groups = {}
for group in _board_groups():
    for i in group:
        if not _in_groups.has_key(i):
            _in_groups[i] = []
        _in_groups[i].append(group)

# list of tile index -> index of box tile is in
in_box = range(81) # prefill
for box_i, group in enumerate(BOX_GROUP_INDICES):
    for tile_i in group:
        in_box[tile_i] = box_i

def related_groups(tile_i):
    """return all index groups which tile index belongs"""
    return _in_groups[tile_i]

def in_box(tile_i):
    """return index of box in which tile is"""

class Sudoku(object):
    def __init__(self):
        self.board = [0 for x in range(81)]

    def valid_move(self, index, val):
        if val == 0:
            return True
        for group in related_groups(index):
            if any(self.board[i] == val for i in group if i != index):
                return False
        return True

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            board_data = f.read()
        board_data = [int(c) for c in board_data if c in '0123456789']

        if len(board_data) != 81:
            raise InvalidBoardException('File contains invalid data')

        self.board = board_data

if __name__ == '__main__':
    board = Sudoku()
