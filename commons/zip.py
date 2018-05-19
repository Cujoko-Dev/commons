# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import time
import zipfile


def extract_from_zip(zip_name, dir_name):
    with zipfile.ZipFile(zip_name) as zip_file:
        for zip_member in zip_file.infolist():
            zip_file.extract(zip_member, dir_name)
            zip_member_time = time.mktime(zip_member.date_time + (0, 0, -1))
            os.utime(os.path.join(dir_name, zip_member.filename), (zip_member_time, zip_member_time))


def write_to_zip(zip_name, in_name, file_names=None):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        mtime = -1.
        if os.path.isfile(in_name):
            zip_file.write(in_name, os.path.basename(in_name))
            mtime = os.stat(in_name).st_mtime
        elif os.path.isdir(in_name):
            if not file_names:
                file_names = in_name.rglob('*')
            for file_name in file_names:
                if os.path.isfile(file_name):
                    zip_file.write(file_name, os.path.relpath(file_name, in_name))
                    file_stat_result = os.stat(file_name)
                    if mtime < file_stat_result.st_mtime:
                        mtime = file_stat_result.st_mtime
        return mtime
