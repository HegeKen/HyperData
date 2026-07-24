---
name: 小米设备📱ROM版本查询
description: 查询小米/Redmi/POCO设备的HyperOS和MIUI ROM版本信息，支持设备搜索、版本筛选、固件下载链接获取
tags: [小米, ROM, HyperOS, MIUI, 固件, 刷机, 设备查询, 版本查询, 系统更新]
version: 1.1.0
skill_id: xiaomi_rom_query
update_time: 1781689767
add_time: 1781689767
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: 📱
    requires:
      env: []
      bins: []
    homepage: https://data.hyperos.fans
---
# 小米📱ROM版本查询 
## 概述 
一站式查询小米、Redmi、POCO设备的HyperOS与MIUI ROM版本信息。融合双数据源（HyperOS数据源和MIUI数据源），支持设备搜索、版本筛选、固件下载链接获取等功能。 
## 应用场景 
- 用户询问"查询小米ROM版本" / "查看HyperOS固件" / "MIUI刷机包下载"  
- 用户需要查询特定设备的系统版本信息  
- 用户需要获取Recovery/线刷固件下载链接  
- 用户需要了解设备支持的Android版本  
- 用户需要对比不同分支（开发版/稳定版）的ROM版本  
- 用户需要查询国际版、欧洲版、印度版等多地区ROM  
## 核心能力 
- **多源数据融合**：同时查询HyperOS和MIUI数据源，自动合并马甲机信息  
- **智能搜索**：支持设备名称、代号模糊搜索，支持品牌/数据源筛选  
- **版本详情**：显示支持的HyperOS/MIUI版本、Android版本、发布日期、安全补丁日期  
- **固件下载**：提供Recovery（卡刷）和Fastboot（线刷）下载链接  
- **多地区分支**：支持中国版、国际版、欧洲版、台湾版、印度版、俄罗斯版、印度尼西亚版、土耳其版  
- **多版本类型**：支持Beta版、正式版、开发版、体验增强版、Android开发者预览版  
- **运营商定制版**：支持中国电信、中国移动、中国联通定制版ROM  
- **智能链接拼接**：自动根据ROM类型拼接正确的下载链接，支持多镜像源  
## 数据源说明
| 数据源 | 设备数量 | 版本范围 | Android版本 | 设备类型 |
|--------|----------|----------|-------------|----------|
| HyperOS | 130+ | OS1.0-OS3.0 | 13.0-16.0 | 手机/平板 |
| MIUI | 200+ | V1-V14.0 | 2.3.5-14.0 | 手机/平板 |

## HyperOS设备详情 API 数据结构说明

> **数据源**：`GET https://data.hyperos.fans/devices/{code}.json`
> 
> 以下为 HyperOS 设备详情 API 的完整响应结构说明。

### 顶层设备字段

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `device` | string | 设备代号（唯一标识） | `"houji"` |
| `name.zh` | string | 中文名称 | `"小米 14"` |
| `name.en` | string | 英文名称 | `"Xiaomi 14"` |
| `code` | string | 设备区域代码 | `"NC"` |
| `suppports` | string[] | 支持的 HyperOS 版本数组 | `["OS1.0", "OS2.0", "OS3.0"]` |
| `android` | string[] | 支持的 Android 版本数组 | `["14.0", "15.0", "16.0"]` |
| `type` | string | 设备类型 | `"phone"` / `"tablet"` |
| `miui` | string | 是否有 MIUI 数据源 | `"yes"` / `"no"` |
| `merged` | string | 是否为马甲机合并数据 | `"yes"` / `"no"` |
| `branches` | array | ROM 分支数组，详见下方 | 见分支字段 |

### branches[] 分支字段

