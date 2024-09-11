import threading
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


from src.util.config import  config
from . import report_writer,record_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.controller.page_controller import PageController
from src.controller.content_parser import ContentParser
from selenium.common.exceptions import TimeoutException
from src.util.report_item import ReportItem
from .search_page import SearchPage


class TargetSearch:
    def __init__(self ):
        # self.driver = driver
        self.lock=threading.Lock()
        self.url = config.get_search_page()
        self.controller = PageController()
        self.record = record_manager.load()
        self.parser = ContentParser()
        self.reports=[]
        self.original_index=self.record.index
        self.searcher=SearchPage(self.record)
        self.page_max=None if config.max_page==-1 else config.max_page
        self.drivers = {}

        pass

    def start(self):
        # self.controller.fullscreen()
        # self.driver.get(self.url)
        print(f'开始从 Page {self.record.page}, Index {self.record.index} 开始爬取数据...')
        try :
            # 先恢复上次中断点
            while True:
                # 获得此轮要爬取的reports的基本信息
                self.get_products_url_list()
                self.get_report_info()

                print(f'Page {self.record.page} 爬取完毕，现在爬取 Page {self.record.page+1}')
                self.write_report_data()
                self.record_page(True)
                if self.record.page>=self.page_max:
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
        # 根据page和page_size来获取Product
        products,url_list,data_page=self.searcher.get_pages_url(self.record.page)
        if self.page_max is None:
            self.page_max = data_page

        self.reports.clear()

        # 从上次中断的位置开始
        for index in range(self.record.index,len(products)):
            item = products[index]
            price = item['price']
            if config.check_price(price):
                report=ReportItem()

                # 从list中读取部分数据
                date= item['published_date_format']
                category=item['category_name']
                pages=item['pages']
                url=item['url']

                report.date=date
                report.category=category
                report.pages=pages
                report.price=price
                report.link = url_list[index]
                report.url = url

                self.reports.append(report)
        # return url_list[self.original_index:]


    """
    爬取文章详情页面的数据
    """
    def process_single_report(self, report, index):
        # driver=self.get_driver()
        url = report.link
        report.id = url.split('/')[-2]
        # self.controller.fullscreen(driver)
        # driver.get(url)
        # WebDriverWait(driver, 15).until(
        #     EC.url_to_be(url)
        # )
        # xpaths = {
        #     'first_ph': '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/pre[1]',
        #     'title': '//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div/h1',
        #     'table': '//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/ul',
        # }

        # results = {}
        # for key, xpath in xpaths.items():
        #     results[key] = self.get_element_text(driver,xpath)
        data = self.searcher.get_report_info(report)

        first_ph=data['description'][0]
        title =data['name']
        company_text='\n'.join(data['companies_mentioned'].split(', '))
        type_text = '\n'.join(data['classification'])
        application_text = '\n'.join(data['application'])


        million_digit, cagr_digit, summary =        self.parser.parser_first_ph(first_ph)
        title =                                     self.parser.parser_title(title)
        # company_text, type_text, application_text = self.parser.parser_table(results['table'])

        report.million_digit = million_digit
        report.cagr_digit = cagr_digit
        report.title = title
        report.summary_text = summary
        report.company_text = company_text
        report.type_text = type_text
        report.application_text = application_text

        print(f'Index {index} Title {title} 爬取完毕')
        time.sleep(config.sleep_time())

        return report

    def get_report_info(self):
        with ThreadPoolExecutor(max_workers=config.thread_num) as executor:  # Adjust max_workers as needed
            future_to_report = {executor.submit(self.process_single_report, report, index): (report, index)
                                for index, report in enumerate(self.reports)}

            for future in concurrent.futures.as_completed(future_to_report):
                report, index = future_to_report[future]
                try:
                    updated_report = future.result()
                    self.reports[index] = updated_report
                    self.record.index += 1
                except Exception as exc:
                    print(f'Report at index {index} generated an exception: {exc}')
        # self.close_all_drivers()

        print("All reports processed.")



    def write_report_data(self):
        report_writer.write_items(self.reports[:self.record.index-self.original_index])
        report_writer.save()


    # """v2版本中弃用，改用request进行爬取页面"""
    # def goto_next_page(self):
    #     self.controller.scroll_to_bottom()
    #     next_button = WebDriverWait(self.driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[4]/div/div/div[2]/div[2]/div/button[2]'))
    #     )
    #     if next_button.get_attribute('disabled')=='disabled':
    #         return False
    #
    #     next_button.click()
    #     self.wait_for_internal_loading()
    #     return True

    def record_page(self,flag):
        if self.record.index==config.page_size or flag:
            self.record.page+=1
            self.record.index=0
            self.original_index=0

        record_manager.save(self.record)

    def get_element_text(self,driver,xpath, wait_time=1):
        count =1
        if 'ul' in xpath:
            count = 10

        element=''
        for i in range(count):
            try:
                element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                ).text.strip()
                break
            except TimeoutException:
                # print(f"第 {i + 1} 次滚动后未找到表格，继续滚动")
                self.controller.scroll_by_pixel(driver,400)
        return element

    # def get_driver(self):
    #     thread_id = threading.get_ident()
    #     if thread_id not in self.drivers:
    #         self.drivers[thread_id] = create_driver()
    #         print(f'{thread_id} 线程创建成功')
    #     return self.drivers[thread_id]

    # def close_all_drivers(self):
    #     for driver in self.drivers.values():
    #         driver.quit()
    #     self.drivers.clear()



# def create_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")  # 在Windows上需要
#     options.add_argument("--no-sandbox")  # 在某些环境中需要
#     custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
#     options.add_argument(f'user-agent={custom_user_agent}')
#
#     driver = webdriver.Edge(options=options)
#     return driver






