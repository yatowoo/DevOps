#!/usr/bin/env python3

# USTC-NEWS

import requests
import bs4
import socks
import json
import time
import pymysql
import re

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

# Open MySQL connection
with open('private-db.json') as f:
  API_DB = json.load(f)['rss']
  db = pymysql.connect('localhost',API_DB['USER'], API_DB['PASS'], 'rss')
  p = db.cursor()

def get_html(url, encoding='UTF-8'):
  time.sleep(REQUEST_DELAY)
  r = s.get(url)
  if(r.status_code == 200):
    print('[-] Connection OK : '+url)
    r.encoding = encoding
    if(r.url != url):
      print('[+] Redirect to: '+r.url)
      return None
    else:
      return bs4.BeautifulSoup(r.text, 'html.parser')
  else:
    print('[X] Connection FAILED: '+url)
    return None


def get_page(news_url, news_title, source='USTC', store_content = True):
  ### Check MySQL DB
  news_title = re.sub('[\[\]]',' ',news_title)
  cmd = "SELECT * FROM info WHERE title='%s' AND source='%s'" % (news_title, source)
  if(p.execute(cmd) > 0):
    print('[+] INFO existed - ' + news_title)
    return False
  else:  
    print('[+] INFO NEWS found - ' + news_title)
  try:
    cmd = "INSERT INTO info(title, abstract, url, source, info_time) VALUES ('%s', '%s','%s','%s', '%s')" % \
      (news_title, '', news_url, source, time.strftime("%Y-%m-%d 00:00:00"))
    p.execute(cmd)
    db.commit()
  except:
    db.rollback()
    raise
  ### Store page content
  if(not store_content):
    return
  ### Check External pages
  EXTERNAL_PAGE = False
  if(not news_url.startswith(url_host + '/20')):
    news_date = time.strftime('%Y%m%d') # today
    EXTERNAL_PAGE = True
  else:
    news_date = ''.join(news_url.split('/')[3:5])

  if(EXTERNAL_PAGE):
    print('[+] WARNING - Skipped external page : '+news_url)
    return False
  ### Get NEWS page content
  dom = get_html(news_url)
  if(not dom):
    print('[+] WARNING - Fail to resolve page.')
    return False

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
  return True

print('\n======RSS Update : USTC-NEWS======')
dom_news = get_html(url_news)
for elem in dom_news.find_all('tr',{'class':'light'}):
  get_page(url_host + elem.a['href'], elem.a.text)

dom_notice = get_html(url_notice)
for notice_list in dom_notice.find_all('table',{'portletmode':'simpleNews'}):
  for elem in notice_list.find_all('a'):
    get_page(url_host + elem['href'], elem.text)

# SKLPDE News
  # List: DOM.find_all('table')[7].find_all('a')
  # Content: dom.find_all('span',{'portletmode':'simpleArticleAttri'})
print('\n======RSS Update : USTC-SKLPDE======')
host_sklpde = 'http://sklpde.ustc.edu.cn'
url_sklpde = 'http://sklpde.ustc.edu.cn/7107/list.htm'
dom_sklpde = get_html(url_sklpde)
for elem in dom_sklpde.find_all('table')[7].find_all('a'):
  get_page(host_sklpde + elem['href'], elem['title'], source='USTC-SKLPDE', store_content=False)

# PNP - Particle and Nuclear Physics
  # List: ul[2] -> a
print('\n======RSS Update : USTC-PNP======')
host_pnp = 'http://pnp.ustc.edu.cn/html'
  # NEWS
url_pnp = 'http://pnp.ustc.edu.cn/html/news.php'
dom_pnp = get_html(url_pnp)
for elem in dom_pnp.find_all('ul')[2].find_all('a'):
  get_page(host_pnp + '/' + elem['href'], elem.text, source='USTC-PNP', store_content=False)
  # Seminar
url_pnp_seminar = 'http://pnp.ustc.edu.cn/html/activities.php'
dom_pnp = get_html(url_pnp_seminar)
for elem in dom_pnp.find_all('ul')[2].find_all('a'):
  get_page(host_pnp + '/' + elem['href'], elem.text, source='USTC-PNP', store_content=False)

# Physics
print('\n======RSS Update : USTC-Physics======')
host_phys = 'https://physics.ustc.edu.cn'
  # News
url_phys_news = 'https://physics.ustc.edu.cn/3588/list.htm'
dom = get_html(url_phys_news)
elem = dom.find(id='wp_news_w06').find_all('a')[1]
get_page(host_phys + elem['href'], elem['title'], source='USTC-Physics', store_content=False)
for elem in  dom.find(id='wp_news_w07').find_all('a'):
  get_page(host_phys + elem['href'], elem['title'], source='USTC-Physics', store_content=False)
  # Notice
url_phys_notice = 'https://physics.ustc.edu.cn/3584/list.htm'
dom = get_html(url_phys_notice)
for elem in dom.find(id='wp_news_w06').find_all('a') + dom.find(id='wp_news_w07').find_all('a'):
  get_page(host_phys + elem['href'], elem['title'], source='USTC-Physics', store_content=False)

# Graduate School
print('\n======RSS Update : USTC-Gradschool======')
host_grad = 'https://gradschool.ustc.edu.cn/'
dom = get_html(host_grad)
for elem in dom.find('div',{'class':'notice'}).find_all('a')[1:] + dom.find('div',{'class':'news'}).find_all('a')[1:]:
  url = elem['href']
  if(not url.startswith('http')):
    url = host_grad + '/' + url
  get_page(url, elem['title'], source='USTC-Gradschool', store_content=False)


db.close()
