import common

for device in common.currentStable:
  devdata = common.localData(device)
  for i in range(0,len(devdata['branches'])):
    j = i -1
    for rom in devdata['branches'][j]["roms"]:
      current = devdata['branches'][j]["roms"][rom]
      if current['recovery'] == '':
        i = 0
      else:
        flag = current['recovery'].split('_')[1]
        if flag in common.flags:
          i = 0
        else:
          common.writeFlag(flag,device)
      if current['fastboot'] == '':
        i = 0
      else:
        flag = current['fastboot'].split('_images')[0]
        if flag in common.flags:
            i = 0
        else:
          common.writeFlag(flag,device)

