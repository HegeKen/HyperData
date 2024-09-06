import OScommon

def check_os_in_recovery_and_fastboot(data,device):
  for branch in data['branches']:
    if data['device'] in branch['branchCode']:
      roms = branch['roms']
      bname = branch['name']['zh']
      for os_version, rom_info in roms.items():
        if rom_info['android'] == "" and rom_info['os'] == "" and rom_info['release'] == "" and rom_info['recovery'] == "" and rom_info['fastboot'] == "":
          i = 0
        else:
          if rom_info['android'] == "":
            print(f"错误:机型 {device} {bname} {os_version} 安卓版本未标注")
          if rom_info['os'] == "":
            print(f"错误:机型 {device} {bname} {os_version} OS版本未标注")
          if rom_info['release'] == "":
            print(f"错误:机型 {device} {bname} {os_version} 发布时间未标注")
          if rom_info['recovery'] != "":
            if rom_info['android'] not in rom_info['recovery']:
              print(f"错误:机型 {device} {bname} {os_version} 卡刷包与当前记录的安卓版本不一致")
            if rom_info['os'] not in rom_info['recovery']:
              print(f"错误:机型 {device} {bname} {os_version} 卡刷包与当前记录的OS版本不一致")
          if rom_info['fastboot'] != "":
            if rom_info['android'] not in rom_info['fastboot']:
              print(f"错误:机型 {device} {bname} {os_version} 线刷包与当前记录的安卓版本不一致")
            if rom_info['os'] not in rom_info['fastboot']:
              print(f"错误:机型 {device} {bname} {os_version} 线刷包与当前记录的OS版本不一致")
            if branch['branchCode'] not in rom_info['fastboot']:
              print(f"错误:机型 {device} {bname} {os_version} 线刷包与当前记录的版本分支代码不一致")

if __name__ == "__main__":
  for device in OScommon.currentStable:
    check_os_in_recovery_and_fastboot(OScommon.localData(device),device)