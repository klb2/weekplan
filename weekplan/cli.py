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




@cli.group("task")
def task():
    pass

@task.command()
def add():
    click.echo("add task")


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

if __name__ == "__main__":
    cli()
