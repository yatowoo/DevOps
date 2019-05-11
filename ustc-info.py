#!/usr/bin/env python3

# USTC-NEWS

import requests
import bs4
import socks
import json
import time

REQUEST_DELAY = 0.2 # second

url_host = 'https://www.ustc.edu.cn'

# News
  # DOM.find_all('tr',{'class':'light'})
  # NEWS_URL = url_host + ELEM.a['href']
url_news = 'https://www.ustc.edu.cn/kdyw2/list.htm'
# Notice
  # DOM.find_all('table',{'portletmode':'simpleNews'})
  # NOTICE_LIST.find_all('a')
  # NOTICE_URL = url_host + ELEM['href']
url_notice = 'https://www.ustc.edu.cn/2014/list.htm'

# News content
  # DOM.find('td',{'class':'title'})
  # DOM.find_all('table')[4].find_all('p')
news_url = 'https://www.ustc.edu.cn/2019/0426/c2017a379602/page.htm'

# SKLPDE News
  # List: DOM.find_all('table')[7].find_all('a')
  # Content: dom.find_all('span',{'portletmode':'simpleArticleAttri'})
url_sklpde = 'http://sklpde.ustc.edu.cn/7107/list.htm'

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

INFO_DBFILE = open('media/USTC-INFO.json','r')
NEWS_DB = json.load(INFO_DBFILE)
INFO_DBFILE.close()

def get_html(url):
  time.sleep(REQUEST_DELAY)
  r = s.get(url)
  if(r.status_code == 200):
    print('[-] Connection OK : '+url)
    r.encoding = 'UTF-8'
    return bs4.BeautifulSoup(r.text, 'html.parser')
  else:
    print('[X] Connection FAILED: '+url)
    return None

def update_db():
  with open('media/USTC-INFO.json','w') as INFO_DBFILE:
    json.dump(NEWS_DB, INFO_DBFILE, ensure_ascii=False, indent=2)
    print('[-] DB - Update: '+INFO_DBFILE.name)

def get_page(news_url, news_title):
  ### Check External pages
  EXTERNAL_PAGE = False
  if(not news_url.startswith(url_host + '/20')):
    news_date = time.strftime('%Y%m%d') # today
    EXTERNAL_PAGE = True
  else:
    news_date = ''.join(news_url.split('/')[3:5])

  ### Check DB contents
  if(not NEWS_DB.get(news_date)):
    NEWS_DB[news_date] = []
  else:
    for news in NEWS_DB[news_date]:
      if(news['url'] == news_url):
        return False
  NEWS_DB[news_date].append({
    "title": news_title,
    "url": news_url})
  print('[+] NEWS found : ' + news_title)

  if(EXTERNAL_PAGE):
    print('[+] WARNING - Skipped external page : '+news_url)
    update_db()
    return None
  ### Get NEWS page content
  dom = get_html(news_url)

  news_title = dom.find('td',{'class':'title'}).text
  news_body = dom.find_all('table')[4]
  news_text = ''
  for line in news_body.find_all('p'):
    news_text += line.text + '\n\n'

  news_media = []
  media_count = 0
  for line in news_body.find_all('img'):
    if(not line.get('sudyfile-attr')):
      media_name = news_title[0:8] + '-' + repr(media_count) + '.' + line['src'].split('.')[1]
    else:
      media_name = json.loads(line['sudyfile-attr'].replace("'",'"'))['title']
    news_media.append({
      "name": media_name,
      "url": line['src']})
    media_count += 1
  for line in news_body.find_all('a'):
    if(line.get('href') and line['href'].startswith('/')):
      news_media.append({
        "name": line.text,
        "url": line['href']})
  # Download media (images and attachments)
  for media in news_media:
    print('----> [+] MEDIA found: '+media['name'])
    if(media['url'].startswith('/')):
      media_url = url_host + media['url']
    else:
      media_url = media['url']
    time.sleep(REQUEST_DELAY)
    r = s.get(media_url)
    if(r.status_code == 200):
      with open('media/'+news_date+'-'+media['name'].replace('/','-'),'wb') as data:
        data.write(r.content)
    else:
      print('[X] ERROR - FAIL to download media : '+media_url)
  # Output text content
  with open('media/'+news_date+'-'+news_title.replace('/','-')+'.md','w') as f:
    f.write('# '+news_title+'\n\n'+news_text)
  # Update Database
  update_db()
  return True

dom_news = get_html(url_news)
for elem in dom_news.find_all('tr',{'class':'light'}):
  get_page(url_host + elem.a['href'], elem.a.text)

dom_notice = get_html(url_notice)
for notice_list in dom_notice.find_all('table',{'portletmode':'simpleNews'}):
  for elem in notice_list.find_all('a'):
    get_page(url_host + elem['href'], elem.text)

with open('media/USTC-INFO.json','w') as INFO_DBFILE:
  json.dump(NEWS_DB, INFO_DBFILE, ensure_ascii=False, indent=2)
  print('[-] Output: '+INFO_DBFILE.name)