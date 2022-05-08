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
    categories: set[str] = dataclasses.field(default_factory=set)
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

    def remove_date(self, date: (DATE, str)):
        if isinstance(date, str):
            date = DATE.fromisoformat(date)
        if date in self.dates:
            self.dates.remove(date)
        self.dates = sorted(self.dates)

    def add_category(self, category: str):
        self.categories.add(category)


def create_project_from_template(name, template: str, **kwargs) -> Project:
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, TEMPLATE_FILE))
    template = template.lower()
    p = Project(name, **kwargs)
    _keys = {"tasks": (Task, p.add_task),
             "categories": (str, p.add_category),
            }
    for _key, (_class, _add_func) in _keys.items():
        try:
            group = config.get(template, _key)
        except configparser.NoOptionError:
            continue
        group = group.strip()
        group = group.split("\n")
        for _item in group:
            _t = _class(_item)
            _add_func(_t)
    return p
