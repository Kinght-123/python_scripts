# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # 服务器环境可能需要
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存问题
chrome_options.add_argument("--window-size=1920,1080")  # 设置窗口大小

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://10.188.73.101/")

    custom_headers = {
        "authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc0NzIwNDE3OCwiaWF0IjoxNzM5NDI4MTc4LCJqdGkiOiJjdW1wMmttZzBqYmZ2dHNkZ3IyMCIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJjb3UzanFhdG5uMHF0MzFxZ2k2ZyIsInNwYWNlX2lkIjoiY291M2pxYXRubjBxdDMxcWdpNDAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY291M2pxYXRubjBxdDMxcWdpM2ciLCJyb2xlcyI6WyJ2aWRlb19nZW5fYWNjZXNzIl19.ElKfITWqX8kQ0PIr69uzT2zKlsELbetpzJtG4Dz1pcaxRYa3rUIc0LG9a12C_epHYIUVdCoIZWhZDAaxJZGsWQ",
    }
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": custom_headers})

    driver.get("http://10.188.73.101/fleet/map")

    time.sleep(20)
    driver.save_screenshot('screenshot.png')
    print("截图已保存：screenshot.png")

finally:
    driver.quit()