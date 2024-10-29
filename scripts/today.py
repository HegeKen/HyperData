import OScommon
from datetime import datetime

btags = ['Beta','ADPC','ADPG','CnODB','CnOO','CnOT','CnOM','CnOU','CnOD','EPSTD','EPCJCC','CNTP','GBEB', 'GBOO', 'EEAB', 'EEAO','RUSO','INSO',
         'IDSO','TRSO','THAS','SKSO','JAPS','EUHG','EUOR','EUVF','EUBY','EUTF','EUTI','EUSF','ZAVC','ZAMT','GTTG','CLEN','MXAT']

Beta = []
ADPC = []
ADPG = []
CnODB = []
CnOO = []
Dev = []
CnOT = []
CnOM = []
CnOU = []
CnOD = []
EPSTD = []
EPCJCC = []
CNTP = []
GBEB = []
GBOO = []
GBDC = []
EEAB = []
EEAO = []
RUSO = []
INSO = []
IDSO = []
TRSO = []
THAS = []
SKSO = []
JAPS = []
EUHG = []
EUOR = []
EUVF = []
EUBY = []
EUTF = []
EUTI = []
EUSF = []
ZAVC = []
ZAMT = []
GTTG = []
CLEN = []
MXAT = []
MXTC = []
LMCR = []
LMMS = []

for device in OScommon.order:
  devdata = OScommon.localData(device)
  for num in range(len(devdata['branches'])):
    tag = devdata['branches'][num]['idtag']
    for rom in devdata['branches'][num]['roms']:
      if devdata['branches'][num]['roms'][rom]['release'] == datetime.now().strftime("%Y-%m-%d"):
      # if devdata['branches'][num]['roms'][rom]['release'] == "2024-08-18":
        if tag in btags:
          if tag == "Beta":
            Beta.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "ADPC":
            ADPC.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "ADPG":
            ADPG.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnODB":
            CnODB.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnOO":
            CnOO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnOT":
            CnOT.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnOM":
            CnOM.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnOU":
            CnOU.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "Dev":
            Dev.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CnOD":
            CnOD.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EPSTD":
            EPSTD.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EPCJCC":
            EPCJCC.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CNTP":
            CNTP.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "GBEB":
            GBEB.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "GBOO":
            GBOO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "GBDC":
            GBDC.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EEAB":
            EEAB.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EEAO":
            EEAO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "RUSO":
            RUSO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "INSO":
            INSO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "IDSO":
            IDSO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "TRSO":
            TRSO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "THAS":
            THAS.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "SKSO":
            SKSO.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "JAPS":
            JAPS.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUHG":
            EUHG.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUOR":
            EUOR.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUVF":
            EUVF.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUBY":
            EUBY.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUTF":
            EUTF.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUTI":
            EUTI.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "EUSF":
            EUSF.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "ZAVC":
            ZAVC.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "ZAMT":
            ZAMT.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "GTTG":
            GTTG.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "CLEN":
            CLEN.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "MXAT":
            MXAT.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "MXTC":
            MXTC.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "LMCR":
            LMCR.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          elif tag == "LMMS":
            LMMS.append(devdata['branches'][num]['device']['zh']+"("+devdata['device']+")："+devdata['branches'][num]['roms'][rom]['os'])
          else:
            print("Error: "+tag)

file = open("public/data/scripts/todays.txt", "a", encoding='utf-8')
file.write("OS每日公告速递("+datetime.now().strftime("%Y.%m.%d")+")")

if len(Beta) != 0:
  file.write("\n中国大陆体验增强版 Beta\n")
  for i in Beta:
    file.write(i.replace(":","：")+"\n")
if len(CnODB) != 0:
  file.write("\n中国大陆正式版每日构建版本\n")
  for i in CnODB:
    file.write(i.replace(":","：")+"\n")
if len(CnOO) != 0:
  file.write("\n中国大陆正式版(含内测)\n")
  for i in CnOO:
    file.write(i.replace(":","：")+"\n")
if len(CNTP) != 0:
  file.write("\n中国台湾地区正式版\n")
  for i in CNTP:
    file.write(i.replace(":","：")+"\n")
if len(GBEB) != 0:
  file.write("\n国际体验增强版 Beta\n")
  for i in GBEB:
    file.write(i.replace(":","：")+"\n")
