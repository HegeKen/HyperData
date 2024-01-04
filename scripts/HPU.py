from selenium import webdriver
from bs4 import BeautifulSoup
import common


urls = []
driver = webdriver.Edge()
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
      common.checkExist(filename)
for url in urls:
  common.MiFirm(url)