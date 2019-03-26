# Scripts for server devops

## YQZX

Submit script for USTC Intergrated Research Instrument Sharing Center

### Dependecies

* python 2 (test on 2.7.12)
* [pytesseract](https://github.com/madmaze/pytesseract) (require PIL & [tesseract](https://github.com/tesseract-ocr/tesseract))

### Authentication

* Redirect to USTC-CAS
* Request username & password from keyboard
* Handle validation code (version 2019.03)

### Test form

* Create for last 4 days
* Loop form data in yqzx.json