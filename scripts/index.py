import OScommon
from datetime import datetime, timedelta
import json
import os

weekday_number = datetime.now().date().weekday()
weeks = []

for i in range(0 - weekday_number , 7):
	day = datetime.now().date() + timedelta(days=i)
	weeks.append(day.strftime("%Y-%m-%d"))
updates = {
	"recent":{
		"time": "",
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
		if branch == 'X' or branch == 'D' or "Enterprise" in devdata["branches"][num]["name"]["en"] or "EP" in devdata["branches"][num]["name"]["en"]:
			i = 0
		else:
			for rom in devdata['branches'][num]['roms']:
				if devdata['branches'][num]['roms'][rom]['release'] in weeks:
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
time = updates['recent']['time'].replace(" " , "-")
cmd_str = f"cd public/data && git add . && git commit -m '{time}' && git push origin main"
os.system(f"cd public/data && git add . && git commit -m '{time}' && git push origin main")