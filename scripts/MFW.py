from selenium import webdriver
import OScommon
from selenium.webdriver.common.by import By
import os


urls = []
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
driver.get('https://mifirmware.com/hyperos/')
elements = driver.find_elements(By.TAG_NAME,"a")
for element in elements:
  link = element.get_attribute("href")
  if link is None:
    i = 0
  elif "-firmware" in link:
    urls.append(link)
  elif ".zip" in link or ".tgz" in link:
    OScommon.checkExist(link.split('/')[4])
  else:
    i = 0
driver.quit()

os.system('cls')
for url in urls:
  print('\r'+url + '              ',end='')
  OScommon.MiFirm2(url)