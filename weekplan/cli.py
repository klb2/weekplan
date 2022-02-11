from datetime import date

import click
import columnar

from . import Project, Task
from . import io
from .base import create_project_from_template


@click.group(invoke_without_command=True)
@click.pass_context
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
def list_projects(verbose):
    projects = io.load_projects()
    for _project in projects:
        click.echo(click.style(_project.name, bold=True))
        if verbose >= 1:
            click.echo(click.style(_project.description, italic=True))
            for _task_idx, _task in enumerate(_project.tasks):
                if verbose < 2:
                    if _task.completed: continue
                click.echo(f"{_task_idx:02d}\t{_task.name}") 
            click.echo("\n")
        click.echo('---')
    #click.echo(projects)

def _list_projects(projects):
    for idx, _p in enumerate(projects):
        click.echo(f"{idx:>2d}: {_p.name}")

def _list_active_projects(projects):
    for idx, _p in enumerate(projects):
        if _p.completed is not None: continue
        click.echo(f"{idx:>2d}: {_p.name}")

def _list_tasks(tasks):
    for idx, _t in enumerate(tasks):
        click.echo(f"{idx:>2d}: {_t.name}")

def _list_active_tasks(tasks, day):
    for idx, _t in enumerate(tasks):
        if (day in _t.dates) or (_t.completed): continue
        click.echo(f"{idx:>2d}: {_t.name}")



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



@cli.group("week", invoke_without_command=True)
@click.pass_context
def week(ctx):
    if ctx.invoked_subcommand is None:
        table = _show_week()
        click.echo(table)

def _show_week():
    today = date.today()
    week = today.isocalendar().week
    week = [date.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = io.load_projects()
    table = []
    patterns = [
        (r'[A-Z][a-z]+ \([A-Z][a-z]+ [0-9]{2}\)', lambda text: click.style(text, bold=True)),
        ]
    for p in projects:
        for _task in p.tasks:
            #_days_in_week = sorted(set(_task.dates).intersection(week))
            row = [_task.name if _day in _task.dates else "" for _day in week]
            if not row == [""]*len(week):
                table.append(row)
    if not table:
        return
    table = columnar.columnar(data=table, headers=[_d.strftime("%a (%b %d)")
                                                   for _d in week],
                              justify='c', patterns=patterns)
    return table

@week.command("show")
def show_week():
    click.echo(_show_week())

@week.command("plan")
def plan_week():
    today = date.today()
    week = today.isocalendar().week
    week = [date.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = io.load_projects()
    for day in week:
        while True:
            click.echo(click.style(day.strftime("%A: %b %d"), bold=True))
            #_list_projects(projects)
            _list_active_projects(projects)
            _sel_p = click.prompt("Select project", default=-1, type=int)
            if _sel_p == -1: break
            _p = projects[_sel_p]
            click.echo()
            while True:
                click.echo(click.style(day.strftime("%A: %b %d"), bold=True))
                _list_active_tasks(_p.tasks, day)
                _sel_t = click.prompt("Select task", default=-1, type=int)
                if _sel_t == -1: break
                _t = _p.tasks[_sel_t].add_date(day)
            click.echo()
            io.save_project(_p)
        click.clear()

if __name__ == "__main__":
    cli()
