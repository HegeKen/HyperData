import json
from collections import OrderedDict
from datetime import datetime


def load_devices_data():
    """加载 devices.json 数据"""
    with open('public/data/devices.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_brand_display_name(brand_key, brand_data):
    """获取品牌的显示名称（返回包含中英文的对象）"""
    if brand_key == 'mi':
        return {'zh': '小米手机', 'en': 'Xiaomi Phones'}
    elif brand_key == 'redmi':
        return {'zh': 'Redmi 手机', 'en': 'Redmi Phones'}
    elif brand_key == 'poco':
        return {'zh': 'POCO 手机', 'en': 'POCO Phones'}
    return {'zh': brand_data.get('zh', brand_key), 'en': brand_data.get('en', brand_key)}


def group_devices_by_series(devices):
    """按 series 字段分组设备，保持原始顺序（返回包含中英文的对象）"""
    series_dict = OrderedDict()
    for device in devices:
        series_raw = device.get('series', '其他')
        # 处理 series 为对象的情况（新格式）或字符串（旧格式兼容）
        if isinstance(series_raw, dict):
            series_name = {
                'zh': series_raw.get('zh', '其他'),
                'en': series_raw.get('en', 'Other')
            }
        else:
            series_name = {'zh': series_raw, 'en': series_raw}
        
        # 使用中文作为 key 进行分组
        series_key = series_name['zh']
        if series_key not in series_dict:
            series_dict[series_key] = {
                'name': series_name,
                'devices': []
            }
        series_dict[series_key]['devices'].append(device)
    return series_dict


def generate_device_chip(device):
    """生成单个设备的 chip HTML（包含中英文数据属性）"""
    code = device.get('code', '')
    name_zh = device.get('name', {}).get('zh', '')
    name_en = device.get('name', {}).get('en', '')
    
    # 构建显示文本：中文名/英文名(代号)
    display_text_zh = f"{name_zh}({code})"
    display_text_en = f"{name_en}({code})"
    
    return f'<div class="mdui-chip" data-name-zh="{display_text_zh}" data-name-en="{display_text_en}"><a href="devices/{code}.json"><span class="mdui-chip-title HyperBlue lang-text" data-lang-zh="{display_text_zh}" data-lang-en="{display_text_en}"> {display_text_zh} </span></a></div>'


def generate_series_section(series_info, lang='zh'):
    """生成一个 series 分区的 HTML"""
    series_name_zh = series_info['name']['zh']
    series_name_en = series_info['name']['en']
    devices = series_info['devices']
    
    html_parts = []
    
    # Series 标题（避免重复添加"系列"字样）
    # 中文标签
    label_zh = '：' if series_name_zh.endswith('系列') else '系列：'
    # 英文标签（确保有空格）
    if series_name_en.endswith('Series'):
        label_en = ': '
    elif series_name_en and not series_name_en.endswith(' '):
        # 如果名称不以空格结尾，添加空格后再加 "Series: "
        label_en = ' Series: '
    else:
        label_en = 'Series: '
    
    # 添加双语数据属性到系列标题
    full_text_zh = f"{series_name_zh}{label_zh}"
    full_text_en = f"{series_name_en}{label_en}"
    
    html_parts.append(f'<div class="series HyperBlue lang-text" data-lang-zh="{full_text_zh}" data-lang-en="{full_text_en}"> {full_text_zh}</div>')
    
    # 设备列表
    for device in devices:
        html_parts.append(generate_device_chip(device))
    
    return '\n                '.join(html_parts)


def generate_brand_section(brand_key, brand_data):
    """生成一个品牌分区的 HTML（包含双语数据）"""
    display_names = get_brand_display_name(brand_key, brand_data)
    devices = brand_data.get('devices', [])
    
    # 按 series 分组
    series_groups = group_devices_by_series(devices)
    
    # 生成 HTML
    html_parts = []
    html_parts.append(f'''        <div id="{brand_key.upper()}" class="mdui-container-fluid">
          <div mdui-panel class="mdui-panel mdui-panel-gapless mdui-shadow-0">
            <div class="mdui-panel-item mdui-panel-item-open">
              <div class="mdui-panel-item-header">
                <div class="mdui-panel-item-title HyperBlue lang-text" data-lang-zh="{display_names['zh']}" data-lang-en="{display_names['en']}"> {display_names['zh']}</div> <i class="mdui-panel-item-arrow mdui-icon material-icons">keyboard_arrow_down</i>
              </div>
              <div class="mdui-panel-item-body">''')
    
    # 添加各个 series 分区
    for series_name, series_info in series_groups.items():
        html_parts.append('                ' + generate_series_section(series_info, lang='zh'))
    
    html_parts.append('''              </div>
            </div>
          </div>
        </div>''')
    
    return '\n'.join(html_parts)


def generate_html(data):
    """生成完整的 HTML 文件（包含中英文切换功能）"""
    
    # 获取当前年份
    current_year = datetime.now().year
    
    # HTML 头部模板 - 包含语言切换 JavaScript
    html_header = f'''<!doctype html>
<html data-n-head-ssr lang="zh">

<head>
  <title>HyperOS ROMS 数据</title>
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
  <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "2c63818efa744adc8db506104596506e"}}'></script>
  <script>
    // 语言切换功能
    function switchLanguage(lang) {{
      // 保存语言偏好到 localStorage
      localStorage.setItem('preferred-language', lang);
      
      // 更新 HTML lang 属性
      document.documentElement.lang = lang;
      
      // 更新所有带有 lang-text 类的元素
      const elements = document.querySelectorAll('.lang-text');
      elements.forEach(el => {{
        const text = el.getAttribute('data-lang-' + lang);
        if (text) {{
          el.textContent = ' ' + text + ' ';
        }}
      }});
      
      // 更新设备芯片中的文本
      const chips = document.querySelectorAll('.mdui-chip');
      chips.forEach(chip => {{
        const span = chip.querySelector('.lang-text');
        if (span) {{
          const text = span.getAttribute('data-lang-' + lang);
          if (text) {{
            span.textContent = ' ' + text + ' ';
          }}
        }}
      }});
      
      // 更新页面标题
      const title = lang === 'zh' ? 'HyperOS ROMS 数据' : 'HyperOS ROMS Data';
      document.title = title;
      document.querySelector('.mdui-typo-title').textContent = title;
      
      // 更新语言切换按钮文本
      const langBtn = document.getElementById('lang-switch-btn');
      if (langBtn) {{
        langBtn.innerHTML = '<i class="mdui-icon material-icons">language</i> ' + (lang === 'zh' ? 'English' : '中文');
      }}
      
      // 更新底部链接文本
      updateFooterLinks(lang);
      
      // 更新免责声明 - 动态获取当前年份
      updateDisclaimer(lang);
    }}
    
    function updateFooterLinks(lang) {{
      const links = {{
        'weibo': lang === 'zh' ? '微博' : 'Weibo',
        'community': lang === 'zh' ? '小米社区' : 'Mi Community',
        'bilibili': lang === 'zh' ? '哔哩哔哩' : 'Bilibili',
        'backtotop': lang === 'zh' ? '返回顶部' : 'Back to Top'
      }};
      
      document.querySelectorAll('.mdui-bottom-nav a label').forEach(label => {{
        const parent = label.parentElement;
        if (parent.href.includes('weibo')) label.textContent = links.weibo;
        else if (parent.href.includes('miui.com')) label.textContent = links.community;
        else if (parent.href.includes('bilibili')) label.textContent = links.bilibili;
        else if (parent.href.includes('#top')) label.textContent = links.backtotop;
      }});
    }}
    
    function updateDisclaimer(lang) {{
      // 获取当前年份
      const currentYear = new Date().getFullYear();
      const disclaimer = lang === 'zh' 
        ? '2023 - ' + currentYear + ' -- 非小米集团旗下网站 . 我们与小米以及Hyper<span class="HyperBlue"> OS</span>开发团队没有任何联系'
        : '2023 - ' + currentYear + ' -- This is NOT an official website of Xiaomi Group. We have no affiliation with Xiaomi or the HyperOS development team.';
      
      const fsElement = document.querySelector('.mdui-bottom-nav.fs .mdui-text-center');
      if (fsElement) {{
        fsElement.innerHTML = disclaimer;
      }}
    }}
    
    // 页面加载时应用保存的语言偏好
    document.addEventListener('DOMContentLoaded', function() {{
      const savedLang = localStorage.getItem('preferred-language') || 'zh';
      if (savedLang !== 'zh') {{
        switchLanguage(savedLang);
      }}
    }});
  </script>
</head>

<body>
  <div>
    <div>
      <div>
        <div>
          <div class="mdui-appbar mdui-appbar-fixed mdui-color-blue-accent mdui-text-color-white">
            <div class="mdui-toolbar">
              <span class="mdui-typo-title">HyperOS ROMS 数据</span>
              <div class="mdui-toolbar-spacer"></div>
              <a href="javascript:void(0)" id="lang-switch-btn" class="mdui-btn mdui-ripple mdui-text-color-white" onclick="switchLanguage(document.documentElement.lang === 'zh' ? 'en' : 'zh')">
                <i class="mdui-icon material-icons">language</i>
                English
              </a>
            </div>
          </div>
          <br />
          <br />
          <br />
        </div> <br>
        <!-- 此处开始自动化替换 -->'''
    
    # HTML 尾部模板
    html_footer = f'''        <!-- 此处结束自动化替换 -->
        <div><br> <br> <br>
          <div class="mdui-bottom-nav footer mdui-color-grey-100">
            <a href="https://github.com/HegeKen" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-GitHub fic"></i><label>GitHub</label></a> 
            <a href="https://gitlab.com/HegeKen" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-gitlab fic"></i><label>GitLab</label></a> 
            <a href="https://weibo.com/Heliljan" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-weibo fic"></i><label>微博</label></a> 
            <a href="https://web.vip.miui.com/page/info/mio/mio/homePage?uid=311975809" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-MiBBS fic"></i><label>小米社区</label></a> 
            <a href="https://space.bilibili.com/19940729" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon icon-bilibili fic"></i><label>哔哩哔哩</label></a> 
            <a href="#top" class="mdui-ripple mdui-bottom-nav-active"><i class="mdui-icon material-icons">arrow_upward</i><label>返回顶部</label></a>
          </div>
          <div class="mdui-bottom-nav footer mdui-color-grey-100 fs">
            <div class="mdui-center mdui-text-center">2023 - {current_year} -- 非小米集团旗下网站 . 我们与小米以及Hyper<span class="HyperBlue"> OS</span>开发团队没有任何联系</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
<style>
  .mdui-color-white-accent {{
    background-color: #155ffe !important;
  }}

  .HyperBlue {{
    color: #155ffe !important;
  }}
</style>

</html>'''
    
    # 生成品牌分区
    brand_sections = []
    for brand_key in ['mi', 'redmi', 'poco']:
        if brand_key in data:
            brand_sections.append(generate_brand_section(brand_key, data[brand_key]))
    
    # 组合完整 HTML
    html_content = html_header + '\n' + '\n'.join(brand_sections) + '\n' + html_footer
    
    return html_content


def main():
    """主函数"""
    print("正在加载 devices.json...")
    data = load_devices_data()
    
    # 生成包含中英文切换功能的单页面
    print("正在生成 index.html (支持中英文切换)...")
    html_content = generate_html(data)
    output_path = 'public/data/index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ 成功生成 {output_path}")
    
    # 统计信息
    print("\n统计信息:")
    for brand_key in ['mi', 'redmi', 'poco']:
        if brand_key in data:
            brand_data = data[brand_key]
            devices = brand_data.get('devices', [])
            # 处理 series 为对象的情况
            series_set = set()
            for d in devices:
                series_raw = d.get('series', '其他')
                if isinstance(series_raw, dict):
                    series_set.add(series_raw.get('zh', '其他'))
                else:
                    series_set.add(series_raw)
            print(f"  {brand_key}: {len(devices)} 个设备, {len(series_set)} 个系列")
    
    print("\n完成！页面已支持中英文切换功能。")


if __name__ == '__main__':
    main()