import OScommon
import json
langs = ['zh_CN', 'en_US']
logs_zh = []
logs_en = []
pre_zh = "SELECT id,logs_zh FROM roms WHERE logs_zh IS NOT NULL"
pre_en = "SELECT id,logs_en FROM roms WHERE logs_en IS NOT NULL"
results = OScommon.db_job(pre_zh)
for result in results:
  log = OScommon.strip_log(json.loads(result[1]))
  id = result[0]
  uplog = OScommon.db_job(f"UPDATE roms SET logs_zh = '{json.dumps(OScommon.remove_spaces(log), ensure_ascii=False)}' WHERE id = %s" % (id))

results = OScommon.db_job(pre_en)
for result in results:
  log = OScommon.strip_log(json.loads(result[1]))
  id = result[0]
  uplog = OScommon.db_job(f"UPDATE roms SET logs_en = '{json.dumps(OScommon.remove_spaces(log), ensure_ascii=False)}' WHERE id = %s" % (id))