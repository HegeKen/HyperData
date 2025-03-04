import OScommon

file = open("public/data/scripts/NewROMs.txt", "r", encoding='utf-8')
lines = file.readlines()
for line in lines:
  line = line.rstrip()
  if line == "":
    continue
  else:
    device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = [item for item in OScommon.getData(line)]
    OScommon.checkDatabase(device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename)