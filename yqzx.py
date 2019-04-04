#coding=utf-8
# Script for YQZX.USTC auto login & test creating
# Refer : https://www.2cto.com/kf/201208/145281.html

import urllib 
import urllib2
import cookielib
import json
import datetime
import sys
import getpass
import time
from PIL import Image
import cStringIO
import pytesseract

def CheckUrl(response):
  if response.getcode() == 200:
    print "[-] Connected to " + response.geturl()
  else:
    exit()

# 设置运行时编码，避免urlencode出错
reload(sys)
sys.setdefaultencoding('utf-8')

REQUEST_DELAY = 0.5 # time (ms)

start_url = 'http://yqzx.ustc.edu.cn'
login_url = 'http://yqzx.ustc.edu.cn/login_cas'
submit_url = 'http://yqzx.ustc.edu.cn/api/testing/create'

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie 
cj = cookielib.LWPCookieJar() 
cookie_support = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
urllib2.install_opener(opener) 
 
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功） 
start_headers = {
          'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
           'Upgrade-Insecure-Requests' : 1,
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'DNT': 1,
           'Accept-Encoding': 'gzip, deflate',
           'Cache-Control':'max-age=0',
           'Connection':'keep-alive'
}
response = urllib2.urlopen(urllib2.Request(start_url, data=None, headers=start_headers)) 
CheckUrl(response)

start_headers['Referer'] = start_url
response = urllib2.urlopen(
  urllib2.Request(login_url, data=None, headers=start_headers)) 
CheckUrl(response)

#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。 
login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
           'Upgrade-Insecure-Requests' : 1,
           'Referer' : 'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fyqzx.ustc.edu.cn%2Flogin_cas',
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'DNT': 1,
           'Accept-Encoding': 'gzip, deflate, br'
} 
login_url = response.geturl()
# 处理验证码
validate_code = ''
validate_code_url = 'https://passport.ustc.edu.cn/validatecode.jsp?type=login'
response = urllib2.urlopen(
  urllib2.Request(validate_code_url, data=None, headers=start_headers))
CheckUrl(response)
pytesseract.pytesseract.tesseract_cmd = 'tesseract'
validate_code_img = Image.open(cStringIO.StringIO(response.read()))
validate_code = pytesseract.image_to_string(validate_code_img)
validate_code = ''.join(e for e in validate_code if e.isalnum())
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
 
#需要给Post数据编码 
login_data = urllib.urlencode(login_data) 
 
#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
response = urllib2.urlopen(
  urllib2.Request(login_url, login_data, login_headers)) 
CheckUrl(response)

# Submit new test
submit_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
           'Upgrade-Insecure-Requests' : 1,
           'Referer' : 'http://yqzx.ustc.edu.cn/testing/create',
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'DNT': 1,
           'Accept-Encoding': 'gzip, deflate',
           'X-Requested-With': 'XMLHttpRequest'
}

file = open('yqzx.json')
data = json.load(file)
file.close()

DATE_LIMIT = 4
for test_name in data['test'].keys():
  time.sleep(REQUEST_DELAY)
  submit_data = data['form']
  print "[-] Processing test : " + test_name
  # 组装待提交测试表单
  for key in data['test'][test_name].keys():
    submit_data[key] = data['test'][test_name][key]
  for n_days in range(DATE_LIMIT):
    test_date = datetime.date.today() - datetime.timedelta(n_days)
    submit_data['test_date'] = test_date.strftime("%Y-%m-%d")
    print "  Date : " + submit_data['test_date'] 
    response = urllib2.urlopen(
      urllib2.Request(submit_url, data=urllib.urlencode(submit_data), headers=submit_headers))
    CheckUrl(response)
    print response.read()