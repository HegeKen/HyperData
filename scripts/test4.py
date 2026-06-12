import OScommon

# 测试 tgz 线刷包
url = "https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/OS2.0.203.0.VPFMIDM/charoite_global_images_OS2.0.203.0.VPFMIDM_20260119.0000.00_15.0_global_50d87c0c9b.tgz"
patch_date = OScommon.get_security_patch_from_ota_url(url, 'fastboot')
print(f"安全补丁日期: {patch_date}")