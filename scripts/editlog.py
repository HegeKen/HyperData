import OScommon
import json
langs = ['zh_CN', 'en_US']
logs_zh = []
logs_en = []
pre_zh = "SELECT id,logs_zh FROM roms WHERE logs_zh IS NOT NULL"
pre_en = "SELECT id,logs_en FROM roms WHERE logs_en IS NOT NULL"
results = OScommon.db_job(pre_zh)
for result in results:
  # 库中已是 ID 引用结构，先解码为原文对象再按原逻辑清洗，最后重新编码回 ID 结构
  log = OScommon.strip_log(OScommon.changelog_decode(result[1]))
  id = result[0]
  encoded = OScommon.changelog_encode(OScommon.remove_spaces(log))
  uplog = OScommon.db_job(f"UPDATE roms SET logs_zh = '{encoded}' WHERE id = %s" % (id))

results = OScommon.db_job(pre_en)
for result in results:
  log = OScommon.strip_log(OScommon.changelog_decode(result[1]))
  id = result[0]
  encoded = OScommon.changelog_encode(OScommon.remove_spaces(log))
  uplog = OScommon.db_job(f"UPDATE roms SET logs_en = '{encoded}' WHERE id = %s" % (id))
