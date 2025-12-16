# -*- coding: utf-8 -*-

from __future__ import annotations
import argparse
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from .config import Settings
from .utils.browser import create_driver
from .utils.files import ensure_dir
from .utils.dates import last_n_days
from .utils.log import log

from .crawlers.baemin import crawl_baemin
from .preprocess.baemin import preprocess_baemin_csv, save_baemin_excel

from .crawlers.idus import crawl_idus_download_excel
from .preprocess.idus import preprocess_latest_idus_excel, save_idus_excel, cleanup_idus_downloads

from .crawlers.okpos import crawl_okpos_download_excels
from .preprocess.okpos import merge_okpos_excels, save_okpos_excel, cleanup_okpos_downloads

def run_baemin(s: Settings, date_label: str) -> None:
    driver = create_driver(headless=s.headless)
    try:
        raw_csv = crawl_baemin(driver, s.BAEMIN_ID, s.BAEMIN_PW, date_label, s.download_dir)
        if not raw_csv:
            return
        df = preprocess_baemin_csv(raw_csv)
        save_baemin_excel(df, s.output_dir, date_label)
    finally:
        try: driver.quit()
        except Exception: pass

def run_idus(s: Settings, date_label: str) -> None:
    driver = create_driver(headless=s.headless)
    try:
        crawl_idus_download_excel(driver, s.IDUS_ID, s.IDUS_PW)
    finally:
        try: driver.quit()
        except Exception: pass

    df, path = preprocess_latest_idus_excel(s.download_dir)
    save_idus_excel(df, s.output_dir, date_label)
    cleanup_idus_downloads(s.download_dir)

def run_okpos(s: Settings, date_label: str) -> None:
    driver = create_driver(headless=s.headless)
    try:
        crawl_okpos_download_excels(driver, s.OKPOS_ID, s.OKPOS_PW, s.days)
    finally:
        try: driver.quit()
        except Exception: pass

    df = merge_okpos_excels(s.download_dir, pattern="*.xls*")
    save_okpos_excel(df, s.output_dir, date_label)
    cleanup_okpos_downloads(s.download_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channels", nargs="+", default=["all"], choices=["all", "baemin", "idus", "okpos"])
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--download-dir", type=str, default=None)
    parser.add_argument("--out-dir", type=str, default=None)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    s = Settings()
    # CLI override
    if args.days is not None:
        object.__setattr__(s, "days", args.days)  # type: ignore
    if args.download_dir is not None:
        object.__setattr__(s, "download_dir", args.download_dir)  # type: ignore
    if args.out_dir is not None:
        object.__setattr__(s, "output_dir", args.out_dir)  # type: ignore
    if args.headless:
        object.__setattr__(s, "headless", True)  # type: ignore

    ensure_dir(s.download_dir)
    ensure_dir(s.output_dir)

    dr = last_n_days(s.days)
    date_label = dr.label

    chs = args.channels
    if "all" in chs:
        chs = ["baemin", "idus", "okpos"]

    for ch in chs:
        log(f"RUN: {ch}")
        if ch == "baemin":
            run_baemin(s, date_label)
        elif ch == "idus":
            run_idus(s, date_label)
        elif ch == "okpos":
            run_okpos(s, date_label)

    log("DONE")

if __name__ == "__main__":
    main()
