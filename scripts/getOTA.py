import OScommon
import json


settings = {
  "OS1.0":"816",
  "V816.":"V140",
  "":"816"
}
  


for device in OScommon.currentStable:
  branchids = []
  devdata = OScommon.localData(device)
  devlength = len(devdata["branches"])
  for i in range(0,devlength):
    branchids.append(i)
  ids = list(set(branchids))
  for id in ids:
    OScommon.HyperOSForm["d"] = devdata["branches"][id]["branchCode"]
    branchname = devdata["branches"][id]["name"]['en']
    if devdata["branches"][id]["region"] == "cn":
      OScommon.HyperOSForm["pn"] = devdata["branches"][id]["branchCode"]
      OScommon.HyperOSForm["r"] = 'CN'
    else:
      OScommon.HyperOSForm["r"] = 'GL'
      if devdata["branches"][id]["branchCode"] == devdata["device"]+"_global":
        OScommon.HyperOSForm["pn"] = devdata["branches"][id]["branchCode"]
      else:
        OScommon.HyperOSForm["pn"] = devdata["branches"][id]["branchCode"].split("_global")[0]
      OScommon.HyperOSForm["b"] = devdata["branches"][id]["branchtag"]
      OScommon.HyperOSForm["options"]["zone"] = devdata["branches"][id]["zone"]
    print("\r正在完成"+devdata["name"]["zh"]+"("+devdata["branches"][id]["branchCode"]+")"+"                                                       ",end="")
    for rom in devdata["branches"][id]["roms"]:
      current = devdata['branches'][id]["roms"][rom]
      if current["os"] == "":
        continue
      else:
        if current["android"] == "":
          OScommon.HyperOSForm["c"] = "14"
        else:
          OScommon.HyperOSForm["c"] = current["android"].split(".0")[0]
        if "Developer Preview" in branchname:
          OScommon.HyperOSForm["v"] = "MIUI-V816.0."+ current["os"]
          OScommon.HyperOSForm["obv"] = current["os"]
          OScommon.HyperOSForm["bv"] = "V816"
        else:
          OScommon.HyperOSForm["v"] = "MIUI-"+ current["os"].replace('OS1','V816')
          OScommon.HyperOSForm["obv"] = current["os"][:5]
          OScommon.HyperOSForm["bv"] = settings[current["os"][:5]]
        OScommon.getFromApi(OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm)))
    