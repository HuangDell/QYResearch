import configparser
from urllib.parse import quote

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../../config.ini')


    def get_search_page(self):
        return quote(self.config['Crawler']['SearchUrl']+quote(self.config['Crawler']['Target']))


config = Config()