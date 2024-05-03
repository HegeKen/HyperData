import OScommon
import json

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


def os_replace(ver):
  if 'OS1' in ver:
    return ver.replace('OS1', 'V816')
  elif 'V816' in ver:
    return ver
  else:
    return 'V816'


device = 'zeus'
OScommon.MiOTAForm['d'] = device + ''
OScommon.MiOTAForm['R'] = 'CN'
OScommon.MiOTAForm['b'] = 'F'
OScommon.MiOTAForm['pn'] = OScommon.MiOTAForm['d'].split('_global')[0]
OScommon.MiOTAForm['c'] = '14'
OScommon.MiOTAForm['sdk'] = OScommon.sdk[OScommon.MiOTAForm['c']]
OScommon.MiOTAForm['p'] = device
OScommon.MiOTAForm['options']['zone'] = '1'
OScommon.MiOTAForm['options']['cv'] = os_replace('OS1.0.2.0.ULBCNXM')
OScommon.MiOTAForm['options']['previewPlan'] = '1'
OScommon.MiOTAForm['v'] = os_replace('OS1.0.2.0.ULBCNXM')


encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.MiOTAForm))
OScommon.getChangelog(encrypted_form, device)
