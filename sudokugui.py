#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

class SudokuGui(object):
    def __init__(self, surface, x, y, colour):
        self.surface = surface
        self.x = x
        self.y = y
        self.colour = colour
        self.tile_center = \
            [[(i, j) for i in (2, 6, 10, 15, 19, 23, 28, 32, 36)] \
                     for j in (1, 3, 5, 8, 10, 12, 15, 17, 19)]
        self.selected_tile = (0, 0)

    def process_move(self, arrow_key):
        i, j = self.selected_tile
        if arrow_key == curses.KEY_RIGHT:
            j = (j + 1) % 9
        elif arrow_key == curses.KEY_LEFT:
            j = (j - 1) % 9
        if arrow_key == curses.KEY_DOWN:
            i = (i + 1) % 9
        elif arrow_key == curses.KEY_UP:
            i = (i - 1) % 9

        self.selected_tile = (i, j)
        return self.get_tile_index()
    
    def get_tile_index(self):
        i, j = self.selected_tile
        x, y = self.tile_center[i][j]
        return (x + self.x, y + self.y)

    def get_selected_index(self):
        return self.selected_tile

    ## 
    ## This is what the grid should look like.
    ## ┌───┬───┬───┐┌───┬───┬───┐┌───┬───┬───┐
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## └───┴───┴───┘└───┴───┴───┘└───┴───┴───┘
    ## ┌───┬───┬───┐┌───┬───┬───┐┌───┬───┬───┐
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## └───┴───┴───┘└───┴───┴───┘└───┴───┴───┘
    ## ┌───┬───┬───┐┌───┬───┬───┐┌───┬───┬───┐
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## ├───┼───┼───┤├───┼───┼───┤├───┼───┼───┤
    ## │   │   │   ││   │   │   ││   │   │   │
    ## └───┴───┴───┘└───┴───┴───┘└───┴───┴───┘
    def draw(self):
        try:
            for i, j in ((x * 13 + self.x, y * 7 + self.y) \
                    for y in range(3) for x in range(3)):
                k = i + 12
                l = j + 6
                # corners
                self.surface.addch(j, i, curses.ACS_ULCORNER, self.colour)
                self.surface.addch(j, k, curses.ACS_URCORNER, self.colour)
                self.surface.addch(l, i, curses.ACS_LLCORNER, self.colour)
                self.surface.addch(l, k, curses.ACS_LRCORNER, self.colour)

                # vertical T 
                self.surface.addch(j + 2, i, curses.ACS_LTEE, self.colour)
                self.surface.addch(j + 4, i, curses.ACS_LTEE, self.colour)
                self.surface.addch(j + 2, k, curses.ACS_RTEE, self.colour)
                self.surface.addch(j + 4, k, curses.ACS_RTEE, self.colour)

                # horizontal T
                self.surface.addch(j, i + 4, curses.ACS_TTEE, self.colour)
                self.surface.addch(j, i + 8, curses.ACS_TTEE, self.colour)
                self.surface.addch(l, i + 4, curses.ACS_BTEE, self.colour)
                self.surface.addch(l, i + 8, curses.ACS_BTEE, self.colour)

                # crosses
                self.surface.addch(j + 2, i + 4, curses.ACS_PLUS, self.colour)
                self.surface.addch(j + 2, i + 8, curses.ACS_PLUS, self.colour)
                self.surface.addch(j + 4, i + 4, curses.ACS_PLUS, self.colour)
                self.surface.addch(j + 4, i + 8, curses.ACS_PLUS, self.colour)

            # vertical lines
            for i, j in ((self.x + x + k * 13, self.y + y + l * 7) \
                    for x in range(0, 13, 4) for y in range(1, 6, 2) \
                    for k in range(3) for l in range(3)):
                self.surface.addch(j, i, curses.ACS_VLINE, self.colour)

            # horizontal lines
            for i, j in ((k * 13 + x + self.x, l * 7 + y + self.y) \
                    for x in range(1, 12) for y in range(0, 7, 2) \
                    for k in range(3) for l in range(3) if x % 4 != 0):
                self.surface.addch(j, i, curses.ACS_HLINE, self.colour)
        except curses.error:
            pass

        self.surface.refresh()

    def update_content(self, sudoku_data):
        self.content = sudoku_data
        tile_center = [y for x in self.tile_center for y in x]
        for i in range(9 * 9):
            c = self.content[i] + ord('0') if self.content[i] != 0 else ' '
            x, y = tile_center[i]
            self.surface.addch(y + self.y, x + self.x, c)
