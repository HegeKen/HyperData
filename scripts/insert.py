import OScommon

for device in OScommon.currentStable:
  devdata = OScommon.localData(device)
  for cur_branch in devdata['branches']:
    pre = "SELECT code FROM branches WHERE code = '" + cur_branch['branchCode'] + "'"
    if len(OScommon.db_job(pre)) > 0:
      up = "UPDATE branches SET os=1,active=1 WHERE code = '" + cur_branch['branchCode'] + "'"
      OScommon.db_job(up)
    else: 
      ins_sql = "INSERT INTO branches (codename,code,branch,tag,cnname,enname,cnbranch,enbranch,region,os,ui,mark,carrier,zone,ep,listed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      OScommon.db_job(ins_sql,(
        devdata['device'],
        cur_branch['branchCode'],
        cur_branch['branchtag'],
        cur_branch['idtag'],
        devdata['name']['zh'],
        devdata['name']['en'],
        cur_branch['name']['zh'],
        cur_branch['name']['en'],
        cur_branch['region'],
        1,
        0,
        '',
        str(cur_branch['carrier']),
        cur_branch['zone'],
        cur_branch['ep'],
        1
        ))