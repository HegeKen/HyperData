import OScommon

for device in OScommon.currentStable:
  devdata = OScommon.localData(device)
  for i in range(0,len(devdata['branches'])):
    j = i -1
    if devdata['branches'][j]['branchCode'] == '':
      print("请修补机型： "+device+"文件中未指定的区域代码\n")
    elif devdata['branches'][j]['branchCode'] in OScommon.flags:
      i = 0
    else:
      OScommon.writeFlag(devdata['branches'][j]['branchCode'],device)
    for rom in devdata['branches'][j]["roms"]:
      current = devdata['branches'][j]["roms"][rom]
      if current['recovery'] == '':
        i = 0
      else:
        if devdata['branches'][j]['branchCode'] == current['recovery'].split('-')[0]:
          flag = devdata['branches'][j]['branchCode']
        else:
          flag = current['recovery'].split('_')[1]
        if flag in OScommon.flags:
          i = 0
        else:
          OScommon.writeFlag(flag,device)
      if current['fastboot'] == '':
        i = 0
      else:
        flag = current['fastboot'].split('_images')[0]
        if flag in OScommon.flags:
            i = 0
        else:
          OScommon.writeFlag(flag,device)

