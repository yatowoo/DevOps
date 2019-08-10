#!/usr/bin/env python3

# Push to WeChat by Server酱

import requests
import json
import time
import sys
import pymysql

DB_FILE = open('private-db.json')
DB_DATA = json.load(DB_FILE)
PUSH_API = DB_DATA['push']
DB_FILE.close()

if( len(sys.argv) > 1 and sys.argv[1] == 'debug'):
  PUSH_ALERT = True
else:
  PUSH_ALERT = False
# Daily push at 10 pm.
PUSH_DAILY = False
if(int(time.strftime("%H")) == 22 ): 
  PUSH_DAILY = True
  PUSH_ALERT = True


# Open MySQL connection
with open('private-db.json') as f:
  API_DB = json.load(f)['rss']
  db = pymysql.connect('localhost',API_DB['USER'], API_DB['PASS'], 'rss')
  p = db.cursor()

# Load log contents for pushing
log = ''
# 科大新闻
TODAY = time.strftime("%Y%m%d")
log = log + '## 科大新闻 - '+TODAY+'\n\n'
datestamp = time.strftime("%Y-%m-%d 00:00:00")
cmd = "SELECT * FROM info WHERE DATE(scrap_time) >= '" + datestamp + "' AND source LIKE '%USTC%'"
if(p.execute(cmd) > 0):
  result = p.fetchall()
  for row in result:
    log = log + '[' + row[2] + '](' + row[4] + ')\n\n'

# 上海博物馆
log = log + '## 上海博物馆\n'
if(PUSH_DAILY):
  datestamp = time.strftime("%Y-%m-%d 00:00:00")
else:
  datestamp = time.strftime("%Y-%m-%d %H:00:00")
cmd = "SELECT * FROM info WHERE DATE(scrap_time) >= '" + datestamp + "' AND source='上海博物馆'"
if(p.execute(cmd) > 0):
  PUSH_ALERT = True
  result = p.fetchall()
  for row in result:
    log = log + '[' + row[2] + '](' + row[4] + ')\n\n'

db.close()

if(not PUSH_ALERT):
  exit()
# Push to WeChat by Server酱
PUSH_SCKEY = PUSH_API['SCKEY']
push_url = 'https://sc.ftqq.com/'+PUSH_SCKEY+'.send'
push_header = {}
push_header['Content-Type'] = 'application/x-www-form-urlencoded'
push_data = {}
push_data['text'] = 'ustc.fun订阅与监控'
push_data['desp'] = log

print('[-] Push info to WeChat.')
s = requests.Session()
r = s.post(push_url,headers=push_header,data=push_data)
if(r.status_code == 200):
  print('----> '+r.text)
else:
  print('[X] Push FAILED : '+r.text)
  exit()

