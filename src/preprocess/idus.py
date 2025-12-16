# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import re
import pandas as pd
from datetime import datetime

from ..utils.files import latest_file_in_dir, ensure_dir, move_file, delete_globs
from ..utils.log import log

def remove_emoji(s: str) -> str:
    return s.encode("cp949", "ignore").decode("cp949")

def preprocess_latest_idus_excel(download_dir: str) -> tuple[pd.DataFrame, str]:
    path = latest_file_in_dir(download_dir)
    if not path:
        raise FileNotFoundError(f"No downloaded file found in {download_dir}")

    xls = pd.ExcelFile(path)
    df1 = pd.read_excel(xls, sheet_name=0)

    for c in df1.columns:
        if df1[c].dtype == object:
            df1[c] = df1[c].astype(str).map(remove_emoji)

    return df1, path

def save_idus_excel(df: pd.DataFrame, out_dir: str, date_label: str) -> str:
    ensure_dir(out_dir)
    out_path = os.path.join(out_dir, f"idus_{date_label}.xlsx")
    df.to_excel(out_path, index=False)
    log(f"IDUS: saved excel -> {out_path}")
    return out_path

def cleanup_idus_downloads(download_dir: str) -> int:
    today = datetime.now().strftime("%Y%m%d")
    patterns = [
        os.path.join(download_dir, f"order_list*{today}*"),
    ]
    removed = delete_globs(patterns)
    log(f"IDUS: cleanup removed={removed}")
    return removed


