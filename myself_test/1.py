# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# 设置 Chrome 的无头模式参数
def configure_chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return options


# 初始化 WebDriver
def initialize_driver():
    options = configure_chrome_options()
    return webdriver.Chrome(options=options)


# 设置自定义请求头
def set_custom_headers(driver, headers):
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})


# 等待页面加载
def wait_for_page_load(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def main():
    driver = initialize_driver()

    try:
        # 打开首页
        driver.get("http://10.188.73.101/")
        wait_for_page_load(driver)

        # 设置自定义请求头
        custom_headers = {
            "authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc0NzIwNDE3OCwiaWF0IjoxNzM5NDI4MTc4LCJqdGkiOiJjdW1wMmttZzBqYmZ2dHNkZ3IyMCIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJjb3UzanFhdG5uMHF0MzFxZ2k2ZyIsInNwYWNlX2lkIjoiY291M2pxYXRubjBxdTMxcWdpNDAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY291M2pxYXRubjBxdTMxcWdpM2ciLCJyb2xlcyI6WyJ2aWRlb19nZW5fYWNjZXNzIl19.ElKfITWqX8kQ0PIr69uzT2zKlsELbetpzJtG4Dz1pcaxRYa3rUIc0LG9a12C_epHYIUVdCoIZWhZDAaxJZGsWQ"
        }
        set_custom_headers(driver, custom_headers)

        # 打开目标页面
        driver.get("http://10.188.73.101/fleet/map")
        wait_for_page_load(driver)

        # 等待页面完全加载
        time.sleep(5)

        # 保存截图
        driver.save_screenshot('screenshot.png')
        print("截图已保存：screenshot.png")

    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()