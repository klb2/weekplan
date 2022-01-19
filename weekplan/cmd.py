import curses
import calendar
#from datetime import datetime

def main_cmd_curses(stdscr):
    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()
    #stdscr.bkgd(curses.color_pair(1))
    num_columns = 5
    _col_width = width//num_columns
    for day in range(num_columns):
        win = curses.newwin(height//2, _col_width-1, 5, day*_col_width+1)
        #win.bkgd(curses.color_pair(2))
        win.box()
        win.addstr(0, 1, calendar.day_name[day])
        win.refresh()
    #stdscr.addstr(0, 0, "Test")

    #stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    curses.wrapper(main_cmd_curses)
