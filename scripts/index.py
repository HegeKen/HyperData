import OScommon
from datetime import datetime, timedelta, timezone
import json
import os
import config
import time
from sys import platform

# 获取东八区时区
tz = timezone(timedelta(hours=8))

weekday_number = datetime.now().date().weekday()
weeks = []

for i in range(0 - weekday_number , 7):
	day = datetime.now().date() + timedelta(days=i)
	weeks.append(day.strftime("%Y-%m-%d"))

# 获取当前东八区时间
current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

updates = {
	"recent":{
		"time": current_time,
		"developing": "no",
		"roms": {}
	}
}

# 更新 index.json 的 time 字段
index_json_path = 'public/data/index.json'
if os.path.exists(index_json_path):
	with open(index_json_path, 'r', encoding='utf-8') as f:
		index_data = json.load(f)
	index_data["recent"]["time"] = current_time
	with open(index_json_path, 'w', encoding='utf-8') as f:
		json.dump(index_data, f, ensure_ascii=False, indent=2)
	print(f"✓ 已更新 index.json 的 time 字段: {current_time}")

errors = []
for device in OScommon.currentStable:
	if device in OScommon.unreleased:
		i = 0
	else:
		devdata = OScommon.localData(device)
		checker = OScommon.entryChecker(devdata,device)
		devlength = len(devdata["branches"])
		for num in range(devlength): 	
			branch = devdata["branches"][num]["branchtag"]
			if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"]:
				i = 0
			else:
				roms = [list(devdata['branches'][num]["roms"].keys())][0]
				for i in range(len(roms)-1):
					if OScommon.compare(roms[i],roms[i+1]) == False:
						errors.append(1)
						print(device,roms[i],roms[i+1],"版本顺序有误，请核实")
					else:
						i = 0
		if checker ==0:
			i = 0
		else:
			errors.append(1)

if 1 in list(set(errors)):
	print("数据有误，请核实后提交git")
else:
	print("开始更新 devices.json 中的 supports 和 android 字段...")
	
	# 读取 devices.json
	devices_json_path = 'public/data/devices.json'
	with open(devices_json_path, 'r', encoding='utf-8') as f:
		devices_data = json.load(f)
	updated_count = 0
	for brand_key in devices_data:
		brand_info = devices_data[brand_key]
		if 'devices' not in brand_info:
			continue
		for device_idx, device_info in enumerate(brand_info['devices']):
			code = device_info.get('code')
			if not code:
				continue
			device_file_path = f'public/data/devices/{code}.json'
			if not os.path.exists(device_file_path):
				print(f"  ⚠ 警告: 设备文件不存在 - {device_file_path}")
				continue
			
			try:
				with open(device_file_path, 'r', encoding='utf-8') as f:
					device_data = json.load(f)
				supports = device_data.get('suppports', [])
				android = device_data.get('android', [])
				
				if supports or android:
					devices_data[brand_key]['devices'][device_idx]['supports'] = supports
					devices_data[brand_key]['devices'][device_idx]['android'] = android
					updated_count += 1
					
			except Exception as e:
				print(f"  ✗ 错误: 处理 {code} 时出错 - {str(e)}")
				continue
	with open(devices_json_path, 'w', encoding='utf-8') as f:
		json.dump(devices_data, f, ensure_ascii=False, indent='\t')
	
	print(f"✓ 完成！共更新了 {updated_count} 个设备的 supports 和 android 字段")
	print()
	os.system(f"cd public/data && git add . && git commit -m {updates['recent']['time'].replace(" " , "-")} && git push origin main")
	time.sleep(8)
	os.system(f"curl -X POST \"{config.deploy_url}\"")
	if platform == "win32":
		os.system(f"cls")
	else:
		os.system(f"clear")
	print("数据提交成功")
	print("网站已更新")