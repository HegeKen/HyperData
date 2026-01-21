import os
import json
import OScommon
from datetime import datetime

DEVICES_DIR = os.path.join(os.path.dirname(__file__), '../devices')
DEVICES_DIR = os.path.abspath(DEVICES_DIR)
devices = [f for f in os.listdir(DEVICES_DIR) if f.endswith('.json')]


with open("public/data/index.html", "r", encoding='utf-8') as file:
  file_content = file.read()
devlist = json.loads(open("public/data/devices.json", 'r', encoding='utf-8').read())
for device in devices:
  device = device.replace('.json', '')
  if device in OScommon.unreleased:
    continue
  else:
    if device in str(devlist):
      continue
    else:
      print(device)
    if device in OScommon.order:
      if device in file_content:
        continue
      else:
        device_page = f"""<div class="mdui-chip"><a href="devices/{device}.json"><span class="mdui-chip-title HyperBlue"> {OScommon.localData(device)['name']['zh']}({device}) </span></a></div>"""
        print(device_page)
      continue
    else:
      device_page = f"""<div class="mdui-chip"><a href="devices/{device}.json"><span class="mdui-chip-title HyperBlue"> {OScommon.localData(device)['name']['zh']}({device}) </span></a></div>"""
      print(device_page)



header_html = """
<!doctype html>
<html data-n-head-ssr lang="zh-CN">
<head>
  <title>HyperOS ROMS Data</title>
  <meta charset="utf-8">
  <meta name="author" content="HegeKen">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta data-hid="description" name="description" content="">
  <meta name="format-detection" content="telephone">
  <link rel="icon" type="image/x-icon" href="https://www.hyperos.fans/favicon.ico">
  <link rel="stylesheet" href="https://data.miuier.com/assets/mdui/css/mdui.min.css">
  <link rel="stylesheet" href="https://cdn-font.hyperos.mi.com/font/css?family=MiSans_VF:VF:Chinese_Simplify,Latin&display=swap">
  <link rel="stylesheet" href="https://data.miuier.com/assets/miuiroms.css">
  <link rel="stylesheet" href="https://at.alicdn.com/t/c/font_2478867_iq2uuq05ql.css">
  <script src="https://data.miuier.com/assets/mdui/js/mdui.min.js"></script>
  <script src="https://data.miuier.com/assets/jquery/jquery.min.js"></script>
  <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "2c63818efa744adc8db506104596506e"}'></script>
</head>
<body>
  <div>
    <div>
      <div>
        <div>
          <div class="mdui-appbar mdui-appbar-fixed mdui-color-blue-accent mdui-text-color-white">
            <div class="mdui-toolbar"><span class="mdui-typo-title">HyperOS ROMS Data</span>
            </div>
          </div>
          <br />
          <br />
          <br />
        </div> <br>"""
footer_html = f"""
        <div><br> <br> <br>
          <div class="mdui-bottom-nav footer mdui-color-grey-100"><a href="https://github.com/HegeKen" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-GitHub fic"></i><label>GitHub</label></a> <a href="https://gitlab.com/HegeKen" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-gitlab fic"></i><label>GitLab</label></a> <a href="https://weibo.com/Heliljan" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-weibo fic"></i><label>微博</label></a> <a href="https://web.vip.miui.com/page/info/mio/mio/homePage?uid=311975809" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-MiBBS fic"></i><label>小米社区</label></a> <a href="https://space.bilibili.com/19940729" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-bilibili fic"></i><label>哔哩哔哩</label></a> <a href="#top" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon material-icons">arrow_upward</i><label>返回顶部</label></a></div>
          <div class="mdui-bottom-nav footer mdui-color-grey-100 fs">
            <div class="mdui-center mdui-text-center">2023 - {datetime.now().year} -- 非小米集团旗下网站 . 我们与小米以及Hyper<span class="HyperBlue">OS</span>开发团队没有任何联系</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
<style>
  .mdui-color-white-accent {{background-color: #155ffe !important;}}
  .HyperBlue {{color: #155ffe !important;}}
</style>
</html>
"""