每个分支对象包含以下字段：

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `name.zh` | string | 分支中文名称 | `"小米澎湃 OS 正式版"` |
| `name.en` | string | 分支英文名称 | `"Xiaomi HyperOS Stable"` |
| `branchCode` | string | 分支代码（通常与device相同） | `"houji"` |
| `brand` | string | 品牌 | `"Xiaomi"` / `"REDMI"` / `"POCO"` |
| `device.zh` | string | 分支对应的中文设备名 | `"小米 14"` |
| `device.en` | string | 分支对应的英文设备名 | `"Xiaomi 14"` |
| `idtag` | string | 分支唯一标识符 | `"CnOO"` / `"GBOO"` / `"Dev"` |
| `tag` | string | 版本区域标签 | `"CNXM"` / `"MIXM"` |
| `url` | string | 相关链接（可选，开发者预览版等） | `"https://..."` |
| `branchtag` | string | 分支类型标识 | `"F"`=正式版, `"X"`=测试/开发版 |
| `table` | string[] | roms 对象中包含的字段列表 | `["os","android","release","aspatch","recovery","fastboot"]` |
| `show` | string | 是否对外展示 | `"1"`=展示, `"0"`=隐藏 |
| `carrier` | string[] | 支持的运营商列表 | `["", "chinatelecom", "chinamobile", "chinaunicom"]` |
| `region` | string | 地区代码 | `"cn"` / `"global"` / `"eea"` / `"tw"` / `"in"` / `"ru"` / `"id"` / `"tr"` |
| `zone` | string | 区域分组 | `"1"`=中国大陆时区, `"2"`=国际时区 |
| `ep` | string | 是否政企版 | `"1"`=政企版, `"0"`=普通版 |
| `roms` | object | ROM 版本集合（key为版本号） | 详见 ROM 字段 |

### branches[].roms{} ROM 版本字段

每个 ROM 版本对象以版本号为 key，包含以下字段：

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `os` | string | HyperOS 版本号 | `"OS3.0.303.0.WNCCNXM"` |
| `android` | string | Android 版本 | `"16.0"` |
| `release` | string | 发布日期 (YYYY-MM-DD) | `"2026-06-10"` |
| `aspatch` | string | 安全补丁日期 (YYYY-MM-DD) | `"2026-05-01"` |
| `recovery` | string | Recovery 卡刷包文件名 | `"houji-ota_full-OS3.0.303.0.WNCCNXM-user-16.0-c5d245a441.zip"` |
| `fastboot` | string | Fastboot 线刷包文件名 | `"houji_images_OS3.0.303.0.WNCCNXM_20260529.0000.00_16.0_cn_05084cd0ea.tgz"` |
| `ctelecom` | string | 中国电信定制线刷包文件名（可选） | `"houji_images_OS3.0.303.0.WNCCNXM_20260529.0000.00_16.0_cn_chinatelecom_...tgz"` |
| `chinamobile` | string | 中国移动定制线刷包文件名（可选） | 同上 |
| `chinaunicom` | string | 中国联通定制线刷包文件名（可选） | 同上 |
| `originrec` | string | 原始卡刷包 URL（开发者预览版） | `"https://cdn.cnbj1.fds.api.mi-img.com/..."` |
| `originfb` | string | 原始线刷包 URL（开发者预览版） | `"https://cdn.cnbj1.fds.api.mi-img.com/..."` |

### 完整 JSON 响应示例

```json
{
  "device": "houji",
  "name": {
    "zh": "小米 14",
    "en": "Xiaomi 14"
  },
  "code": "NC",
  "suppports": ["OS1.0", "OS1.1", "OS2.0", "OS3.0"],
  "android": ["14.0", "15.0", "16.0"],
  "type": "phone",
  "miui": "no",
  "merged": "no",
  "branches": [
    {
      "name": {
        "zh": "小米澎湃 OS 正式版",
        "en": "Xiaomi HyperOS Stable"
      },
      "branchCode": "houji",
      "brand": "Xiaomi",
      "device": {
        "zh": "小米 14",
        "en": "Xiaomi 14"
      },
      "idtag": "CnOO",
      "tag": "CNXM",
      "branchtag": "F",
      "table": ["os", "android", "release", "aspatch", "recovery", "fastboot", "ctelecom"],
      "show": "1",
      "carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
      "region": "cn",
      "zone": "1",
      "ep": "0",
      "roms": {
        "OS3.0.303.0.WNCCNXM": {
          "os": "OS3.0.303.0.WNCCNXM",
          "android": "16.0",
          "release": "2026-06-10",
          "aspatch": "2026-05-01",
          "recovery": "houji-ota_full-OS3.0.303.0.WNCCNXM-user-16.0-c5d245a441.zip",
          "fastboot": "houji_images_OS3.0.303.0.WNCCNXM_20260529.0000.00_16.0_cn_05084cd0ea.tgz",
          "ctelecom": "houji_images_OS3.0.303.0.WNCCNXM_20260529.0000.00_16.0_cn_chinatelecom_c7f477e555.tgz"
        }
      }
    }
  ]
}
```

### 字段枚举值说明

