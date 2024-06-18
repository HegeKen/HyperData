import OScommon
from datetime import datetime

for device in OScommon.currentStable:
  devdata = OScommon.localData(device)
  devlength = len(devdata["branches"])
  for num in range(devlength):
    code = devdata["branches"][num]["branchCode"]
    region = devdata["branches"][num]["region"]
    zone = devdata["branches"][num]["zone"]
    branch = devdata["branches"][num]["branchtag"]
    current = devdata['branches'][num]["roms"][list(devdata['branches'][num]["roms"].keys())[0]]
    android = current['android']
    version = current['os']
    print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t正在完成"+devdata["name"]["zh"]+"("+device+")，分支为："+devdata["branches"][num]["branchCode"]+"                                                       ",end="")
    if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"]:
      OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, version)))
    else:
      for i in range(0,3):
        OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, OScommon.versionAdd(current['os'],i))))