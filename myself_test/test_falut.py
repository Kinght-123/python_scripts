from selenium import webdriver

# 获取 chromedriver 的路径
chromedriver_path = webdriver.Chrome().service.path
print("Chromedriver 路径：", chromedriver_path)