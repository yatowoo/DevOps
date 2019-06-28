#!/usr/bin/env python3

# Push to WeChat by Server酱

import requests
import json
import time
import sys

DB_FILE = open('private-db.json')
DB_DATA = json.load(DB_FILE)
PUSH_API = DB_DATA['push']
DB_FILE.close()

if( len(sys.argv) > 1 and sys.argv[1] == 'debug'):
  PUSH_ALERT = True
else:
  PUSH_ALERT = False

# Load log contents for pushing
log = ''
# 科大新闻
with open('media/USTC-INFO.json') as f:
  NEWS_DB = json.load(f)
  TODAY = time.strftime("%Y%m%d")
  log = log + '## 科大新闻 - '+TODAY+'\n\n'
  if(NEWS_DB.get(TODAY)):
    for news in NEWS_DB[TODAY]:
      log = log + '[' + news['title'] + '](' + news['url'] + ')\n\n'
  if(int(time.strftime("%H")) == 22 ): # Daily push at 10 pm.
    PUSH_ALERT = True

# 上海博物馆
with open('activity.log') as f:
  activity_log = f.read()
  log = log + '## 上海博物馆\n'
  if(len(activity_log) > 1):
    PUSH_ALERT = True
    log = log + activity_log

# kingss状态
with open('ss/kingss-traffic.log') as f:
  print('[-] Load log : kingss traffic')
  kingss_log = f.read()
  try:
    if(float(kingss_log.split('\n')[3].split(' ')[1]) > 95.):
      PUSH_ALERT = True
    log = log+'## kingss状态\n'+kingss_log.replace('\n','\n\n')
  except:
    log = log+'## kingss状态\n[X] ERROR - Fail to resolve traffic log\n\n'
    PUSH_ALERT = True
with open('ss/kingss-ping.log') as f:
  print('[-] Load log : kingss ping latency')
  log = log + f.read().replace('\n','\n\n')

log = log+'> [More details.]('+PUSH_API['detail']+')\n\n'

if(not PUSH_ALERT):
  print('[-] All is WELL.')
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
