# -*- coding: utf-8 -*-
from collections import OrderedDict
# noinspection PyCompatibility
from pathlib import Path

from appdirs import site_data_dir, user_data_dir
from six import PY2
import yaml
import yodl


class SettingsError(Exception):
    """Settings Error"""


def get_settings(file_path=Path('settings.yaml'), **kwargs):
    if PY2:
        def construct_yaml_str(loader, node):
            return loader.construct_scalar(node).encode('utf-8')

        yodl.OrderedDictYAMLLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)

    # Settings
    if not file_path.is_file():
        app_name = None
        if 'app_name' in kwargs:
            app_name = kwargs['app_name']
        if app_name is None:
            raise AttributeError('Argument \'app_name\' does not exist')
        app_author = None
        if 'app_author' in kwargs:
            app_author = kwargs['app_author']
        file_path = Path(user_data_dir(app_name, app_author, roaming=True)) / file_path.name
        if not file_path.is_file():
            file_path = Path(site_data_dir(app_name, app_author)) / file_path.name
            if not file_path.is_file():
                raise SettingsError('Settings file does not exist')
    with file_path.open(encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)
    if settings is None:
        settings = OrderedDict()
    return settings


class OrderedDictMergeException(Exception):
    # todo Добавить описание
    pass


def merge(a, b, path=None):
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
