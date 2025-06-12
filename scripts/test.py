import OScommon
import json

def os_replace(ver):
  if 'OS1' in ver:
    return ver.replace('OS1', 'V816')
  else:
    return ver

langs = ['zh_CN', 'en_US']
logs_zh = []
logs_en = []
pre = "SELECT id FROM roms WHERE logs_zh IS NULL OR logs_en IS NULL"
result = OScommon.db_job(pre)
if len(result) > 0:
  ids = [x[0] for x in result]
else:
  i = 0
ids.reverse()
start = 0
i = 0
for id in ids:
  i = i+1
  if start !=0 and id >=start:
    continue
  else:
    info = OScommon.db_job("SELECT device,code,region,branch,android,version,zone FROM roms WHERE id = %s" % (id))
    current = info[0]
    OScommon.HyperOSForm['d'] = current[1]
    OScommon.HyperOSForm['R'] = current[2]
    OScommon.HyperOSForm['b'] = current[3]
    OScommon.HyperOSForm['pn'] = current[1].split('_global')[0]
    OScommon.HyperOSForm['c'] = current[4]
    OScommon.HyperOSForm['sdk'] = OScommon.sdk[current[4]]
    OScommon.HyperOSForm['p'] = current[0]
    OScommon.HyperOSForm['options']['zone'] = current[6]
    OScommon.HyperOSForm['options']['cv'] = os_replace(current[5])
    OScommon.HyperOSForm['v'] = os_replace(current[5])
    OScommon.HyperOSForm['ov'] = os_replace(current[5])
    print("\r",id,current[5],current[1],i,"/",len(ids),"                         ",end="")
    for lang in langs:
      OScommon.HyperOSForm['l'] = lang
      encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm))
      log = OScommon.getChangelog2DB(encrypted_form, current[0],current[5])
      if log == False:
        continue
      else:
        # print(log)
        if lang == 'zh_CN':
          uplog = OScommon.db_job(f"UPDATE roms SET logs_zh = '{log}' WHERE id = %s" % (id))
        elif lang == 'en_US':
          uplog = OScommon.db_job(f"UPDATE roms SET logs_en = '{log}' WHERE id = %s" % (id))