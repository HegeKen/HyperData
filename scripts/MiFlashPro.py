import sqlite3
import OScommon


# C:\Users\Hege\AppData\Roaming\Xiaomi\miflash_pro\Config
conn = sqlite3.connect('D:/Projects/HyperOS.fans/Nuxt3MR/public/MRData/scripts/MiFlashPro/download.db3')
c = conn.cursor()
query = """SELECT dl_rom_name from download_storage"""
cursor = c.execute(query)
for row in cursor:
  OScommon.checkExist(row[0])
