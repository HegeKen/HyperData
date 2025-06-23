import OScommon
import sys
# sys.path.append("D:\\Projects\\HyperOS.fans\\Nuxt3MR\\public\\MRData\\scripts\\")
sys.path.append("../NuxtMR/public/MRData/scripts/")
import common # type: ignore

for flag in OScommon.flags:
  if flag in common.flags:
    i = 0
  else:
    print("\"" + flag + "\" : \"" + OScommon.flags[flag] + "\",")