# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
from pathlib import Path
import time
from typing import List
import zipfile

from appdirs import site_data_dir, user_data_dir
import yaml
import yodl

__version__ = '1.1.0'


class SettingsException(Exception):
    pass


def get_settings(file_name: str = 'settings.yaml', **kwargs) -> OrderedDict:
    # Settings
    settings_file_path = Path(file_name)
    if not settings_file_path.is_file():
        app_name = None
        if 'app_name' in kwargs:
            app_name = kwargs['app_name']

        if app_name is None:
            raise AttributeError('Argument \'app_name\' does not exist!')

        app_author = None
        if 'app_author' in kwargs:
            app_author = kwargs['app_author']

        settings_file_path = Path(user_data_dir(app_name, app_author, roaming=True)) / settings_file_path.name
        if not settings_file_path.is_file():
            settings_file_path = Path(site_data_dir(app_name, app_author)) / settings_file_path.name
            if not settings_file_path.is_file():
                raise SettingsException('Settings file does not exist!')

    with settings_file_path.open(encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)

    return settings


class OrderedDictMergeException(Exception):
    pass


def merge(a: OrderedDict, b: OrderedDict, path: List[str] = None) -> OrderedDict:
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                raise OrderedDictMergeException('Conflict at {}'.format('.'.join(path + [str(key)])))
        else:
            a[key] = b[key]

    return a


def extract_from_zip(zip_path: Path, dir_path: Path) -> None:
    with zipfile.ZipFile(str(zip_path)) as zip_file:
        for zip_member in zip_file.infolist():
            zip_file.extract(zip_member, str(dir_path))
            zip_member_time = time.mktime(zip_member.date_time + (0, 0, -1))
            os.utime(str(dir_path / zip_member.filename), (zip_member_time, zip_member_time))


def write_to_zip(zip_path: Path, in_path: Path, file_paths: List[Path] = None) -> float:
    with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zip_file:
        mtime = -1.

        if in_path.is_file():
            zip_file.write(str(in_path), str(in_path.name))
            mtime = os.stat(str(in_path)).st_mtime
        elif in_path.is_dir():
            if not file_paths:
                file_paths = in_path.rglob('*')

            for file_path in file_paths:
                if file_path.is_file():
                    zip_file.write(str(file_path), str(file_path.relative_to(in_path)))
                    file_stat_result = os.stat(str(file_path))
                    if mtime < file_stat_result.st_mtime:
                        mtime = file_stat_result.st_mtime

        return mtime
