#!/usr/bin/env python3

# Check latest Geant4 and datasets

# Request Geant4 software download page
# Format: 
# Download example:
# http://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.04.p02.tar.gz
# 

import requests
import bs4
import json

g4_url = 'http://geant4.web.cern.ch/support/download'

raw = requests.get(g4_url)
if(raw.status_code == 200):
	print('[-] Connected to Geant4 software\n\t' + g4_url)
else:
 print('[X] Error '+ raw.status_code + '- Fail to connect Geant4 software\n\t' + g4_url)
 exit()

dom = bs4.BeautifulSoup(raw.text,'html.parser')

latest = dom.select('h2')[0].text.replace('\xa0',' ')
print('[-] Geant4 latest version\n\t'+latest)

print('[-] Generate Geant4 download link')
site = 'http://geant4-data.web.cern.ch/geant4-data'

fileName = 'G4DataList.txt'
f = open(fileName,'w')
g4src = dom.select('tr')[1].text.split('"')[1]
link = site+'/releases/' + g4src
print(link)
f.write(link+'\n')

for elem in dom.select('tr'):
  if(elem.text.find('downloaddata') > -1):
    tmp = elem.text.split('"')
    link = site + '/datasets/' + tmp[1]+'.'+tmp[3]+'.tar.gz'
    f.write(link+'\n')

print('[-] Geant4 update done.\n\tDownload links output in '+fileName)
