from datetime import date

from weekplan import Project, Task
from weekplan import base

def test_task_class():
    t = base.Task("name")
    assert isinstance(t, Task)

def test_task_name():
    name = "name"
    t = base.Task(name)
    assert t.name == name

def test_task_add_date():
    _date = date(year=2020, month=2, day=7)
    t = base.Task("name")
    t.add_date(_date)
    assert _date in t.dates

def test_task_add_date_duplicate():
    _date = date(year=2020, month=2, day=7)
    _date_dup = date(year=2020, month=2, day=7)
    t = base.Task("name")
    t.add_date(_date)
    t.add_date(_date_dup)
    assert _date in t.dates and len(t.dates) == 1

def test_project_class():
    p = base.Project("name")
    assert isinstance(p, Project)

def test_project_name():
    name = "name"
    p = base.Project(name)
    assert p.name == name

def test_project_add_task():
    p = base.Project("project_name")
    t = base.Task("task_name")
    p.add_task(t)
    assert t in p.tasks
