import curses
import calendar
from datetime import datetime, timedelta

from .io import load_projects

def main_cmd_curses(stdscr):
    today = datetime.today()
    week = today.isocalendar().week
    week = [datetime.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = load_projects()

    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()
    num_columns = 5
    _col_width = width//num_columns - 1
    _col_height = height//2
    for day in range(num_columns):
        win = curses.newwin(_col_height, _col_width, 5, day*(_col_width+1)+1)
        win.box()
        win.addstr(0, 1, calendar.day_name[day], curses.A_BOLD)
        win.addstr(1, 1, week[day].strftime("%b %d"), curses.A_BOLD)
        inner = win.derwin(_col_height-2, _col_width-2, 1, 1)
        for idx, p in enumerate(projects):
            inner.addstr(2+2*idx, 0, p.name)
        win.refresh()

    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    curses.wrapper(main_cmd_curses)
