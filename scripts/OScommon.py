import json
from sys import platform
import urllib
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

sdk = {
  "14": "34",
  "13": "33"
}

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"


currentStable = ["chenfeng", "opal", "sapphire", "aurora", "emerald", "ares", "enuma","mona",
								 "houji", "nabu", "elish", "spesn", "spes", "viva", "veux", "zijin", "shennong_t", 
								 "evergo",  "sheng", "ziyi", "cetus" ,"lisa", "pissarro", "agate", "aristotle", "babylon",
								 "corot","cupid", "dagu", "daumier", "diting", "duchamp", "earth", "fire", "fuxi", "garnet", "gold",
								 "ingres", "ishtar", "light", "lightcm", "liuqin", "manet", "marble", "matisse", "mayfly",
								 "mondrian", "moonstone", "nuwa", "pipa", "plato", "psyche","redwood", "rock", "rubens", "ruby", "sea",
								 "shennong", "sky", "socrates", "sunstone", "sweet_k6a","taoyao", "tapas", "thor", "topaz", "unicorn",
								 "vermeer", "xun", "yudi", "yuechu", "yunluo", "zeus", "zircon", "zizhan"]
newDevices = ["chenfeng", "dizi", "goku", "peridot", "ruan", "ruyi", "houji", "shennong", "aurora", "sheng", 
			  "duchamp", "vermeer", "manet"]

onedevices = ["blue"]
cn_devices = ['sheng', 'ziyi', 'cetus', 'lisa', 'pissarro', 'ruyi', 'babylon', 'dagu', 'daumier', 'garnet', 'gold', 'houji', 'lightcm', 'liuqin', 'manet', 'matisse', 'mayfly', 'psyche', 'rubens', 'shennong', 'socrates', 'thor', 'unicorn', 'vermeer', 'xun', 'yudi', 'yuechu', 'zircon', 'zizhan']
gb_devices = ['agate', 'aristotle', 'fire', 'moonstone', 'plato', 'rock', 'sea', 'sunstone', 'sweet_k6a', 'taoyao', 'tapas', 'topaz']
both_regions = ['aurora', 'corot', 'cupid', 'diting', 'duchamp', 'earth', 'fuxi', 'ingres', 'ishtar', 'light', 'marble', 'mondrian', 'nuwa', 'pipa', 'redwood', 'ruby', 'sky', 'yunluo', 'zeus']


