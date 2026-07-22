import OScommon
from datetime import datetime
import subprocess
from sys import platform

subprocess.run(["cls"] if platform == "win32" else ["clear"])
for device in OScommon.currentStable:
	devdata = OScommon.localData(device)
	devlength = len(devdata["branches"])
	for num in range(devlength):
		code = devdata["branches"][num]["branchCode"]
		region = devdata["branches"][num]["region"]
		zone = devdata["branches"][num]["zone"]
		branch = devdata["branches"][num]["branchtag"]
		
		# 修改这里：检查 roms 字典是否为空，并安全地获取第一个键值
		rom_keys = list(devdata['branches'][num]["roms"].keys())
		if rom_keys and len(rom_keys) > 0:
			first_key = rom_keys[0]
			if first_key != "":  # 忽略空键的情况
				current = devdata['branches'][num]["roms"][first_key]
			else:
				# 如果第一个键是空的，尝试找非空的键
				non_empty_key = None
				for key in rom_keys:
					if key != "":
						non_empty_key = key
						break
				if non_empty_key:
					current = devdata['branches'][num]["roms"][non_empty_key]
				else:
					continue  # 跳过没有有效 ROM 数据的分支
		else:
			continue  # 跳过没有 ROM 数据的分支
		
		android = current['android']
		version = current['os']
		release = current['release']
		if android == "" and version == "" and release == "":
			i = 0
		else:
			if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"]:
				print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"正在检测",device,devdata["branches"][num]["branchCode"],version,end="                                            ", flush=True)
				OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, version)))
			else:
				print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"正在检测",device,devdata["branches"][num]["branchCode"],version,end="                                            ", flush=True)
				OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, version)))
				if version =="":
					i = 0
				else:
					for i in range(0,4):
						newVer = OScommon.versionAdd(version,i)
						print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"正在检测",device,devdata["branches"][num]["branchCode"],newVer,end="                                            ", flush=True)
						OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, code, region, branch, zone, android, newVer)))