# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List
import zipfile

import time


def extract_from_zip(zip_path: Path, dir_path: Path) -> None:
    with zipfile.ZipFile(str(zip_path)) as zip_file:
        for zip_member in zip_file.infolist():
            zip_file.extract(zip_member, str(dir_path))
            zip_member_time = time.mktime(zip_member.date_time + (0, 0, -1))
            os.utime(str(dir_path / zip_member.filename), (zip_member_time, zip_member_time))


def write_to_zip(zip_path: Path, in_path: Path, file_paths: List[Path] = None) -> float:
    with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zip_file:
        mtime = -1.
        if in_path.is_file():
            zip_file.write(str(in_path), str(in_path.name))
            mtime = os.stat(str(in_path)).st_mtime
        elif in_path.is_dir():
            if not file_paths:
                file_paths = in_path.rglob('*')
            for file_path in file_paths:
                if file_path.is_file():
                    zip_file.write(str(file_path), str(file_path.relative_to(in_path)))
                    file_stat_result = os.stat(str(file_path))
                    if mtime < file_stat_result.st_mtime:
                        mtime = file_stat_result.st_mtime
        return mtime
