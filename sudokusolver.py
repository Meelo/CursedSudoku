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
        prev_solved = 0
        while solved_tiles > prev_solved:
            prev_solved = solved_tiles
            self.update_possibles()
            self.fill_obvious()
            solved_tiles = sum(1 for x in self.board if x > 0)
        return self.board

    def update_possibles(self):
        for i in range(81):
            tile = self.board[i]
            for group in sudoku.related_groups(i):
                for other_i in (oi for oi in group if oi != i):
                    if tile in self.possibles[other_i]:
                        self.possibles[other_i].remove(tile)

    def fill_obvious(self):
        unfilled = (i for i in range(81) if self.board[i] == 0)
        for i in unfilled:
            if len(self.possibles[i]) == 1:
                self.board[i] = self.possibles[i][0]
