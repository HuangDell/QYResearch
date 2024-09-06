from src.util.config import  config
from . import report_writer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.util.report_item import ReportItem


class TargetSearch:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.get_search_page()
        self.reports=None

        print(self.url)
        pass

    '''
        用于获取qyr一页的搜索结果，存储在list中
    '''
    def get_one_page_list(self):
        ele = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div/div/div[2]/ul[1]'))
        )
        list_items = ele.find_elements(By.TAG_NAME,'li')
        list_urls = []
        self.reports=[]
        for item in list_items:
            price = item.find_element(By.XPATH,'./div[2]/div[1]/div/span').text
            if config.check_price(price):
                report=ReportItem()

                # 从list中读取部分数据
                date = item.find_element(By.XPATH,'./div[2]/div[2]/div[1]/div[1]/p').text.split(' ')[-1]
                category= item.find_element(By.XPATH,'./div[2]/div[2]/div[1]/div[3]/p/span').text
                pages =item.find_element(By.XPATH,'./div[2]/div[2]/div[1]/div[2]/p').text.split(' ')[-1]

                report.date=date
                report.category=category
                report.pages=pages
                report.price=price

                self.reports.append(report)
                list_urls.append(item.find_element(By.CLASS_NAME,'h3_p1').find_element(By.CLASS_NAME,'h3_p1').get_attribute('href'))
        return list_urls


    def get_report_info(self, list_urls):
        for index,url in enumerate(list_urls):
            self.reports[index].id = url.split('/')[-2]
            self.driver.get(config.combine_link(url))
            WebDriverWait(self.driver, 15).until(
                EC.url_to_be(url)
            )

    def record_data(self):
        report_writer.write_items(self.reports)
        report_writer.save()

    def start(self):
        self.driver.get(self.url)
        list_urls=self.get_one_page_list()
        self.get_report_info(list_urls)
        self.record_data()


