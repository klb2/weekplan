from datetime import datetime
import dataclasses
from dataclasses import dataclass


@dataclass
class Task:
    name: str
    dates: list[datetime] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        for field in dataclasses.fields(self):
            if field.type == datetime:
                value = getattr(self, field.name)
                if not isinstance(value, field.type) and not value is None:
                    print(type(value))
                    setattr(self, field.name, datetime.fromisoformat(value))

    def add_date(self, date: (datetime, str)):
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        self.dates.append(date)
        self.dates = sorted(self.dates)

@dataclass
class Project:
    name: str
    description: str = ""
    created: datetime = datetime.now()
    completed: datetime = None
    tasks: list[Task] = dataclasses.field(default_factory=list)
    key: int = 0

    def __post_init__(self):
        for field in dataclasses.fields(self):
            if field.type == datetime:
                value = getattr(self, field.name)
                if not isinstance(value, field.type) and not value is None:
                    print(type(value))
                    setattr(self, field.name, datetime.fromisoformat(value))

    def add_task(self, task: Task):
        self.tasks.append(task)

