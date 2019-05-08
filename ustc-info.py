#!/usr/bin/env python3

# USTC-NEWS

import requests
import bs4
import socks
import json

url_host = 'https://www.ustc.edu.cn'

  # DOM.find_all('table')[4].find_all('a')
url_info = 'https://www.ustc.edu.cn/2014/list.htm'

# News content
  # DOM.find('td',{'class':'title'})
  # DOM.find_all('table')[4].find_all('p')
news_url = 'https://www.ustc.edu.cn/2019/0426/c2017a379602/page.htm'

s = requests.Session()
s.header = {
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 
  'Upgrade-Insecure-Requests' : "1",
  'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,de;q=0.4,zh-TW;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'DNT': "1",
  'Accept-Encoding': 'gzip, deflate, br',
}
s.proxies = {
  'http':'',
  'https':''}

r = s.get(news_url)
r.encoding = 'UTF-8'
dom = bs4.BeautifulSoup(r.text, 'html.parser')

news_date = ''.join(news_url.split('/')[3:5])
news_title = dom.find('td',{'class':'title'}).text
news_body = dom.find_all('table')[4]
news_text = ''
for line in news_body.find_all('p'):
  news_text += line.text + '\n\n'

news_media = []
for line in news_body.find_all('img'):
  news_media.append({
    "name": json.loads(line['sudyfile-attr'].replace("'",'"'))['title'],
    "url": line['src']})
for line in news_body.find_all('a'):
  if(line['href'].startswith('/')):
    news_media.append({
      "name": line.text,
      "url": line['href']})

with open('media/'+news_date+'-'+news_title+'.md','w') as f:
  f.write('# '+news_title+'\n\n'+news_text)

for media in news_media:
  media_url = url_host + media['url']
  r = s.get(media_url)
  with open('media/'+news_date+'-'+media['name'],'wb') as data:
    data.write(r.content)
