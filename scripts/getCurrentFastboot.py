import OScommon
from datetime import datetime
import os

os.system(f"clear")
base_url = "https://update.intl.miui.com/updates/miota-fullrom.php?d="
for device in OScommon.currentStable:
  devdata = OScommon.localData(device)
  for branch in devdata["branches"]:
    code = branch["branchCode"]
    if code == "":
      print("请修补机型： "+device+"文件中未指定的区域代码\n")
    else:
      i = 0
    btag = branch["branchtag"]
    region = branch["region"]
    carriers = branch["carrier"]
    if len(carriers)==0:
      print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t"+base_url+code+"&b="+btag+"&r="+region+"&n="+"                                   ",end="")
      print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t"+base_url+code+"&b="+btag+"&r="+region+"&n="+"                                   ",end="")
      OScommon.getFastboot(base_url+code+"&b="+btag+"&r="+region+"&n=")
    else:
      for carrier in carriers:
        print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t"+base_url+code+"&b="+btag+"&r="+region+"&n="+carrier+"                                   ",end="")
        print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t"+base_url+code+"&b="+btag+"&r="+region+"&n="+carrier+"                                   ",end="")   
        OScommon.getFastboot(base_url+code+"&b="+btag+"&r="+region+"&n="+carrier)