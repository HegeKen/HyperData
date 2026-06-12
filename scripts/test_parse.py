#!/usr/bin/env python3
"""测试特定文件名是否能被正确解析"""

import OScommon

# 测试文件名列表
test_files = [
    "nezha_dpp-ota_full-OS3.3.260422.2.XPACNXM.STABLE-DPP-user-17.0-871d44f4c2.zip",
    "pudding_dpp-ota_full-OS3.3.260420.2.XPCCNXM.STABLE-DPP-user-17.0-4028bc5322.zip",
    "pudding_dpp_global-ota_full-OS3.3.260420.2.XPCMIXM.STABLE-DPP-user-17.0-2c6fb4e997.zip",
    "nezha_dpp_global-ota_full-OS3.3.260420.2.XPAMIXM.STABLE-DPP-user-17.0-96a5bcca8f.zip",
    "klimt_dpp_global-ota_full-OS3.3.260423.1.XOSMIXM.STABLE-DPP-user-17.0-0b7c4286bc.zip"
]

print("=" * 80)
print("测试文件名解析")
print("=" * 80)

for filename in test_files:
    print(f"\n文件名: {filename}")
    result = OScommon.getData(filename)
    if result == 0:
        print("❌ 解析失败：返回 0")
    else:
        device, code, android, version, rom_type, bigver, region, tag, zone, branch, filetype = [item for item in result]
        print(f"✅ 解析成功:")
        print(f"   设备代号 (device): {device}")
        print(f"   代码 (code): {code}")
        print(f"   版本 (version): {version}")
        print(f"   Android版本 (android): {android}")
        print(f"   ROM类型 (rom_type): {rom_type}")
        print(f"   大版本 (bigver): {bigver}")
        print(f"   区域 (region): {region}")
        print(f"   标签 (tag): {tag}")
        print(f"   区域带 (zone): {zone}")
        print(f"   分支 (branch): {branch}")
        print(f"   文件类型 (filetype): {filetype}")

print("\n" + "=" * 80)
