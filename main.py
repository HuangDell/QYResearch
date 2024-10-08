import time
from src.controller.search import TargetSearch
from selenium import webdriver
from selenium.webdriver.edge.options import Options


def init():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # 在Windows上需要
    options.add_argument("--no-sandbox")  # 在某些环境中需要
    custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    options.add_argument(f'user-agent={custom_user_agent}')

    driver = webdriver.Edge(options=options)
    return driver


def start(driver):
    crawler = TargetSearch(driver)
    crawler.start()


if __name__ == '__main__':
    print('正在初始化环境，请稍等...')
    driver = init()
    start(driver)
    driver.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
