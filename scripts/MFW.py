from selenium import webdriver
from bs4 import BeautifulSoup
import common


urls = []
driver = webdriver.Edge()
driver.get('https://mifirmware.com/hyperos/')
soup = BeautifulSoup(driver.page_source, 'lxml')
lists = soup.find_all('a', attrs={'data-content' :'Download'})
for list in lists:
  link = list.attrs['href']
  if 'mifirmware'in link:
    if link in urls:
      i = 0
    else:
      urls.append(link)
  else:
    if '.zip' in link:
      common.checkExit(link.split('/')[4].strip("?t="))
    elif '.tgz' in link:
      common.checkExit(link.split('/')[4].strip("?t="))
    else:
      common.writeData(link)
for url in urls:
  common.MiFirm(url)
