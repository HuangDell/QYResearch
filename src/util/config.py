import configparser
from urllib.parse import quote

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.domain = self.config['Crawler']['SearchUrl']
        self.price = self.config['Crawler']['Price']


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

config = Config()