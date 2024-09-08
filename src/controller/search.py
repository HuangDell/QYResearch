import time

from src.util.config import  config
from . import report_writer,record_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.controller.page_controller import PageController
from src.controller.content_parser import ContentParser
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.util.report_item import ReportItem


class TargetSearch:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.get_search_page()
        self.controller = PageController(self.driver)
        self.record = record_manager.load()
        self.parser = ContentParser()
        self.reports=[]
        self.original_index=self.record.index

        pass

    def start(self):
        self.controller.fullscreen()
        self.driver.get(self.url)
        print(f'开始从 Page {self.record.page}, Index {self.record.index} 开始爬取数据...')
        try :
            # 先恢复上次中断点
            while not self.choose_page():pass
            i=0
            while True:
                list_urls=self.get_one_page_list()
                self.get_report_info(list_urls)

                if not self.goto_next_page():
                    print("所有数据抓取完毕，爬虫结束...")
                    break
                else:
                    print(f'Page {self.record.page} 爬取完毕，现在爬取 Page {self.record.page+1}')
                    self.write_report_data()
                    self.record_page()
                if i==2:
                    break
                i+=1
        except KeyboardInterrupt:
            print('程序正常退出，记录此次爬取的位置...')
            self.write_report_data()
            self.record_page()
            time.sleep(2)

    def choose_page(self):
        self.controller.scroll_to_bottom()
        # 定位到页码视图
        pages_view = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div[3]/div[4]/div/div/div[2]/div[2]/div/ul'))
        )
        pages_list = pages_view.find_elements(By.TAG_NAME, 'li')
        # 三种情况的页码处理
        search_range = range(5)
        jump_page = pages_list[4]
        if pages_list[1].get_attribute('class') == 'el-icon more btn-quickprev el-icon-more' \
                and pages_list[5].get_attribute('class') == 'el-icon more btn-quicknext el-icon-more':
            search_range = range(2, 5)
            jump_page = pages_list[5]
        elif pages_list[1].get_attribute('class') == 'el-icon more btn-quickprev el-icon-more':
            search_range = range(2, 6)

        for index in search_range:
            # 找到目标页面就点击并且返回函数
            if str(self.record.page) == pages_list[index].text and pages_list[index].get_attribute('class')=='number':
                pages_list[index].click()
                self.wait_for_internal_loading()
                return True
            elif str(self.record.page) == pages_list[index].text :
                return True

        jump_page.click()
        self.wait_for_internal_loading()
        return False

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
        self.reports.clear()

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

                list_urls.append(item.find_element(By.CLASS_NAME,'h3_p1').find_element(By.CLASS_NAME,'h3_p1').get_attribute('href'))
                report.link=list_urls[-1]
                self.reports.append(report)
        return list_urls




    """
    爬取文章详情页面的数据
    """
    def get_report_info(self, list_urls):
        for index,url in enumerate(list_urls):
            self.reports[index].id = url.split('/')[-2]
            original_window=self.controller.open_url_in_new_tab(url)
            WebDriverWait(self.driver, 15).until(
                EC.url_to_be(url)
            )
            xpaths = {
                'first_ph': '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/pre[1]',
                'title': '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/h1',
                'table':'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/ul',
            }


            results = {}
            for key, xpath in xpaths.items():
                results[key] = self.get_element_text(xpath)

            million_digit,cagr_digit,summary= self.parser.parser_first_ph(results['first_ph'])
            title = self.parser.parser_title(results['title'])
            company_text,type_text,application_text= self.parser.parser_table(results['table'])


            self.reports[index].million_digit=million_digit
            self.reports[index].cagr_digit=cagr_digit
            self.reports[index].title=title
            self.reports[index].summary_text=summary
            self.reports[index].company_text=company_text
            self.reports[index].type_text=type_text
            self.reports[index].application_text=application_text

            print(f'Index {self.record.index} Title {title} 爬取完毕')
            self.record.index+=1
            time.sleep(config.sleep_time())
            self.controller.close_current_tab_and_switch_back(original_window)




    def write_report_data(self):
        report_writer.write_items(self.reports[:self.record.index-self.original_index])
        report_writer.save()


    def goto_next_page(self):
        self.controller.scroll_to_bottom()
        next_button = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[4]/div/div/div[2]/div[2]/div/button[2]'))
        )
        if next_button.get_attribute('disabled')=='disabled':
            return False

        next_button.click()
        self.wait_for_internal_loading()
        return True

    def record_page(self):
        if self.record.index==10:
            self.record.page+=1
            self.record.index=0
            self.original_index=0

        record_manager.save(self.record)

    def get_element_text(self,xpath, wait_time=1):
        count =1
        if 'ul' in xpath:
            count = 15

        element=''
        for i in range(count):
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                ).text.strip()
            except TimeoutException:
                # print(f"第 {i + 1} 次滚动后未找到表格，继续滚动")
                self.controller.scroll_by_pixel(400)
        return element

    def wait_for_internal_loading(self):
        loader_locator = (By.CSS_SELECTOR, "div.loading")
        # 首先等待加载指示器出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(loader_locator)
        )
        # 然后等待加载指示器消失
        WebDriverWait(self.driver, 30).until_not(
            EC.presence_of_element_located(loader_locator)
        )
        print("加载指示器已消失，页面加载完成")





