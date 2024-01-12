import os
from bs4 import BeautifulSoup
import re
import common

directory = "D:\\Projects\\MIUIROMS\\XFU\\pages\\miui"

for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      button_tags = soup.find_all('button')
      pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      link_pattern = re.compile(pattern, re.IGNORECASE)
      for button in button_tags:
        for link in link_pattern.findall(str(button)):
          if "zip" in link:
            link = re.split(r'\.zip', link)[0]+'.zip'
          elif "tgz" in link:
            link = re.split(r'\.tgz', link)[0]+'.tgz'
          else:
            link = ""

          if link != "":
            if 'ota' in link or 'OS' in link:
              i = 0
            else:
              package = link.split('/')[4]
              common.checkExist(package)
          else:
            i = 0
