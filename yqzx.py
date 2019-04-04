#coding=utf-8
# Script for YQZX.USTC auto login & test creating
# Refer : https://www.2cto.com/kf/201208/145281.html

import urllib 
import urllib2
import cookielib
import json
from copy import deepcopy
from pprint import pprint
import datetime
import sys
import getpass
import time
from PIL import Image
import cStringIO
import pytesseract

def CheckUrl(response):
  if response.getcode() == 200:
    print("[-] 连接成功 ： " + response.geturl())
  else:
    print("[X] 连接错误 - "+response.getcode()+"： " + response.geturl())
    exit()

# 设置运行时编码，避免urlencode出错
reload(sys)
sys.setdefaultencoding('utf-8')

REQUEST_DELAY = 0.5 # time (ms)

start_url = 'http://yqzx.ustc.edu.cn'
login_url = 'http://yqzx.ustc.edu.cn/login_cas'
submit_url = 'http://yqzx.ustc.edu.cn/api/testing/create'

#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。 
post_header = {
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
  'Upgrade-Insecure-Requests' : '1',
  'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'DNT': '1',
  'Accept-Encoding': 'gzip, deflate, br',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive'
}

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie 
cj = cookielib.LWPCookieJar() 
cookie_support = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
urllib2.install_opener(opener) 
 
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功） 
print("=== 启动登录流程 ===")
response = urllib2.urlopen(urllib2.Request(start_url, data=None, headers=post_header)) 
CheckUrl(response)

post_header['Referer'] = start_url
response = urllib2.urlopen(
  urllib2.Request(login_url, data=None, headers=post_header)) 
CheckUrl(response)


login_url = response.geturl()
post_header['Referer'] = login_url
# 处理验证码
validate_code = ''
validate_code_url = 'https://passport.ustc.edu.cn/validatecode.jsp?type=login'
response = urllib2.urlopen(
  urllib2.Request(validate_code_url, data=None, headers=post_header))
CheckUrl(response)
pytesseract.pytesseract.tesseract_cmd = 'tesseract'
validate_code_img = Image.open(cStringIO.StringIO(response.read()))
raw_code = pytesseract.image_to_string(validate_code_img)
validate_code = ''.join(e for e in raw_code if e.isalnum())
if(len(validate_code) != 4):
  print("[X] 验证码识别出错：" + validate_code + "，请查看当前目录下_tmp.png，手动打码")
  validate_code_img.save('_tmp.png')
  validate_code = raw_input('---> 验证码：')
  validate_code_img.save('_tmp_'+validate_code+'.png')
else:
  print("[-] 验证码识别完成，结果："+raw_code+' -> '+validate_code)
  validate_code_img.save(validate_code+'.png')
validate_code_img.close()

#构造Post数据，2019.03上线含验证码版本 
login_data = {'model' : 'uplogin.jsp',
            'service': 'http://yqzx.ustc.edu.cn/login_cas',
            'username' : raw_input('UserID : '), 
            'password' : getpass.getpass('Passwd : '),
            'LT': validate_code,
            'button' : ''
            } 

#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
response = urllib2.urlopen(
  urllib2.Request(login_url, urllib.urlencode(login_data), post_header)) 
CheckUrl(response)

# 载入测试表单
file = open('yqzx.json')
data = json.load(file)
file.close()

# 确认工作模式 - new, edit, debug
if(len(sys.argv) > 1):
  mode = sys.argv[1]
else:
  mode = 'new'
# MODE - NEW
#   - 创建新测试，每次最多四天
DATE_LIMIT = 4
post_header['Referer'] = 'http://yqzx.ustc.edu.cn/testing/create'
for test_name in data['test'].keys():
  time.sleep(REQUEST_DELAY)
  submit_data = deepcopy(data['form'])
  print("[-] Processing test : " + test_name)
  # 组装待提交测试表单
  for key in data['test'][test_name].keys():
    submit_data[key] = data['test'][test_name][key]
  for n_days in range(DATE_LIMIT):
    test_date = datetime.date.today() - datetime.timedelta(n_days)
    submit_data['test_date'] = test_date.strftime("%Y-%m-%d")
    print("  Date : " + submit_data['test_date'])
    if(mode == 'debug'):
      pprint(submit_data)
    else:
      response = urllib2.urlopen(
        urllib2.Request(submit_url, data=urllib.urlencode(submit_data), headers=post_header))
      CheckUrl(response)
      print response.read()