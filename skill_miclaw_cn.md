---
name: 小米设备📱ROM版本查询
description: 查询小米/Redmi/POCO设备的HyperOS和MIUI ROM版本信息，支持设备搜索、版本筛选、固件下载链接获取
tags: [小米, ROM, HyperOS, MIUI, 固件, 刷机, 设备查询, 版本查询, 系统更新]
version: 1.0.6
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

## 数据结构说明
**设备字段**：`device`/`codename`(代号)、`name`/`zh-cn`(中文名)、`android`(Android版本)、`branches`(分支列表)等

**分支字段**：`idtag`(分支标识)、`region`(地区)、`tag`(版本标签)、`branchtag`(类型)、`carrier`(运营商)、`show`(显示)、`ep`(政企版)等

**ROM版本字段**：`os`/`miui`(版本号)、`android`、`release`(发布日期)、`aspatch`(安全补丁)、`recovery`(卡刷包)、`fastboot`(线刷包)等

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
| 中国大陆 | {版本} | {Android} | {日期} | [📦]({链接}) [⚡]({链接}) |
| 国际版 | {版本} | {Android} | {日期} | [📦]({链接}) [⚡]({链接}) |
| 欧洲EEA | {版本} | {Android} | {日期} | [📦]({链接}) [⚡]({链接}) |

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