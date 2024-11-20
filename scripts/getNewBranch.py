import OScommon
from datetime import datetime

for device in OScommon.currentStable:
	devdata = OScommon.localData(device)
	device = devdata['device']
	code = devdata['code']
	andvs = devdata['android']
	oss = devdata['suppports']
	for branch in OScommon.branches:
		for os in oss:
			for andv in andvs:
				devcode = device+branch['code']
				version = os+".7.0."+OScommon.android(andv)+code+branch['tag']
				if version in devdata:
					i = 0
				else:
					print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"正在检测的是",device,devcode,version,end="               ", flush=True)
					OScommon.getFromApi(OScommon.miui_encrypt(OScommon.OTAFormer(device, devcode, branch['region'], 'F', branch['zone'], andv, version)))
					
