import execjs
import base64
import re
from bs4 import BeautifulSoup # 用来解析HTML
from loguru import logger

jsctx = None  # 全局变量，用于存储JavaScript执行上下文
script_src = None  # 用于存储提取的script src属性

def process_html(html_content):
    """
    处理 BeautifulSoup 对象，返回你需要的数据。
    这里以获取页面标题为例，可根据需要自定义。
    """
    if html_content is None:
        return None
    # 使用BeautifulSoup提取
    bs_results = extract_with_bs(html_content)
    src = extract_script_src(html_content)  # 提取src属性
    js_code = bs_results[0]  # 假设第一个脚本就是我们需要的JavaScript代码
    ctx = exec_js(js_code)   # 执行JavaScript代码
    
    global jsctx
    jsctx = ctx  # 将执行上下文存储到全局变量中
    global script_src
    script_src = src  # 存储提取的script src属性
    
    logger.debug(f"Extracted script src: {script_src}")
    res = auth()  # 执行授权函数
    return res  # 如果授权成功，返回结果
  

# 使用BeautifulSoup提取
def extract_with_bs(html):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    return [script.string for script in scripts if script.string]

def extract_script_src(html):
    # 正则表达式匹配src属性到defer结束
    pattern = r'src=[\'"](.*?)[\'"][^>]*?defer>\s*</script>'
    matches = re.findall(pattern, html, re.DOTALL)
    if matches:
        return matches[0]  # 返回第一个匹配的src属性
    else:
        return None  # 如果没有匹配，返回None

def exec_js(js_code):
    """
    执行JavaScript代码并返回结果
    """
    # 创建JS环境并调用d函数
    ctx = execjs.compile(js_code + "\nfunction getD(index){return gC.d(index);}")
    return ctx
   
 
def getGC(i,j):
    if jsctx is None:
        logger.error("JavaScript context is not initialized. Please run scrape_page first.")
        return None
    res_i = jsctx.call("getD",i)  # 调用gc.d(1) 里的第一个元素
    res = res_i[j] if j < len(res_i) else None
    return res
    
# ['var gC={};(function(){var z={"ijs":[0,9,7],
#  "leu":["MjEgNCAxIDI1IDI2IDQ5IDE2IDMxIDU0IDM1IDYwIDUzIDM5IDMgMzYgNTQgMTYgMjEgNTMgMzkgNTMgNTcgMTkgMzkgNDQgNDcgNDEgMTcgMzAgNTYgNDQgNiA0MiA1OSA2IDIxIDQ1IDQ4IDUgNTQ=","gFew3P9uVrRUDOTLcA2XBnjmtSZbKi87NHhpsqJMQoCaWYGk6Ev41zdIyflx05","16d73c16316e731ae56b1dc9156cfd48"],
#  "bhs":["Q2JvZk9Mc3hJZWdRQ1hIemM2ZWEsNXIzTmZoS2xrUGdXRUZNT29LaTU=",2,0,0,1," ","0","121","44","bkl"],
#  "jud":["aWpz","bGV1","Ymhz"]};

# 获取auth信息
def auth():
    e = getGC(2,6) + chr(int(getGC(2,7))) + "-"
    t = len(e)
    # 模拟document.getElementById('y2mate').src
    y2mate_src = script_src  # 需要替换为实际获取方式
    pattern = re.compile(getGC(2,9) + "=([a-zA-Z]{6})")
    r = pattern.search(y2mate_src)
    
    if not r:
        return False

    decoded = base64.b64decode(getGC(1,0)).decode('utf-8')
    split_values = decoded.split(getGC(2,5))

    gc_23 = getGC(2, 3)
    gc_24 = getGC(2, 4)
    gc_11 = getGC(1, 1)
    source_str = gc_11[::-1] if gc_24 > 0 else gc_11

    for n in range(len(split_values)):
       index = int(split_values[n]) - gc_23
       e += source_str[index]
    
    if getGC(2,1) == 1:
        e = e[:t] + e[t:].lower()
    elif getGC(2,1) == 2:
        e = e[:t] + e[t:].upper()
    
    if len(getGC(2,0)) > 0:

        decoded_str = base64.b64decode(getGC(2,0)).decode('utf-8')
        modified = decoded_str.replace(chr(int(getGC(2,8))), "")
        return base64.b64encode((modified + "_" + getGC(1,2)).encode()).decode()
    elif getGC(2,2) > 0:
        return base64.b64encode((e[:getGC(2,2)+t] + "-" + r.group(1) + "_" + getGC(1,2)).encode()).decode()
    else:
        return base64.b64encode((e + "-" + r.group(1) + "_" + getGC(1,2)).encode()).decode()
