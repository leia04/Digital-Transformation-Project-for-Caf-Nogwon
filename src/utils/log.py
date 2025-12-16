# -*- coding: utf-8 -*-

from __future__ import annotations
import datetime as dt

def log(msg: str) -> None:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
