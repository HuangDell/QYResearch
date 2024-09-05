import time
from src.controller.search import TargetSearch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init():
    chrome_options = Options()
    custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    chrome_options.add_argument(f'user-agent={custom_user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def start(driver):
    crawler = TargetSearch(driver)
    crawler.start()
    time.sleep(5)
    pass


if __name__ == '__main__':
    driver = init()
    start(driver)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
