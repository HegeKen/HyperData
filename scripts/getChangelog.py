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
    return ver[:5]


device = 'rothko'
OScommon.HyperOSForm['d'] = device + ''
OScommon.HyperOSForm['R'] = 'CN'
OScommon.HyperOSForm['b'] = 'F'
OScommon.HyperOSForm['pn'] = OScommon.HyperOSForm['d'].split('_global')[0]
OScommon.HyperOSForm['c'] = '14'
OScommon.HyperOSForm['sdk'] = OScommon.sdk[OScommon.HyperOSForm['c']]
OScommon.HyperOSForm['p'] = device
OScommon.HyperOSForm['options']['zone'] = '1'
OScommon.HyperOSForm['options']['cv'] = os_replace('OS1.0.29.0.UNNCNXM')
OScommon.HyperOSForm['options']['previewPlan'] = '0'
OScommon.HyperOSForm['v'] = os_replace('OS1.0.29.0.UNNCNXM')


encrypted_form = OScommon.miui_encrypt(json.dumps(OScommon.HyperOSForm))
OScommon.getChangelog(encrypted_form, device)
