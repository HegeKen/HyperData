import OScommon
import os
import time


def entryChecker(data,device):
	check =[]
	# 1是有问题，0是没有问题
	code = data['code']
	for branch in data['branches']:
		if data['device'] in branch['branchCode']:
			roms = branch['roms']
			bname = branch['name']['zh']
			menu_items = branch['table']
			if len(menu_items) != len(set(menu_items)):
				print(device, bname, "菜单项重复")
				check.append(1)
			else:
				for os_version, rom_info in roms.items():
					if os_version[:5] not in data['suppports']:
						if "Developer" in branch['name']['en']:
							i = 0
						else:
							print(device, bname, os_version[:5], os_version, "大版本号没有记录")
							check.append(1)
					if rom_info['android'] not in data['android']:
						print(device, bname, rom_info['android'], os_version, "Android版本号没有记录")
						check.append(1)
					if rom_info['recovery'] != "" and rom_info['recovery'].endswith(".zip") and os_version in rom_info['recovery']:
						i = 0
					elif rom_info['recovery'] == "":
						i = 0
					else:
						if "Developer" in branch['name']['en']:
							i = 0
						else:
							print(device, bname, os_version, "卡刷包的信息不对")
							check.append(1)
					for i in range(4,len(menu_items)):
						if rom_info[menu_items[i]] != "" and rom_info[menu_items[i]].endswith(".tgz") and os_version in rom_info[menu_items[i]]:
							i = 0
						elif rom_info[menu_items[i]] == "":
							i = 0
						else:
							if "Developer" in branch['name']['en']:
								i = 0
							else:
								print(device, bname, os_version, "线刷包的信息不对")
								check.append(1)
					if os_version != rom_info['os']:
						print(device, bname, os_version, "版本号不匹配")
						check.append(1)
					else:
						if branch['ep'] == "1" or branch['branchtag'] == 'X':
							i = 0
						else:
							if code+branch['tag'] in os_version:
								i = 0
							else:
								print(device, bname, os_version, "版本号不匹配")
							check.append(1)
		else:
			print(device, "机型与分支不配，请核实", branch['branchCode'])
			check.append(1)
	return check
	
errors = []
device = ['star']
for device in OScommon.currentStable:
	if entryChecker(OScommon.localData(device),device):
		continue
	else:
		continue