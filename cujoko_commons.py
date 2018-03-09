# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path

from appdirs import site_data_dir, user_data_dir
import yaml
import yodl

__version__ = '1.0.0'


class SettingsException(Exception):
    pass


def get_settings(app_name: str, app_author: str, file_name: str = 'settings.yaml') -> OrderedDict:
    # Settings
    settings_file_path = Path(file_name)
    if not settings_file_path.is_file():
        settings_file_path = Path(user_data_dir(app_name, app_author, roaming=True)) / settings_file_path.name
        if not settings_file_path.is_file():
            settings_file_path = Path(site_data_dir(app_name, app_author)) / settings_file_path.name
            if not settings_file_path.is_file():
                raise SettingsException('Settings file does not exist!')

    with settings_file_path.open(encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)

    return settings
