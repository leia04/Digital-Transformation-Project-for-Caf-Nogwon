# -*- coding: utf-8 -*-

from __future__ import annotations
import os
from glob import glob
from datetime import datetime
import pandas as pd

from ..utils.dates import to_excel_date, to_excel_time_hms
from ..utils.files import ensure_dir, delete_globs
from ..utils.log import log

def preprocess_okpos_df(df: pd.DataFrame) -> pd.DataFrame:
    date_hint = df.iloc[1, 0].split("조회일자 : ")[1].strip()
    df = df.drop([0, 2, 3]).reset_index(drop=True)

    updated_value = df.iloc[0, 0].replace("조회일자 : ", "")
    df.iloc[:, 0] = updated_value
    df = df.drop(0).reset_index(drop=True)

    df.iloc[0, 0] = "조회일자"
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)
    df = df.iloc[:-1, :]

    df = df.sort_values(by=["조회일자", "영수증번호"]).reset_index(drop=True)
    df["상품명"] = df["상품명"].astype(str).str.replace("HOT|ICED|ICE|TOGO", "", regex=True).str.rstrip()
    df["상품명"] = df["상품명"].replace(["청귤 캐모마일", "청귤캐모마일"], "청캐", regex=True)

    drop_cols = [
        "조회일자","테이블명","최초주문","상품코드","바코드","ERP 매핑코드","비고",
        "할인구분","할인액","실매출액","가액","부가세"
    ]
    drop_cols = [c for c in drop_cols if c in df.columns]
    df = df.drop(drop_cols, axis=1, errors="ignore")

    date_obj = datetime.strptime(date_hint, "%Y-%m-%d")
    weekday_names = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]
    df["조회요일"] = weekday_names[date_obj.weekday()]

    df["조회일자_excel"] = to_excel_date(date_obj)
    if "최종주문시각" in df.columns:
        df["최종주문시각_excel"] = df["최종주문시각"].astype(str).apply(lambda s: to_excel_time_hms(s, assume_pm_if_lt_12=False))

    return df

def merge_okpos_excels(download_dir: str, pattern: str = "*.xls*") -> pd.DataFrame:
    files = sorted(glob(os.path.join(download_dir, pattern)))
    if not files:
        raise FileNotFoundError(f"No OKPOS excel files in {download_dir}")

    out = []
    for p in files:
        try:
            raw = pd.read_excel(p, header=None)
            out.append(preprocess_okpos_df(raw))
        except Exception as e:
            log(f"OKPOS: preprocess failed for {p}: {e}")

    if not out:
        return pd.DataFrame()
    return pd.concat(out, ignore_index=True)

def save_okpos_excel(df: pd.DataFrame, out_dir: str, date_label: str) -> str:
    ensure_dir(out_dir)
    out_path = os.path.join(out_dir, f"okpos_{date_label}.xlsx")
    df.to_excel(out_path, index=False)
    log(f"OKPOS: saved excel -> {out_path}")
    return out_path

def cleanup_okpos_downloads(download_dir: str) -> int:
    removed = delete_globs([os.path.join(download_dir, "*.xls*")])
    log(f"OKPOS: cleanup removed={removed}")
    return removed


