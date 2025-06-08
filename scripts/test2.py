import OScommon
import json

def os_replace(ver):
  if 'OS1' in ver:
    return ver.replace('OS1', 'V816')
  else:
    return ver

langs = ['zh_CN', 'en_US']
pre = "SELECT id FROM roms"
result = OScommon.db_job(pre)
if len(result) > 0:
  ids = [x[0] for x in result]
else:
  i = 0
ids.reverse()
info = OScommon.db_job("SELECT device,code,region,branch,android,version,zone FROM roms WHERE id = 41114")
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
for lang in langs:
  OScommon.HyperOSForm['l'] = lang
  encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm))
  OScommon.getChangelog2DB(encrypted_form, current[0],current[5])