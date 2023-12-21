import common
import json

for device in common.currentStable:
  devdata = common.localData(device)
  for i in range(0,len(devdata["branches"])):
    j = i -1
    for branch in devdata["branches"]:
      latest = 0
      common.MiOTAForm["d"] = branch["branchCode"]
      if branch["region"] == "cn":
        common.MiOTAForm["pn"] = branch["branchCode"]
        common.MiOTAForm["r"] = 'GL'
      else:
        common.MiOTAForm["r"] = 'CN'
        if branch["branchCode"] == devdata["device"]+"_global":
          common.MiOTAForm["pn"] = branch["branchCode"]
        else:
          common.MiOTAForm["pn"] = branch["branchCode"].split("_global")[0]
      common.MiOTAForm["b"] = branch["branchtag"]
      common.MiOTAForm["options"]["zone"] = branch["zone"]
      common.MiOTAForm["sdk"] = common.sdk[common.MiOTAForm["c"]]
      for rom in devdata["branches"][j]["roms"]:
        current = devdata['branches'][j]["roms"][rom]
        common.MiOTAForm["c"] = current["android"].split(".0")[0]
        if current["android"] == "":
          common.MiOTAForm["c"] = "14"
        if branch["ep"] == 1:
          latest = 0
        else:
          i = 0
        common.MiOTAForm["v"] = "MIUI-"+ current["os"].replace('OS1','V816')
        common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm)),device)
        latest = current["android"]
  print("\r"+devdata["name"]["zh"]+"已完成                            ",end="")