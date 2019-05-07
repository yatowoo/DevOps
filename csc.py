#!/usr/bin/env python3

# APPLY.CSC login script

import requests
import bs4
import time
import json

REQUEST_DELAY = 0.5 # second

DB_FILE = open('private-db.json')
DATA = json.load(DB_FILE)
API_DATA = DATA['csc']
PUSH_API = DATA['push']
DB_FILE.close()


login_url = API_DATA['url']

login_header = {
  'Accept-Language': 'zh-CN',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
  'Host': API_DATA['host'],
  'Referer': login_url,
  'Accept-Encoding': 'gzip, deflate, br',
  'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'}

login_data = {
  'mainForm:registerFlag': '',
  'jsf_sequence': '1',
  'mainForm:userName': API_DATA['username'],
  'mainForm:pwd': API_DATA['password'],
  'mainForm:inputVrfCode': '2919',
  'mainForm_SUBMIT': '1',
  'mainForm:timeZone': '-8',
  'mainForm:_idJsp1.x': '12',
  'mainForm:_idJsp1.y': '2'}

s = requests.Session()
r = s.get(login_url, headers=login_header)
if(r.status_code == 200):
  dom = bs4.BeautifulSoup(r.text,'html.parser')
  login_data['mainForm:inputVrfCode'] = dom.find(id='mainForm:vrfImg').text
  print('[-] CSC connected.')
else:
  print('[X] Connection error : ' + login_url)
  exit()

time.sleep(REQUEST_DELAY)
login_header['Content-Type'] = 'application/x-www-form-urlencoded'
r = s.post(login_url, headers=login_header, data=login_data)

if(r.status_code != 200):
  print('[X] CSC Login error : ' + login_url)
  exit()

print('[-] CSC Login successfully.')
# Application Form
dom = bs4.BeautifulSoup(r.text,'html.parser')

# 学号
id_pos = r.text.find('2019')
csc_id = r.text[id_pos:id_pos+12]

# pit4: 姓名
# pit6: '审核中，请耐心等待'
csc_name = dom.find(id='mainForm:pit4').text
csc_status = dom.find(id='mainForm:pit6').text
# tit6: '- 您的申报材料所处的状态为：'
# tit7: '您的申请表已经提交,请等待基金委审核.'
csc_status_full = dom.find(id='mainForm:pageview:tit7').text

print('[+] Info - 学号: '+csc_id+', 姓名: '+csc_name)
print('----> '+csc_status)
print('----> '+csc_status_full)

# Push to WeChat by Server酱
PUSH_SCKEY = PUSH_API['SCKEY']
push_url = 'https://sc.ftqq.com/'+PUSH_SCKEY+'.send'
push_header = {}
push_header['Content-Type'] = 'application/x-www-form-urlencoded'
push_data = {}
push_data['text'] = 'CSC申请状态'
push_data['desp'] = '## 申请人信息\n学号：'+csc_id+'\n\n'+'姓名：'+csc_name+'\n## 当前状态\n'+csc_status+'\n\n'+csc_status_full+'\n'

print('[-] Push info to WeChat.')
s = requests.Session()
r = s.post(push_url,headers=push_header,data=push_data)
if(r.status_code == 200):
  print('----> '+r.text)
else:
  print('[X] Push FAILED : '+r.text)
  exit()