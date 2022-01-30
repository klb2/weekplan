from datetime import date

import click
import columnar

from . import Project, Task
from . import io


@click.group()
def cli():
    """Top level"""
    pass

@cli.group("project")
def project():
    pass

@project.command()
@click.argument("name", type=str)
@click.option("--description", type=str, default="")
def add(name, description):
    p = Project(name, description=description)
    click.echo(p)
    io.save_project(p)

@project.command()
@click.option('-v', '--verbose', count=True)
def list(verbose):
    projects = io.load_projects()
    for _project in projects:
        click.echo(click.style(_project.name, bold=True))
        if verbose >= 1:
            click.echo(click.style(_project.description, italic=True))
        #click.echo("Tasks:")
        for _task_idx, _task in enumerate(_project.tasks):
            if verbose == 0:
                if _task.completed: continue
            click.echo(f"{_task_idx:02d}\t{_task.name}") 
        click.echo('\n---\n')
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

@task.command()
@click.argument("name", type=str)
def add(name):
    t = Task(name)
    projects = io.load_projects()
    _list_projects(projects)
    _selected_idx = click.prompt("Project to add to", type=int)
    _selected_project = projects[_selected_idx]
    _selected_project.add_task(t)
    io.save_project(_selected_project)


@cli.group("week")
def week():
    pass

@week.command()
def show():
    today = date.today()
    week = today.isocalendar().week
    week = [date.fromisocalendar(today.year, week, i+1) for i in range(5)]
    projects = io.load_projects()
    table = []
    for p in projects:
        for _task in p.tasks:
            #_days_in_week = sorted(set(_task.dates).intersection(week))
            row = [_task.name if _day in _task.dates else "" for _day in week]
            if not row == [""]*len(week):
                table.append(row)
    table = columnar.columnar(data=table, headers=[_d.strftime("%b %d") for _d in week])
    click.echo(table)

@week.command()
def plan():
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
            while True:
                click.echo(click.style(day.strftime("%A: %b %d"), bold=True))
                _list_active_tasks(_p.tasks, day)
                _sel_t = click.prompt("Select task", default=-1, type=int)
                if _sel_t == -1: break
                _t = _p.tasks[_sel_t].add_date(day)
            io.save_project(_p)

        #click.clear()

if __name__ == "__main__":
    cli()
