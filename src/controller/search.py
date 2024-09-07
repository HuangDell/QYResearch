from src.util.config import  config
from . import report_writer,record_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.controller.page_controller import PageController
from src.controller.content_parser import ContentParser

from src.util.report_item import ReportItem


class TargetSearch:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.get_search_page()
        self.controller = PageController(self.driver)
        self.record = record_manager.load()
        self.parser = ContentParser()
        self.reports=None

        print(self.url)
        pass

    def start(self):
        self.driver.get(self.url)

        while not self.choose_page():
            pass

        while True:
            list_urls=self.get_one_page_list()
            self.get_report_info(list_urls)
            self.record_data()
            if not self.goto_next_page():
                print("所有数据抓取完毕，爬虫结束...")
                break
            print(f'Page {self.record.page} 爬取完毕，现在爬取 Page {self.record.page+1}')
            self.record_page()
            break
        pass


    '''
        用于获取qyr一页的搜索结果，存储在list中
    '''
    def get_one_page_list(self):
        self.controller.scroll_to_top()
        ele = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div/div/div[2]/ul[1]'))
        )
        list_items = ele.find_elements(By.TAG_NAME,'li')
        list_urls = []
        self.reports=[]

        for index in range(self.record.index,len(list_items)):
            item = list_items[index]
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


    def choose_page(self):
        self.controller.scroll_to_bottom()
        # 定位到页码视图
        pages_view = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[4]/div/div/div[2]/div[2]/div/ul'))
        )
        pages_list = pages_view.find_elements(By.TAG_NAME,'li')
        # 三种情况的页码处理
        search_range=range(5)
        jump_page=pages_list[4]
        if pages_list[1].get_attribute('class')=='el-icon more btn-quickprev el-icon-more'\
                and pages_list[5].get_attribute('class')=='el-icon more btn-quicknext el-icon-more':
            search_range=range(2,5)
            jump_page=pages_list[5]
        elif pages_list[1].get_attribute('class')=='el-icon more btn-quickprev el-icon-more':
            search_range=range(2,6)

        for index in search_range:
            # 找到目标页面就点击并且返回函数
            if str(self.record.page)==pages_list[index].text:
                pages_list[index].click()
                return True
        jump_page.click()
        return False


    """
    爬取文章详情页面的数据
    """
    def get_report_info(self, list_urls):
        for index,url in enumerate(list_urls):
            self.reports[index].id = url.split('/')[-2]
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(
                EC.url_to_be(url)
            )

            first_ph_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/pre[3]')))

            title_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/h1'))
            )

            companies_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id ="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/ul/li[contains(., \'Companies Covered\')]/following-sibling::li[1]'))
            )
            type_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/ul/li[contains(., \'by Type\')]/following-sibling::li[1]')
                )
            )
            application_element=WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/ul/li[contains(., \'by Application\')]/following-sibling::li[1]')
                )
            )

            million_digit,cagr_digit,summary= self.parser.parser_first_ph(first_ph_element.text)
            title = self.parser.parser_title(title_element.text)
            companies_text = companies_element.text.strip()
            type_text = type_element.text.strip()


            self.reports[index].million_digit=million_digit
            self.reports[index].cagr_digit=cagr_digit
            self.reports[index].title=title
            self.reports[index].summary_text=summary
            self.reports[index].companies_text=companies_text
            self.reports[index].type_text=type_text




    def record_data(self):
        report_writer.write_items(self.reports)
        report_writer.save()


    def goto_next_page(self):
        self.controller.scroll_to_bottom()
        next_button = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[4]/div/div/div[2]/div[2]/div/button[2]'))
        )
        if next_button.get_attribute('disabled')=='disabled':
            return False

        next_button.click()
        return True

    def record_page(self):
        self.record.page+=1
        self.record.index=0
        record_manager.save(self.record)





