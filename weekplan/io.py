import os.path
import dataclasses
from datetime import date, datetime
import json
import re

from .base import Project

BASE_DIR = os.path.expanduser("~/.weekplan")

def _json_serial_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def sanitize_name(name: str) -> str:
    name = name.replace(" ", "-")
    name = name.lower()
    name = re.sub(r'[^-a-z0-9]+', "", name)
    name = name.encode("ascii", "ignore")
    name = name.decode("ascii")
    return name

def load_project_from_dict(d: dict) -> Project:
    p = Project(**d)
    return p

def save_project(project: Project):
    _asdict = dataclasses.asdict(project)
    _filename = "{}.json".format(sanitize_name(project.name))
    target_file = os.path.join(BASE_DIR, _filename)
    #with open(target_file, 'w') as out_file:
    #    json.dump(_asdict, out_file, default=_json_serial_datetime,
    #              indent=4)
    return _asdict
