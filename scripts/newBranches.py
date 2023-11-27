import common

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="

carriers = ["","chinatelecom","chinaunicom","chinamobile"]
cnbranches = ["","_demo","_ep_yunke","_ep_stdee","_ep_xy","_ep_kywl","_ep_cqrcb","_ep_ec","_ep_sxht","_ep_yfan","_ep_yx","_ep_stdce",
              "_ep_xdja","_ep_litee","_ep_yy","_ep_tly","_ep_sdlybjcg","_tl","_ep_tl","_ep_tkgwdl"]
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

onedevices=["tissot","jasmine","laurel","tiare","ice","water"]


for device in common.newDevices:
  if device in onedevices:
    for branch in gfbranches:
      print("\r"+base_url+device+branch+"&b=F&r=cn&n=                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=&n=")
  else:
    for branch in cnbranches:
      for carrier in carriers:
        print("\r"+base_url+device+branch+"&b=F&r=cn&n="+carrier+"                                      ",end="")
        common.getFastboot(base_url+device+branch+"&b=F&r=cn&n="+carrier)
    for branch in gbbranches:
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in eeabranches:
      print("\r"+base_url+device+branch+"&b=F&r=eea&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=eea&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in rubranches:
      print("\r"+base_url+device+branch+"&b=F&r=ru&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=ru&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in inbranches:
      print("\r"+base_url+device+branch+"&b=F&r=in&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=in&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in idbranches:
      print("\r"+base_url+device+branch+"&b=F&r=id&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=id&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in trbranches:
      print("\r"+base_url+device+branch+"&b=F&r=tr&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=tr&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in krbranches:
      print("\r"+base_url+device+branch+"&b=F&r=kr&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=kr&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in jpbranches:
      print("\r"+base_url+device+branch+"&b=F&r=jp&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=jp&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")

for device in common.currentStable:
  if device in onedevices:
    for branch in gfbranches:
      print("\r"+base_url+device+branch+"&b=F&r=cn&n=                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=&n=")
  else:
    for branch in cnbranches:
      for carrier in carriers:
        print("\r"+base_url+device+branch+"&b=F&r=cn&n="+carrier+"                                      ",end="")
        common.getFastboot(base_url+device+branch+"&b=F&r=cn&n="+carrier)
    for branch in gbbranches:
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in eeabranches:
      print("\r"+base_url+device+branch+"&b=F&r=eea&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=eea&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in rubranches:
      print("\r"+base_url+device+branch+"&b=F&r=ru&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=ru&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in inbranches:
      print("\r"+base_url+device+branch+"&b=F&r=in&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=in&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in idbranches:
      print("\r"+base_url+device+branch+"&b=F&r=id&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=id&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in trbranches:
      print("\r"+base_url+device+branch+"&b=F&r=tr&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=tr&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in krbranches:
      print("\r"+base_url+device+branch+"&b=F&r=kr&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=kr&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")
    for branch in jpbranches:
      print("\r"+base_url+device+branch+"&b=F&r=jp&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=jp&n=")
      print("\r"+base_url+device+branch+"&b=F&r=global&n="+"                                      ",end="")
      common.getFastboot(base_url+device+branch+"&b=F&r=global&n=")