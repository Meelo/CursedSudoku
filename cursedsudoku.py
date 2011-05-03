#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import cursessudoku
    from optparse import OptionParser

    desc = 'Cursed Sudoku - client'
    usage = 'usage: %prog {options}'
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option('-f', '--file', dest='file',
                      help='input board file')
    options, args = parser.parse_args()

    exit_message = ''
    cs = cursessudoku.CursesSudoku()
    try:
        if options.file is not None:
            cs.sudoku.load_from_file(options.file)
        cs.draw()
        cs.run()
    except KeyboardInterrupt:
        exit_message = 'User exit'
    finally:
        cs.quit()
        if exit_message:
            print exit_message
