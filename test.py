
import requests
from urllib.parse import urlencode
import random
import time

# 用户代理列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(user_agents)

# 基础URL
base_url = "https://www.qyresearch.com/api/product/list"
base_report_url = 'https://www.qyresearch.com/reports/'

# 请求参数
params = {
    "keyWord": "Market Research Report 2024",
    "orderBy": "time",
    "page": 1,
    "pageSize": 30
}

# 构建完整的URL
full_url = f"{base_url}?{urlencode(params)}"

# 自定义headers
headers = {
    "User-Agent": get_random_user_agent(),
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

# 添加一个随机延迟
# time.sleep(random.uniform(1, 3))

try:
    # 发送GET请求
    response = requests.get(full_url, headers=headers, timeout=10)

    # 检查响应状态
    response.raise_for_status()  # 如果状态码不是200，将引发HTTPError异常

    # 请求成功
    data = response.json()['data'] # 假设响应是JSON格式
    reports_url=[]
    print("请求成功!")
    for item in data['product']:
        reports_url.append(f'{base_report_url}{item["id"]}/{item["url"]}')
    print(f"响应数据: {reports_url}")

except requests.exceptions.HTTPError as errh:
    print(f"HTTP错误: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"连接错误: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"超时错误: {errt}")
except requests.exceptions.RequestException as err:
    print(f"其他错误: {err}")

# 打印编码后的完整URL
print(f"\n完整的编码URL: {full_url}")
print(f"使用的User-Agent: {headers['User-Agent']}")
