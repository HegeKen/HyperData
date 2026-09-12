#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从数据库 roms 表比对 HyperOS 数据是否已收录到设备 JSON 文件：
- 版本在 JSON 任意分支都不存在时，按对应分支的 table 结构补建条目并插入到正确的版本位置
  （os/android/release/aspatch/文件名等数据全部来自数据库，不发起网络请求）
- 版本已在目标分支但缺少 recovery/fastboot/运营商定制机文件字段时，用数据库数据补全
- 版本实际已在其他分支（数据库 tag 标注漂移）时跳过，避免重复收录
- 补建条目后，同步核查设备的 supports / android 字段（仅内存修改，随设备文件一起写回）

用法：
  python3 sync_roms_from_db.py              # 执行比对并写入 JSON
  python3 sync_roms_from_db.py --dry-run    # 只比对并打印结果（含跳过明细），不写文件
  python3 sync_roms_from_db.py houji klee   # 只处理指定设备（可与 --dry-run 组合）
"""

import OScommon
import json
import os
import sys
from collections import OrderedDict

# 基于脚本位置(public/data/scripts)推导项目根目录，兼容任意工作目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'public', 'data', 'devices')

# 数据库文件字段 -> JSON 文件字段（运营商字段命名不一致）
FILE_FIELD_MAP = (
	('recovery', 'recovery'),
	('fastboot', 'fastboot'),
	('ctelecom', 'ctelecom'),
	('cmobile', 'cnmobile'),
	('cunicom', 'cnunicom'),
)

# 行字段下标：id, device, code, tag, version, android,
# recovery, fastboot, ctelecom, cmobile, cunicom,
# aspatch, beta_date, public_date, release_date
SELECT_SQL = """
SELECT id, device, code, tag, version, android,
       recovery, fastboot, ctelecom, cmobile, cunicom,
       aspatch, beta_date, public_date, release_date
