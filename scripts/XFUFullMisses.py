import os
from bs4 import BeautifulSoup
import json
import OScommon


XFUpacks = []
FXUMisses = []
IHave = []

# directories = [
#   "D:\\Projects\\MIUIROMS\\XFU\\pages\\miui",
#   "D:\\Projects\\MIUIROMS\\XFU\\pages\\hyperos"
# ]
directory = "D:\\Projects\\MIUIROMS\\XFU\\pages\\hyperos"
# for directory in directories:
for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    print('\r'+file_path+"                                           ",end="")
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.findAll('span', {'id': 'filename'})
      for tag in span_tags:
        XFUpacks.append(tag.text)
        OScommon.checkExist(tag.text)

for device in OScommon.currentStable:
  branchids = []
  devdata = OScommon.localData(device)
  devlength = len(devdata["branches"])
  for i in range(0,devlength):
    branchids.append(i)
  ids = list(set(branchids))
  for id in ids:
    for rom in devdata["branches"][id]["roms"]:
      link = devdata['branches'][id]["roms"][rom]
      if link['recovery'] == '':
        i = 0
      else:
        IHave.append(link['recovery'])
      if link['fastboot'] == '':
        i = 0
      else:
        IHave.append(link['fastboot'])


for link in IHave:
  if link not in XFUpacks:
    if "OS1." in link:
      file = open('public/data/scripts/XFUMisses_OS.txt', 'a', encoding='utf-8')
      file.write(link+'\n')
      file.close()
    else:
      file = open('public/data/scripts/XFUMisses_UI.txt', 'a', encoding='utf-8')
      file.write(link+'\n')
      file.close()