**branchtag 分支类型**
| 值 | 说明 |
|----|------|
| `"F"` | 正式版/稳定版 |
| `"X"` | 测试版/开发版/预览版 |
| `"D"` | 每日构建版（隐藏） |

**type 设备类型**
| 值 | 说明 |
|----|------|
| `"phone"` | 手机 |
| `"tablet"` | 平板 |

**zone 区域分组**
| 值 | 说明 |
|----|------|
| `"1"` | 中国大陆时区 |
| `"2"` | 国际时区 |

**ep 政企版标识**
| 值 | 说明 |
|----|------|
| `"0"` | 普通消费版 |
| `"1"` | 企业/政府定制版 |

**show 显示控制**
| 值 | 说明 |
|----|------|
| `"1"` | 对外展示（正常分支） |
| `"0"` | 隐藏（演示机等特殊分支） |

**miui 是否有 MIUI 数据源**
| 值 | 说明 |
|----|------|
| `"yes"` | 该设备同时在 MIUI 数据源中存在 |
| `"no"` | 仅 HyperOS 设备 |

**merged 是否为马甲机合并**
| 值 | 说明 |
|----|------|
| `"yes"` | 多品牌/马甲机数据已合并 |
| `"no"` | 单一品牌数据 |

## MIUI设备详情 API 数据结构说明

> **数据源**：`GET https://data.miuier.com/data/devices/{code}.json`
> 
> 以下为 MIUI 设备详情 API 的完整响应结构说明。注意：MIUI 数据结构与 HyperOS 有显著差异。

### 顶层设备字段

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `codename` | string | 设备代号（唯一标识） | `"alioth"` |
| `zh-cn` | string | 中文名称 | `"Redmi K40/小米 11X/POCO F3"` |
| `en-us` | string | 英文名称 | `"Redmi K40/Mi 11X/POCO F3"` |
| `attentions` | array | 注意事项数组（含zh-cn/en-us） | `[{"zh-cn":"","en-us":""}]` |
| `cdid` | string | 客户端设备ID | `"37339049"` |
| `ismiui` | string | 是否为 MIUI 数据源设备 | `"0"`=是, `"1"`=否 |
| `ccshow` | string | 是否显示 CC 入口 | `"1"`=显示, `"0"`=不显示 |
| `cbshow` | string | 是否显示 CB 入口 | `"1"`=显示, `"0"`=不显示 |
| `csid` | string[] | CS ID 列表 | `["323"]` |
| `cbid` | string[] | CB ID 列表 | `["322"]` |
| `gdid` | string | GID（组ID） | `"10389"` |
| `pcid` | string | PCID（产品ID） | `"11369"` |
| `code` | string | 设备区域代码 | `"KH"` |
| `android` | string[] | 支持的 Android 版本数组 | `["11.0", "12.0", "13.0"]` |
| `miui` | string[] | 支持的 MIUI 版本数组 | `["V12.0", "V12.5", "V13.0", "V14.0"]` |
| `branches` | array | ROM 分支数组，详见下方 | 见分支字段 |

### branches[] 分支字段

每个分支对象包含以下字段：

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `code` | string | 分支代码（通常与codename相同） | `"alioth"` |
| `btag` | string | 分支类型标识 | `"F"`=正式版, `"X"`=开发/测试版 |
| `branch` | string | 分支名称标识 | `"Dev"`=开发版, `"Stable"`=稳定版 |
| `zh-cn` | string | 分支中文名称 | `"开发版"` |
| `en-us` | string | 分支英文名称 | `"China Beta"` |
| `region` | string | 地区代码 | `"cn"` / `"global"` / `"eea"` / `"in"` / `"ru"` / `"id"` / `"tr"` / `"tw"` |
| `tag` | string | 版本区域标签 | `""` / `"CNXM"` / `"MIXM"` |
| `zone` | string | 区域分组 | `"1"`=中国大陆时区, `"2"`=国际时区 |
| `pn` | string | 产品编号（部分设备有） | `"cepheus"` |
| `show` | string | 是否对外展示 | `"1"`=展示, `"0"`=隐藏 |
| `ep` | string | 是否政企版 | `"1"`=政企版, `"0"`=普通版 |
| `carrier` | string[] | 支持的运营商列表 | `["", "chinatelecom", "chinamobile", "chinaunicom"]` |
| `links` | array | ROM 版本列表（数组形式） | 详见 links 字段 |

