# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path

from appdirs import site_data_dir, user_data_dir
import yaml
import yodl


class SettingsError(Exception):
    """Settings Error"""


def get_settings(file_path=Path('settings.yaml'), **kwargs) -> OrderedDict:
    # Settings
    file_fullpath = file_path.absolute()
    if not file_fullpath.is_file():
        app_name = None
        if 'app_name' in kwargs:
            app_name = kwargs['app_name']
        if app_name is None:
            raise AttributeError('Argument \'app_name\' does not exist')
        app_author = None
        if 'app_author' in kwargs:
            app_author = kwargs['app_author']
        file_fullpath = Path(user_data_dir(app_name, app_author, roaming=True), file_path)
        if not file_fullpath.is_file():
            file_fullpath = Path(site_data_dir(app_name, app_author), file_path)
    if file_fullpath.is_file():
        with file_fullpath.open(encoding='utf-8') as settings_file:
            settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)
        if settings is None:
            settings = OrderedDict()
    else:
        settings = OrderedDict()
    return settings


class OrderedDictMergeException(Exception):
    """Ordered Dict Merge Exception"""


def merge(a: dict, b: dict, path=None) -> dict:
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
