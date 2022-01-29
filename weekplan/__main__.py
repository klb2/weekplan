import curses

from . import __version__
from .cmd import CmdApp
from .cli import cli

def main_cmd():
    #curses.wrapper(main_cmd_curses)
    #curses.wrapper(CmdApp)
    cli()
