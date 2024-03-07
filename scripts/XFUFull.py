import os
from bs4 import BeautifulSoup
import OScommon

directory = "D:\\Projects\\MIUIROMS\\XFU\\pages\\hyperos"

for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    print('\r'+file_path+"                                           ",end="")
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.findAll('span', {'id': 'filename'})
      for tag in span_tags:
        OScommon.checkExist(tag.text)