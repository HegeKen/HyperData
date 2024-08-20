# import OScommon

# OS = "OS1.0.24.2.26.DEV"
# osbv = OS[:5]
# print(osbv)

import json
dev = []

devices = json.loads(open("public/data/devices.json", 'r', encoding='utf-8').read())
for brand in devices:
  for device in devices[brand]['devices']:
    if device in dev:
      i = 0
    else:
      dev.append(device['code'])

print(dev)