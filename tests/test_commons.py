# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
import tempfile
import unittest

from commons.settings import OrderedDictMergeException, get_settings, merge
from commons.zip import extract_from_zip, write_to_zip


class MainTestCase(unittest.TestCase):
    def test_get_settings_1(self):
        with self.assertRaisesRegex(Exception, 'Settings file does not exist!'):
            get_settings(app_name='bla', app_author='bla')

    def test_get_settings_2(self):
        with self.assertRaisesRegex(Exception, r'Argument \'app_name\' does not exist!'):
            get_settings(Path('bla.yaml'))

    def test_get_settings_3(self):
        self.assertIsInstance(get_settings(Path('tests/data/settings.yaml')), OrderedDict)

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
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir_path = Path(temp_dir_name)
            extract_from_zip(Path('tests/data/test.zip'), temp_dir_path)
            self.assertTrue(Path(temp_dir_name, 'test.txt').is_file())

    def test_write_to_zip_1(self):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir_path = Path(temp_dir_name)
            write_to_zip(temp_dir_path / 'test.zip', Path('tests/data/test.txt'))
            self.assertTrue((temp_dir_path / 'test.zip').is_file())

    def test_write_to_zip_2(self):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir_path = Path(temp_dir_name)
            write_to_zip(temp_dir_path / 'test.zip', Path('tests/data/test'))
            self.assertTrue((temp_dir_path / 'test.zip').is_file())
