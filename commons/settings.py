# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
from typing import List

from appdirs import site_data_dir, user_data_dir
import yaml
import yodl


class SettingsException(Exception):
    pass


def get_settings(file_path: Path = Path('settings.yaml'), **kwargs) -> OrderedDict:
    # Settings
    if not file_path.is_file():
        app_name = None
        if 'app_name' in kwargs:
            app_name = kwargs['app_name']
        if app_name is None:
            raise AttributeError('Argument \'app_name\' does not exist!')
        app_author = None
        if 'app_author' in kwargs:
            app_author = kwargs['app_author']
        file_path = Path(user_data_dir(app_name, app_author, roaming=True)) / file_path.name
        if not file_path.is_file():
            file_path = Path(site_data_dir(app_name, app_author)) / file_path.name
            if not file_path.is_file():
                raise SettingsException('Settings file does not exist!')
    with file_path.open(encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)
    if settings is None:
        settings = OrderedDict()
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
                raise OrderedDictMergeException('Conflict at \'{0}\''.format('.'.join(path + [str(key)])))
        else:
            a[key] = b[key]
    return a
