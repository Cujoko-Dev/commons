# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import codecs
from collections import OrderedDict
import os

from appdirs import site_data_dir, user_data_dir
from six import PY2
import yaml
import yodl


class SettingsError(Exception):
    """Settings Error"""


def get_settings(file_name='settings.yaml', **kwargs):
    if PY2:
        def construct_yaml_unicode(loader, node):
            return loader.construct_scalar(node)

        yodl.OrderedDictYAMLLoader.add_constructor(u'tag:yaml.org,2002:unicode', construct_yaml_unicode)

    # Settings
    file_fullname = os.path.abspath(file_name)
    if not os.path.isfile(file_fullname):
        app_name = None
        if 'app_name' in kwargs:
            app_name = kwargs['app_name']
        if app_name is None:
            raise AttributeError('Argument \'app_name\' does not exist')
        app_author = None
        if 'app_author' in kwargs:
            app_author = kwargs['app_author']
        file_fullname = os.path.join(user_data_dir(app_name, app_author, roaming=True), file_name)
        if not os.path.isfile(file_fullname):
            file_fullname = os.path.join(site_data_dir(app_name, app_author), file_name)
            if not os.path.isfile(file_fullname):
                raise SettingsError('Settings file does not exist')
    with codecs.open(file_fullname, encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)
    if settings is None:
        settings = OrderedDict()
    return settings


class OrderedDictMergeException(Exception):
    """Ordered Dict Merge Exception"""


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
