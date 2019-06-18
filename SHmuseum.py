#!/usr/bin/env python3

# Subscribe Shanghai Museum activities

import requests
import bs4
import time
import json

REQUEST_DELAY = 0.5 # second

HOST_URL = 'https://www.shanghaimuseum.net'

API_URL = 'https://www.shanghaimuseum.net/education/show/show-list'

WEB_URL = 'https://www.shanghaimuseum.net/education/show/show.action'

login_header = {
  'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
  'Accept-Encoding': 'gzip, deflate, br',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

API_DATA = {
  'dateSelector': '',
  'keyword': '',
  'seriesId': '',
  'pageNo': 1
}

s = requests.Session()

r = s.get(HOST_URL, headers=login_header)

login_header['Referer'] = WEB_URL
login_header['X-Requested-With'] = 'XMLHttpRequest' 

for pageNo in range(1,10):
  time.sleep(REQUEST_DELAY)
  API_DATA['pageNo'] = pageNo
  r = s.post(API_URL, headers=login_header, data=API_DATA)
  RAW = json.loads(r.text)
  for act in RAW['activityList']:
    #print(act['activityDate'] + ' ' + act['activityName'])
    if(act['activityStatus'] != '该活动预约人数已至上限。' and act['activityStatus'] != '该活动已结束。'):
      print(act['activityDate'] + ' ' + act['activityName']+' '+act['speaker']+'\n')
      print('> '+act['activityContent']+'\n')