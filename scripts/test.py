import OScommon

for device in OScommon.order:
  devdata = OScommon.localData(device)
  devcode = OScommon.stringify(devdata['device'])
  for branch in devdata['branches']:
    code = OScommon.stringify(branch['branchCode'])
    type=OScommon.stringify("HyperOS")
    region = OScommon.stringify(branch['region'])
    btag = OScommon.stringify(branch['branchtag'])
    tag = OScommon.stringify(branch['idtag'])
    zone = int(branch['zone'])
    devlength = len(devdata["branches"])
    romlength = len(branch["table"])
    for rom_key in reversed(branch["roms"]):
      android = OScommon.stringify(branch["roms"][rom_key]["android"])
      version = OScommon.stringify(branch["roms"][rom_key]["os"])
      release = OScommon.stringify(branch["roms"][rom_key]["release"])
      recovery = OScommon.stringify(branch["roms"][rom_key]["recovery"])
      fastboot = OScommon.stringify(branch["roms"][rom_key]["fastboot"])
      if "OS1" in version:
        bigver = OScommon.stringify("HyperOS 1")
      elif "OS2" in version:
        bigver = OScommon.stringify("HyperOS 2")
      else:
        bigver = OScommon.stringify("")
      if region == "'cn'":
        ins_sql = f"INSERT INTO roms (device,code,type,bigver,region,branch,tag,zone,version,android,beta_date,recovery,fastboot) VALUES (%s, %s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s, %s)" % (devcode,code,type,bigver,region,btag,tag,zone,version,android,release,recovery,fastboot)
      else:
        ins_sql = f"INSERT INTO roms (device,code,type,bigver,region,branch,tag,zone,version,android,release_date,recovery,fastboot) VALUES (%s, %s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s, %s)" % (devcode,code,type,bigver,region,btag,tag,zone,version,android,release,recovery,fastboot)
      OScommon.db_job(ins_sql)
      if romlength > 5:
        if "ctelecom" in branch['table']:
          ctelecom = OScommon.stringify(branch["roms"][rom_key]['ctelecom'])
          update_sql = f"UPDATE roms SET ctelecom = %s WHERE version = %s and code = %s" % (ctelecom,version,code)
          OScommon.db_job(update_sql)
        if "cnmobile" in branch['table']:
          cmobile = OScommon.stringify(branch["roms"][rom_key]['cnmobile'])
          update_sql = f"UPDATE roms SET cmobile = %s WHERE version = %s and code = %s" % (cmobile,version,code)
          OScommon.db_job(update_sql)
        if "cnunicom" in branch['table']:
          cunicom = OScommon.stringify(branch["roms"][rom_key]['cnunicom'])
          update_sql = f"UPDATE roms SET cunicom = %s WHERE version = %s and code = %s" % (cunicom,version,code)
          OScommon.db_job(update_sql)
        if "origin" in branch['table']:
          others = OScommon.stringify(branch["roms"][rom_key]['origin'])
          update_sql = f"UPDATE roms SET others = %s WHERE version = %s and code = %s" % (others,version,code)
          OScommon.db_job(update_sql)
        else:
          print(device,version)
      else:
        i = 0