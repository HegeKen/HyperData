import requests
import json
import common

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'}
headers = {'Connection': 'close'}
domains = ['https://sgp-api.buy.mi.com/bbs/api/','https://ams-api.buy.mi.com/bbs/api/']
params = '/phone/getlinepackagelist'
regions = ['global','rs','bd','id','my','pk','ph','tr','vn','th','de','es','fr',
           'it','pl','uk','ru','ua','mie','br','co','mx','pe','cl','ng','eg']



def getFastboot(region):
  for domain in domains:
    url = domain+region+params
    print('\r'+url+'              ',end='')
    response = requests.get(url, headers=headers)
    content = response.content.decode('utf8')
    if (response.status_code != 404):
      packages = json.loads(content)['data']
      if packages == None:
        i = 0
      else:
        for package in packages:
          fastboot = package['package_url'].split('/')[4].split('?')[0]
          common.checkExit(fastboot)
    response.close()


for region in regions:
  getFastboot(region)
