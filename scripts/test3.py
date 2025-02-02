import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import pytz
 
def get_time(url):
  try:
    response = requests.head(url, allow_redirects=True)
    if 'Last-Modified' in response.headers:
      last_modified_str = response.headers['Last-Modified']
      date = datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=8)
      return date.strftime("%Y-%m-%d")
    else:
      return ""
  except requests.RequestException as e:
    return f"访问URL失败: {e}"

# 示例URL
url = "https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/OS1.0.12.0.ULCCNXM/cupid_images_OS1.0.12.0.ULCCNXM_20241226.0000.00_14.0_cn_49bacfe6f1.tgz"
print(get_time(url))