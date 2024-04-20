import OScommon
import json

devlist = json.loads(open("public/data/devices.json", 'r', encoding='utf-8').read())

for brand in devlist:
  for device in devlist[brand]['devices']:
    data = OScommon.localData(device['code'])['name']['zh']
    string = "<div class=\"mdui-chip\"><a href=\"devices\/"+device['code']+".json\"><span class=\"mdui-chip-title HyperBlue\">"+data+"("+device['code']+")</span></a></div>"
    print(string)
