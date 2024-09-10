import configparser
from urllib.parse import quote

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini',encoding='utf-8')
        self.domain = self.config['Crawler']['SearchUrl']
        self.price = self.config['Crawler']['Price']
        self.time=float(self.config['Crawler']['SleepTime'])
        self.page_size=int(self.config['Crawler']['PageSize'])
        self.thread_num=int(self.config['Crawler']['ThreadNum'])
        self.max_page=int(self.config['Crawler']['MaxPage'])


    def get_search_page(self):
        return self.config['Crawler']['SearchUrl']+quote(self.config['Crawler']['Target'])

    def combine_link(self,url):
        return self.domain+url

    def check_price(self,price):
        if self.price=='None':
            return True
        return self.price==price

    def get_filename(self):
        return self.config['Data']['FileName']

    def get_record_file(self):
        return self.config['Data']['RecordName']

    def get_target(self):
        return self.config['Crawler']['Target']

    def sleep_time(self):
        return self.time

config = Config()