if len(GBOO) != 0:
  file.write("\n国际正式版\n")
  for i in GBOO:
    file.write(i.replace(":","：")+"\n")
if len(GBDC) != 0:
  file.write("\n国际 DC 正式版\n")
  for i in GBDC:
    file.write(i.replace(":","：")+"\n")
if len(EEAB) != 0:
  file.write("\n欧洲EEA体验增强版 Beta\n")
  for i in EEAB:
    file.write(i.replace(":","：")+"\n")
if len(EEAO) != 0:
  file.write("\n欧洲EEA正式版\n")
  for i in EEAO:
    file.write(i.replace(":","：")+"\n")
if len(EUHG) != 0:
  file.write("\n欧洲ThreeHK运营商定制版\n")
  for i in EUHG:
    file.write(i.replace(":","：")+"\n")
if len(EUOR) != 0:
  file.write("\n欧洲Orange运营商定制版\n")
  for i in EUOR:
    file.write(i.replace(":","：")+"\n")
if len(EUVF) != 0:
  file.write("\n欧洲Vodafone运营商定制版\n")
  for i in EUVF:
    file.write(i.replace(":","：")+"\n")
if len(EUBY) != 0:
  file.write("\n欧洲Bouygues Telecom 运营商定制版\n")
  for i in EUBY:
    file.write(i.replace(":","：")+"\n")
if len(EUTF) != 0:
  file.write("\n欧洲Telefonica运营商定制版\n")
  for i in EUTF:
    file.write(i.replace(":","：")+"\n")
if len(EUTI) != 0:
  file.write("\n欧洲TIM运营商定制版\n")
  for i in EUTI:
    file.write(i.replace(":","：")+"\n")
if len(EUSF) != 0:
  file.write("\n欧洲Altice(SFR)运营商定制版\n")
  for i in EUSF:
    file.write(i.replace(":","：")+"\n")
if len(RUSO) != 0:
  file.write("\n俄罗斯正式版\n")
  for i in RUSO:
    file.write(i.replace(":","：")+"\n")
if len(INSO) != 0:
  file.write("\n印度正式版\n")
  for i in INSO:
    file.write(i.replace(":","：")+"\n")
if len(IDSO) != 0:
  file.write("\n印度尼西亚正式版\n")
  for i in IDSO:
    file.write(i.replace(":","：")+"\n")
if len(TRSO) != 0:
  file.write("\n土耳其正式版\n")
  for i in TRSO:
    file.write(i.replace(":","：")+"\n")
if len(THAS) != 0:
  file.write("\n泰国AIS运营商定制版\n")
  for i in THAS:
    file.write(i.replace(":","：")+"\n")
if len(SKSO) != 0:
  file.write("\n韩国正式版\n")
  for i in SKSO:
    file.write(i.replace(":","：")+"\n")
if len(JAPS) != 0:
  file.write("\n日本正式版\n")
  for i in JAPS:
    file.write(i.replace(":","：")+"\n")
if len(ZAVC) != 0:
  file.write("\n南非Vodacom运营商定制版\n")
  for i in ZAVC:
    file.write(i.replace(":","：")+"\n")
if len(ZAMT) != 0:
  file.write("\n南非MTN运营商定制版\n")
  for i in ZAMT:
    file.write(i.replace(":","：")+"\n")
if len(GTTG) != 0:
  file.write("\n危地马拉Tigo运营商定制版\n")
  for i in GTTG:
    file.write(i.replace(":","：")+"\n")
if len(CLEN) != 0:
  file.write("\n智利Entel运营商定制版\n")
  for i in CLEN:
    file.write(i.replace(":","：")+"\n")
if len(MXAT) != 0:
  file.write("\n墨西哥AT&T运营商定制版\n")
  for i in MXAT:
    file.write(i.replace(":","：")+"\n")
if len(MXTC) != 0:
  file.write("\n墨西哥Telcel运营商定制版\n")
  for i in MXTC:
    file.write(i.replace(":","：")+"\n")
if len(LMCR) != 0:
  file.write("\n拉丁美洲Claro运营商定制版\n")
  for i in LMCR:
    file.write(i.replace(":","：")+"\n")
if len(LMMS) != 0:
  file.write("\n拉丁美洲Movistar运营商定制版\n")
  for i in LMMS:
    file.write(i.replace(":","：")+"\n")
file.close()