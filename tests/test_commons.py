# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
import os
import shutil
import tempfile
import unittest

from six import assertRaisesRegex

from commons.compat import u
from commons.settings import OrderedDictMergeException, get_settings, merge
from commons.zip import extract_from_zip, write_to_zip


class MainTestCase(unittest.TestCase):
    def test_get_settings_1(self):
        with assertRaisesRegex(self, Exception, 'Settings file does not exist'):
            get_settings(app_name='bla', app_author='bla')

    def test_get_settings_2(self):
        with assertRaisesRegex(self, Exception, r'Argument \'app_name\' does not exist'):
            get_settings('bla.yaml')

    def test_get_settings_3(self):
        self.assertIsInstance(get_settings('tests/data/settings.yaml'), OrderedDict)

    def test_merge_1(self):
        a = OrderedDict()
        a['a'] = 1
        b = OrderedDict()
        b['a'] = 1
        self.assertIsInstance(merge(a, b), OrderedDict)

    def test_merge_2(self):
        a = OrderedDict()
        a['a'] = 1
        b = OrderedDict()
        b['a'] = 2
        with self.assertRaises(OrderedDictMergeException):
            merge(a, b)

    def test_merge_3(self):
        a = OrderedDict()
        a['b'] = OrderedDict([('a', 1)])
        b = OrderedDict()
        b['b'] = OrderedDict([('b', 2)])
        c = merge(a, b)
        self.assertIsInstance(c, OrderedDict)

    def test_extract_from_zip(self):
        temp_dir_fullname = u(tempfile.mkdtemp())
        extract_from_zip('tests/data/test.zip', temp_dir_fullname)
        self.assertTrue(os.path.isfile(os.path.join(temp_dir_fullname, 'test.txt')))
        shutil.rmtree(temp_dir_fullname)

    def test_write_to_zip_1(self):
        temp_dir_fullname = u(tempfile.mkdtemp())
        write_to_zip(os.path.join(temp_dir_fullname, 'test.zip'), 'tests/data/test.txt')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir_fullname, 'test.zip')))
        shutil.rmtree(temp_dir_fullname)

    def test_write_to_zip_2(self):
        temp_dir_fullname = u(tempfile.mkdtemp())
        write_to_zip(os.path.join(temp_dir_fullname, 'test.zip'), 'tests/data/test')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir_fullname, 'test.zip')))
        shutil.rmtree(temp_dir_fullname)
