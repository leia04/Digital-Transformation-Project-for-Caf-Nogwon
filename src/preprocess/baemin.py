# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import pandas as pd
from datetime import datetime

from ..utils.dates import to_excel_date, to_excel_time_hms
from ..utils.files import ensure_dir, delete_globs
from ..utils.log import log

def preprocess_baemin_csv(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path, encoding="cp949")
    if df.empty:
        return df

    df[["조회일자", "조회요일", "결제시각"]] = df["주문시간"].str.split(". \\(|\\n", expand=True)
    df.drop("주문시간", axis=1, inplace=True)
    df[["구분", "주문번호_상세"]] = df["주문번호"].str.split("\\n", expand=True)
    df["수량"] = df["주문상품"].str.extract(r"(\\d+개?$)")
    df["상품명"] = df["주문상품"].str.replace(r"\\d+개?$", "", regex=True).str.strip()
    df.drop("주문상품", axis=1, inplace=True)
    df.rename(columns={"매출": "총매출액"}, inplace=True)

    df["총매출액"] = (
        df["총매출액"].astype(str).str.replace(",", "").str.replace("원", "").str.strip()
    )
    df["총매출액"] = pd.to_numeric(df["총매출액"], errors="coerce").fillna(0).astype(int)

    df["조회일자_dt"] = pd.to_datetime(df["조회일자"], errors="coerce")
    df["조회일자_excel"] = df["조회일자_dt"].apply(lambda x: to_excel_date(x.to_pydatetime()) if pd.notna(x) else None)

    df["결제시각_excel"] = df["결제시각"].apply(lambda s: to_excel_time_hms(str(s), assume_pm_if_lt_12=True))

    cols = [
        "조회일자", "조회요일", "결제시각",
        "구분", "주문번호_상세", "배달유형", "상품명", "수량", "총매출액",
        "조회일자_excel", "결제시각_excel",
    ]
    cols = [c for c in cols if c in df.columns]
    return df[cols]

def save_baemin_excel(df: pd.DataFrame, out_dir: str, date_label: str) -> str:
    ensure_dir(out_dir)
    out_path = os.path.join(out_dir, f"baemin_{date_label}.xlsx")
    df.to_excel(out_path, index=False)
    log(f"BAEMIN: saved excel -> {out_path}")
    return out_path


