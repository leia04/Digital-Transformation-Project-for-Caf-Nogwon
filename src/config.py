# -*- coding: utf-8 -*-

from __future__ import annotations
import os
from dataclasses import dataclass

def _get_env(key: str, default: str = "") -> str:
    v = os.getenv(key)
    return v if v is not None and v.strip() != "" else default

@dataclass(frozen=True)
class Settings:
    # download / output
    download_dir: str = _get_env("DOWNLOAD_DIR", "./downloads")
    output_dir: str = _get_env("OUTPUT_DIR", "./output")

    # crawling period
    days: int = int(_get_env("DAYS", "7"))

    # selenium
    headless: bool = _get_env("HEADLESS", "0") in ("1", "true", "True", "TRUE")

    # credentials
    BAEMIN_ID: str = _get_env("BAEMIN_ID")
    BAEMIN_PW: str = _get_env("BAEMIN_PW")
    IDUS_ID: str = _get_env("IDUS_ID")
    IDUS_PW: str = _get_env("IDUS_PW")
    OKPOS_ID: str = _get_env("OKPOS_ID")
    OKPOS_PW: str = _get_env("OKPOS_PW")

