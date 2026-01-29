import OScommon
import json

devlist = json.loads(open("public/data/devices.json", 'r', encoding='utf-8').read())
with open("public/data/index.html", "r", encoding='utf-8') as file:
  file_content = file.read()

# print(file_content)
for brand in devlist:
  for device in devlist[brand]['devices']:
    data = OScommon.localData(device['code'])['name']['zh']
    string = f"""<div class="mdui-chip"><a href="devices/{device['code']}.json"><span class="mdui-chip-title HyperBlue"> {data}({device['code']}) </span></a></div>"""
    if string in file_content:
      continue
    else:
      print(string)