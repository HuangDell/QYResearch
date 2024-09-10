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
from .search_page import SearchPage


class TargetSearch:
    def __init__(self, driver):
        self.driver = driver
        self.url = config.get_search_page()
        self.controller = PageController(self.driver)
        self.record = record_manager.load()
        self.parser = ContentParser()
        self.reports=[]
        self.original_index=self.record.index
        self.searcher=SearchPage(self.record)
        self.page_max=None

        pass

    def start(self):
        self.controller.fullscreen()
        self.driver.get(self.url)
        print(f'开始从 Page {self.record.page}, Index {self.record.index} 开始爬取数据...')
        try :
            # 先恢复上次中断点
            while True:
                self.get_products_url_list()

                self.get_report_info()

                print(f'Page {self.record.page} 爬取完毕，现在爬取 Page {self.record.page+1}')
                self.write_report_data()
                self.record_page(True)
                if self.record.page>self.page_max:
                    print('所有数据爬取完毕，爬虫结束...')
                    break
        except KeyboardInterrupt:
            print('程序正常退出，记录此次爬取的位置...')
        except TimeoutException:
            print(f'爬取超时，请检查网络是否正常...')
        except Exception as e:
            print(f'遇到未知异常，请联系管理员\n{e}')
        self.write_report_data()
        self.record_page(False)
        print('数据记录完毕')

    """利用request模块获取reports列表的url和基本信息"""
    def get_products_url_list(self):
        products,url_list,data_page=self.searcher.get_pages_url(self.record.page)
        if self.page_max is None:
            self.page_max = data_page

        self.reports.clear()

        for index in range(self.record.index,len(products)):
            item = products[index]
            price = item['price']
            if config.check_price(price):
                report=ReportItem()

                # 从list中读取部分数据
                date= item['published_date_format']
                category=item['category_name']
                pages=item['pages']

                report.date=date
                report.category=category
                report.pages=pages
                report.price=price
                report.link = url_list[index]

                self.reports.append(report)
        # return url_list[self.original_index:]
    """
    爬取文章详情页面的数据
    """
    def get_report_info(self):
        for index,report in enumerate(self.reports):
            url=report.link
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


    """v2版本中弃用，改用request进行爬取页面"""
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

    def record_page(self,flag):
        if self.record.index==10 or flag:
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

    """v2版本中弃用"""
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





