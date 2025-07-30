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
pre_zh = "SELECT id FROM roms WHERE logs_zh IS NULL AND branch !='X'"
pre_en = "SELECT id FROM roms WHERE logs_en IS NULL AND branch !='X'"
result = OScommon.db_job(pre_zh)
if len(result) > 0:
  ids_zh = [x[0] for x in result]
else:
  i = 0
ids_zh.reverse()
start = 46000
i = 0
for id in ids_zh:
  i = i+1
  if start !=0 and id <=start:
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
    print("\r",id,current[5],current[1],i,"/",len(ids_zh),"zh_CN","                         ",end="")
    OScommon.HyperOSForm['l'] = 'zh_CN'
    encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm))
    log = OScommon.getChangelog2DB(encrypted_form, current[0],current[5])
    if log == False:
      continue
    else:
      # print(log)
      uplog = OScommon.db_job(f"UPDATE roms SET logs_zh = '{log}' WHERE id = %s" % (id))

pre_en = "SELECT id FROM roms WHERE logs_en IS NULL AND branch !='X'"
result = OScommon.db_job(pre_en)
if len(result) > 0:
  ids_en = [x[0] for x in result]
else:
  i = 0
ids_en.reverse()
start = 46000
i = 0
for id in ids_en:
  i = i+1
  if start !=0 and id <=start:
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
    print("\r",id,current[5],current[1],i,"/",len(ids_en),"en_US","                         ",end="")
    OScommon.HyperOSForm['l'] = 'en_US'
    encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm))
    log = OScommon.getChangelog2DB(encrypted_form, current[0],current[5])
    if log == False:
      continue
    else:
      # print(log)
      uplog = OScommon.db_job(f"UPDATE roms SET logs_en = '{log}' WHERE id = %s" % (id))