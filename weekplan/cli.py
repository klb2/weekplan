import click

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
    pass


if __name__ == "__main__":
    cli()
