# -*- coding: utf-8 -*-
from collections import OrderedDict
from pathlib import Path
import shutil
import tempfile
import unittest

from commons.settings import OrderedDictMergeException, get_settings, merge
from commons.zip import extract_from_zip, write_to_zip


class MainTestCase(unittest.TestCase):
    def test_get_settings_1(self) -> None:
        with self.assertRaisesRegex(Exception, 'Settings file does not exist'):
            get_settings(app_name='bla', app_author='bla')

    def test_get_settings_2(self) -> None:
        with self.assertRaisesRegex(Exception, r'Argument \'app_name\' does not exist'):
            get_settings(Path('bla.yaml'))

    def test_get_settings_3(self) -> None:
        self.assertIsInstance(get_settings(Path('tests/data/settings.yaml')), OrderedDict)

    def test_merge_1(self) -> None:
        a = OrderedDict()
        a['a'] = 1
        b = OrderedDict()
        b['a'] = 1
        self.assertIsInstance(merge(a, b), OrderedDict)

    def test_merge_2(self) -> None:
        a = OrderedDict()
        a['a'] = 1
        b = OrderedDict()
        b['a'] = 2
        with self.assertRaises(OrderedDictMergeException):
            merge(a, b)

    def test_merge_3(self) -> None:
        a = OrderedDict()
        a['b'] = OrderedDict([('a', 1)])
        b = OrderedDict()
        b['b'] = OrderedDict([('b', 2)])
        c = merge(a, b)
        self.assertIsInstance(c, OrderedDict)

    def test_extract_from_zip(self) -> None:
        temp_dir_fullpath = Path(tempfile.mkdtemp())
        extract_from_zip(Path('tests/data/test.zip'), temp_dir_fullpath)
        self.assertTrue(Path(temp_dir_fullpath, 'test.txt').is_file())
        shutil.rmtree(temp_dir_fullpath)

    def test_write_to_zip_1(self) -> None:
        temp_dir_fullpath = Path(tempfile.mkdtemp())
        write_to_zip(Path(temp_dir_fullpath, 'test.zip'), Path('tests/data/test.txt'))
        self.assertTrue(Path(temp_dir_fullpath, 'test.zip').is_file())
        shutil.rmtree(temp_dir_fullpath)

    def test_write_to_zip_2(self) -> None:
        temp_dir_fullpath = Path(tempfile.mkdtemp())
        write_to_zip(Path(temp_dir_fullpath, 'test.zip'), Path('tests/data/test'))
        self.assertTrue(Path(temp_dir_fullpath, 'test.zip').is_file())
        shutil.rmtree(temp_dir_fullpath)
