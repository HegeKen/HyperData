import OScommon
from datetime import datetime

def check_os_in_recovery_and_fastboot(data,device):
  for branch in data['branches']:
    roms = branch['roms']
    for os_version, rom_info in roms.items():
      if 'recovery' in rom_info and rom_info['recovery']:
        if os_version not in rom_info['recovery']:
          print(f"错误: OS {os_version} not found in recovery for branch {branch['name']['zh']} in device " + device)
        if rom_info['android'] not in rom_info['recovery']:
          print(f"错误: OS {rom_info['android']} not found in recovery for branch {branch['name']['zh']} in device " + device)
      if 'fastboot' in rom_info and rom_info['fastboot']:
        if os_version not in rom_info['fastboot']:
          print(f"错误: OS {os_version} not found in fastboot for branch {branch['name']['zh']} in device " + device)
        if rom_info['android'] not in rom_info['fastboot']:
          print(f"错误: OS {rom_info['android']} not found in fastboot for branch {branch['name']['zh']} in device " + device)

if __name__ == "__main__":
  for device in OScommon.currentStable:
    check_os_in_recovery_and_fastboot(OScommon.localData(device),device)