### branches[].links[] ROM 版本字段

每个 ROM 版本对象包含以下字段：

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `miui` | string | MIUI 版本号 | `"V14.0.23.4.17.DEV"` |
| `android` | string | Android 版本 | `"13.0"` |
| `recovery` | string | Recovery 卡刷包文件名 | `"miui_ALIOTH_V14.0.23.4.17.DEV_8d19a97090_13.0.zip"` |
| `fastboot` | string | Fastboot 线刷包文件名（空字符串表示无） | `"alioth_images_V14.0.23.1.30.DEV_20230131.0000.00_13.0_cn_3d9a22fe03.tgz"` |
| `release` | string | 发布日期 (YYYY-MM-DD) | `"2023-04-21"` |

### 完整 JSON 响应示例

```json
{
  "codename": "alioth",
  "zh-cn": "Redmi K40/小米 11X/POCO F3",
  "en-us": "Redmi K40/Mi 11X/POCO F3",
  "attentions": [
    {
      "zh-cn": "",
      "en-us": ""
    }
  ],
  "cdid": "37339049",
  "ismiui": "0",
  "ccshow": "1",
  "cbshow": "1",
  "csid": ["323"],
  "cbid": ["322"],
  "gdid": "10389",
  "pcid": "11369",
  "code": "KH",
  "android": ["11.0", "12.0", "13.0"],
  "miui": ["V12.0", "V12.5", "V13.0", "V14.0"],
  "branches": [
    {
      "code": "alioth",
      "btag": "X",
      "region": "cn",
      "carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
      "branch": "Dev",
      "tag": "",
      "zone": "1",
      "show": "1",
      "ep": "0",
      "zh-cn": "开发版",
      "en-us": "China Beta",
      "links": [
        {
          "miui": "V14.0.23.4.17.DEV",
          "android": "13.0",
          "recovery": "miui_ALIOTH_V14.0.23.4.17.DEV_8d19a97090_13.0.zip",
          "fastboot": "",
          "release": "2023-04-21"
        },
        {
          "miui": "V14.0.23.1.30.DEV",
          "android": "13.0",
          "recovery": "miui_ALIOTH_V14.0.23.1.30.DEV_87d9b90cff_13.0.zip",
          "fastboot": "alioth_images_V14.0.23.1.30.DEV_20230131.0000.00_13.0_cn_3d9a22fe03.tgz",
          "release": "2023-02-03"
        }
      ]
    }
  ]
}
```

### 字段枚举值说明

**btag 分支类型**
| 值 | 说明 |
|----|------|
| `"F"` | 正式版/稳定版 |
| `"X"` | 开发版/测试版 |

**branch 分支名称**
| 值 | 说明 |
|----|------|
| `"Dev"` | 开发版（每周更新） |
| `"Stable"` | 稳定版 |

**ismiui 是否为 MIUI 设备**
| 值 | 说明 |
|----|------|
| `"0"` | 是 MIUI 设备 |
| `"1"` | 非 MIUI 设备 |
| `""` | 未标注（如 cepheus） |

**zone 区域分组**
| 值 | 说明 |
|----|------|
| `"1"` | 中国大陆时区 |
| `"2"` | 国际时区 |

**ep 政企版标识**
| 值 | 说明 |
|----|------|
| `"0"` | 普通消费版 |
| `"1"` | 企业/政府定制版 |

**show 显示控制**
| 值 | 说明 |
|----|------|
| `"1"` | 对外展示（正常分支） |
| `"0"` | 隐藏（演示机等特殊分支） |

**ccshow / cbshow 显示开关**
| 值 | 说明 |
|----|------|
| `"1"` | 显示对应入口 |
| `"0"` / `""` | 隐藏对应入口 |

### MIUI 与 HyperOS 数据结构对比

| 对比项 | HyperOS | MIUI |
|--------|---------|------|
| 根标识字段 | `device` | `codename` |
| 名称字段 | `name.zh` / `name.en` | `zh-cn` / `en-us` |
| ROM版本字段 | `os` | `miui` |
| ROM存储结构 | `roms{}` 对象（key为版本号） | `links[]` 数组 |
| 分支标识 | `idtag` | `branch` |
| 分支类型 | `branchtag` | `btag` |
| 特有字段 | `suppports`, `type`, `merged`, `table` | `attentions`, `cdid`, `ismiui`, `ccshow`, `cbshow`, `csid`, `cbid`, `gdid`, `pcid`, `pn` |
| 版本号格式 | `OSx.x.x.x.XXXXXX` | `Vx.x.x.x.XXXXXX` / `xx.x.x` |

