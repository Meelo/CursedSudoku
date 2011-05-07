#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import sudoku
import sudokugui as sg
import sudokusolver

class CursesSudoku(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.PRINT_MODE = curses.A_NORMAL

        self.window = curses.newwin(24, 80, 0, 0)
        self.window.border(0,0,0,0,0,0,0,0)
        self.window.keypad(1)
        self.window.refresh()

        self.sudoku = sudoku.Sudoku()
        self.sudoku_gui = sg.SudokuGui(self.window, 1, 1, curses.color_pair(2))

    def draw(self):
        self.sudoku_gui.draw()
        self.sudoku_gui.update_content(self.sudoku.board)

    def run(self):
        x, y = self.sudoku_gui.get_tile_index()
        while 1:
            self.window.move(y, x)
            c = self.window.getch()
            if c == ord('q'):
                break # quit
            elif c == ord('s'):
                self.solve_board()
            elif c in (curses.KEY_UP, curses.KEY_DOWN,
                       curses.KEY_LEFT, curses.KEY_RIGHT):
                x, y = self.sudoku_gui.process_move(c)
            elif c == curses.KEY_DC:
                i, j = self.sudoku_gui.get_selected_index()
                self.set_value(i * 9 + j, 0)
            elif ord('1') <= c <= ord('9'):
                val = c - ord('0')
                i, j = self.sudoku_gui.get_selected_index()
                self.set_value(i * 9 + j, val)

    def set_value(self, i, val):
        if val != 0 and not self.sudoku.valid_move(i, val):
            return
        x, y = self.sudoku_gui.get_tile_index()
        self.sudoku.board[i] = val
        self.window.move(y, x)
        self.sudoku_gui.update_content(self.sudoku.board)

    def solve_board(self):
        solver = sudokusolver.Solver(self.sudoku)
        solution_board = solver.solve()

        self.sudoku.board = solution_board
        self.draw()
        self.sudoku_gui.update_content(self.sudoku.board)

    def quit(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
