import os.path
from datetime import date as DATE
import dataclasses
from dataclasses import dataclass
import configparser


BASE_DIR = os.path.expanduser("~/.weekplan")
CONF_FILE = 'weekplan.ini'
SECT_INI_PROJECTS = 'projects'

TEMPLATE_FILE = "templates.ini"


def _get_unique_dates(dates):
    _dates = set()
    for _date in dates:
        if not isinstance(_date, DATE) and not _date is None:
            _date = DATE.fromisoformat(_date)
        _dates.add(_date)
    return sorted(_dates)

@dataclass
class Task:
    name: str
    dates: list[DATE] = dataclasses.field(default_factory=list)
    completed: bool = False

    def __post_init__(self):
        self.dates = _get_unique_dates(self.dates)

    def add_date(self, date: (DATE, str)):
        if isinstance(date, str):
            date = DATE.fromisoformat(date)
        if date not in self.dates:
            self.dates.append(date)
        self.dates = sorted(self.dates)


@dataclass
class Project:
    name: str
    description: str = ""
    created: DATE = DATE.today()
    completed: DATE = None
    dates: list[DATE] = dataclasses.field(default_factory=list)
    tasks: list[Task] = dataclasses.field(default_factory=list)
    key: int = 0

    def __post_init__(self):
        for field in dataclasses.fields(self):
            if field.type == DATE:
                value = getattr(self, field.name)
                if not isinstance(value, field.type) and not value is None:
                    setattr(self, field.name, DATE.fromisoformat(value))
        self.tasks = [Task(**_t) for _t in self.tasks]
        self.dates = _get_unique_dates(self.dates)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_date(self, date: (DATE, str)):
        if isinstance(date, str):
            date = DATE.fromisoformat(date)
        if date not in self.dates:
            self.dates.append(date)
        self.dates = sorted(self.dates)


def create_project_from_template(name, template: str, **kwargs) -> Project:
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, TEMPLATE_FILE))
    template = template.lower()
    tasks = config.get(template, "tasks")
    tasks = tasks.strip()
    tasks = tasks.split("\n")
    p = Project(name, **kwargs)
    for _task in tasks:
        _t = Task(_task)
        p.add_task(_t)
    return p
