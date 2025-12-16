# -*- coding: utf-8 -*-

from __future__ import annotations
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..utils.log import log

OKPOS_URL = "https://kis.okpos.co.kr/login/login_form.jsp"

def crawl_okpos_download_excels(driver, okpos_id: str, okpos_pw: str, days: int) -> None:
    if not okpos_id or not okpos_pw:
        raise ValueError("OKPOS_ID/OKPOS_PW is required (set env vars).")

    current = datetime.now()
    start = current - timedelta(days=days)
    date_list = [start + timedelta(days=i) for i in range(days)]
    formatted = [d.strftime("%Y-%m-%d") for d in date_list]

    log("OKPOS: open login page")
    driver.get(OKPOS_URL)
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user_id"))).send_keys(okpos_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user_pwd"))).send_keys(okpos_pw)
    driver.find_element(By.CSS_SELECTOR, "#loginForm > div:nth-child(4) > div:nth-child(5) > img").click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cswmMenuButtonGroup_15"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cswmItemGroup_15_6"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cswmItem6_24"))).click()
    time.sleep(1)

    iframe = driver.find_element(By.ID, "MainFrm")
    driver.switch_to.frame(iframe)

    for d in formatted:
        driver.execute_script(f"document.getElementById('date1').value = '{d}';")
        driver.find_element(By.XPATH, '//*[@id="form1"]/div/div[1]/div[4]/button[1]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="form1"]/div/div[1]/div[4]/button[2]').click()
        time.sleep(1)

        try:
            alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
            alert.accept()
            log(f"OKPOS: no data for {d}")
        except Exception:
            pass

    log("OKPOS: download flow done")