FROM roms
WHERE type = 'HyperOS'
ORDER BY id
"""


def date_str(value):
	"""date/datetime -> 'YYYY-MM-DD'，空值返回空字符串"""
	if not value:
		return ''
	return str(value)


def infer_android(version):
	"""从 HyperOS 版本号推断安卓大版本（OS1->14.0, OS2->15.0, OS3+->16.0）"""
	if version.startswith('OS'):
		try:
			major = int(version.split('.')[0][2:])
		except (ValueError, IndexError):
			return ''
		if major == 1:
			return '14.0'
		if major == 2:
			return '15.0'
		if major >= 3:
			return '16.0'
	return ''


def resolve_branch(devdata, code, db_tag, version):
	"""确定数据库记录在 JSON 中对应的分支

	优先级：
	1. EP 政企版（版本含 EP.STDEE，数据库 code 可能不带 _ep_stdee 后缀）
	2. .BETA 后缀的 Beta 分支
	3. branchCode == code 且 idtag == 数据库 tag（权威匹配）
	4. CNXM 版本按构建号回退（build 0 -> CnOO 正式版，否则 CnOB 测试版）
	5. 非 CNXM 版本按版本号末尾 tag（如 EUXM/IDXM）匹配
	6. branchCode 唯一候选直接使用
	"""
	branches = devdata.get('branches', [])

	def same_code():
		return [b for b in branches if b.get('branchCode') == code]

	# 1. EP 政企版
	if '.EP.STDEE' in version or 'EPSTDE' in version:
		for b in branches:
			if b.get('idtag') in ('EPSTD', 'STDEE') or b.get('ep') == '1':
				if b.get('branchCode') in (code, code + '_ep_stdee'):
					return b

	# 2. .BETA 版本
	if version.endswith('.BETA'):
		for b in same_code():
			if b.get('idtag') == db_tag or b.get('idtag') == 'Beta':
				return b

	# 3. code + 数据库 idtag 精确匹配
	exact = [b for b in same_code() if b.get('idtag') == db_tag]
	if len(exact) == 1:
		return exact[0]
	if len(exact) > 1:
		# 重复分支：优先选已包含该版本的，否则取第一个
		for b in exact:
			if version in b.get('roms', {}):
				return b
		return exact[0]

	# 4. CNXM 按构建号判定
	if 'CNXM' in version:
		parts = version.split('.')
		try:
			want = 'CnOO' if int(parts[3]) == 0 else 'CnOB'
		except (ValueError, IndexError):
			want = 'CnOB'
		for b in same_code():
			if b.get('idtag') == want:
				return b

	# 5. 版本号末尾 tag 匹配（如 OS...EUXM 取最后 4 位）
	parts = version.split('.')
	if len(parts) >= 5:
		suffix = parts[-1][-4:]
		for b in same_code():
			if b.get('tag') == suffix:
				return b
		# tag 命中且 branchCode 包含 code
		for b in branches:
			if b.get('tag') == suffix and code in b.get('branchCode', ''):
				return b

	# 6. 唯一候选
	candidates = same_code()
	if len(candidates) == 1:
		return candidates[0]

	return None


def build_rom_entry(branch, row):
	"""按分支 table 定义、以数据库记录构建新的 ROM 条目"""
	version = row[4]
	android = row[5] or infer_android(version)
	# recovery 发布日期取 beta_date，其次 fastboot 的 public_date
	release = date_str(row[12]) or date_str(row[13]) or date_str(row[14])
	aspatch = date_str(row[11])

	table = branch.get('table') or ['os', 'android', 'release', 'aspatch', 'recovery', 'fastboot']
	entry = {}
	for field in table:
		if field == 'os':
			entry[field] = version
		elif field == 'android':
			entry[field] = android
		elif field == 'release':
			entry[field] = release
		elif field == 'aspatch':
			entry[field] = aspatch
		else:
			entry[field] = ''

	# 按数据库中的文件名填充对应字段
	for idx, (_, json_field) in enumerate(FILE_FIELD_MAP, start=6):
		filename = row[idx]
		if filename and json_field in table:
			entry[json_field] = filename
	return entry


def fill_missing_files(branch, rom_data, row):
	"""版本已存在时，用数据库数据补全 JSON 中缺失的文件字段，返回补充的字段列表"""
	table = branch.get('table', [])
	filled = []
	for idx, (_, json_field) in enumerate(FILE_FIELD_MAP, start=6):
		filename = row[idx]
		if filename and json_field in table and not rom_data.get(json_field):
			rom_data[json_field] = filename
			filled.append(json_field)
	return filled


def insert_rom_sorted(branch, version, entry):
	"""按版本号降序插入到分支 roms 的正确位置（与 add_rom_to_json 规则一致）"""
	roms = branch.get('roms', {})

	def sort_key(v):
		parsed = OScommon.parse_version(v)
		return parsed if parsed is not None else (999, 999, 999, 999)

	ordered = OrderedDict()
	inserted = False
	for existing in sorted(roms.keys(), key=sort_key, reverse=True):
		if not inserted and OScommon.compare(version, existing):
			ordered[version] = entry
			inserted = True
		ordered[existing] = roms[existing]
	if not inserted:
		ordered[version] = entry
	branch['roms'] = dict(ordered)


def sync_hyperos_to_json(dry_run=False, only_devices=None):
	rows = OScommon.db_job(SELECT_SQL)
	print(f"数据库 HyperOS 记录共 {len(rows)} 条" + ("（dry-run，不写入文件）" if dry_run else ''))
	if only_devices:
		print(f"仅处理设备: {', '.join(only_devices)}")
	print('-' * 80)

	dev_cache = {}       # device -> devdata
	dirty = set()        # 有变更的设备
	stats = {
		'added': 0,        # 补建的版本条目
		'filled': 0,       # 补全的文件字段（条目数）
		'exists': 0,       # 版本已存在且数据完整
		'in_other': 0,     # 版本已在其他分支，跳过
		'no_branch': 0,    # 找不到对应分支
		'no_file': 0,      # 数据库记录没有任何文件名
	}

	def load_device(device):
		if device not in dev_cache:
			path = os.path.join(DATA_DIR, device + '.json')
			if not os.path.exists(path):
				dev_cache[device] = None
			else:
				with open(path, 'r', encoding='utf-8') as f:
					dev_cache[device] = json.load(f)
		return dev_cache[device]

	for row in rows:
		rom_id, device, code, db_tag, version = row[0], row[1], row[2], row[3], row[4]
		if only_devices and device not in only_devices:
			continue

		filenames = {json_field: row[6 + i] for i, (_, json_field) in enumerate(FILE_FIELD_MAP) if row[6 + i]}
		if not filenames:
			stats['no_file'] += 1
			continue

		devdata = load_device(device)
		if devdata is None:
			print(f"✗ id=  {rom_id} {device} {version}：设备 JSON 文件不存在，跳过")
			stats['no_branch'] += 1
			continue

		branch = resolve_branch(devdata, code, db_tag, version)
		if branch is None:
			print(f"✗ id=  {rom_id} {device} {version}：找不到对应分支(code={code}, tag={db_tag})，跳过")
			stats['no_branch'] += 1
			continue

		roms = branch.setdefault('roms', {})

		# 版本已在目标分支：只补缺文件字段
		if version in roms:
			filled = fill_missing_files(branch, roms[version], row)
			if filled:
				stats['filled'] += 1
				dirty.add(device)
				print(f"↧ id= {rom_id} {device} {version} -> {branch.get('idtag')}：补全字段 {', '.join(filled)}")
			else:
				stats['exists'] += 1
			continue

		# 版本已在其他分支（数据库 tag 漂移）：不重复收录
		other = [b.get('idtag') for b in devdata.get('branches', []) if version in b.get('roms', {})]
		if other:
			stats['in_other'] += 1
			if dry_run:
				print(f"＝ id= {rom_id} {device} {version}：目标分支 {branch.get('idtag')} ，"
					  f"实际已在 {', '.join(other)}，跳过")
			continue

		# 补建版本条目
		entry = build_rom_entry(branch, row)
		insert_rom_sorted(branch, version, entry)
		OScommon.check_devices_supports(device, entry.get('android', ''), version, devdata)
		dirty.add(device)
		stats['added'] += 1
		print(f"＋ id= {rom_id} {device} {version} -> {branch.get('idtag')} "
			  f"({branch.get('tag', '')}/{branch.get('branchCode', '')})，文件字段：{', '.join(filenames.keys())}")

	# 写回有变更的设备文件
	written_files = 0
	if not dry_run:
		for device in sorted(dirty):
			path = os.path.join(DATA_DIR, device + '.json')
			indent = OScommon.detect_json_indent(path)
			with open(path, 'w', encoding='utf-8', newline='\n') as f:
				json.dump(dev_cache[device], f, ensure_ascii=False, indent=indent, sort_keys=False)
			written_files += 1

	print('-' * 80)
	print(f"补建版本条目: {stats['added']}")
	print(f"补全文件字段的条目: {stats['filled']}")
	print(f"已存在且完整: {stats['exists']}")
	print(f"已在其他分支跳过: {stats['in_other']}")
	print(f"无文件名跳过: {stats['no_file']}")
	print(f"找不到分支/文件: {stats['no_branch']}")
	print(f"变更设备数: {len(dirty)}" + (f"，已写入 {written_files} 个文件" if not dry_run else "（dry-run 未写入）"))


if __name__ == '__main__':
	args = sys.argv[1:]
	dry_run = '--dry-run' in args
	devices = [a for a in args if not a.startswith('--')]
	sync_hyperos_to_json(dry_run=dry_run, only_devices=devices or None)
