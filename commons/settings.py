# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
from typing import Any

from appdirs import site_data_dir, user_data_dir
import yaml
import yodl


def get_attribute(
        kwargs: dict, kwargs_key: str, settings: OrderedDict = None, settings_key: str = None,
        default: Any = None, type_: type = str, allow_none: bool = False) -> Any:
    result = None
    type__ = type_
    if default is not None:
        type__ = type(default)
    if kwargs_key in kwargs:
        result = kwargs[kwargs_key]
        if not isinstance(result, type__):
            raise TypeError('{0}'.format(kwargs_key) if kwargs_key else None)
    if settings is not None and settings_key is not None:
        if settings_key in settings:
            result = settings[settings_key]
            if not isinstance(result, type__):
                raise TypeError('{0}'.format(settings_key) if settings_key else None)
        else:
            raise AttributeError('{0}'.format(settings_key))
    else:
        raise AttributeError('{0}'.format(kwargs_key))
    if result is None:
        result = default
    if result is None and not allow_none:
        raise ValueError('{0}'.format(settings_key))
    return result


def get_path_attribute(
        kwargs: dict, kwargs_key: str, settings: OrderedDict = None, settings_key: str = None,
        default_path: Path = None, is_dir: bool = True, check_if_exists: bool = True, create_dir: bool = True,
        create_parents: bool = True) -> Path:
    if kwargs_key in kwargs:
        result = kwargs[kwargs_key]
        if not isinstance(result, Path):
            raise TypeError('{0}'.format(kwargs_key) if kwargs_key else None)
    elif settings is not None and settings_key is not None:
        if settings_key in settings:
            result_str = settings[settings_key]
            if not isinstance(result_str, str):
                raise TypeError('{0}'.format(settings_key) if settings_key else None)
            result = Path(result_str)
            if not isinstance(result, Path):
                raise TypeError('{0}'.format(settings_key) if settings_key else None)
        else:
            raise AttributeError('{0}'.format(settings_key))
    else:
        raise AttributeError('{0}'.format(kwargs_key))
    if result is None and isinstance(default_path, Path):
        result = default_path
    if result is None:
        raise ValueError('{0}'.format(settings_key))
    if result.exists():
        if not is_dir and result.is_dir():
            raise FileExistsError('{0} Not A File'.format(kwargs_key) if kwargs_key else None, result)
        elif is_dir and result.is_file():
            raise NotADirectoryError('{0}'.format(kwargs_key) if kwargs_key else None, result)
    else:
        if check_if_exists:
            raise FileExistsError('{0}'.format(kwargs_key) if kwargs_key else None, result)
        if is_dir and create_dir:
            result.mkdir(parents=create_parents)
    return result


class SettingsError(Exception):
    """Settings Error"""


def get_settings(file_path=Path('settings.yaml'), **kwargs) -> OrderedDict:
    # Settings
    if not file_path.is_file():
        app_name = kwargs.get('app_name', None)
        if not isinstance(app_name, str):
            raise AttributeError('Argument "app_name" Not Exists')

        app_author = kwargs.get('app_author', None)
        if not isinstance(app_author, str):
            raise AttributeError('Argument "app_author" Not Exists')

        file_path = Path(user_data_dir(app_name, app_author, roaming=True), file_path)
        if not file_path.is_file():
            file_path = Path(site_data_dir(app_name, app_author), file_path)

    if file_path.is_file():
        with file_path.open(encoding='utf-8') as settings_file:
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
