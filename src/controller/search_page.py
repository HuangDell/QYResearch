import random
from urllib.parse import urlencode

import requests

from src.util.config import config
from src.util.record_item import RecordItem


class SearchPage:
    def __init__(self, record:RecordItem):
        self.config = config
        self.record = record
        self.target = config.get_target()
        # 用户代理列表
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        ]


        self.base_url = "https://www.qyresearch.com/api/product/list"
        self.base_report_url = 'https://www.qyresearch.com/reports/'

        # 自定义headers
        self.headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.qyresearch.com/",
            "Origin": "https://www.qyresearch.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }



    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_pages_url(self,page):
        # 请求参数
        params = {
            "keyWord": self.target,
            "orderBy": "time",
            "page": page,
            "pageSize": 10
        }
        # 构建完整的URL
        full_url = f"{self.base_url}?{urlencode(params)}"
        # 发送GET请求
        response = requests.get(full_url, headers=self.headers, timeout=10)

        # 检查响应状态
        response.raise_for_status()  # 如果状态码不是200，将引发HTTPError异常

        # 请求成功
        data = response.json()['data']  # 假设响应是JSON格式
        reports_url = []
        print(f"获取 Page {page}信息成功!")
        for item in data['product']:
            reports_url.append(f'{self.base_report_url}{item["id"]}/{item["url"]}')
        return data['product'],reports_url,int(data['pageCount'])



