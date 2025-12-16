# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import shutil
from glob import glob
from typing import Optional, List

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def move_file(src_path: str, dst_dir: str) -> str:
    ensure_dir(dst_dir)
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))
    if os.path.abspath(src_path) == os.path.abspath(dst_path):
        return dst_path
    if os.path.exists(dst_path):
        os.remove(dst_path)
    shutil.move(src_path, dst_path)
    return dst_path

def latest_file_in_dir(dir_path: str) -> Optional[str]:
    if not os.path.isdir(dir_path):
        return None
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        return None
    return max(files, key=lambda p: os.path.getmtime(p))

def delete_globs(patterns: List[str]) -> int:
    removed = 0
    for pat in patterns:
        for p in glob(pat):
            try:
                os.remove(p)
                removed += 1
            except OSError:
                pass
    return removed


