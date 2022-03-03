from datetime import date

import click
import columnar

from . import Project, Task
from . import io
from . import __version__
from .base import create_project_from_template


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(__version__)
def cli(ctx):
    """Top level"""
    if ctx.invoked_subcommand is None:
        table = _show_week()
        click.echo(table)

@cli.group("project")
def project():
    pass

@project.command("add")
@click.argument("name", type=str)
@click.option("--description", type=str, default="")
@click.option("-t", "--template", type=str, default=None)
def add_project(name, description, template):
    if isinstance(template, Project):
        p = template(name, description=description)
    elif isinstance(template, str) and not template == "":
        p = create_project_from_template(name, template=template,
                                         description=description)
    else:
        p = Project(name, description=description)
    click.echo(p)
    io.save_project(p)

@project.command("list")
@click.option('-v', '--verbose', count=True)
@click.option("-a", "--show_all", is_flag=True, default=False)
def list_projects(verbose, show_all):
    projects = io.load_projects()
    for _project in projects:
        _project_style = {"bold": True}
        if _project.completed is not None:
            if not show_all: continue
            _project_style["fg"] = "green"
            #_project_style["strikethrough"] = True
        click.secho(_project.name, **_project_style)
        if verbose >= 1:
            click.secho(_project.description, italic=True)
            _task_style = {}
            for _task_idx, _task in enumerate(_project.tasks):
                if verbose < 2:
                    if _task.completed: continue
                else:
                    _task_style = {"fg": "green"} if _task.completed else {"fg": "red"}
                click.secho(f"{_task_idx:02d}\t{_task.name}", **_task_style) 
            click.echo("\n")
        click.echo('---')
    #click.echo(projects)

def _list_projects(projects):
    for idx, _p in enumerate(projects):
        click.echo(f"{idx:>2d}: {_p.name}")

def _list_active_projects(projects, day=None):
    for idx, _p in enumerate(projects):
        if _p.completed is not None: continue
        if day in _p.dates: continue
        click.echo(f"{idx:>2d}: {_p.name}")

def _list_scheduled_projects(projects, day):
    for idx, _p in enumerate(projects):
        if day in _p.dates:
            click.echo(f"{idx:>2d}: {_p.name}")

def _list_tasks(tasks):
    for idx, _t in enumerate(tasks):
        click.echo(f"{idx:>2d}: {_t.name}")

def _list_active_tasks(tasks, day=None):
    for idx, _t in enumerate(tasks):
        if (day in _t.dates) or (_t.completed): continue
        click.echo(f"{idx:>2d}: {_t.name}")


@project.command("complete")
def complete_project():
    projects = io.load_projects()
    _list_active_projects(projects)
    _sel_p = click.prompt("Select project", default=-1, type=int)
    if _sel_p == -1: return
    _p = projects[_sel_p]
    _p.completed = date.today()
    io.save_project(_p)


@cli.group("task")
def task():
    pass

@task.command("add")
@click.argument("name", type=str)
def add_task(name):
    t = Task(name)
    projects = io.load_projects()
    _list_projects(projects)
    _selected_idx = click.prompt("Project to add to", type=int)
    _selected_project = projects[_selected_idx]
    _selected_project.add_task(t)
    io.save_project(_selected_project)

@task.command("complete")
def complete_task():
    projects = io.load_projects()
    while True:
        _list_active_projects(projects)
        _sel_p = click.prompt("Select project", default=-1, type=int)
        if _sel_p == -1: break
        _p = projects[_sel_p]
        while True:
            _list_active_tasks(_p.tasks)
            _sel_t = click.prompt("Select task", default=-1, type=int)
            if _sel_t == -1: break
            _p.tasks[_sel_t].completed = True
        io.save_project(_p)
        click.clear()


@cli.group("week", invoke_without_command=True)
@click.pass_context
def week(ctx):
    if ctx.invoked_subcommand is None:
        table = _show_week()
        click.echo(table)

def _show_week(week: int | None=None, day: int | None=None):
    today = date.today()
    if week is None:
        week = today.isocalendar().week
    week = [date.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = io.load_projects()
    table = []
    patterns = [
        (r'[A-Z][a-z]+ \([A-Z][a-z]+ [0-9]{2}\)', lambda text: click.style(text, bold=True)),
        ]
    for p in projects:
        row = [p.name if _day in p.dates else "" for _day in week]
        if not row == [""]*len(week):
            table.append(row)
        #for _task in p.tasks:
        #    #_days_in_week = sorted(set(_task.dates).intersection(week))
        #    row = [_task.name if _day in _task.dates else "" for _day in week]
        #    if not row == [""]*len(week):
        #        table.append(row)
    if not table:
        return
    headers = [_d.strftime("%a (%b %d)") for _d in week]
    if day is not None:
        headers[day] = click.style(headers[day], reverse=True, bold=True)
    table = columnar.columnar(data=table, headers=headers, justify='c',
                              patterns=patterns)
    return table

@week.command("show")
def show_week():
    click.echo(_show_week())

@week.command("plan")
@click.option("-w", "--week", type=int, default=None)
@click.option("-n", "--next_week", is_flag=True, default=False)
@click.option("-r", "--remove", is_flag=True, default=False)
def plan_week(week, next_week, remove):
    today = date.today()
    if week is None:
        week = today.isocalendar().week
        if next_week:
            week = week + 1
    week_number = week
    week = [date.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = io.load_projects()
    for idx_day, day in enumerate(week):
        while True:
            click.clear()
            click.echo(_show_week(week_number, idx_day))
            click.secho(day.strftime("%A: %b %d"), bold=True)
            #_list_projects(projects)
            if remove:
                click.secho("Warning: Removing projects!", fg='red', bold=True)
                _list_scheduled_projects(projects, day)
            else:
                _list_active_projects(projects, day)
            _sel_p = click.prompt("Select project", default=-1, type=int)
            if _sel_p == -1: break
            _p = projects[_sel_p]
            if remove:
                _p.remove_date(day)
            else:
                _p.add_date(day)
            click.echo()
            #while True:
            #    click.echo(click.style(day.strftime("%A: %b %d"), bold=True))
            #    _list_active_tasks(_p.tasks, day)
            #    _sel_t = click.prompt("Select task", default=-1, type=int)
            #    if _sel_t == -1: break
            #    _t = _p.tasks[_sel_t].add_date(day)
            #click.echo()
            io.save_project(_p)
            #click.clear()

if __name__ == "__main__":
    cli()
