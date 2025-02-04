import OScommon
from openpyxl import load_workbook
import pandas as pd

file_path = "roms.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')
data_string = df.to_csv(sep='\t', index=False, header=False)

for device in OScommon.order:
  devdata = OScommon.localData(device)
  devcode = OScommon.stringify(devdata['device'])
  for branch in devdata['branches']:
    for rom_key in reversed(branch["roms"]):
      for tab in branch["table"]:
        entry = branch["roms"][rom_key][tab]
        if entry in data_string:
          i = 0
        else:
          if entry.startswith("202"):
            continue
          else:
            print(device,entry)