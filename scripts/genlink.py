import OScommon


devdata = OScommon.localData("shennong")
branchids = []
for i in range(0,len(devdata["branches"])):
  if devdata["branches"][i]["idtag"] == "Dev" or devdata["branches"][i]["idtag"] == "CnOO":
    branchids.append(i)
  else:
    k = 0

ids = list(set(branchids))
for id in ids:
  for rom in devdata["branches"][id]["roms"]:
    data = devdata['branches'][id]["roms"][rom]
    if data["recovery"] != "":
      print("https://cdn-ota.azureedge.net/"+data["os"]+"/"+data["recovery"])
    else:
      k = 0
    if data["fastboot"] != "":
      print("https://cdn-ota.azureedge.net/"+data["os"]+"/"+data["fastboot"])
    else:
      k = 0