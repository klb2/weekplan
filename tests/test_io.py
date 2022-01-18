from weekplan import io
from weekplan import Project, Task


def test_project_export():
    p = Project("project_name")
    t1 = Task("task_name")
    t2 = Task("second_task")
    t1.add_date("2020-05-02")
    t1.add_date("2019-01-01")
    p.add_task(t1)
    p.add_task(t2)
    #print(io.save_project(p))
