import requests
import OScommon
from bs4 import BeautifulSoup
import re

def MiFirm2(url):
  response = requests.post(url)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    if content == "":
        i = 0
    else:
      soup = BeautifulSoup(content, 'lxml')
      table_tags = soup.find_all("table", class_="firm_data")
      for tag in table_tags:
        tdtags = BeautifulSoup(str(tag), 'lxml')
        tds = tdtags.find_all("td")
        for td in tds:
          if ".tgz" in td.text or ".zip" in td.text:
            print(td.text)

url = "https://mifirmware.com/redmi-k70e/"

MiFirm2(url)