flags = {
	"HOUJI": "houji",
	"HOUJIDEMO": "houji",
	"houji": "houji",
	"houji_demo": "houji",
	"houji_global": "houji",
	"HOUJIGlobal": "houji",
	"houji_in_global": "houji",
	"HOUJIINGlobal": "houji",
	"houji_id_global": "houji",
	"HOUJIIDGlobal": "houji",
	"houji_tw_global": "houji",
	"HOUJITWGlobal": "houji",
	"houji_tr_global": "houji",
	"HOUJITRGlobal": "houji",
	"garnet_global": "garnet",
	"GARNETGlobal": "garnet",
	"fire_in_global":"fire",
	"FIREINGlobal":"fire",
	"ruby_tr_global":"ruby",
	"RUBYTRGlobal":"ruby",
	"opal_tw_global":"opal",
	"OPALTWGlobal":"opal",
	"evergreen_tw_global": "evergreen",
	"EVERGREENTWGlobal": "evergreen",
	"agate_eea_vf_global": "agate",
	"AGATEEEAVFGlobal": "agate",
	"agate_eea_by_global":"agate",
	"AGATEEEABYGlobal":"agate",
	"sky_jp_global": "sky",
	"SKYJPGlobal": "sky",
	"sky_ep_stdee": "sky",
	"SKYEPSTDEE": "sky",
	"sapphire_global": "sapphire",
	"SAPPHIREGlobal": "sapphire",
	"xun_ru_global": "xun",
	"chenfeng_demo": "chenfeng",
	"CHENFENGDEMO": "chenfeng",
	"XUNRUGlobal": "xun",
	"chenfeng":"chenfeng",
	"duchamp_ep_stdee": "duchamp",
  "DUCHAMPEPSTDEE": "duchamp",
	"agate_eea_ti_global": "agate",
	"AGATEEEATIGlobal": "agate",
	"zircon_id_global":"zircon",
	"ZIRCONIDGlobal":"zircon",
	"zircon_global":"zircon",
	"ZIRCONGlobal":"zircon",
	"dizi":"dizi",
	"goku":"goku",
	"aurora_global": "aurora",
	"AURORAGlobal": "aurora",
	"aurora_tw_global": "aurora",
	"AURORATWGlobal": "aurora",
	"agate_eea_hg_global": "agate",
	"AGATEEEAHGGlobal": "agate",
	"peridot":"peridot",
	"ruan":"ruan",
	"CHENFENG":"chenfeng",
	"DIZI":"dizi",
	"GOKU":"goku",
	"PERIDOT":"peridot",
	"RUAN":"ruan",
	"garnet_in_global": "garnet",
	"GARNETINGlobal": "garnet",
	"ruby_in_global": "ruby",
	"RUBYINGlobal": "ruby",
	"ruby_ep_stdee": "ruby",
	"RUBYEPSTDEE": "ruby",
	"earth_eea_by_global": "earth",
	"EARTHEEABYGlobal": "earth",
	"ares": "ares",
	"mona":"mona",
	"MONA":"mona",
	"XUNEEAGlobal":"xun",
	"xun_eea_global":"xun",
	"earth_eea_tf_global": "earth",
	"EARTHEEATFGlobal": "earth",
	"earth_eea_ti_global": "earth",
	"EARTHEEATIGlobal": "earth",
	"ARES":"ares",
	"SPESGlobal":"spes",
	"fleur_global": "fleur",
	"FLEURGlobal": "fleur",
	"sunstone_in_global": "sunstone",
	"SUNSTONEINGlobal": "sunstone",
	"emerald_global": "emerald",
	"EMERALDGlobal": "emerald",
	"psyche_global": "psyche",
	"PSYCHEGlobal": "psyche",
	"ruby_tw_global": "ruby",
	"RUBYTWGlobal": "ruby",
	"moonstone_tw_global": "moonstone",
	"MOONSTONETWGlobal": "moonstone",
	"VIVAGlobal":"viva",
	"blue_lm_cr_global": "blue",
	"zeus_in_global":"zeus",
	"ZEUSINGlobal":"zeus",
	"gold_eea_global": "gold",
	"GOLDEEAGlobal": "gold",
	"aurora_eea_global": "aurora",
	"AURORAEEAGlobal": "aurora",
	"ingres_id_global": "ingres",
	"INGRESIDGlobal": "ingres",
	"ZIRCONINGlobal":"zircon",
	"zircon_in_global":"zircon",
	"light_eea_ti_global": "light",
	"LIGHTEEATIGlobal": "light",
	"blue_in_global": "blue",
  "BLUEINGlobal": "blue",
	"viva_eea_global": "viva",
	"VIVAEEAGlobal": "viva",
	"light_id_global": "light",
	"LIGHTIDGlobal": "light",
	"enuma": "enuma",
	"ENUMA": "enuma",
	"zircon": "zircon",
	"ZIRCON": "zircon",
	"nabu": "nabu",
	"NABU": "nabu",
	"xun_global": "xun",
	"XUNGlobal": "xun",
	"aurora": "aurora",
	"AURORA": "aurora",
	"spesn_global": "spesn",
	"SPESNGlobal": "spesn",
	"sky_tw_global": "sky",
	"SKYTWGlobal": "sky",
	"aurora_demo": "aurora",
	"houji_ru_global": "houji",
	"HOUJIRUGlobal": "houji",
	"shennong_t": "shennong_t",
	"SHENNONGT": "shennong_t",
	"veux": "veux",
	"VEUX": "veux",
	"zijin": "zijin",
	"ZIJIN": "zijin",
	"garnet_eea_global": "garnet",
	"GARNETEEAGlobal": "garnet",
	"spes_global": "spes",
	"SPESGlobal": "spes",
	"viva_global": "viva",
	"viva_global": "viva",
	"light_in_global": "light",
	"LIGHTINGlobal": "light",
	"light_tw_global": "light",
	"LIGHTTWGlobal": "light",
	"elish": "elish",
	"ELISH": "elish",
	"AURORADEMO": "aurora",
	"fire_tr_global": "fire",
	"FIRETRGlobal": "fire",
	"gold_global": "gold",
	"GOLDGlobal": "gold",
	"cupid_id_global": "cupid",
	"CUPIDIDGlobal": "cupid",
	"ziyi":"ziyi",
	"ZIYI":"ziyi",
	"ruyi": "ruyi",
	"RUYI": "ruyi",
	"aristotle_ru_global": "aristotle",
	"aristotle_tr_global": "aristotle",
	"ARISTOTLERUGlobal": "aristotle",
	"ARISTOTLETRGlobal": "aristotle",
	"yunluo_in_global": "yunluo",
	"YUNLUOINGlobal": "yunluo",
	"yunluo_eea_global": "yunluo",
	"YUNLUOEEAGlobal": "yunluo",
	"taoyao_ru_global": "taoyao",
	"TAOYAORUGlobal": "taoyao",
	"houji_eea_global": "houji",
	"HOUJIEEAGlobal": "houji",
	"corot_tw_global": "corot",
	"COROTTWGlobal": "corot",
	"corot_ru_global": "corot",
	"COROTRUGlobal": "corot",
	"earth_tr_global": "earth",
	"EARTHTRGlobal": "earth",
	"earth_ru_global": "earth",
	"EARTHRUGlobal": "earth",
	"light_eea_global": "light",
	"LIGHTEEAGlobal": "light",
	"sheng": "sheng",
	"SHENG": "sheng",
	"sheng_demo": "sheng",
	"SHENGDEMO": "sheng",
	"garnet": "garnet",
	"GARNET": "garnet",
	"earth_id_global": "earth",
	"EARTHIDGlobal": "earth",
	"rock_id_global": "rock",
	"ROCKIDGlobal": "rock",
	"moonstone_ru_global": "moonstone",
	"MOONSTONERUGlobal": "moonstone",
	"zeus_global": "zeus",
	"ZEUSGlobal": "zeus",
	"cetus":"cetus",
	"CETUS":"cetus",
	"redwood_ru_global": "redwood",
	"REDWOODRUGlobal": "redwood",
	"redwood_tw_global": "redwood",
	"REDWOODTWGlobal": "redwood",
	"redwood_tr_global": "redwood",
	"REDWOODTRGlobal": "redwood",
	"earth_tw_global": "earth",
	"EARTHTWGlobal": "earth",
	"sweet_k6a_ru_global": "sweet_k6a",
	"SWEETK6ARUGlobal": "sweet_k6a",
	"sweet_k6a_eea_global": "sweet_k6a",
	"rock_tw_global": "rock",
	"ROCKTWGlobal": "rock",
	"rock_ru_global": "rock",
	"ROCKRUGlobal": "rock",
	"rock_tr_global": "rock",
	"ROCKTRGlobal": "rock",
	"SWEETK6AEEAGlobal": "sweet_k6a",
	"fire_ru_global": "fire",
	"earth_eea_global": "earth",
	"FIRERUGlobal": "fire",
	"fire_id_global": "fire",
	"FIREIDGlobal": "fire",
	"EARTHEEAGlobal": "earth",
	"diting_tw_global": "diting",
	"DITINGGlobal": "diting",
	"diting_global": "diting",
	"DITINGTWGlobal": "diting",
	"diting_ru_global": "diting",
	"DITINGRUGlobal": "diting",
	"diting_tr_global": "diting",
	"DITINGTRGlobal": "diting",
	"moonstone_eea_global": "moonstone",
	"rock_global": "rock",
	"MOONSTONEEEAGlobal": "moonstone",
	"ROCKGlobal": "rock",
	"daumier": "daumier",
	"sky_global": "sky",
	"SKYGlobal": "sky",
	"marble_in_global": "marble",
	"MARBLEINGlobal": "marble",
	"REDWOOD": "redwood",
	"redwood": "redwood",
	"DAGU": "dagu",
	"sky_in_global": "sky",
	"SKYINGlobal": "sky",
	"lisa_eea_global": "lisa",
	"LISAEEAGlobal": "lisa",
	"sunstone_tw_global": "sunstone",
	"SUNSTONETWGlobal": "sunstone",
	"fire_eea_global": "fire",
	"FIREEEAGlobal": "fire",
	"DUCHAMPIDGlobal": "duchamp",
	"duchamp_id_global": "duchamp",
	"redwood_global": "redwood",
	"REDWOODGlobal": "redwood",
	"ruby_eea_global": "ruby",
	"RUBYEEAGlobal": "ruby",
	"ruby_kr_global": "ruby",
	"RUBYKRGlobal": "ruby",
	"sky_eea_global": "sky",
	"SKYEEAGlobal": "sky",
	"ruby": "ruby",
	"GOLD": "gold",
	"gold": "gold",
	"topaz_ru_global": "topaz",
	"TOPAZRUGlobal": "topaz",
	"plato_ru_global": "plato",
	"PLATORUGlobal": "plato",
	"marble": "marble",
	"MARBLE": "marble",
	"light_global": "light",
	"LIGHTGlobal": "light",
	"pipa_id_global": "pipa",
	"PIPAIDGlobal": "pipa",
	"PIPADEMO": "pipa",
	"redwood_eea_global": "redwood",
	"REDWOODEEAGlobal": "redwood",
	"redwood_in_global": "redwood",
	"REDWOODINGlobal": "redwood",
	"agate_eea_global": "agate",
	"AGATEEEAGlobal": "agate",
	"agate_ru_global": "agate",
	"AGATERUGlobal": "agate",
	"rock_in_global": "rock",
	"ROCKINGlobal": "rock",
	"blue_ru_global": "blue",
	"BLUERUGlobal": "blue",
	"blue_global": "blue",
	"BLUEGlobal": "blue",
	"blue_id_global": "blue",
	"BLUEIDGlobal": "blue",
	"RUBYIDGlobal": "ruby",
	"ruby_id_global": "ruby",
	"LIUQINDEMO": "liuqin",
	"YUDIDEMO": "yudi",
	"pipa_demo": "pipa",
	"yuechu_demo": "yuechu",
	"YUECHUDEMO": "yuechu",
	"liuqin_demo": "liuqin",
	"yudi_demo": "yudi",
	"RUBY": "ruby",
	"fuxi_ru_global": "fuxi",
	"FUXIRUGlobal": "fuxi",
	"pipa_tw_global": "pipa",
	"PIPATWGlobal": "pipa",
	"DUCHAMPTWGlobal": "duchamp",
	"duchamp_tw_global": "duchamp",
	"taoyao_eea_global": "taoyao",
	"TAOYAOEEAGlobal": "taoyao",
	"psyche": "psyche",
	"PSYCHE": "psyche",
	"ingres_global": "ingres",
	"INGRESGlobal": "ingres",
	"ingres_tw_global": "ingres",
	"INGRESTWGlobal": "ingres",
	"ingres_eea_global": "ingres",
	"INGRESEEAGlobal": "ingres",
	"sweet_k6a_global": "sweet_k6a",
	"SWEETK6AGlobal": "sweet_k6a",
	"aristotle_tw_global": "aristotle",
	"ARISTOTLETWGlobal": "aristotle",
	"cupid_eea_global": "cupid",
	"CUPIDEEAGlobal": "cupid",
	"redwood_id_global": "redwood",
	"REDWOODIDGlobal": "redwood",
	"mondrian_ru_global": "mondrian",
	"MONDRIANRUGlobal": "mondrian",
	"mondrian_tr_global": "mondrian",
	"MONDRIANTRGlobal": "mondrian",
	"corot_tr_global": "corot",
	"COROTTRGlobal": "corot",
	"ruby_global": "ruby",
	"RUBYGlobal": "ruby",
	"marble_tr_global": "marble",
	"MARBLETRGlobal": "marble",
	"pipa_in_global": "pipa",
	"PIPAINGlobal": "pipa",
	"pipa_global": "pipa",
	"PIPAGlobal": "pipa",
	"aristotle_id_global": "aristotle",
	"ARISTOTLEIDGlobal": "aristotle",
	"tapas_tr_global": "tapas",
	"TAPASTRGlobal": "tapas",
	"plato_tr_global": "plato",
	"PLATOTRGlobal": "plato",
	"earth_in_global": "earth",
	"EARTHINGlobal": "earth",
	"plato_id_global": "plato",
	"PLATOIDGlobal": "plato",
	"taoyao_id_global": "taoyao",
	"TAOYAOIDGlobal": "taoyao",
	"earth": "earth",
	"EARTH": "earth",
	"sea_ru_global": "sea",
	"SEARUGlobal": "sea",
	"vermeer_ep_stdee": "vermeer",
	"VERMEEREPSTDEE": "vermeer",
	"rock_eea_global": "rock",
	"ROCKEEAGlobal": "rock",
	"yunluo_global": "yunluo",
	"YUNLUOGlobal": "yunluo",
	"marble_tw_global": "marble",
	"MARBLETWGlobal": "marble",
	"marble_ru_global": "marble",
	"MARBLERUGlobal": "marble",
	"sunstone": "sunstone",
	"SUNSTONE": "sunstone",
	"sunstone_global": "sunstone",
	"SUNSTONEGlobal": "sunstone",
	"evergo": "evergo",
	"EVERGO": "evergo",
	"moonstone_global": "moonstone",
	"MOONSTONEGlobal": "moonstone",
	"moonstone_in_global": "moonstone",
	"MOONSTONEINGlobal": "moonstone",
	"taoyao_global": "taoyao",
	"TAOYAOGlobal": "taoyao",
	"taoyao_tr_global": "taoyao",
	"TAOYAOTRGlobal": "taoyao",
	"taoyao_tw_global": "taoyao",
	"TAOYAOTWGlobal": "taoyao",
	"xun": "xun",
	"XUN": "xun",
	"topaz_id_global": "topaz",
	"TOPAZIDGlobal": "topaz",
	"sea_tr_global": "sea",
	"SEATRGlobal": "sea",
	"mondrian_tw_global": "mondrian",
	"MONDRIANTWGlobal": "mondrian",
	"pipa_tr_global": "pipa",
	"PIPATRGlobal": "pipa",
	"pipa_ru_global": "pipa",
	"PIPARUGlobal": "pipa",
	"DUCHAMPGlobal": "duchamp",
	"duchamp_global": "duchamp",
	"DUCHAMPEEAGlobal": "duchamp",
	"duchamp_eea_global": "duchamp",
	"DUCHAMPRUGlobal": "duchamp",
	"duchamp_ru_global": "duchamp",
	"DUCHAMPINGlobal": "duchamp",
	"duchamp_in_global": "duchamp",
	"zeus_eea_global": "zeus",
	"nuwa_tw_global": "nuwa",
	"NUWATWGlobal": "nuwa",
	"ZEUSEEAGlobal": "zeus",
	"topaz_eea_global": "topaz",
	"TOPAZEEAGlobal": "topaz",
	"fire_global": "fire",
	"FIREGlobal": "fire",
	"SKY": "sky",
	"LIGHT": "light",
	"SEAEEAGlobal": "sea",
	"sea_eea_global": "sea",
	"LIGHTCM": "lightcm",
	"sunstone_eea_global": "sunstone",
	"SUNSTONEEEAGlobal": "sunstone",
	"PLATOGlobal": "plato",
	"plato_global": "plato",
	"sky": "sky",
	"yunluo": "yunluo",
	"YUNLUO": "yunluo",
	"corot_global": "corot",
	"COROTGlobal": "corot",
	"light": "light",
	"lightcm": "lightcm",
	"diting_eea_global": "diting",
	"DITINGEEAGlobal": "diting",
	"MARBLEGlobal": "marble",
	"marble_global": "marble",
	"marble_id_global": "marble",
	"MARBLEIDGlobal": "marble",
	"ARISTOTLEEEAGlobal": "aristotle",
	"aristotle_eea_global": "aristotle",
	"ARISTOTLEGlobal": "aristotle",
	"aristotle_global": "aristotle",
	"babylon_demo": "babylon",
	"BABYLONDEMO": "babylon",
	"earth_global": "earth",
	"EARTHGlobal": "earth",
	"ISHTARGlobal": "ishtar",
	"ishtar_global": "ishtar",
	"corot_eea_global": "corot",
	"COROTEEAGlobal": "corot",
	"fuxi_demo": "fuxi",
	"dagu": "dagu",
	"PIPA": "pipa",
	"YUECHU": "yuechu",
	"yuechu": "yuechu",
	"houji_ep_stdee": "houji",
	"HOUJIEPSTDEE": "houji",
	"AGATEGlobal": "agate",
	"MONDRIANGlobal": "mondrian",
	"pipa": "pipa",
	"agate_global": "agate",
	"mondrian_global": "mondrian",
	"shennong_demo": "shennong",
	"SHENNONG": "shennong",
	"SHENNONGDEMO": "shennong",
	"LIUQIN": "liuqin",
	"liuqin": "liuqin",
	"DAUMIER": "daumier",
	"MARBLEEEAGlobal": "marble",
	"SEAGlobal": "sea",
	"PLATOEEAGlobal": "plato",
	"TOPAZGlobal": "topaz",
	"FUXIEEAGlobal": "fuxi",
	"FUXIGlobal": "fuxi",
	"ISHTARTWGlobal": "ishtar",
	"ishtar_tw_global": "ishtar",
	"ishtar_ru_global": "ishtar",
	"ISHTARRUGlobal": "ishtar",
	"ISHTAREEAGlobal": "ishtar",
	"marble_eea_global": "marble",
	"sea_global": "sea",
	"plato_eea_global": "plato",
	"topaz_global": "topaz",
	"fuxi_eea_global": "fuxi",
	"fuxi_global": "fuxi",
	"ishtar_eea_global": "ishtar",
	"RUBENS": "rubens",
	"MATISSE": "matisse",
	"INGRES": "ingres",
	"DITING": "diting",
	"rubens": "rubens",
	"matisse": "matisse",
	"ingres": "ingres",
	"diting": "diting",
	"shennong": "shennong",
	"FUXIDEMO": "fuxi",
	"yudi": "yudi",
	"YUDI": "yudi",
	"FUXI": "fuxi",
	"fuxi": "fuxi",
	"nuwa": "nuwa",
	"nuwa_demo": "nuwa",
	"shennong_ep_stdee": "shennong",
	"SHENNONGEPSTDEE": "shennong",
	"MONDRIAN": "mondrian",
	"MONDRIANDEMO": "mondrian",
	"mondrian_demo": "mondrian",
	"mondrian": "mondrian",
	"VERMEER": "vermeer",
	"VERMEERDEMO": "vermeer",
	"mondrian_eea_global": "mondrian",
	"pipa_eea_global": "pipa",
	"PIPAEEAGlobal": "pipa",
	"plato_tw_global": "plato",
	"fuxi_tw_global": "fuxi",
	"FUXITWGlobal": "fuxi",
	"nuwa_ru_global": "nuwa",
	"NUWARUGlobal": "nuwa",
	"sea_tw_global": "sea",
	"SEATWGlobal": "sea",
	"PLATOTWGlobal": "plato",
	"MONDRIANEEAGlobal": "mondrian",
	"vermeer_demo": "vermeer",
	"vermeer": "vermeer",
	"NUWAINGlobal": "nuwa",
	"nuwa_in_global": "nuwa",
	"DUCHAMP": "duchamp",
	"TAPASGlobal": "tapas",
	"TAPASINGlobal": "tapas",
	"tapas_in_global": "tapas",
	"tapas_global": "tapas",
	"DUCHAMPDEMO": "duchamp",
	"duchamp_demo": "duchamp",
	"duchamp": "duchamp",
	"MANET": "manet",
	"CUPID": "cupid",
	"ZEUS": "zeus",
	"lisa":"lisa",
	"LISA":"lisa",
	"pissarro": "pissarro",
	"PISSARRO": "PISSARRO",
	"MAYFLY": "mayfly",
	"UNICORN": "unicorn",
	"THOR": "thor",
	"COROT": "corot",
	"cupid": "cupid",
	"zeus": "zeus",
	"mayfly": "mayfly",
	"unicorn": "unicorn",
	"thor": "thor",
	"nuwa_global": "nuwa",
	"NUWAGlobal": "nuwa",
	"nuwa_eea_global": "nuwa",
	"NUWAEEAGlobal": "nuwa",
	"corot": "corot",
	"MANETDEMO": "manet",
	"manet_demo": "manet",
	"manet": "manet",
	"SOCRATES": "socrates",
	"socrates": "socrates",
	"ZIZHAN": "zizhan",
	"BABYLON": "babylon",
	"babylon": "babylon",
	"zizhan": "zizhan",
	"NUWA": "nuwa",
	"NUWADEMO": "nuwa",
	"ISHTAR": "ishtar",
	"ishtar": "ishtar",
	"ISHTARDEMO": "ishtar",
	"ishtar_demo": "ishtar",
}


