import os
import os.path
import dataclasses
from datetime import date, datetime
import json
import re
import configparser

from .base import Project

BASE_DIR = os.path.expanduser("~/.weekplan")
CONF_FILE = 'weekplan.ini'

SECT_INI_PROJECTS = 'projects'

def generate_ini_file() -> None:
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, CONF_FILE))
    if not config.has_section(SECT_INI_PROJECTS):
        config.add_section(SECT_INI_PROJECTS)
    for _file in os.listdir(BASE_DIR):
        if _file.endswith("json"):
            p = load_project_from_json(os.path.join(BASE_DIR, _file))
            config.set(SECT_INI_PROJECTS, p.name, _file)
    with open(os.path.join(BASE_DIR, CONF_FILE), 'w') as _conf_file:
        config.write(_conf_file)

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

def load_project_from_json(f: str) -> Project:
    with open(f, 'r') as json_file:
        project_dict = json.load(json_file)
    p = load_project_from_dict(project_dict)
    return p

def save_project(project: Project):
    _asdict = dataclasses.asdict(project)
    _filename = "{}.json".format(sanitize_name(project.name))
    target_file = os.path.join(BASE_DIR, _filename)
    with open(target_file, 'w') as out_file:
        json.dump(_asdict, out_file, default=_json_serial_datetime,
                  indent=4)
    return _asdict

def load_projects() -> list[Project]:
    projects = []
    for _file in os.listdir(BASE_DIR):
        if _file.endswith("json"):
            p = load_project_from_json(os.path.join(BASE_DIR, _file))
            projects.append(p)
    return projects
