# -*- coding: utf-8 -*-

from __future__ import annotations
from selenium import webdriver

def create_driver(headless: bool = False) -> webdriver.Chrome:
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("disable-gpu")
    opts.add_argument("lang=ko_KR")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )
    if headless:
        opts.add_argument("--headless=new")
    return webdriver.Chrome(options=opts)

