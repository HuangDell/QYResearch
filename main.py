from src.controller.search import TargetSearch
from src.util.config import config

if __name__ == '__main__':
    print('爬虫版本v3.0')
    print('正在初始化环境，请稍等...')
    print(f'当前设置的线程数：{config.thread_num}, Page Size：{config.page_size}')
    crawler = TargetSearch()
    crawler.start()
    crawler.close_all_drivers()
    input("按q键退出...")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