## 支持的地区分支
| 地区 | 代码 | 标识 | 主要分支 |
|------|------|------|----------|
| 中国大陆 | cn | CnOO/CnOB/Dev/Beta | 正式版/Beta版/开发版/体验增强版 |
| 国际版 | global | GBOO | 全球国际版 |
| 欧洲EEA | eea | EEAO | 欧洲经济区版 |
| 中国台湾 | tw | CNTP | 中国台湾地区版 |
| 印度 | in | INSO | 印度版 |
| 俄罗斯 | ru | RUSO | 俄罗斯版 |
| 印度尼西亚 | id | IDSO | 印度尼西亚版 |
| 土耳其 | tr | TRSO | 土耳其版 |
| 其他 | th/jp/kr/za/mx/lm | THAS/JAPS/SKSO/ZAVC/MXAT/LMCR | 泰国/日本/韩国/南非/墨西哥/拉美运营商定制版 |

## 支持的分支类型
| 分支名称 | 标识 | branchtag | 说明 |
|----------|------|-----------|------|
| 小米澎湃OS正式版 | CnOO/GBOO/EEAO/INSO等 | F | 各地区稳定版 |
| 小米澎湃OS Beta | CnOB | F | 中国大陆Beta测试版 |
| 小米澎湃OS开发版 | Dev | X | 中国大陆开发版 |
| 小米澎湃OS体验增强版Beta | Beta | F | 体验增强测试版 |
| 小米澎湃OS安卓开发者预览版 | ADPC/ADPG | X | Android开发者预览版 |
| MIUI稳定版 | Stable | F | MIUI稳定版 |
| MIUI开发版 | Dev | X | MIUI开发版 |

## 版本号格式说明
| 类型 | 格式示例 | 说明 |
|------|----------|------|
| HyperOS正式版 | OS3.0.305.0.WNACNXM | OS版本.主版本.子版本.构建号.区域标识 |
| HyperOS政企版 | OS1.0.24.6.4.EP.STDEE.N1 | 带EP标识的政企版本 |
| HyperOS演示机版 | OS3.0.301.0.WPJCNDM | 带WPJ标识的演示机版本 |
| MIUI稳定版 | V14.0.10.0.TKBCNXM | V版本.主版本.子版本.日期.区域标识 |
| MIUI开发版 | V14.0.23.4.17.DEV | 带DEV标识的开发版本 |
| MIUI预览版 | 22.10.26 | 开发版预览格式（年份.月.日） |

## 隐藏分支说明（不对外展示）
| 分支类型 | 过滤条件 | 说明 |
|----------|----------|------|
| 政企标准版 | `ep="1"` 或 `idtag="EPSTD"` | 专为企业和政府用户定制 |
| CJCC政企定制版 | `idtag="EPCJCC"` | 中国政企定制版 |
| 演示机系统 | `idtag="CnOD"/"GBOO"/"EEAD"/"IDDM"` 或 `tag="CNDM"/"MIDM"` | 小米门店展示专用 |
| 国际DC版 | `idtag="GBDC"` | 国际版DC定制版 |
| 每日构建版 | `branchtag="D"` | 每日自动编译的测试版本 |

**过滤规则**：仅显示 `show="1"` 且 `ep="0"` 且 `branchtag≠"D"` 且非演示机版、非政企定制版、非DC版的分支

## 示例对话
**示例1**：用户查询小米14的ROM版本 → 搜索关键词"小米14" → 匹配设备：小米14 (代号: houji) → 显示设备详情和ROM版本列表

**示例2**：用户需要小米13 Ultra的HyperOS开发版下载 → 定位设备：小米13 Ultra (ishtar) → 筛选分支：开发版/内测版 → 显示Recovery和Fastboot下载链接

**示例3**：用户查询POCO X8 Pro国际版ROM → 定位设备：POCO X8 Pro (klee) → 筛选分支：国际正式版 → 显示国际版ROM版本列表  

