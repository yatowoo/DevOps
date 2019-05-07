#!/usr/bin/env python3

# Push to WeChat by Server酱

import requests
import json
import time

DB_FILE = open('private-db.json')
PUSH_API = json.load(DB_FILE)['push']
DB_FILE.close()

# Load log contents for pushing
text = ''
with open('csc.log') as f:
  print('[-] Load log : CSC')
  log = '## CSC申请状态\n'+f.read()
with open('ss/kingss-traffic.log') as f:
  print('[-] Load log : kingss traffic')
  log = log+'## kingss状态\n'+f.read().replace('\n','\n\n')
with open('ss/kingss-ping.log') as f:
  print('[-] Load log : kingss ping latency')
  log = log + f.read().replace('\n','\n\n')

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