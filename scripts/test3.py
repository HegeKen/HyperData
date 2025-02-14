import OScommon

roms = ["miui_VENUS_OS1.0.12.0.UKBCNXM_77aa77ab20_14.0.zip"]

for rom in roms:
  OScommon.checkDatabase(rom)