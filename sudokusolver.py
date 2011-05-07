#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sudoku

class Solver(object):
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.board = self.sudoku.board[:] # copy, don't change original

    def solve(self):
        self.possibles = [range(1, 10) for x in range(81)]
        solved_tiles = sum(1 for x in self.board if x > 0)
        while True:
            self.update_possibles()
            if self.fill_only_possibles():
                continue
            if self.fill_one_possibles_per_group():
                continue
            if self.reduce_intergroup_possibles():
                continue
            break

        return self.board

    def update_possibles(self):
        for i in range(81):
            tile = self.board[i]
            if tile == 0:
                continue
            self.possibles[i] = []
            for group in sudoku.related_groups(i):
                for other_i in (oi for oi in group if oi != i):
                    if tile in self.possibles[other_i]:
                        self.possibles[other_i].remove(tile)

    def fill_one_possibles_per_group(self):
        filled_this_round = 0
        groups = sudoku.ROW_GROUP_INDICES + sudoku.COL_GROUP_INDICES + \
                 sudoku.BOX_GROUP_INDICES
        for g in groups:
            places = [set() for i in range(10)]
            for tile_i in g:
                for nbr in self.possibles[tile_i]:
                    places[nbr].add(tile_i)
            for nbr in range(1, 10):
                if len(places[nbr]) == 1:
                    # number can be in only one place in group, fill it
                    tile_i = places[nbr].pop()
                    self.board[tile_i] = nbr
                    self.possibles[tile_i] = []
                    filled_this_round += 1
                    for rg in sudoku.related_groups(tile_i):
                        for other_i in rg:
                            if nbr in self.possibles[other_i]:
                                self.possibles[other_i].remove(nbr)
        return filled_this_round


    def fill_only_possibles(self):
        unfilled = (i for i in range(81) if self.board[i] == 0)
        filled_this_round = 0
        for i in unfilled:
            if len(self.possibles[i]) == 1:
                self.board[i] = self.possibles[i].pop()
                filled_this_round += 1
        return filled_this_round

    def possibles_boxlist_by_column(self, col_i):
        boxes_of_nbr = [set() for i in range(10)] # set of boxes each number can be in

        for tile_i in sudoku.COL_GROUP_INDICES[col_i]:
            box_i = sudoku.in_box[tile_i]
            for nbr in self.possibles[tile_i]:
                boxes_of_nbr[nbr].add(box_i)

        return boxes_of_nbr

    def possibles_boxlist_by_row(self, row_i):
        boxes_of_nbr = [set() for i in range(10)] # set of boxes each number can be in

        for tile_i in sudoku.ROW_GROUP_INDICES[row_i]:
            box_i = sudoku.in_box[tile_i]
            for nbr in self.possibles[tile_i]:
                boxes_of_nbr[nbr].add(box_i)

        return boxes_of_nbr

    def possibles_collist_by_box(self, box_i):
        cols_of_nbr = [set() for i in range(10)] # set of columns each number can be in

        for tile_i in sudoku.BOX_GROUP_INDICES[box_i]:
            col_i = sudoku.in_col[tile_i]
            for nbr in self.possibles[tile_i]:
                cols_of_nbr[nbr].add(col_i)

        return cols_of_nbr

    def possibles_rowlist_by_box(self, box_i):
        rows_of_nbr = [set() for i in range(10)] # set of rows each number can be in

        for tile_i in sudoku.BOX_GROUP_INDICES[box_i]:
            row_i = sudoku.in_row[tile_i]
            for nbr in self.possibles[tile_i]:
                rows_of_nbr[nbr].add(row_i)

        return rows_of_nbr

    def reduce_intergroup_possibles(self):
        """Reduce possibles by checking two related tile groups

        For example: If '4' is missing from column A and all its
        possible locations on that column are inside 3x3 box X, '4' can't
        be placed inside X in tiles outside column A.

        """
        reduced_this_round = 0

        for col_i in range(9):
            boxes_of_nbr = self.possibles_boxlist_by_column(col_i)
            for nbr in range(1, 10):
                if len(boxes_of_nbr[nbr]) == 1:
                    # number can be inside only one box in column col_i
                    box_i = boxes_of_nbr[nbr].pop()
                    for tile_i in sudoku.BOX_GROUP_INDICES[box_i]:
                        # remove nbr from possibles in box outside column col_i
                        if self.board[tile_i] == 0 and \
                           sudoku.in_col[tile_i] != col_i and \
                           nbr in self.possibles[tile_i]:
                             self.possibles[tile_i].remove(nbr)
                             reduced_this_round += 1

        for row_i in range(9):
            boxes_of_nbr = self.possibles_boxlist_by_row(row_i)
            for nbr in range(1, 10):
                if len(boxes_of_nbr[nbr]) == 1:
                    # number can be inside only one box in row row_i
                    box_i = boxes_of_nbr[nbr].pop()
                    for tile_i in sudoku.BOX_GROUP_INDICES[box_i]:
                        # remove nbr from possibles in box outside column col_i
                        if self.board[tile_i] == 0 and \
                           sudoku.in_row[tile_i] != row_i and \
                           nbr in self.possibles[tile_i]:
                             self.possibles[tile_i].remove(nbr)
                             reduced_this_round += 1

        for box_i in range(9):
            cols_of_nbr = self.possibles_collist_by_box(box_i)
            for nbr in range(1, 10):
                if len(cols_of_nbr[nbr]) == 1:
                    # number can be in only one column in box box_i
                    col_i = cols_of_nbr[nbr].pop()
                    for tile_i in sudoku.COL_GROUP_INDICES[col_i]:
                        # remove nbr from possibles in column outside box box_i
                        if self.board[tile_i] == 0 and \
                           sudoku.in_box[tile_i] != box_i and \
                           nbr in self.possibles[tile_i]:
                             self.possibles[tile_i].remove(nbr)
                             reduced_this_round += 1

        for box_i in range(9):
            rows_of_nbr = self.possibles_rowlist_by_box(box_i)
            for nbr in range(1, 10):
                if len(rows_of_nbr[nbr]) == 1:
                    # number can be in only one row in box box_i
                    row_i = rows_of_nbr[nbr].pop()
                    for tile_i in sudoku.ROW_GROUP_INDICES[row_i]:
                        # remove nbr from possibles in row outside box box_i
                        if self.board[tile_i] == 0 and \
                           sudoku.in_box[tile_i] != box_i and \
                           nbr in self.possibles[tile_i]:
                             self.possibles[tile_i].remove(nbr)
                             reduced_this_round += 1

        return reduced_this_round
