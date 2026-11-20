import os
import re
import sys
import OScommon


def load_flag_draft():
	"""解析 Flags.json（非标准 JSON：逐行 "flag":"device"，允许重复 key）

	返回 (原始行列表, {flag: device})，同 flag 重复时优先保留非空 device。
	"""
	path = OScommon.get_platform_path("public/data/scripts/Flags.json")
	try:
		with open(path, encoding='utf-8') as f:
			lines = f.readlines()
	except FileNotFoundError:
		return [], {}
	mapping = {}
	for line in lines:
		m = re.search(r'"([^"]+)"\s*:\s*"([^"]*)"', line)
		if not m:
			continue
		flag, device = m.group(1), m.group(2)
		if flag not in mapping or (device and not mapping[flag]):
			mapping[flag] = device
	return lines, mapping


def known_devices():
	"""所有已知机型代号（devices 目录下的 JSON 文件名）"""
	devices_dir = OScommon.get_platform_path("public/data/devices")
	return {name[:-5] for name in os.listdir(devices_dir) if name.endswith('.json')}


def infer_device(flag, device, devices):
	"""推断 flag 所属机型：草稿已带机型则直接使用，否则按机型名最长前缀匹配

	例如 hongkong_tw_global -> hongkong，sweet_k6a_global -> sweet_k6a；
	MIUI 风格 flag（如 HOUJIGlobal）无法判断时返回空串。
	"""
	if device:
		return device
	matches = [d for d in devices if flag == d or flag.startswith(d + '_')]
	return max(matches, key=len) if matches else ''


def merge_into_oscommon(mapping):
	"""把 flag -> device 写入 OScommon.py 的 flags 字典，返回可从草稿清除的 flag 集合"""
	path = OScommon.get_platform_path("public/data/scripts/OScommon.py")
	with open(path, encoding='utf-8') as f:
		lines = f.readlines()

	start = end = None
	for i, line in enumerate(lines):
		if re.match(r'^flags\s*=\s*\{', line):
			start = i
		elif start is not None and line.strip() == '}':
			end = i
			break
	if start is None or end is None:
		print('未找到 OScommon.flags 定义，跳过自动更新')
		return set()

	existing = set(re.findall(r'^\s*"([^"]+)"\s*:', ''.join(lines[start:end]), re.M))
	added = []
	for flag, device in mapping.items():
		if flag in existing:
			continue
		# 原字典最后一项可能没写逗号，插入前补齐，避免拼接出语法错误
		prev = lines[end - 1].rstrip('\n')
		if prev.strip().endswith('}') is False and not prev.rstrip().endswith(','):
			lines[end - 1] = prev + ',\n'
		lines.insert(end, f'\t"{flag}": "{device}",\n')
		end += 1
		added.append(flag)

	if added:
		with open(path, 'w', encoding='utf-8') as f:
			f.writelines(lines)
		print(f'已写入 OScommon.flags {len(added)} 条: {", ".join(added)}')
	return set(mapping)  # 已存在 + 新写入的都视为已解决


def rewrite_draft(lines, resolved):
	"""从 Flags.json 移除已解决的条目，保留无法自动判断的"""
	path = OScommon.get_platform_path("public/data/scripts/Flags.json")
	kept = []
	for line in lines:
		m = re.search(r'"([^"]+)"\s*:', line)
		if m and m.group(1) in resolved:
			continue
		kept.append(line)
	with open(path, 'w', encoding='utf-8') as f:
		f.writelines(kept)


def sync_flags():
	"""把 Flags.json 中可判断机型的条目自动合并进 OScommon.flags"""
	lines, mapping = load_flag_draft()
	if not mapping:
		print('Flags.json 没有待处理条目')
		return
	devices = known_devices()
	resolved, pending = {}, []
	for flag, device in mapping.items():
		codename = infer_device(flag, device, devices)
		if codename:
			resolved[flag] = codename
		else:
			pending.append(flag)
	if resolved:
		merge_into_oscommon(resolved)
		rewrite_draft(lines, set(resolved))
	for flag in pending:
		print(f'无法自动判断机型，保留在 Flags.json: {flag}')


def scan():
	for device in OScommon.currentStable:
		devdata = OScommon.localData(device)
		for i in range(0,len(devdata['branches'])):
			j = i -1
			if devdata['branches'][j]['branchCode'] == '':
				print("请修补机型： "+device+"文件中未指定的区域代码\n")
			elif devdata['branches'][j]['branchCode'] in OScommon.flags:
				i = 0
			else:
				OScommon.writeFlag(devdata['branches'][j]['branchCode'],device)
			for rom in devdata['branches'][j]["roms"]:
				current = devdata['branches'][j]["roms"][rom]
				if current['recovery'] == '':
					i = 0
				else:
					if devdata['branches'][j]['branchCode'] == current['recovery'].split('-')[0]:
						flag = devdata['branches'][j]['branchCode']
					else:
						flag = OScommon.extract_flag_from_filename(current['recovery'])
					if flag in OScommon.flags:
						i = 0
					else:
						OScommon.writeFlag(flag,device)
				if current['fastboot'] == '':
					i = 0
				else:
					flag = OScommon.extract_flag_from_filename(current['fastboot'])
					if flag in OScommon.flags:
						i = 0
					else:
						OScommon.writeFlag(flag,device)


if __name__ == '__main__':
	if '--sync-only' not in sys.argv:
		scan()
	sync_flags()
