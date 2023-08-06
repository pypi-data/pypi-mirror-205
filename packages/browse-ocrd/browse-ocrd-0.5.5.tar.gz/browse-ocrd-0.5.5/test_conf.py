from __future__ import annotations

import re
import shlex
import sys

from configparser import ConfigParser
from collections import defaultdict
from pydantic import BaseSettings, BaseModel as PydanticBaseModel, Field, validator
from rich import print as pprint
from shutil import which
from typing import Dict, Any, List, Optional


class _DummyObject:
    """
    Dummy object to test formatstrings with nested properties
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, shlex.quote(v) if isinstance(v, str) else v)


def _snake_case(s: str) -> str:
    return re.sub('(?!^)([A-Z]+)', r'_\1', s).lower()


def _split_regexes(cls, v: str) -> List[re.Pattern]:
    """
    Split a string at ',' and returns the parts as compiled regexes
    """
    try:
        return [re.compile(r.strip()) for r in v.split(',')]
    except re.error as e:
        raise ValueError(f'Error in pattern "{e.pattern}" @ pos {e.pos}: "{e.msg}"') from e


def _check_commandline(cls, v: str, **placeholders: _DummyObject) -> str:
    """
    Checks for a valid shell command string with placeholders

    1) does the executable exists
    2) Are only existing placeholders used
    """
    executable, *rest = shlex.split(v)
    if not which(executable):
        raise ValueError(f'Executable "{executable}" not found in "{v}"')
    try:
        v.format(**placeholders)
    except Exception as e:
        raise ValueError(f'{e!s} in "{v}"') from e
    return v


DUMMY_FILE = _DummyObject(
    ID='ID1',
    basename='IMG1.tif',
    basename_without_extension='IMG1',
    extension='tif',
    fileGrp='IMG',
    loctype='URL',
    mimetype='image/tiff',
    otherloctype=None,
    pageId='PAGE1',
    url='IMG/IMG1.tif',
    path=_DummyObject(absolute='/tmp/test/IMG/IMG1.tif', relative='IMG/IMG1.tif')
)

DUMMY_WORKSPACE = _DummyObject(directory='/tmp/test/', baseurl='/tmp/test/mets.xml')


class BaseModel(PydanticBaseModel):
    class Config:
        env_nested_delimiter = '__'


class Tool(BaseModel):
    commandline: str
    shortcut: Optional[str]

    @validator('commandline')
    @classmethod
    def check_commandline(cls, v):
        return _check_commandline(cls, v, file=DUMMY_FILE, workspace=DUMMY_WORKSPACE)


class View(BaseModel):
    groups: List[re.Pattern]

    split_groups = validator('groups', pre=True, allow_reuse=True)(_split_regexes)


class FileGroups(BaseModel):
    preferred_images: List[re.Pattern]

    split_preferred_images = validator('preferred_images', pre=True, allow_reuse=True)(_split_regexes)


class Settings(BaseSettings):
    file_groups: FileGroups
    tool: Dict[str, Tool] = Field({})
    view: Dict[str, View] = Field({})


configstr = """
[FileGroups]
preferredImages = OCR-D-IMG, OCR-D-IMG-*, ORIGINAL 

[Tool PageViewer]
commandline = /usr/bin/java -jar /home/jk/bin/JPageViewer/JPageViewer.jar --resolve-dir {workspace.directory} {file.path.absolute}

[Tool Open]
commandline = xdg-open {file.path.absolute}
shortcut = o
"""


def convert_config(conf: ConfigParser) -> Dict[str, Any]:
    config: Dict[str, Any] = defaultdict(dict)
    for section, values in conf.items():
        if section == 'DEFAULT':
            continue
        parts = section.split(' ', 2)
        top = _snake_case(parts[0])
        sub = parts[1] if len(parts) > 1 else None
        if sub:
            config[top][sub] = dict(values)
        else:
            config[top] = dict(values)

    return dict(config)


# field.field_info.extra['env_names']
if __name__ == "__main__":
    conf = ConfigParser()
    conf.optionxform = _snake_case
    conf.read_string(configstr)
    config = convert_config(conf)
    pprint(config)
    s = Settings.parse_obj(config)
    pprint(s)
    sys.exit()

# print(dict(config.items()))
