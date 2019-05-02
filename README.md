# DevOps

> Scripts for server devops.

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

* [DevOps](#devops)
	* [Contents](#contents)
	* [SS](#ss)
		* [Usage](#usage)
		* [ChangeLogs](#changelogs)
	* [YQZX](#yqzx)
		* [Usage](#usage-1)
		* [ChangeLogs](#changelogs-1)
		* [Dependecies](#dependecies)
		* [Authentication](#authentication)
		* [Test form](#test-form)

<!-- /code_chunk_output -->


## Contents

Script|Description|Source|
-|-|-|
bench-teddysun.sh|Print system info and run benchmark on I/O and network|[TeddySun](https://teddysun.com/444.html)|
certbot-auto.sh|Auto SSL certification from Let's Encrypt||
shadowsocsR.sh|Setup and Start shadowsocks server|[TeddySun](https://shadowsocks.be/9.html)|
geant4-get.py|Get latest [geant4](http://geant4.web.cern.ch/support/download) source and data url. Output `G4DataList.txt`||
yqzx.py|Submit and Edit script for`yqzx.ustc.edu.cn`||
ss/kingss.py|Check traffic usage of __kingss__||
ss/check-ss.sh|Check traffic usage and ping latency of kingss||s

## SS

To check __traffic usage__ and __ping latency__ of ss servers.

All codes stored and running under `ss/`, but read server info from `private-db.json`

### Usage

* __*./kingss.py*__: Retrieve traffic data from web server (`requests`, `bs4`).
* __*./check-ss.sh*__: Main script, output logs.

### ChangeLogs

2019.05.01 - Init from old scripts.

## YQZX

Submit script for USTC Intergrated Research Instrument Sharing Center

### Usage

./yqzx.py [new | edit] [debug]

### ChangeLogs

2019.04.04 - Feedback from lzy9404 & zhui

* FIX form issue caused by shallow copy
* NEW mode for form editting
* Check validation code and get intput from user when failed
* MORE outputs/prompts in Chinese

2019.03.26 - New login feature for validation code

2018.12.13 - Move YQZX to this repo

### Dependecies

* python 2 (test on 2.7.12)
* [pytesseract](https://github.com/madmaze/pytesseract) (require PIL & [tesseract](https://github.com/tesseract-ocr/tesseract))

### Authentication

* Redirect to USTC-CAS
* Request username & password from keyboard
* Handle validation code

### Test form

* Create for last 4 days
* Loop form data in yqzx.json
* Edit/Update all submitted testings or add userdefined filter inline