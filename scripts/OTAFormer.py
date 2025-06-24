import OScommon
from datetime import datetime
import os

os.system(f"clear")
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
		release = current['release']
		if android == "" and version == "" and release == "":
			i = 0
		else:
			if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"]:
				print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t正在完成 "+device+" ， 分支为："+devdata["branches"][num]["branchCode"]+"，版本为: "+version,end="               ", flush=True)
				OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, version)))
			else:
				print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t正在完成 "+device+" ， 分支为："+devdata["branches"][num]["branchCode"]+"，版本为: "+version,end="               ", flush=True)
				OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, version)))
				if version =="":
					i = 0
				else:
					for i in range(0,4):
						newVer = OScommon.versionAdd(version,i)
						print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t正在完成 "+device+" ， 分支为："+devdata["branches"][num]["branchCode"]+"，版本为: "+newVer,end="               ", flush=True)
						OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, newVer)))