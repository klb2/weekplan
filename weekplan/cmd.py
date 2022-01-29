import curses
from curses import panel
import calendar
from datetime import date, timedelta

from .io import load_projects



class Menu:
    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(("exit", "exit"))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.position == len(self.items) - 1:
                    break
                else:
                    self.items[self.position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class LoopBreak(Exception):
    pass

class MainMenu:
    def __init__(self, items):
        pass


class CmdApp:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
    
        self.projects = load_projects()
        self.today = date.today()
        week = self.today.isocalendar().week
        self.week = [date.fromisocalendar(self.today.year, week, i+1)
                     for i in range(5)]

        #submenu_items = [("beep", curses.beep), ("flash", curses.flash)]
        #submenu = MainMenuMenu(submenu_items, self.screen)

        #main_menu_items = [
        #    ("beep", curses.beep),
        #    ("flash", curses.flash),
        #    #("submenu", submenu.display),
        #]
        #self.main_menu = MainMenu(main_menu_items, self.screen)
        #self.display()

        self.main_menu_items = {ord("q"): self.quit,
                                ord("x"): self.quit,
                               }
        self.run()


    @staticmethod
    def quit():
        raise LoopBreak

    def run(self):
        while True:
            self.screen.clear()
            self.screen.refresh()
            self.build_columns()
            c = self.screen.getch()
            try:
                self.main_menu_items.get(c)()
            except LoopBreak:
                break
            except:
                print("This command does not exist")
            #if c in [ord('x'), ord('q')]:
            #    break
            #elif c == curses.KEY_F1:
            #    self.screen.addstr(5, 10, "OK")
            #else:
            #    self.screen.addstr(25, 15, str(c))

        #stdscr.refresh()
        #stdscr.getkey()

    def build_columns(self):
        height, width = self.screen.getmaxyx()
        num_columns = 5
        _col_width = width//num_columns - 1
        _col_height = height-5 #height//2
        for day in range(num_columns):
            win = curses.newwin(_col_height, _col_width, 2, day*(_col_width+1)+1)
            win.box()
            win.addstr(0, 1, "{} ({})".format(calendar.day_name[day],
                                              self.week[day].strftime("%b %d")),
                       curses.A_BOLD)
            #win.addstr(1, 1, week[day].strftime("%b %d"), curses.A_BOLD)
            inner = win.derwin(_col_height-2, _col_width-2, 1, 1)
            line = 2
            for idx, p in enumerate(self.projects):
                for _task in p.tasks:
                    if self.week[day] in _task.dates:
                        #inner.addstr(line, 0, "{}\n({})".format(_task.name, p.name))
                        inner.addstr(line, 0, _task.name)
                        line = line + 2
            win.refresh()

    def display(self):
        self.main_menu.panel.top()
        self.main_menu.panel.show()
        self.screen.clear()

        while True:
            self.screen.refresh()
            curses.doupdate()
            for index, item in enumerate(self.main_menu.items):
                if index == self.main_menu.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.screen.addstr(1 + index, 1, msg, mode)

            key = self.screen.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.main_menu.position == len(self.main_menu.items) - 1:
                    break
                else:
                    self.main_menu.items[self.main_menu.position][1]()

            elif key == curses.KEY_UP:
                self.main_menu.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.main_menu.navigate(1)

        self.screen.clear()
        self.main_menu.panel.hide()
        panel.update_panels()
        curses.doupdate()



if __name__ == "__main__":
    #curses.wrapper(main_cmd_curses)
    curses.wrapper(CmdApp)
