import OScommon
from datetime import datetime
import os

os.system(f"clear")
increment = ["1","100","200"]
one_devices = ['warm']
base_url = "https://update.intl.miui.com/updates/miota-fullrom.php?d="
devices = list(dict.fromkeys(OScommon.unreleased+ OScommon.currentStable))
for device in devices:
	devdata = OScommon.localData(device)
	device = devdata['device']
	code = devdata['code']
	andvs = devdata['android']
	oss = devdata['suppports']
	for branch in OScommon.branches:
		for os in oss:
			for andv in andvs:
				devcode = device+branch['code']
				# https://update.intl.miui.com/updates/miota-fullrom.php?d=rodinep_cjcc&b=F&r=cn&n=
				for carrier in branch['carrier']:
					if device in one_devices:
						url = base_url+devcode+"&b=F&r=&n="+carrier
					else:
						url = base_url+devcode+"&b=F&r="+branch['region']+"&n="+carrier
					print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),url,end="                   ", flush=True)
					OScommon.getFastboot(url)
				for i in increment:
					if code != "":
						version = os+"."+i+".0."+OScommon.android(andv)+code+branch['tag']
						if version in devdata:
							i = 0
						else:
							print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"正在检测的是",device,devcode,version,end="                                            ", flush=True)
							if device in one_devices:
								OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, devcode, '', 'F', branch['zone'], andv, version)))
							else:
								OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, devcode, branch['region'], 'F', branch['zone'], andv, version)))
					else:
						i = 0