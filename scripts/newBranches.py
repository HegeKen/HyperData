import OScommon
from datetime import datetime

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
urls = []
known_urls = []

def chekc_known_urls_exits(url):
  if url in known_urls:
    i = 0
  else:
    known_urls.append(url)

def chekc_url_exits(url):
  if url in urls or url in known_urls:
    i = 0
  else:
    urls.append(url)

carriers = ["","chinatelecom","chinaunicom","chinamobile"]
cnbranches = ['','_demo','_ep_yunke','_ep_stdee','_ep_xy','_ep_kywl','_ep_cqrcb','_ep_ec','_ep_sxht','_ep_yfan','_ep_yx','_ep_stdce',
              '_ep_xdja','_ep_litee','_ep_yy','_ep_tly','_ep_sdlybjcg','_tl','_ep_tl','_ep_tkgwdl', '_ep_dhao', '_ep_by', '_ep_qiy',
              '_ep_ui','_ep_tlkj', '_ep_tq', '_ep_wosq', '_ep_xzm', '_ep_zc360', '_ep_zdjt', '_ep_zzyglkg', '_soter', '_pre_wechat',
              '_ep_justsafe', '_ep_nio', '_ep_txzx', '_factory', '_pre_7475vbl', '_ep_dameng', '_ep_yxyun', '_ep_hujing', '_ep_jwm',
              '_ep_yfd', '_ep_zzybp', '_ep_daote', '_ep_jd', '_ep_tjzf', '_ep_tpybx', '_ep_bds', '_ep_hfwd', '_ep_hn', '_ep_jyrj',
              '_cm', '_ct', '_pfc', '_ep_byd', '_miui_factory', '_stable_cmcc01', '_fs', '_liuniu', '_ep_mjwxns', '_ep_czht',
              '_ep_sbgl', '_y002_pre']
twbranches = ["_tw_global"]
gfbranches = ["_global","_tw_global","_eea_global","_ru_global","_id_global","_in_global","in_global","_in_fk_global","_kr_global",
              "in_in_global","_tr_global","_jp_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_jp_kd_global",
              "_kr_gu_global","_kr_kt_global","_kr_sk_global","_h3g_global","_eea_hg_global","_eea_or_global","_eea_tf_global",
              "_eea_by_global","_eea_vf_global","_mx_tc_global","_mx_at_global","_lm_cr_global","_cl_en_global","_cl_global",
              "_eea_sf_global","_eea_ti_global""_th_as_global","_lm_ms_global","_pe_ms_global","_za_vc_global","_za_mt_global",]
gbbranches = ["_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_mx_tc_global","_mx_at_global","_lm_cr_global",
              "_cl_en_global","_cl_global","_th_as_global","_lm_ms_global","_pe_ms_global","_za_vc_global","_za_mt_global","_gt_tg_global","_gt_global"]
eeabranches = ["_eea_global","_h3g_global","_eea_hg_global","_eea_or_global","_eea_ee_global","_eea_tf_global","_eea_by_global","_eea_vf_global","_eea_sf_global","_eea_ti_global"]
rubranches = ["_ru_global"]
inbranches = ["_in_global","in_global","_in_fk_global","_in_jo_global","in_in_global"]
idbranches = ["_id_global"]
trbranches = ["_tr_global"]
krbranches = ["_kr_global","_kr_gu_global","_kr_kt_global","_kr_sk_global"]
jpbranches = ["_jp_global","_jp_sb_global","_jp_kd_global","_jp_rk_global"]

onedevices = ["blue"]

for device in OScommon.only_os:
  devdata = OScommon.localData(device)
  for branch in devdata["branches"]:
    code = branch["branchCode"]
    if code == "":
      print("请修补机型： "+device+"文件中未指定的区域代码\n")
    else:
      i = 0
    btag = branch["branchtag"]
    region = branch["region"]
    carriers = branch["carrier"]
    if region == "cn":
      if len(carriers)==0:
        chekc_known_urls_exits(code+"&b="+btag+"&r="+region+"&n=")
      else:
        for carrier in carriers:
          chekc_known_urls_exits(code+"&b="+btag+"&r="+region+"&n="+carrier)
    elif region == "global":
      chekc_known_urls_exits(code+"&b="+btag+"&r="+region+"&n=")
    else:
      chekc_known_urls_exits(code+"&b="+btag+"&r="+region+"&n=")
      chekc_known_urls_exits(code+"&b="+btag+"&r="+code.split("_global")[0]+"&n=")
      chekc_known_urls_exits(code+"&b="+btag+"&r=eea&n=")
      chekc_known_urls_exits(code+"&b="+btag+"&r="+code.split("_global")[0]+"&n=")
      chekc_known_urls_exits(code+"&b="+btag+"&r=global"+"&n=")

for device in OScommon.only_os:
  if device in onedevices:
    for branch in gfbranches:
      chekc_url_exits(device+branch+"&b=F&r=&n=")
  else:
    for branch in cnbranches:
      for carrier in carriers:
        chekc_url_exits(device+branch+"&b=F&r=cn&n="+carrier)
    for branch in gbbranches:
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in eeabranches:
      chekc_url_exits(device+branch+"&b=F&r=eea&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in rubranches:
      chekc_url_exits(device+branch+"&b=F&r=ru&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in inbranches:
      chekc_url_exits(device+branch+"&b=F&r=in&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in idbranches:
      chekc_url_exits(device+branch+"&b=F&r=id&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in trbranches:
      chekc_url_exits(device+branch+"&b=F&r=tr&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in krbranches:
      chekc_url_exits(device+branch+"&b=F&r=kr&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")
    for branch in jpbranches:
      chekc_url_exits(device+branch+"&b=F&r=jp&n=")
      chekc_url_exits(device+branch+"&b=F&r=global&n=")

# for device in OScommon.currentStable:
#   if device in onedevices:
#     for branch in gfbranches:
#       url = base_url+device+branch+"&b=F&r=&n="
#       chekc_url_exits()
#   else:
#     for branch in cnbranches:
#       for carrier in carriers:
#         url = base_url+device+branch+"&b=F&r=cn&n="+carrier
#         chekc_url_exits()
#     for branch in gbbranches:
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in eeabranches:
#       url = base_url+device+branch+"&b=F&r=eea&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in rubranches:
#       url = base_url+device+branch+"&b=F&r=ru&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in inbranches:
#       url = base_url+device+branch+"&b=F&r=in&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in idbranches:
#       url = base_url+device+branch+"&b=F&r=id&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in trbranches:
#       url = base_url+device+branch+"&b=F&r=tr&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in krbranches:
#       url = base_url+device+branch+"&b=F&r=kr&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()
#     for branch in jpbranches:
#       url = base_url+device+branch+"&b=F&r=jp&n="
#       chekc_url_exits()
#       url = base_url+device+branch+"&b=F&r=global&n="
#       chekc_url_exits()

for url in urls:
  print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"\t"+base_url+url+"                                             ",end="")
  OScommon.getFastboot(base_url+url)