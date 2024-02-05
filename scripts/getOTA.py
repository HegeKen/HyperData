import OScommon
import json


for device in OScommon.currentStable:
  branchids = []
  devdata = OScommon.localData(device)
  devlength = len(devdata["branches"])
  for i in range(0,devlength):
    branchids.append(i)
  ids = list(set(branchids))
  for id in ids:
    OScommon.MiOTAForm["d"] = devdata["branches"][id]["branchCode"]
    if devdata["branches"][id]["region"] == "cn":
      OScommon.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"]
      OScommon.MiOTAForm["r"] = 'GL'
    else:
      OScommon.MiOTAForm["r"] = 'CN'
      if devdata["branches"][id]["branchCode"] == devdata["device"]+"_global":
        OScommon.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"]
      else:
        OScommon.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"].split("_global")[0]
      OScommon.MiOTAForm["b"] = devdata["branches"][id]["branchtag"]
      OScommon.MiOTAForm["options"]["zone"] = devdata["branches"][id]["zone"]
    for rom in devdata["branches"][id]["roms"]:
      current = devdata['branches'][id]["roms"][rom]
      if current["android"] == "":
        OScommon.MiOTAForm["c"] = "14"
      else:
        OScommon.MiOTAForm["c"] = current["android"].split(".0")[0]
      OScommon.MiOTAForm["v"] = "MIUI-"+ current["os"].replace('OS1','V816')
      OScommon.getFromApi(OScommon.miui_encrypt(json.dumps(OScommon.MiOTAForm)),device)
    print("\r"+devdata["name"]["zh"]+"已完成                            ",end="")
    
