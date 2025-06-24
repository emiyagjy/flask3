from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from loguru import logger
import random
from .scrape import scrape_page
import json
# import scrape  # 导入scrape.py中的函数

app = Flask(__name__)
CORS(app)  # 允许所有源访问,如果你只想允许特定来源：,origins=["http://127.0.0.1:5500"]

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有源，也可以指定具体源如 'http://example.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


BASE_URL = 'https://y2mate.as/'

headers = {
        'Origin': 'https://y2mate.nu', # https://y2mate.nu
        'Referer':'https://y2mate.nu', #/
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

@app.route('/')
def home():
    return 'Hello! My first flask api for Vercel!'

@app.route('/api/url', methods=['POST'])
def geturl():
    try:
        url = request.json.get('url', '')
        if not url:
            return jsonify({'error': 'URL parameter is required'}), 400
        logger.debug(f"api URL: {url}")
        response = requests.get(url, headers=headers)
        logger.debug(f"Response status code: {response}")
        if response.status_code == 200:
            content =  response.content
            jsonData = json.loads(content)
            logger.debug(f"jsonData: {jsonData}")
            return jsonData
        else:
          return jsonify({'error': f'Failed to fetch resource, status code: {response.status_code}'}), 502

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/getmp', methods=['GET'])
def getmp():
    try:
        # 获取授权信息
        auth_str = scrape_page(BASE_URL)  # 调用scrape.py中的函数获取授权信息
        logger.debug(f"Authorization string: {auth_str}")
        url= f"https://d.mnuu.nu/api/v1/init?a={auth_str}&_={random.random()}"  # 构建请求URL
        logger.debug(f"getmp URL: {url}")
        response = requests.get(url, headers=headers)
        add_cors_headers(response)
        logger.debug(f"Response status code: {response}")
        if response.status_code == 200:
            content =  response.content
            jsonData = json.loads(content)
            logger.debug(f"jsonData: {jsonData}")
            return jsonData
        else:
          return jsonify({'error': f'Failed to fetch resource, status code: {response.status_code}'}), 502

    except Exception as e:
        return jsonify({'error': str(e)}), 500
