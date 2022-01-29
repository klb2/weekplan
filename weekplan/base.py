from datetime import date as DATE
import dataclasses
from dataclasses import dataclass


@dataclass
class Task:
    name: str
    dates: list[DATE] = dataclasses.field(default_factory=list)
    completed: bool = False

    def __post_init__(self):
        _dates = []
        for _date in self.dates:
            if not isinstance(_date, DATE) and not _date is None:
                _date = DATE.fromisoformat(_date)
            _dates.append(_date)
        self.dates = _dates

    def add_date(self, date: (DATE, str)):
        if isinstance(date, str):
            date = DATE.fromisoformat(date)
        self.dates.append(date)
        self.dates = sorted(self.dates)


@dataclass
class Project:
    name: str
    description: str = ""
    created: DATE = DATE.today()
    completed: DATE = None
    tasks: list[Task] = dataclasses.field(default_factory=list)
    key: int = 0

    def __post_init__(self):
        for field in dataclasses.fields(self):
            if field.type == DATE:
                value = getattr(self, field.name)
                if not isinstance(value, field.type) and not value is None:
                    setattr(self, field.name, DATE.fromisoformat(value))
        self.tasks = [Task(**_t) for _t in self.tasks]

    def add_task(self, task: Task):
        self.tasks.append(task)
