import OScommon
import sys
sys.path.append("D:\\Projects\\HyperOS.fans\\public\\MRData\\data\\scripts\\")
import common


for flag in OScommon.flags:
  if flag in common.flags:
    i = 0
  else:
    print("\"" + flag + "\" : \"" + OScommon.flags[flag] + "\",")