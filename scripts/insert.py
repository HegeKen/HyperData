from pymysql import Connection
import database.config as config
import OScommon
import json

def db_get(sql):
  cnx = None
  try:
    cnx = Connection(
      user=config.user,
      password=config.password,
      host=config.host,
      port=config.port,
      database=config.database,
      autocommit=True
      )
    cursor = cnx.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
  except Exception as e:
    print(e)
  finally:
    if cnx:
      cnx.close()
def db_insert(sql,data):
  cnx = None
  try:
    cnx = Connection(
      user=config.user,
      password=config.password,
      host=config.host,
      port=config.port,
      database=config.database,
      autocommit=True
      )
    cursor = cnx.cursor()
    cursor.execute(sql,data)
    return cursor.fetchall()
  except Exception as e:
    print(e)
  finally:
    if cnx:
      cnx.close()

for device in OScommon.currentStable:
  devdata = OScommon.localData(device)
  for cur_branch in devdata['branches']:
    pre = "SELECT code FROM branches WHERE code = '" + cur_branch['branchCode'] + "'"
    if len(db_get(pre)) > 0:
      up = "UPDATE branches SET os=1,active=1 WHERE code = '" + cur_branch['branchCode'] + "'"
      db_get(up)
    else:
      ins_sql = "INSERT INTO branches (codename,code,branch,tag,cnname,enname,cnbranch,enbranch,region,os,ui,mark,carrier,zone,ep,listed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      db_insert(ins_sql,(
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
    
