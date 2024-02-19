from selenium import webdriver
from bs4 import BeautifulSoup
import OScommon
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


urls = []
driver = webdriver.Edge()
edge_options = Options()
edge_options.add_argument("--remote-allow-origins=*")
driver = webdriver.Edge(options=edge_options)
driver.get('https://mifirmware.com/hyperos/')
soup = BeautifulSoup(driver.page_source, 'lxml')
a_tags = soup.find_all("a")  
download_links = [a for a in a_tags if a.text == "Download"]  
for link in download_links:
  if "#" in link["href"]:
    i = 0
  elif "firmware" in link["href"]:
    if link["href"] in urls:
      i = 0
    else:
      urls.append(link["href"])
  else:
      filename = link["href"].split('/')[4]
      OScommon.checkExist(filename)
for url in urls:
  print(url)
  OScommon.MiFirm2(url)