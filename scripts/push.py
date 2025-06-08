import OScommon
from datetime import datetime, timedelta
import json
import os
import config
import time
from sys import platform

weekday_number = datetime.now().date().weekday()
weeks = []

for i in range(0 - weekday_number , 7):
	day = datetime.now().date() + timedelta(days=i)
	weeks.append(day.strftime("%Y-%m-%d"))
updates = {
	"recent":{
		"time": "",
		"developing": "no",
		"roms": []
	}
}
updates["recent"]['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for device in OScommon.order:
	devdata = OScommon.localData(device)
	code = devdata['device']
	name = {
		"zh": devdata['name']['zh'],
		"en": devdata['name']['en']
	}
	roms = ""
	for num in range(len(devdata['branches'])):
		tag = devdata['branches'][num]['idtag']
		branch = devdata["branches"][num]["branchtag"]
		if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"] or "Demo" in devdata["branches"][num]["name"]["en"]:
			i = 0
		else:
			for rom in devdata['branches'][num]['roms']:
				if devdata['branches'][num]['roms'][rom]['release'] in weeks:
					if devdata['branches'][num]['roms'][rom]['os'] in roms:
						i = 0
					else:
						roms = roms + "; " + devdata['branches'][num]['roms'][rom]['os']
	if roms[2:] == "":
		i = 0
	elif roms[2:] in updates.__str__():
		i = 0
	else:
		json_str = '{"code": "'+code+'",''"name": '+json.dumps(name)+',"rom": "'+roms[2:]+'"}'
		updates["recent"]['roms'].append(json.loads(json_str))

with open('public/data/index.json', 'w', encoding='utf-8') as f:
	json.dump(updates, f, ensure_ascii=False, indent=2)
f.close()
errors = []
for device in OScommon.currentStable:
	checker = OScommon.entryChecker(OScommon.localData(device),device)
	devdata = OScommon.localData(device)
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
	os.system(f"cd public/data && git add . && git commit -m {updates['recent']['time'].replace(" " , "-")} && git push origin main")