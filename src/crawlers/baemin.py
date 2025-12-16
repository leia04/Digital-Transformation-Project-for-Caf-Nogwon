# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..utils.log import log
from ..utils.files import ensure_dir, move_file

BAEMIN_URL = "https://self.baemin.com/orders/history"

SEL_ID = '#root > div.style__LoginWrap-sc-145yrm0-0.hKiYRl > div > div > form > div:nth-child(1) > span > input[type=text]'
SEL_PW = '#root > div.style__LoginWrap-sc-145yrm0-0.hKiYRl > div > div > form > div.Input__InputWrap-sc-tapcpf-1.kjWnKT.mt-half-3 > span > input[type=password]'
SEL_LOGIN_BTN = '#root > div.style__LoginWrap-sc-145yrm0-0.hKiYRl > div > div > form > button'

X_POPUP_XPATH = '/html/body/div[4]/div/section/header/div/button/div'  # try/except로 닫음 :contentReference[oaicite:13]{index=13}

DURATION_BTN = '#root > div > div.frame-container > div.frame-wrap > div.frame-body > div.OrderHistoryPage-module__R0bB > div.FilterContainer-module___Rxt > button.FilterContainer-module__vSPY.FilterContainer-module__vOLM'
WEEK_TAB_XPATH = '/html/body/div[4]/div/section/div/div[1]/div[1]/label[1]/span'
LAST_7D_XPATH = '/html/body/div[4]/div/section/div/div[1]/div[2]/div/label[3]'

NEXT_PAGE_CSS = '*[aria-label="다음 페이지로 이동"] .button-overlay.css-fowwyy'

def crawl_baemin(driver, baemin_id: str, baemin_pw: str, date_label: str, download_dir: str) -> str | None:
    """
    Returns: saved CSV path (moved into download_dir) or None if no data.
    """
    if not baemin_id or not baemin_pw:
        raise ValueError("BAEMIN_ID/BAEMIN_PW is required (set env vars).")

    ensure_dir(download_dir)
    log("BAEMIN: open login page")
    driver.get(BAEMIN_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SEL_ID))).send_keys(baemin_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SEL_PW))).send_keys(baemin_pw)
    driver.find_element(By.CSS_SELECTOR, SEL_LOGIN_BTN).click()
    time.sleep(5)

    # popup close (best-effort)
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, X_POPUP_XPATH))).click()
    except Exception:
        pass

    # period: last 7days
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, DURATION_BTN))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, WEEK_TAB_XPATH))).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, LAST_7D_XPATH))).click()
    time.sleep(1)

    order_dict = {"주문시간": [], "주문번호": [], "배달유형": [], "주문상품": [], "매출": []}

    while True:
        time.sleep(2)
        try:
            details = driver.find_elements(By.CSS_SELECTOR, "div[class*='OrderHistoryListItem']")
            if not details:
                # fallback:
                break

            for detail in details:
                try:
                    times = detail.find_element(By.CSS_SELECTOR, "*[class*='OrderHistoryListItem'] *[class*='time']")
                    num = detail.find_element(By.CSS_SELECTOR, "*[class*='OrderHistoryListItem'] *[class*='orderNo']")
                    delivery_type = detail.find_element(By.CSS_SELECTOR, "*[class*='OrderHistoryListItem'] *[class*='deliveryType']")
                except Exception:
                    continue

                prods = detail.find_elements(By.CLASS_NAME, "DetailInfo-module__pC_2.FieldItem-module__gYJs")
                for prod in prods:
                    try:
                        product = prod.find_element(By.CLASS_NAME, "DetailInfo-module__nV94").text
                        price = prod.find_element(By.CLASS_NAME, "FieldItem-module__rb57").text
                    except Exception:
                        continue

                    order_dict["주문시간"].append(times.text)
                    order_dict["주문번호"].append(num.text)
                    order_dict["배달유형"].append(delivery_type.text)
                    order_dict["주문상품"].append(product)
                    order_dict["매출"].append(price)

            # next page
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_PAGE_CSS))).click()
            except Exception:
                break
        except Exception as e:
            log(f"BAEMIN: scraping error: {e}")
            break

    if not order_dict["주문시간"]:
        log(f"BAEMIN: no data for {date_label}, skip")
        return None

    df = pd.DataFrame(order_dict)
    csv_name = f"baemin_{date_label}_rowdata.csv"
    tmp_path = os.path.join(os.getcwd(), csv_name)
    df.to_csv(tmp_path, index=False, encoding="cp949")
    final_path = move_file(tmp_path, download_dir)
    log(f"BAEMIN: saved raw csv -> {final_path}")
    return final_path

