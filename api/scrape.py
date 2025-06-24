

import requests
from loguru import logger
import re
from urllib.parse import urljoin # 用来做url 拼接
from bs4 import BeautifulSoup # 用来解析HTML

from .process import process_html # 导入process.py中的函数
 
BASE_URL = 'https://y2mate.as/'

jsctx = None  # 全局变量，用于存储JavaScript执行上下文
script_src = None  # 用于存储提取的script src属性

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    
# 爬取页面,获取script内容
def scrape_page(url):
    logger.info('scraping %s...',url)
    try:
       response = requests.get(url,headers=headers,timeout=10)
       response.raise_for_status()  # 检查请求是否成功
       if response.status_code == 200:
           html_content = response.text
           return process_html(html_content)  # 处理HTML内容
        
       logger.error('get Invalid status code %s while scraping %s',response.status_code,url)
    except requests.RequestException:
       logger.error('error while scraping %s',url,exc_info=True)
       

   

 