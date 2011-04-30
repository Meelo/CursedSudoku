#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import sudoku

class CursesSudoku(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.PRINT_MODE = curses.A_NORMAL

        self.window = curses.newwin(13, 13, 0, 0)
        self.window.border(0,0,0,0,0,0,0,0)
        self.window.keypad(1)
        self.window.refresh()

        self.sudoku = sudoku.Sudoku()
        self.x = 0
        self.y = 0

    def window_xy(self, pos_i):
        base_y = 1
        base_x = 1
        row = pos_i / 9
        col = pos_i % 9
        add_y = row / 3
        add_x = col / 3
        x = base_x + add_x + col
        y = base_y + add_y + row
        return x, y

    def draw(self):
        for i, val in enumerate(self.sudoku.board):
            x, y = self.window_xy(i)
            c = ' ' if val == 0 else str(val)
            self.window.addch(y, x, ord(c), curses.color_pair(1) | self.PRINT_MODE)

    def run(self):
        self.active_i = 0
        while 1:
            x, y = self.window_xy(self.active_i)
            self.window.move(y, x)
            c = self.window.getch()
            move = False
            if c == ord('q'):
                break
            elif c == curses.KEY_UP:
                if self.active_i > 8:
                    self.active_i -= 9
            elif c == curses.KEY_DOWN:
                if self.active_i < 73:
                    self.active_i += 9
            elif c == curses.KEY_LEFT:
                if self.active_i % 9 > 0:
                    self.active_i -= 1
            elif c == curses.KEY_RIGHT:
                if self.active_i % 9 < 8:
                    self.active_i += 1

    def quit(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
