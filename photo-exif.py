#!/bin/env python3

import sys
from PIL import Image

with Image.open(sys.argv[1]) as img:
  try:
    exif = img._getexif()
  except Exception:
    print("Error")
    exit()
  if(exif is None):
    exit()
  cam = exif.get(272)
  if(cam is not None):
    cam = cam.strip('\0')
    if(cam is not None):
      print(cam)