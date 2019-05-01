#!/usr/bin/env python3
#coding=utf-8

# Target : login to kingss and get the traffic usage

# detail selector : $("tr") => $("th"):$("td") => dict
# th = ["产品信息", "详细", "产品名称", "价格 / 周期", "开通时间", "到期时间", "加密方式", "连接端口", "连接密码", "总流量", "流量使用状态", "新加坡", "美国", "美国（finalspeed看教程）", "美国（finalspeed看教程）", "英国", "加拿大", "东京", "东京", "二维码", "续期产品", "状态"]
# td = ["基础流量", "30 元 / 年付", "2017-10-13", "2018-10-13", "aes-256-cfb", "16426", "修改密码", "100 GB", "已用: 30.89 GB 未用:69.11 GB", "sf1.kingss.me 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "SEVER 加密方式:aes-256-cfb[显示二维码]", "当前未选择节点，请点击节点的地址以显示二维码", "该产品禁止续费", "已激活"]

import requests
import bs4
import time
import json

def CheckUrl(response):
  if response.status_code == 200:
    print("[-] Connected to " + response.url)
  else:
    print("[X] ERROR " + repr(response.status_code) + " - Fail to connect " + response.url)
    exit()

DB_FILE = open("../private-db.json")
API_DATA = json.load(DB_FILE)['kingss']

index_url = API_DATA['site']+'/index.php/index/index/'
login_url = API_DATA['site']+'/index.php/index/login/'
detail_url = API_DATA['site']+'/index.php/control/detail/'
detail_id = API_DATA['product_id']

REQUEST_DELAY = 0.5 # second

login_headers = {
          'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 
           'Upgrade-Insecure-Requests' : "1",
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'DNT': "1",
           'Accept-Encoding': 'gzip, deflate, br',
           'Origin': 'http://kingfast.top',
           'Referer': 'http://kingfast.top/index.php/index/login/'
}

login_form = {"swapname":API_DATA['swapname'], "swappass":API_DATA['swappass']}

s = requests.Session()
CheckUrl(
  s.get(login_url, headers=login_headers)
)

time.sleep(REQUEST_DELAY)
login_headers['Content-Type'] =  'application/x-www-form-urlencoded'
r = s.post(login_url, headers=login_headers, data=login_form)
CheckUrl(r)
login_headers.pop('Content-Type')

for id in detail_id:
  time.sleep(REQUEST_DELAY)
  r = s.get(detail_url+repr(id)+'/',headers=login_headers)
  CheckUrl(r)
  dom = bs4.BeautifulSoup(r.text,'html.parser')
  for row in dom.table.find_all('td'):
    print(row.text.strip())
  print("======")
