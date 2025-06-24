import os
import chardet
from bs4 import BeautifulSoup
import OScommon
import os

os.system(f"clear")
false_packs = [
  'OS1.0.4.0.UNKCNXMmiui_VERMEER_OS1.0.4.0.UNKCNXM_c3235c755f_14.0.zip'
]
directory = "../Sources/xmfirmwareupdater.github.io/pages/hyperos"

for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    with open(file_path, 'rb') as f:
      raw_content = f.read()
      result = chardet.detect(raw_content)
      encoding = result['encoding']
      content = raw_content.decode(encoding, errors='replace')
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.find_all('span', {'id': 'filename'})
      for tag in span_tags:
        if tag.text in false_packs:
          continue
        else:
          OScommon.checkExist(tag.text)