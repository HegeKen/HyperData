import OScommon

file = open("public/data/scripts/NewROMs.txt", "r", encoding='utf-8')
lines = file.readlines()
for line in lines:
  line = line.rstrip()
  if line == "":
    continue
  else:
    if line.startswith("http"):
      line = line.split("/")[4].split("?")[0]
    else:
      i = 0
    device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = [item for item in OScommon.getData(line)]
    OScommon.checkDatabase(device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename)