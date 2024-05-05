import OScommon

def check_os_in_recovery_and_fastboot(data,device):
  for branch in data['branches']:
    if data['device'] in branch['branchCode']:
      roms = branch['roms']
      for os_version, rom_info in roms.items():
        if 'recovery' in rom_info and rom_info['recovery']:
          if os_version not in rom_info['recovery']:
            print(f"错误: OS {os_version} not found in recovery for branch {branch['name']['zh']} in device " + device)
          if rom_info['android'] not in rom_info['recovery']:
            print(f"错误: OS {rom_info['android']} not found in recovery for branch {branch['name']['zh']} in device " + device)
        if 'fastboot' in rom_info and rom_info['fastboot']:
          if branch['branchCode'] != rom_info['fastboot'].split('_images')[0]:
            print(f"错误: 机器线刷包包含的 {rom_info['fastboot'].split('_images')[0]} 与版本分支代码 {branch['branchCode']} 不一致")
          if os_version not in rom_info['fastboot']:
            print(f"错误: OS {os_version} not found in fastboot for branch {branch['name']['zh']} in device " + device)
          if rom_info['android'] not in rom_info['fastboot']:
            print(f"错误: OS {rom_info['android']} not found in fastboot for branch {branch['name']['zh']} in device " + device)
    else:
      print(f"错误: 机器 {data['device']} 与版本分支代码 {branch['branchCode']} 不一致")

if __name__ == "__main__":
  for device in OScommon.currentStable:
    check_os_in_recovery_and_fastboot(OScommon.localData(device),device)