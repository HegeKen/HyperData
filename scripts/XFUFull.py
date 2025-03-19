import os
from bs4 import BeautifulSoup
import OScommon


false_packs = [
  'OS1.0.4.0.UNKCNXMmiui_VERMEER_OS1.0.4.0.UNKCNXM_c3235c755f_14.0.zip'
]
# directory = "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\hyperos"
directory = "../Sources/xmfirmwareupdater.github.io/pages/hyperos"

for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.find_all('span', {'id': 'filename'})
      for tag in span_tags:
        if tag.text in false_packs:
          continue
        else:
          OScommon.checkExist(tag.text)