def localData(codename):
	if platform == "win32":
		devdata = json.loads(open("public/data/devices/"+codename+".json", 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open("/sdcard/Codes/HyperOS.fans/public/data/devices/" + codename+".json", 'r', encoding='utf-8').read())
	return devdata


def writeData(filename):
	
	if platform == "win32":
		file = open("public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
	else:
		file = open("/sdcard/Codes/HyperOS.fans/public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
	file.write(filename+"\n")
	if ".zip" in filename:
		flag = filename.split('_')[1]
	elif ".tgz" in filename:
		flag = filename.split('_images')[0]
	print("发现\t"+flag+"\t发现未收录版本")
	file.close()


def writeFlag(flag, device):
	if platform == "win32":
		file = open("public/data/scripts/Flags.json", "a", encoding='utf-8')
	else:
		file = open("/sdcard/Codes/HyperOS.fans/public/data/scripts/Flags.json", "a", encoding='utf-8')
	file.write("\""+flag+"\":\""+device+"\",\n")
	file.close()


def getDeviceCode(filename):
	if ".zip" in filename:
		flag = filename.split('_')[1]
		if flag in flags:
			codename = flags[flag]
			return codename
		else:
			writeData(filename)
			writeFlag(flag, "")
			return 0
	elif ".tgz" in filename:
		flag = filename.split('_images')[0]
		if flag in flags:
			codename = flags[flag]
			return codename
		else:
			writeData(filename)
			writeFlag(flag, "")
			return 0
	else:
		return 0


def checkExist(filename):
	if "OS" in filename:
		if "blockota" in filename:
			return "OTA ROM"
		else:
			if getDeviceCode(filename) == 0:
				writeData(filename)
				return "New ROM"
			elif filename in localData(getDeviceCode(filename)).__str__():
				return "Already Exist"
			else:
				writeData(filename)
				return "New ROM"
	else:
		return "UI Maybe"


def miui_decrypt(encrypted_response):
	decipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	decrypted = decipher.decrypt(base64.b64decode(encrypted_response))
	plaintext = decrypted.decode("utf-8").strip()
	pos = plaintext.rfind("}")
	if pos != -1:
		return json.loads(plaintext[:pos + 1])
	else:
		return json.loads(plaintext)


def miui_encrypt(json_request):
	cipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	cipher_text = cipher.encrypt(
		pad(bytes(str(json_request), encoding="ascii"), AES.block_size))
	encrypted_request = urllib.parse.quote(base64.b64encode(
		cipher_text).decode("utf-8")).replace("/", "%2F")
	return encrypted_request


HyperOSForm = {
	"obv": "OS1.0",
	"channel": "",
	"sys": "0",
	"bv": "816",
	"id": "",
	"sn": "0x0000043b716a25f1",
	"a": "0",
	"b": "F",
	"c": "14",
	"unlock": "0",
	"d": "marble",
	"lockZoneChannel": "normal",
	"f": "1",
	"ov": "OS1.0.2.0.UMRCNXM",
	"g": "9b65722a06722e8d8dffa35a9fd58586",
	"i": "14db85f96df2efc324323fa7679f0d847ff53f3bff7179ea0c778ce5d980bc03",
	"i2": "2cd7c24f21e33b236fc63f26d044227b96d8b39a80400654f88182322688793b",
	"isR": "0",
	"l": "zh_CN",
	"n": "ct",
	"p": "marble",
	"pb": "Redmi",
	"r": "CN",
	"v": "MIUI-V816.0.2.0.UMRCNXM",
	"sdk": "34",
	"pn": "marble",
	"options":
	{"zone": 1,
	 "hashId": "dae7d50f696d7403",
	 "ab": "1",
	 "previewPlan": "0",
	 "sv": 3,
	 "av": "8.4.7",
	 "cv": ""
	 }
}


MiOTAForm = {
	"a": "0",
	"b": "X",
	"c": "14",
	"unlock": "0",
	"d": "fuxi",
	"lockZoneChannel": "",
	"f": "1",
	"g": "a3e178346e97182fa11631a197801c4d",
	"channel": "",
	"i": "4178f5336815cc2a4641611c1619834817ab14bd0b4c7396a55be2f172c95a56",
	"i2": "b92243889a47bc62dc8b5fb4f50ce60c373553e4221d3ebc4b3bd9791ccaa0a7",
	"isR": "0",
	"l": "zh_CN",
	"sys": "0",
	"n": "",
	"p": "fuxi",
	"r": "CN",
	"bv": "816",
	"v": "MIUI-V14.0.23.9.12.DEV",
	"id": "",
	"sn": "0x77309938",
	"sdk": "29",
	"pn": "fuxi",
	"options": {
		"zone": 1,
		"hashId": "2371ef99a72a282c",
		"ab": "0",
		"previewPlan": "0",
		"sv": 3,
		"av": "8.2.1",
		"cv": "V14.0.23.9.12.DEV"
	}
}


def getFromApi(encrypted_data, device):
	headers = {"user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)",
			   "Connection": "Keep-Alive",
			   "Content-Type": "application/x-www-form-urlencoded",
			   "Cache-Control": "no-cache",
			   "Host": "update.miui.com",
			   "Accept-Encoding": "gzip",
			   "Content-Length": "795",
			   "Cookie": "serviceToken=;"
			   }
	data = "q=" + encrypted_data + "&s=1&t="
	response = requests.post(check_url, headers=headers, data=data)
	if "code" in response.text:
		print(json.loads(response.text))
	else:
		data = miui_decrypt(response.text.split("q=")[0])
		if "LatestRom" in data:
			package = data["LatestRom"]["filename"].split("?")[0]
			checkExist(package)
			return 1
		if "CrossRom" in data:
			package = data["CrossRom"]["filename"].split("?")[0]
			checkExist(package)
			return 1
		else:
			return 0
	response.close()


def MiFirm(url):
	options = Options()
	driver = webdriver.Edge(options=options)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	td_tags = soup.find_all("td")
	filtered_td_tags = [
		td for td in td_tags if "zip" in td.text or "tgz" in td.text]
	for tag in filtered_td_tags:
		checkExist(tag.text)


def MiFirm2(url):
	response = requests.post(url)
	if (response.status_code == 200):
		content = response.content.decode("utf8")
		if content == "":
			i = 0
		else:
			soup = BeautifulSoup(content, 'lxml')
			table_tags = soup.find_all("table", class_="firm_data")
			for tag in table_tags:
				tdtags = BeautifulSoup(str(tag), 'lxml')
				tds = tdtags.find_all("td")
				for td in tds:
					if ".tgz" in td.text or ".zip" in td.text:
						checkExist(td.text)
					else:
						i = 0


def getChangelog(encrypted_data, device):
	headers = {"user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)",
			   "Connection": "Keep-Alive",
			   "Content-Type": "application/x-www-form-urlencoded",
			   "Cache-Control": "no-cache",
			   "Host": "update.miui.com",
			   "Accept-Encoding": "gzip",
			   "Content-Length": "795",
			   "Cookie": "serviceToken=;"
			   }
	data = "q=" + encrypted_data + "&s=1&t="
	if platform == "win32":
		devdata = json.loads(
			open("public/data/devices/"+device+".json", 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open(
			"/sdcard/Codes/HyperOS.fans/public/data/devices/"+device+".json", 'r', encoding='utf-8').read())
	response = requests.post(check_url, headers=headers, data=data)
	print("\r"+"正在抓取"+devdata["name"]["zh"]+"(" +
		  devdata["codename"]+")				  ", end="")
	if "code" in response.text:
		print(json.loads(response.text)["desc"])
	else:
		data = miui_decrypt(response.text.split("q=")[0])
		if "LatestRom" in data:
			print("最新版本日志："+data["LatestRom"]["changelog"])
		if "CrossRom" in data:
			print("异常信息："+data)
		if "CurrentRom" in data:
			print("最新版本日志："+data["CurrentRom"]["changelog"])
		else:
			print("异常信息："+data)
			return 0
	response.close()


def getFastboot(url):
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
			   "Connection": "close"}
	response = requests.post(url, headers=headers)
	if (response.status_code == 200):
		content = response.content.decode("utf8")
		if content == "":
			i = 0
		else:
			data = json.loads(content)["LatestFullRom"]
			if len(data) > 0:
				checkExist(data["filename"])
			else:
				i = 0
	else:
		i = 0
	response.close()
