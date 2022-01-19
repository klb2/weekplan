import curses

from . import __version__
from .cmd import main_cmd_curses

def main_cmd():
    curses.wrapper(main_cmd_curses)
