# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, date

@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime
    label: str

def last_n_days(days: int) -> DateRange:
    now = datetime.now()
    start = now - timedelta(days=days)
    yesterday = now - timedelta(days=1)
    label = f"{start.strftime('%Y-%m-%d')}_{yesterday.strftime('%Y-%m-%d')}"
    return DateRange(start=start, end=yesterday, label=label)

def iter_days(start_dt: datetime, days: int):
    base = start_dt.date()
    for i in range(days):
        yield base + timedelta(days=i)

def to_excel_date(dt: datetime) -> int:
    excel_base = datetime(1900, 1, 1)
    return (dt - excel_base).days + 2

def to_excel_time_hms(time_str: str, assume_pm_if_lt_12: bool = False) -> float:
    t = datetime.strptime(time_str, "%H:%M:%S")
    if assume_pm_if_lt_12 and t.hour < 12:
        t = t + timedelta(hours=12)
    excel_base = datetime(1900, 1, 1)
    return (t - excel_base).total_seconds() / (24 * 60 * 60)