## 工作流程
1. **解析查询参数**：提取设备名称/代号、品牌、数据源、地区、版本类型等参数
2. **获取设备列表**：并行调用HyperOS和MIUI数据源API，合并设备数据
3. **应用筛选条件**：按关键词、品牌、数据源、隐藏分支规则过滤设备
4. **展示设备卡片**：显示设备名称、代号、数据源标签、支持版本概览
5. **获取设备详情**：根据用户选择，获取指定设备的详细ROM信息
6. **展示ROM版本**：按分支分类显示版本号、Android版本、发布日期、下载链接
7. **拼接下载链接**：根据ROM类型自动生成Recovery/Fastboot下载链接

**API端点**：
- HyperOS设备列表：`GET https://data.hyperos.fans/devices.json`
- HyperOS设备详情：`GET https://data.hyperos.fans/devices/{code}.json`
- MIUI设备列表：`GET https://data.miuier.com/data/devlist.json`
- MIUI设备详情：`GET https://data.miuier.com/data/devices/{code}.json`

## 输出格式
### 设备列表卡片
**小米ROM版本查询 - 找到 {N} 个设备**
| 设备名称 | 代号 | 支持系统 | 数据源 | 操作 |
|---------|------|----------|--------|------|
| {设备名} | {code} | OS1.0/OS2.0/OS3.0 | 🔵HyperOS | [查看详情] |
| {设备名} | {code} | V12/V13/V14 | 🟠MIUI | [查看详情] |
| {设备名} | {code} | OS1.0/OS2.0/V14 | 🔵HyperOS 🟠MIUI | [查看详情] |

**筛选条件**：品牌={品牌} | 数据源={数据源} | 关键词="{关键词}"

### 设备详情页
**{设备名称} ({代号})**
| 项目 | 详情 |
|------|------|
| **支持系统** | HyperOS {supports列表} / MIUI {miui列表} |
| **支持Android** | {android列表} |
| **品牌** | {品牌} |

**{分支名称} ({分支ID})**
**区域**：{region} | **时区**：{zone}
| 版本号 | Android | 发布日期 | 安全补丁 | 下载 |
|--------|---------|----------|----------|------|
| {版本} | {Android} | {日期} | {补丁日期} | [📦卡刷]({卡刷链接}) [⚡线刷]({线刷链接}) |

### 地区版本对比
| 地区 | 最新版本 | Android | 发布日期 | 下载 |
|------|----------|---------|----------|------|
| 中国大陆 | {版本} | {Android} | {日期} | [📦卡刷]({链接}) [⚡线刷]({链接}) |
| 国际版 | {版本} | {Android} | {日期} | [📦卡刷]({链接}) [⚡线刷]({链接}) |
| 欧洲EEA | {版本} | {Android} | {日期} | [📦卡刷]({链接}) [⚡线刷]({链接}) |

## 下载链接拼接规则
**标准链接格式**：
```
卡刷包：https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/{version}/{recovery}
线刷包：https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/{version}/{fastboot}
电信定制线刷包：https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/{version}/{ctelecom}
```

**开发者预览版**：使用 `originrec` 和 `originfb` 字段中的完整URL

**文件名命名规则**：
- Recovery卡刷包：`miui_{CODENAME}_{VERSION}_{HASH}_{ANDROID}.zip`（普通版）或 `miui_{CODENAME}PRE_{VERSION}_{HASH}_{ANDROID}.zip`（预览版）
- Fastboot线刷包：`{codename}_images_{VERSION}_{DATE}.0000.00_{ANDROID}_{REGION}_{HASH}.tgz`（普通版）或 `{codename}_ctelecom_images_{VERSION}_{DATE}.0000.00_{ANDROID}_cn_{HASH}.tgz`（电信定制版）

**有效性检查**：文件名后缀应为 `.zip`（卡刷）或 `.tgz`（线刷），版本号格式应为 `OSx.x.x.x.xxxxxx`（HyperOS）或 `Vx.x.x.x.xxxxxx`/`xx.x.x`（MIUI），空字符串字段不显示对应下载按钮

## 注意事项
1. **内测版限制**：部分开发版/Beta版ROM需要小米账号权限才能刷入
2. **刷机风险**：刷机前请备份数据，确保电量充足，使用官方工具（MiFlash）进行线刷
3. **地区限制**：部分分支仅适用于特定地区，跨地区刷机可能导致功能异常
4. **版本兼容性**：确保下载的ROM版本与设备当前系统版本兼容
5. **固件完整性**：下载后建议校验文件MD5/SHA256哈希值
6. **隐藏版本**：政企版、演示机版、每日构建版不对外展示，普通用户无需关注