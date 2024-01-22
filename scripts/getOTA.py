import common
import json


for device in common.currentStable:
  branchids = []
  devdata = common.localData(device)
  devlength = len(devdata["branches"])
  for i in range(0,devlength):
    branchids.append(i)
  ids = list(set(branchids))
  for id in ids:
    common.MiOTAForm["d"] = devdata["branches"][id]["branchCode"]
    if devdata["branches"][id]["region"] == "cn":
      common.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"]
      common.MiOTAForm["r"] = 'GL'
    else:
      common.MiOTAForm["r"] = 'CN'
      if devdata["branches"][id]["branchCode"] == devdata["device"]+"_global":
        common.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"]
      else:
        common.MiOTAForm["pn"] = devdata["branches"][id]["branchCode"].split("_global")[0]
      common.MiOTAForm["b"] = devdata["branches"][id]["branchtag"]
      common.MiOTAForm["options"]["zone"] = devdata["branches"][id]["zone"]
    for rom in devdata["branches"][id]["roms"]:
      current = devdata['branches'][id]["roms"][rom]
      if current["android"] == "":
        common.MiOTAForm["c"] = "14"
      else:
        common.MiOTAForm["c"] = current["android"].split(".0")[0]
      common.MiOTAForm["v"] = "MIUI-"+ current["os"].replace('OS1','V816')
      common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm)),device)
    print("\r"+devdata["name"]["zh"]+"已完成                            ",end="")
    
