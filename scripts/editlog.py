import json

import OScommon


def clean_logs(localized):
	"""对已解码的各语言日志重新清洗，返回 {语言列: 清洗后原文对象}"""
	cleaned = {}
	for column, log in localized.items():
		cleaned[column] = OScommon.strip_log(OScommon.remove_spaces(log))
	return cleaned


rows = OScommon.DatabaseManager.execute(
	"SELECT id, logs FROM roms WHERE logs IS NOT NULL AND logs != ''",
	fetch_one=False, raise_on_error=True,
)

for row in rows or []:
	rom_id, value = row[0], row[1]
	try:
		localized = OScommon.LogStore.build_localized(json.loads(value))
	except (json.JSONDecodeError, TypeError):
		continue
	if not localized:
		continue
	encoded = OScommon.LogStore.write_logs(clean_logs(localized))
	OScommon.DatabaseManager.execute(
		"UPDATE roms SET logs = %s WHERE id = %s",
		params=(encoded, rom_id), raise_on_error=True,
	)

print(f"已重新清洗 {len(rows or [])} 条记录的各语言日志")
