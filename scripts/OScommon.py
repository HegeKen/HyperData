import json
from sys import platform
import urllib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pymysql import Connection
import config

sdk = {
	"16.0": "36",
	"16": "36",
	"15": "35",
	"15.0": "35",
	"14": "34",
	"14.0": "34",
	"13.0": "33",
	"13": "33",
	"12": "31",
	"12.0": "31",
	"11": "30",
	"11.0": "30",
	"10": "29",
	"10.0": "29",
	"9": "28",
	"9.0": "28",
	"8.1": "27",
	"8": "26",
	"8.0": "26",
	"7.1": "25",
	"7": "24",
	"7.0": "24",
	"6": "23",
	"6.0": "23",
	"5.1": "22",
	"5": "21",
	"5.0": "21",
	"4.4": "19",
	"4.3": "18",
	"4.2": "17",
	"4.1": "16",
	"4": "14",
	"4.0": "14",
	"2.3.6": "10",
	"2.3.5": "10",
	"2.3": "9",
	"2": "9",
	"2.0": "9"
}

def android(ver):
	if ver == "16.0":
		return "W"
	if ver == "15.0":
		return "V"
	elif ver == "14.0":
		return "U"
	elif ver == "13.0":
		return "T"
	elif ver == "12.0":
		return "S"
	elif ver == "11.0":
		return "R"
	elif ver == "10.0":
		return "Q"
	elif ver == "9.0":
		return "P"
	elif ver == "8.1":
		return "O"
	elif ver == "8.0":
		return "O"
	elif ver == "7.1":
		return "N"
	elif ver == "7.0":
		return "N"
	elif ver == "6.0":
		return "M"
	elif ver == "5.1":
		return "L"
	elif ver == "5.0":
		return "L"
	elif ver == "4.4":
		return "K"
	elif ver == "4.3":
		return "J"
	elif ver == "4.2":
		return "J"
	elif ver == "4.1":
		return "J"
	elif ver == "4.0":
		return "I"
	else:
		return "W"

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"


unreleased = ['coral', 'nezha', 'tornado']
currentStable = ['annibale', 'myron', 'pudding', 'pandora', 'popsicle', 'piano', 'yupei', 'tornado', 'goya', 'klimt', 'flute', 'organ', 'konghou', 'dew', 'spring', 'lapis', 'kunzite', 'coral', 'flourite', 'creek', 'taiko', 'bixi', 'dali', 'turner', 'violin', 'koto', 'dijun', 'jinghu', 'luming', 
								 'onyx', 'serenity', 'emerald_r', 'miro', 'zorn', 'xuanyuan', 'tanzanite', 'obsidian', 'rodin', 'warm', 'dada', 'haotian', 'uke', 'muyu', 
								 'beryl', 'amethyst', 'malachite', 'degas', 'rothko', 'flame', 'lake', 'flare', 'spark', 
								 'ruyi', 'goku', 'agate', 'air', 'alioth', 'ares', 'aristotle', 'aurora', 'babylon', 'breeze', 'cas',
								 'cetus', 'chenfeng', 'cmi', 'corot', 'cupid', 'dagu', 'daumier', 'diting', 'dizi',
								 'duchamp', 'earth', 'elish', 'emerald', 'enuma', 'evergo', 'evergreen', 'fire', 'fleur', 'fuxi',
								 'gale', 'garnet', 'gold', 'haydn', 'houji', 'ingres', 'ishtar', 'light', 'lightcm',
								 'lisa', 'liuqin', 'manet', 'marble', 'matisse', 'mayfly', 'mona', 'mondrian', 'moon', 'moonstone',
								 'munch', 'nabu', 'nuwa', 'odin', 'opal', 'pearl', 'peridot', 'pipa', 'pissarro', 'pissarro_in', 'plato',
								 'psyche', 'redwood', 'rembrandt', 'rock', 'ruan', 'rubens', 'ruby', 'sapphire',
								 'sapphiren', 'sea', 'sheng', 'shennong_t', 'shennong', 'sky', 'socrates', 'spes', 'spesn', 'star',
								 'sunstone', 'sweet_k6a', 'taoyao', 'tapas', 'thor', 'thyme', 'topaz', 'umi', 'unicorn',
								 'venus', 'vermeer', 'veux', 'vida', 'vili', 'viva', 'xaga', 'xun', 'yudi', 'yuechu', 'yunluo',
								 'zeus', 'zijin', 'zircon', 'ziyi', 'zizhan']

only_os = ['dali', 'turner', 'violin', 'koto', 'taiko', 'jinghu', 'luming', 'poussin', 'citrine', 'serenity', 'emerald_r', 'xuanyuan', 'dijun', 'tanzanite', 'rodin', 'warm', 'onyx', 'miro', 'zorn', 
					 'uke', 'muyu',	'dada', 'haotian', 'obsidian', 'beryl', 'amethyst', 'malachite', 'rothko', 'degas',
					 'flame', 'lake','spring', 'flare', 'spark', 'goku', 'ruyi', 'moon', 'breeze', 'vermeer', 'ruan',
					 'dizi', 'peridot', 'aurora', 'chenfeng', 'duchamp', 'houji', 'manet', 'sheng', 'shennong', 'shennong_t']

cn_devices = ['sheng', 'ziyi', 'cetus', 'lisa', 'pissarro', 'ruyi', 'babylon', 'dagu', 'daumier', 'garnet', 'gold', 'houji', 'lightcm', 'liuqin', 'manet', 'matisse', 'mayfly', 'psyche', 'rubens', 'shennong', 'socrates', 'thor', 'unicorn', 'vermeer', 'xun', 'yudi', 'yuechu', 'zircon', 'zizhan']
gb_devices = ['agate', 'aristotle', 'fire', 'moonstone', 'plato', 'rock', 'sea', 'sunstone', 'sweet_k6a', 'taoyao', 'tapas', 'topaz']
both_regions = ['aurora', 'corot', 'cupid', 'diting', 'duchamp', 'earth', 'fuxi', 'ingres', 'ishtar', 'light', 'marble', 'mondrian', 'nuwa', 'pipa', 'redwood', 'ruby', 'sky', 'yunluo', 'zeus']

order = ['umi', 'cmi', 'cas', 'thyme', 'venus', 'star', 'lisa', 'pissarro_in', 'agate', 'vili', 'cupid', 'zeus', 'psyche',
				 'daumier', 'taoyao', 'mayfly', 'unicorn', 'thor', 'plato', 'fuxi', 'nuwa', 'ishtar', 'aristotle',
				 'houji', 'shennong', 'shennong_t', 'aurora', 'degas', 'dada', 'haotian','xuanyuan', 'dijun', 'goya', 'klimt', 'pudding', 'pandora', 'popsicle',
				 'nabu', 'enuma', 'elish', 'dagu', 'pipa',
				 'liuqin', 'yudi','sheng', 'uke', 'muyu', 'jinghu', 'violin', 'piano', 'yupei', 'odin', 'cetus', 'zizhan', 'babylon', 'goku', 'ruyi', 'bixi', 'mona',
				 'zijin', 'ziyi', 'yuechu', 'chenfeng', 'luming','konghou',
				 'fire', 'earth', 'sky', 'gale', 'moon', 'air', 'lake', 'flame', 'creek', 'dew', 'tornado', 'spring', 'evergo', 'light', 'lightcm', 'veux', 'xaga', 'pissarro',
				 'spes', 'spesn', 'viva', 'vida', 'fleur', 'opal', 'sunstone', 'ruby', 'redwood', 'pearl', 'marble', 'tapas', 'topaz',
				 'sweet_k6a', 'sea', 'gold', 'breeze', 'garnet', 'emerald', 'zircon', 'tanzanite', 'obsidian', 'beryl', 'malachite', 'amethyst', 'sapphire', 'sapphiren', 'emerald_r', 'kunzite', 'lapis', 'coral', 'flourite', 'peridot', 'rodin','onyx', 'alioth',
				 'haydn', 'ares', 'munch', 'rubens', 'matisse', 'ingres', 'diting', 'rembrandt', 'mondrian', 'socrates', 'corot', 'duchamp',
				 'vermeer', 'manet', 'rothko', 'zorn', 'miro', 'dali','annibale', 'myron', 
				 'yunluo', 'xun', 'flare', 'spark', 'koto', 'taiko', 'dizi', 'ruan', 'turner', 'warm', 'serenity', 'evergreen', 'rock', 'moonstone']

branches = [
	{
		"code": "",
		"tag": "CNXM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_demo",
		"tag": "CNDM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_tw_global",
		"tag": "TWXM",
		"region": "tw",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_global",
		"tag": "MIXM",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_dc_global",
		"tag": "MIDC",
		"region": "global",
		"carrier": ["dc"],
		"zone": "2"
	},
	{
		"code": "_eea_global",
		"tag": "EUXM",
		"region": "eea",
		"carrier": [""],
		"zone": "2"
	},
		{
		"code": "_eea_global",
		"tag": "EUDM",
		"region": "eea",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_ru_global",
		"tag": "RUXM",
		"region": "ru",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_id_global",
		"tag": "IDXM",
		"region": "id",
		"carrier": [""],
		"zone": "2"
	},
		{
		"code": "_id_global",
		"tag": "IDDM",
		"region": "id",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_tr_global",
		"tag": "TRXM",
		"region": "tr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_jp_global",
		"tag": "JPXM",
		"region": "jp",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_in_global",
		"tag": "INXM",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
		{
		"code": "in_in_global",
		"tag": "INXM",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_eea_hg_global",
		"tag": "EUHG",
		"region": "eea",
		"carrier": ["h3g"],
		"zone": "2"
	},
	{
		"code": "_eea_or_global",
		"tag": "EUOR",
		"region": "eea",
		"carrier": ["orange"],
		"zone": "2"
	},
	{
		"code": "_eea_vf_global",
		"tag": "EUVF",
		"region": "eea",
		"carrier": ["vodafone"],
		"zone": "2"
	},
	{
		"code": "_eea_ti_global",
		"tag": "EUTI",
		"region": "eea",
		"carrier": ["tim"],
		"zone": "2"
	},
	{
		"code": "_eea_sf_global",
		"tag": "EUSF",
		"region": "eea",
		"carrier": ["sfr"],
		"zone": "2"
	},
	{
		"code": "_eea_tf_global",
		"tag": "EUTF",
		"region": "eea",
		"carrier": ["tf"],
		"zone": "2"
	},
	{
		"code": "_eea_by_global",
		"tag": "EUBY",
		"region": "eea",
		"carrier": ["by"],
		"zone": "2"
	},
	{
		"code": "_cl_en_global",
		"tag": "CLEN",
		"region": "cl",
		"carrier": ["en"],
		"zone": "2"
	},
	{
		"code": "_mx_at_global",
		"tag": "MXAT",
		"region": "mx",
		"carrier": ["at"],
		"zone": "2"
	},
	{
		"code": "_lm_cr_global",
		"tag": "LMCR",
		"region": "lm",
		"carrier": ["cr"],
		"zone": "2"
	},
	{
		"code": "_za_vc_global",
		"tag": "ZAVC",
		"region": "za",
		"carrier": ["vc"],
		"zone": "2"
	},
	{
		"code": "_za_mt_global",
		"tag": "ZAMT",
		"region": "za",
		"carrier": ["mt"],
		"zone": "2"
	},
	{
		"code": "_gt_tg_global",
		"tag": "GTTG",
		"region": "gt",
		"carrier": ["tg"],
		"zone": "2"
	},
	{
		"code": "_lm_ms_global",
		"tag": "LMMS",
		"region": "lm",
		"carrier": ["movistar"],
		"zone": "2"
	},
	{
		"code": "_eea_vf_global",
		"tag": "EUTF",
		"region": "eea",
		"carrier": ["tf"],
		"zone": "2"
	},
	{
		"code": "_th_as_global",
		"tag": "THAS",
		"region": "th",
		"carrier": ["as"],
		"zone": "2"
	},
	{
		"code": "_cl_en_global",
		"tag": "LMCR",
		"region": "lm",
		"carrier": ["cr"],
		"zone": "2"
	},
	{
		"code": "_in_fk_global",
		"tag": "INFK",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_kr_global",
		"tag": "KRXM",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_eea_global",
		"tag": "EUHG",
		"region": "eea",
		"carrier": ["h3g"],
		"zone": "2"
	}
]

flags = {
	"HOUJI": "houji",
	"HOUJIDEMO": "houji",
	"houji": "houji",
	"flourite_demo": "flourite",
	"flourite": "flourite",
	"houji_demo": "houji",
	"houji_global": "houji",
	"HOUJIGlobal": "houji",
	"myron": "myron",
	"myron_demo": "myron",
	"annibale": "annibale",
	"annibale_demo": "annibale",
	"houji_in_global": "houji",
	"HOUJIINGlobal": "houji",
	"houji_id_global": "houji",
	"HOUJIIDGlobal": "houji",
	"houji_tw_global": "houji",
	"HOUJITWGlobal": "houji",
	"pudding": "pudding",
	"pudding_demo": "pudding",
	"popsicle": "popsicle",
	"popsicle_demo": "popsicle",
	"pandora": "pandora",
	"pandora_demo": "pandora",
	"houji_tr_global": "houji",
	"HOUJITRGlobal": "houji",
	"RUYITWGlobal":"ruyi",
	"ruan_ep_stdee":"ruan",
	"RUANEPSTDEE": "ruan",
	"taiko_demo":"taiko",
	"taiko":"taiko",
	"taiko_ru_global": "taiko",
	"koto_ru_global": "koto",
	"AMETHYSTTRGlobal":"amethyst",
	"amethyst_tr_global":"amethyst",
	"EARTHEPSTDEE":"earth",
	"earth_ep_stdee":"earth",
	"warm_in_global":"warm",
	"WARMINGlobal":"warm",
	"SERENITYGlobal": "serenity",
	"serenity_global": "serenity",
	"MALACHITEIDGlobal":"malachite",
	"malachite_id_global":"malachite",
	"kunzite": "kunzite",
	"kunzite_demo": "kunzite",
	"lapis": "lapis",
	"klimt_jp_global": "klimt",
	"goya_global": "goya",
	"goya_id_global": "goya",
	"goya_eea_global": "goya",
	"goya_ru_global": "goya",
	"goya_tr_global": "goya",
	"klimt_global": "klimt",
	"klimt_eea_global": "klimt",
	"klimt_id_global": "klimt",
	"klimt_ru_global": "klimt",
	"klimt_tw_global": "klimt",
	"klimt_tr_global": "klimt",
	"klimt_mx_at_global": "klimt",
	"klimt_lm_cr_global": "klimt",
	"turner_tw_global": "turner",
	"dew_lm_cr_global": "dew",
	"tornado_tr_global": "tornado",
	"tornado_lm_cr_global": "tornado",
	"turner_global": "turner",
	"flute_eea_global": "flute",
	"goya_tw_global": "goya",
	"goya_dc_global": "goya",
	"goya_lm_cr_global": "goya",
	"flute_tw_global": "flute",
	"flute_ru_global": "flute",
	"flute_tr_global": "flute",
	"klimt_dc_global": "klimt",
	"goya_mx_at_global": "goya",
	"flute_global": "flute",
	"lapis_demo": "lapis",
	"tanzanite_tw_global": "tanzanite",
	"TANZANITETWGlobal": "tanzanite",
	"TANZANITERUGlobal":"tanzanite",
	"tanzanite_ru_global":"tanzanite",
	"OBSIDIANLMCRGlobal":"obsidian",
	"obsidian_lm_cr_global":"obsidian",
	"amethyst_in_global":"amethyst",
	"AMETHYSTINGlobal":"amethyst",
	"AMETHYSTEEAGlobal":"amethyst",
	"amethyst_eea_global": "amethyst",
	"AMETHYSTTWGlobal":"amethyst",
	"amethyst_tw_global":"amethyst",
	"AMETHYSTIDGlobal":"amethyst",
	"xuanyuan":"xuanyuan",
	"creek_global": "creek",
	"spring_in_global": "spring",
	"creek_ru_global": "creek",
	"creek_id_global": "creek",
	"violin": "violin",
	"dali_demo": "dali",
	"dali": "dali",
	"KONGHOU": "konghou",
	"konghou": "konghou",
	"tornado_global": "tornado",
	"tornado_dc_global": "tornado",
	"tornado_eea_global": "tornado",
	"tornado": "tornado",
	"tornado_demo": "tornado",
	"creek_lm_cr_global": "creek",
	"creek_eea_global": "creek",
	"spring_eea_global": "spring",
	"spring_global": "spring",
	"malachite_gt_tg_global": "malachite",
	"piano": "piano",
	"piano_demo": "piano",
	"yupei": "yupei",
	"yupei_demo": "yupei",
	"turner_demo":"turner",
	"turner": "turner",
	"onyx_tw_global": "onyx",
	"onyx_ru_global": "onyx",
	"onyx_id_global": "onyx",
	"beryl_demo": "beryl",
	"onyx_eea_global": "onyx",
	"onyx_in_global": "onyx",
	"bixi": "bixi",
	"bixi_demo": "bixi",
	"dew_tw_global": "dew",
	"dew_global": "dew",
	"dew_dc_global": "dew",
	"dew_eea_global": "dew",
	"dew_ru_global": "dew",
	"dew_id_global": "dew",
	"dew_tr_global": "dew",
	"spring": "spring",
	"SERENITYDCGlobal": "serenity",
	"serenity_dc_global": "serenity",
	"xuanyuan_demo":"xuanyuan",
	"xuanyuan_in_global":"xuanyuan",
	"emerald_r_eea_global":"emerald_r",
	"EMERALDREEAGlobal":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"EMERALDRTRGlobal":"emerald_r",
	"emerald_r_tr_global":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"emerald_r_global":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"amethyst_id_global":"amethyst",
	"amethyst_ru_global":"amethyst",
	"AMETHYSTRUGlobal":"amethyst",
	"AMETHYSTGlobal":"amethyst",
	"amethyst_global":"amethyst",
	"AMETHYSTDCGlobal":"amethyst",
	"violin_demo": "violin",
	"koto_in_global": "koto",
	"amethyst_dc_global":"amethyst",
	"amethyst_demo":"amethyst",
	"AMETHYSTDEMO":"amethyst",
	"amethyst":"amethyst",
	"AMETHYST":"amethyst",
	"dijun":"dijun",
	"dijun_demo":"dijun",
	"jinghu":"jinghu",
	"jinghu_demo":"jinghu",
	"luming":"luming",
	"luming_demo":"luming",
	"earth_eea_sf_global":"earth",
	"EARTHEEASFGlobal":"earth",
	"ruyi_tw_global":"ruyi",
	"garnet_global": "garnet",
	"STAREEAGlobal":"star",
	"earth_cl_en_global":"earth",
	"EARTHCLENGlobal":"earth",
	"MOONTRGlobal":"moon",
	"moon_tr_global":"moon",
	"rodin_id_global":"rodin",
	"goku_ep_stdee":"goku",
	"pond_global":"pond",
	"flame":"flame",
	"FLAME":"flame",
	"flame_demo":"flame",
	"FLAMEDEMO":"flame",
	"lake_ru_global":"lake",
	"LAKERUGlobal":"lake",
	"uke_demo":"uke",
	"muyu_id_global":"muyu",
	"muyu_ru_global":"muyu",
	"muyu_tr_global":"muyu",
	"muyu_tw_global":"muyu",
	"muyu_eea_global":"muyu",
	"muyu_global":"muyu",
	"uke_id_global":"uke",
	"uke_ru_global":"uke",
	"uke_tw_global":"uke",
	"uke_eea_global":"uke",
	"uke_global":"uke",
	"xuanyuan_tw_global":"xuanyuan",
	"xuanyuan_global":"xuanyuan",
	"xuanyuan_dc_global":"xuanyuan",
	"xuanyuan_eea_global":"xuanyuan",
	"xuanyuan_ru_global":"xuanyuan",
	"xuanyuan_id_global":"xuanyuan",
	"xuanyuan_tr_global":"xuanyuan",
	"dada_tw_global":"dada",
	"dada_global":"dada",
	"dada_dc_global":"dada",
	"dada_eea_global":"dada",
	"dada_ru_global":"dada",
	"dada_in_global":"dada",
	"dada_id_global":"dada",
	"dada_lm_cr_global":"dada",
	"uke_tr_global":"uke",
	"muyu_demo":"muyu",
	"beryl_ep_stdee":"beryl",
	"BERYLEPSTDEE":"beryl",
	"dada":"dada",
	"haotian":"haotian",
	"rothko_jp_global":"rothko",
	"ROTHKOJPGlobal":"rothko",
	"SERENITYINGlobal":"serenity",
	"serenity_in_global":"serenity",
	"SERENITYGTTGGlobal":"serenity",
	"creek_tw_global": "creek",
	"serenity_gt_tg_global":"serenity",
	"BERYLGTTGGlobal":"beryl",
	"beryl_gt_tg_global":"beryl",
	"malachite_tw_global":"malachite",
	"MALACHITETWGlobal":"malachite",
	"malachite_tw_global":"malachite",
	"malachite_global":"malachite",
	"MALACHITEGlobal":"malachite",
	"malachite_global":"malachite",
	"malachite_eea_global":"malachite",
	"MALACHITEEEAGlobal":"malachite",
	"malachite_eea_global":"malachite",
	"MALACHITEDCGlobal":"malachite",
	"malachite_dc_global":"malachite",
	"tanzanite_dc_global":"tanzanite",
	"TANZANITEDCGlobal":"tanzanite",
	"tanzanite_global":"tanzanite",
	"TANZANITEGlobal":"tanzanite",
	"cupid_cl_en_global":"cupid",
	"CUPIDCLENGlobal":"cupid",
	"garnet_dc_global":"garnet",
	"GARNETDCGlobal":"garnet",
	"SERENITYEEAGlobal":"serenity",
	"serenity_eea_global":"serenity",
	"moon_cl_en_global":"moon",
	"MOONLMCRGlobal":"moon",
	"sky_lm_cr_global":"sky",
	"SKYLMCRGlobal":"sky",
	"moon_lm_cr_global":"moon",
	"MOONLMCRGlobal":"moon",
	"tapas_lm_ms_global":"tapas",
	"SERENITYEEASFGlobal": "serenity",
	"serenity_eea_sf_global": "serenity",
	"lake_dc_global":"lake",
	"LAKEDCGlobal":"lake",
	"zorn_demo":"zorn",
	"uke":"uke",
	"zorn": "zorn",
	"ZORN": "zorn",
	"miro": "miro",
	"MIRO": "miro",
	"rodin": "rodin",
	"RODIN": "rodin",
	"rodin_demo":"rodin",
	"muyu":"muyu",
	"viva_lm_ms_global":"viva",
	"VIVALMMSGlobal":"viva",
	"SPESLMMSGlobal":"spes",
	"fleur_lm_ms_global":"fleur",
	"FLEURLMMSGlobal":"fleur",
	"spes_lm_ms_global":"spes",
	"agate_mx_at_global":"agate",
	"agate_mx_at_global":"agate",
	"agate_cl_en_global":"agate",
	"AGATECLENGlobal":"agate",
	"agate_cl_en_global":"agate",
	"CUPIDMXATGlobal":"cupid",
	"fleur_eea_by_global":"fleur",
	"FLEUREEABYGlobal":"fleur",
	"cupid_mx_at_global":"cupid",
	"diting_lm_cr_global":"diting",
	"diting_lm_cr_global":"diting",
	"earth_lm_ms_global":"earth",
	"earth_lm_ms_global":"earth",
	"earth_mx_at_global":"earth",
	"earth_mx_at_global":"earth",
	"earth_lm_cr_global":"earth",
	"earth_lm_cr_global":"earth",
	"fleur_cl_en_global":"fleur",
	"fleur_cl_en_global":"fleur",
	"light_lm_cr_global":"light",
	"light_lm_cr_global":"light",
	"lisa_mx_at_global":"lisa",
	"lisa_mx_at_global":"lisa",
	"lisa_cl_en_global":"lisa",
	"lisa_cl_en_global":"lisa",
	"opal_cl_en_global":"opal",
	"opal_cl_en_global":"opal",
	"plato_lm_cr_global":"plato",
	"plato_lm_cr_global":"plato",
	"ruby_lm_ms_global":"ruby",
	"ruby_lm_ms_global":"ruby",
	"ruby_cl_en_global":"ruby",
	"ruby_cl_en_global":"ruby",
	"ruby_lm_cr_global":"ruby",
	"ruby_lm_cr_global":"ruby",
	"spes_cl_en_global":"spes",
	"spes_cl_en_global":"spes",
	"taoyao_cl_en_global":"taoyao",
	"taoyao_cl_en_global":"taoyao",
	"veux_mx_at_global":"veux",
	"veux_mx_at_global":"veux",
	"vili_mx_at_global":"vili",
	"VILIMXATGlobal":"vili",
	"vili_mx_at_global":"vili",
	"vili_cl_en_global":"vili",
	"VILICLENGlobal":"vili",
	"vili_cl_en_global":"vili",
	"AGATEMXATGlobal":"agate",
	"DITINGLMCRGlobal":"diting",
	"DITINGLMCRGlobal":"diting",
	"DITINGLMCRGlobal":"diting",
	"EARTHLMMSGlobal":"earth",
	"EARTHLMMSGlobal":"earth",
	"EARTHMXATGlobal":"earth",
	"EARTHLMCRGlobal":"earth",
	"EARTHLMCRGlobal":"earth",
	"EARTHLMCRGlobal":"earth",
	"EARTHLMCRGlobal":"earth",
	"FLEURCLENGlobal":"fleur",
	"LIGHTLMCRGlobal":"light",
	"LISAMXATGlobal":"lisa",
	"LISACLENGlobal":"lisa",
	"OPALCLENGlobal":"opal",
	"PLATOLMCRGlobal":"plato",
	"RUBYLMMSGlobal":"ruby",
	"RUBYCLENGlobal":"ruby",
	"RUBYLMCRGlobal":"ruby",
	"SPESCLENGlobal":"spes",
	"TAOYAOCLENGlobal":"taoyao",
	"VEUXMXATGlobal":"veux",
	"veux_cl_en_global":"veux",
	"VEUXCLENGlobal":"veux",
	"veux_cl_en_global":"veux",
	"ruyi_ru_global":"ruyi",
	"RUYIRUGlobal": "ruyi",
	"opal_eea_by_global":"opal",
	"OPALEEABYGlobal":"opal",
	"veux_eea_by_global":"veux",
	"VEUXEEABYGlobal":"veux",
	"FLARETRGlobal":"flare",
	"flare_tr_global":"flare",
	"rothko_eea_global":"rothko",
	"ROTHKOEEAGlobal":"rothko",
	"rothko_global":"rothko",
	"rothko_ru_global":"rothko",
	"rothko_id_global":"rothko",
	"ROTHKOGlobal":"rothko",
	"ROTHKORUGlobal":"rothko",
	"ROTHKOIDGlobal":"rothko",
	"degas_global":"degas",
	"degas_eea_global":"degas",
	"DEGASGlobal":"degas",
	"DEGASEEAGlobal":"degas",
	"degas_id_global": "degas",
	"DEGASIDGlobal": "degas",
	"degas_tr_global":"degas",
	"DEGASTRGlobal":"degas",
	"rothko_ep_stdee":"rothko",
	"ROTHKOEPSTDEE":"rothko",
	"dew_gt_tg_global": "dew",
	"organ_eea_global": "organ",
	"spring_gt_tg_global": "spring",
	"creek_dc_global": "creek",
	"flute_id_global": "flute",
	"organ_global": "organ",
	"organ_tw_global": "organ",
	"creek_mx_at_global": "creek",
	"creek_tr_global": "creek",
	"spesn_eea_by_global":"spesn",
	"SPESNEEABYGlobal":"spesn",
	"lake_id_global":"lake",
	"LAKEIDGlobal":"lake",
	"malachite":"malachite",
	"malachite_demo":"malachite",
	"degas_ru_global":"degas",
	"DEGASRUGlobal":"degas",
	"rothko_tw_global":"rothko",
	"ROTHKOTWGlobal":"rothko",
	"degas_tw_global":"degas",
	"DEGASTWGlobal":"degas",
	"lake_tw_global":"lake",
	"LAKETWGlobal":"lake",
	"MALACHITE":"malachite",
	"MALACHITEDEMO":"malachite",
	"ruyi_eea_global":"ruyi",
	"RUYIEEAGlobal":"ruyi",
	"rothko_tr_global": "rothko",
	"ROTHKOTRGlobal": "rothko",
	"degas_lm_cr_global":"degas",
	"DEGASLMCRGlobal":"degas",
	"degas_mx_at_global":"degas",
	"DEGASMXATGlobal":"degas",
	"rothko_lm_cr_global":"rothko",
	"ROTHKOLMCRGlobal":"rothko",
	"lake_lm_cr_global":"lake",
	"LAKELMCRGlobal":"lake",
	"lake_gt_tg_global":"lake",
	"LAKEGTTGGlobal":"lake",
	"lake_mx_at_global":"lake",
	"LAKEMXATGlobal":"lake",
	"air_lm_cr_global":"air",
	"AIRLMCRGlobal":"air",
	"air_dc_global":"air",
	"AIRDCGlobal":"air",
	"aristotle_lm_cr_global":"aristotle",
	"ARISTOTLELMCRGlobal":"aristotle",
	"aristotle_dc_global":"aristotle",
	"ARISTOTLEDCGlobal":"aristotle",
	"aristotle_cl_en_global":"aristotle",
	"ARISTOTLECLENGlobal":"aristotle",
	"uke_in_global":"uke",
	"MALACHITEMXATGlobal":"malachite",
	"malachite_lm_cr_global":"malachite",
	"malachite_mx_at_global":"malachite",
	"MALACHITELMCRGlobal":"malachite",
	"obsidian_eea_global":"obsidian",
	"obsidian_global":"obsidian",
	"obsidian_dc_global":"obsidian",
	"OBSIDIANGlobal":"obsidian",
	"OBSIDIANDCGlobal":"obsidian",
	"OBSIDIANEEAGlobal":"obsidian",
	"obsidian_ru_global":"obsidian",
	"obsidian_tr_global":"obsidian",
	"OBSIDIANRUGlobal":"obsidian",
	"OBSIDIANTRGlobal":"obsidian",
	"rodin_in_global":"rodin",
	"aristotle_mx_at_global":"aristotle",
	"ARISTOTLEMXATGlobal":"aristotle",
	"emerald_lm_cr_global":"emerald",
	"EMERALDLMCRGlobal":"emerald",
	"emerald_dc_global":"emerald",
	"EMERALDDCGlobal":"emerald",
	"emerald_mx_at_global":"emerald",
	"EMERALDMXATGlobal":"emerald",
	"fire_lm_cr_global":"fire",
	"FIRELMCRGlobal":"fire",
	"fire_dc_global":"fire",
	"FIREDCGlobal":"fire",
	"fire_za_vc_global":"fire",
	"FIREZAVCGlobal":"fire",
	"fire_za_mt_global":"fire",
	"FIREZAMTGlobal":"fire",
	"fire_mx_at_global":"fire",
	"FIREMXATGlobal":"fire",
	"fire_gt_tg_global":"fire",
	"FIREGTTGGlobal":"fire",
	"gale_lm_cr_global":"gale",
	"GALELMCRGlobal":"gale",
	"gale_dc_global":"gale",
	"GALEDCGlobal":"gale",
	"gale_mx_at_global":"gale",
	"GALEMXATGlobal":"gale",
	"gale_gt_tg_global":"gale",
	"GALEGTTGGlobal":"gale",
	"garnet_lm_cr_global":"garnet",
	"GARNETLMCRGlobal":"garnet",
	"gold_lm_cr_global":"gold",
	"GOLDLMCRGlobal":"gold",
	"gold_dc_global":"gold",
	"GOLDDCGlobal":"gold",
	"gold_gt_tg_global":"gold",
	"GOLDGTTGGlobal":"gold",
	"light_cl_en_global":"light",
	"LIGHTCLENGlobal":"light",
	"moon_mx_at_global":"moon",
	"MOONMXATGlobal":"moon",
	"moon_dc_global":"moon",
	"MOONDCGlobal":"moon",
	"moon_gt_tg_global":"moon",
	"MOONGTTGGlobal":"moon",
	"sapphire_lm_cr_global":"sapphire",
	"SAPPHIRELMCRGlobal":"sapphire",
	"sapphire_dc_global":"sapphire",
	"SAPPHIREDCGlobal":"sapphire",
	"sapphire_mx_at_global":"sapphire",
	"SAPPHIREMXATGlobal":"sapphire",
	"sapphiren_dc_global":"sapphiren",
	"SAPPHIRENDCGlobal":"sapphiren",
	"sea_lm_ms_global":"sea",
	"SEALMMSGlobal":"sea",
	"sea_dc_global":"sea",
	"SEADCGlobal":"sea",
	"sea_gt_tg_global":"sea",
	"SEAGTTGGlobal":"sea",
	"sea_cl_en_global":"sea",
	"SEACLENGlobal":"sea",
	"sea_mx_at_global":"sea",
	"SEAMXATGlobal":"sea",
	"sea_lm_cr_global":"sea",
	"SEALMCRGlobal":"sea",
	"sky_cl_en_global":"sky",
	"SKYCLENGlobal":"sky",
	"sky_dc_global":"sky",
	"SKYDCGlobal":"sky",
	"taoyao_lm_cr_global":"taoyao",
	"TAOYAOLMCRGlobal":"taoyao",
	"beryl_in_global":"beryl",
	"BERYLINGlobal":"beryl",
	"malachite_in_global":"malachite",
	"MALACHITEINGlobal":"malachite",
	"TAPASLMMSGlobal":"tapas",
	"tapas_gt_tg_global":"tapas",
	"TAPASGTTGGlobal":"tapas",
	"tapas_cl_en_global":"tapas",
	"TAPASCLENGlobal":"tapas",
	"tapas_mx_at_global":"tapas",
	"TAPASMXATGlobal":"tapas",
	"tapas_lm_cr_global":"tapas",
	"TAPASLMCRGlobal":"tapas",
	"topaz_za_mt_global":"topaz",
	"TOPAZZAMTGlobal":"topaz",
	"topaz_za_vc_global":"topaz",
	"TOPAZZAVCGlobal":"topaz",
	"zircon_lm_cr_global":"zircon",
	"ZIRCONLMCRGlobal":"zircon",
	"zircon_dc_global":"zircon",
	"ZIRCONDCGlobal":"zircon",
	"beryl":"beryl",
	"BERYL":"beryl",
	"taiko_tw_global": "taiko",
	"taiko_global": "taiko",
	"koto_global": "koto",
	"koto_tw_global": "koto",
	"koto_eea_global": "koto",
	"taiko_eea_global": "taiko",
	"taiko_in_global": "taiko",
	"DEGASDCGlobal":"degas",
	"ROTHKODCGlobal":"rothko",
	"degas_dc_global": "degas",
	"rothko_dc_global": "rothko",
	"lake_eea_global":"lake",
	"LAKEEEAGlobal":"lake",
	"flare_ru_global":"flare",
	"spark_ru_global":"spark",
	"FLARERUGlobal":"flare",
	"SPARKRUGlobal":"spark",
	"PONDGlobal":"pond",
	"ruyi_ep_stdee":"ruyi",
	"GOKUEPSTDEE":"goku",
	"RUYIEPSTDEE":"ruyi",
	"fleur_eea_or_global":"fleur",
	"FLEUREEAORGlobal":"fleur",
	"flare_eea_global":"flare",
	"flare_global":"flare",
	"SPARKGlobal":"spark",
	"SPARKEEAGlobal":"spark",
	"FLAREGlobal":"flare",
	"FLAREEEAGlobal":"flare",
	"lake_global":"lake",
	"LAKEGlobal":"lake",
	"spark_global":"spark",
	"spark_eea_global":"spark",
	"spark_tw_global": "spark",
	"SPARKTWGlobal" : "spark",
	"flare_tw_global": "flare",
	"FLARETWGlobal": "flare",
	"spesn_za_mt_global":"spesn",
	"SPESNZAMTGlobal":"spesn",
	"VILIJPGlobal":"vili",
	"spesn_eea_vf_global":"spesn",
	"SPESNEEAVFGlobal":"spesn",
	"spesn_eea_or_global":"spesn",
	"SPESNEEAORGlobal":"spesn",
	"spes_mx_at_global":"spes",
	"SPESMXATGlobal":"spes",
	"GARNETEPCJCC": "garnet",
	"garnet_ep_cjcc": "garnet",
	"air_tw_global":"air",
	"AIRTWGlobal":"air",
	"vili_jp_global":"vili",
	"viva_za_mt_global":"viva",
	"VIVAZAMTGlobal":"viva",
	"star_eea_global":"star",
	"PERIDOTTWGlobal":"peridot",
	"peridot_tw_global":"peridot",
	"klein_demo":"klein",
	"klein":"klein",
	"air_in_global":"air",
	"AIRINGlobal":"air",
	"ruan_in_global":"ruan",
	"RUANINGlobal":"ruan",
	"RUANEEAGlobal":"ruan",
	"ruan_eea_global":"ruan",
	"ruan_ru_global":"ruan",
	"RUANRUGlobal":"ruan",
	"HAYDNEEATIGlobal":"haydn",
	"haydn_eea_by_global":"haydn",
	"HAYDNEEABYGlobal":"haydn",
	"fleur_mx_at_global":"fleur",
	"FLEURMXATGlobal":"fleur",
	"xun_ep_stdee":"xun",
	"XUNEPSTDEE":"xun",
	"ruyi_global":"ruyi",
	"RUYIGlobal":"ruyi",
	"opal_mx_at_global":"opal",
	"OPALMXATGlobal":"opal",
	"SHENGPREDPPGlobal":"sheng",
	"VENUSEEATIGlobal":"venus",
	"diting_cl_en_global":"diting",
	"DITINGCLENGlobal":"diting",
	"air_eea_global":"air",
	"AIREEAGlobal":"air",
	"ruyi_demo":"ruyi",
	"goku_demo":"goku",
	"RUYIDEMO":"ruyi",
	"GOKUDEMO":"goku",
	"COROTJPGlobal":"corot",
	"corot_jp_global":"corot",
	"venus_eea_vf_global":"venus",
	"VENUSEEAVFGlobal":"venus",
	"haydn_eea_ti_global":"haydn",
	"haydn_eea_hg_global":"haydn",
	"HAYDNEEAHGGlobal":"haydn",
	"malachite_ru_global":"malachite",
	"MALACHITERUGlobal":"malachite",
	"gold_ep_stdee":"gold",
	"GOLDEPSTDEE":"gold",
	"haydn_eea_sf_global":"haydn",
	"HAYDNEEASFGlobal":"haydn",
	"opal_eea_hg_global":"opal",
	"OPALEEAHGGlobal":"opal",
	"venus_eea_sf_global":"venus",
	"VENUSEEASFGlobal":"venus",
	"vili_eea_sf_global":"vili",
	"VILIEEASFGlobal":"vili",
	"veux_eea_hg_global":"veux",
	"VEUXEEAHGGlobal":"veux",
	"veux_eea_vf_global":"veux",
	"VEUXEEAVFGlobal":"veux",
	"veux_eea_or_global":"veux",
	"VEUXEEAORGlobal":"veux",
	"diting_mx_at_global":"diting",
	"DITINGMXATGlobal":"diting",
	"garnet_ep_stdee":"garnet",
	"GARNETEPSTDEE":"garnet",
	"breeze_in_global":"breeze",
	"BREEZEINGlobal":"breeze",
	"ruan_global":"ruan",
	"RUANGlobal":"ruan",
	"plato_cl_en_global":"plato",
	"PLATOCLENGlobal":"plato",
	"venus_eea_ti_global":"venus",
	"VENUSEEATIGlobal":"venus",
	"dizi_eea_global":"dizi",
	"DIZIEEAGlobal":"dizi",
	"dizi_ru_global":"dizi",
	"DIZIRUGlobal":"dizi",
	"dizi_id_global":"dizi",
	"diting_jp_global":"diting",
	"DITINGJPGlobal":"diting",
	"star_eea_vf_global":"star",
	"STAREEAVFGlobal":"star",
	"star_eea_or_global":"star",
	"STAREEAORGlobal":"star",
	"xaga_ru_global":"xaga",
	"XAGARUGlobal":"xaga",
	"DIZIIDGlobal":"dizi",
	"dizi_tw_global": "dizi",
	"DIZITWGlobal": "dizi",
	"zircon_jp_global":"zircon",
	"ZIRCONJPGlobal":"zircon",
	"venus_eea_or_global":"venus",
	"VENUSEEAORGlobal":"venus",
	"venus_eea_hg_global":"venus",
	"VENUSEEAHGGlobal":"venus",
	"air_global":"air",
	"AIRGlobal":"air",
	"blue_dc_global": "blue",
	"BLUEDCGlobal": "blue",
	"haydn_eea_vf_global":"haydn",
	"HAYDNEEAVFGlobal":"haydn",
	"SPARKINGlobal":"spark",
	"spark_in_global":"spark",
	"aurora_ep_stdee":"aurora",
	"AURORAEPSTDEE":"aurora",
	"breeze_ep_stdee":"breeze",
	"BREEZEEPSTDEE":"breeze",
	"DIZIINGlobal":"dizi",
	"dizi_in_global":"dizi",
	"light_eea_hg_global":"light",
	"LIGHTEEAHGGlobal":"light",
	"peridot_ep_stdee":"peridot",
	"PERIDOTEPSTDEE":"peridot",
	"liuqin_ep_stdee":"liuqin",
	"LIUQINEPSTDEE":"liuqin",
	"pipa_ep_stdee":"pipa",
	"PIPAEPSTDEE":"pipa",
	"moon_id_global":"moon",
	"MOONIDGlobal":"moon",
	"moon_eea_global":"moon",
	"MOONEEAGlobal":"moon",
	"MOONGlobal":"moon",
	"moon_global":"moon",
	"moon_ru_global":"moon",
	"MOONRUGlobal":"moon",
	"moon_tw_global":"moon",
	"MOONTWGlobal":"moon",
	"XAGATRGlobal":"xaga",
	"XAGATWGlobal":"xaga",
	"xaga_tr_global":"xaga",
	"xaga_tw_global":"xaga",
	"chenfeng_in_global":"chenfeng",
	"CHENFENGINGlobal":"chenfeng",
	"dizi_tr_global":"dizi",
	"DIZITRGlobal":"dizi",
	"air_ep_stdee":"air",
	"AIREPSTDEE":"air",
	"degas_demo":"degas",
	"rothko_demo":"rothko",
	"tides_demo":"tides",
	"ROTHKODEMO":"rothko",
	"TIDESDEMO":"tides",
	"venus_eea_tf_global":"venus",
	"VENUSEEATFGlobal":"venus",
	"star_global":"star",
	"STARGlobal":"star",
	"star_id_global":"star",
	"STARIDGlobal":"star",
	"munch_tr_global":"munch",
	"MUNCHTRGlobal":"munch",
	"munch_tw_global":"munch",
	"MUNCHTWGlobal":"munch",
	"light_th_as_global":"light",
	"LIGHTTHASGlobal":"light",
	"opal_eea_vf_global":"opal",
	"OPALEEAVFGlobal":"opal",
	"veux_eea_tf_global":"veux",
	"VEUXEEATFGlobal":"veux",
	"veux_jp_global":"veux",
	"VEUXJPGlobal":"veux",
	"venus_tr_global":"venus",
	"VENUSTRGlobal":"venus",
	"venus_tw_global":"venus",
	"VENUSTWGlobal":"venus",
	"venus_ru_global":"venus",
	"VENUSRUGlobal":"venus",
	"dizi_global":"dizi",
	"DIZIGlobal":"dizi",
	"fuxi_ep_stdee": "fuxi",
	"FUXIEPSTDEE":"fuxi",
	"xun_in_global":"xun",
	"XUNINGlobal":"xun",
	"vili_eea_tf_global":"vili",
	"VILIEEATFGlobal":"vili",
	"ALIOTHTWGlobal":"alioth",
	"alioth_tw_global":"alioth",
	"aurora_ru_global":"aurora",
	"AURORARUGlobal":"aurora",
	"venus_global":"venus",
	"VENUSGlobal":"venus",
	"peridot_id_global": "peridot",
	"PERIDOTIDGlobal": "peridot",
	"vermeer_tw_global":"vermeer",
	"VERMEERTWGlobal":"vermeer",
	"xaga_eea_global":"xaga",
	"XAGAEEAGlobal":"xaga",
	"odin":"odin",
	"ODIN":"odin",
	"COROTPREDPP":"corot",
	"COROTPREDPPGlobal":"corot",
	"HOUJIPREDPP":"houji",
	"SHENGPREDPP":"sheng",
	"HOUJIPREDPPGlobal":"sheng",
	"SHENNONGPREDPP":"shennong",
	"munch_in_global":"munch",
	"MUNCHINGlobal":"munch",
	"alioth_tr_global":"alioth",
	"ALIOTHTRGlobal":"alioth",
	"alioth_ru_global":"alioth",
	"ALIOTHRUGlobal":"alioth",
	"spesn_eea_sf_global":"spesn",
	"SPESNEEASFGlobal":"spesn",
	"munch_ru_global":"munch",
	"MUNCHRUGlobal":"munch",
	"xaga_in_global":"xaga",
	"XAGAINGlobal":"xaga",
	"rodin_tw_global":"rodin",
	"rodin_ru_global":"rodin",
	"RODINTWGlobal":"rodin",
	"RODINRUGlobal":"rodin",
	"peridot_in_global":"peridot",
	"PERIDOTINGlobal":"peridot",
	"peridot_global":"peridot",
	"PERIDOTGlobal":"peridot",
	"peridot_eea_global":"peridot",
	"PERIDOTEEAGlobal":"peridot",
	"peridot_ru_global":"peridot",
	"PERIDOTRUGlobal":"peridot",
	"sapphiren_tw_global":"sapphiren",
	"SAPPHIRENTWGlobal":"sapphiren",
	"ZIRCONDEMO":"zircon",
	"zircon_demo":"zircon",
	"munch_eea_global":"munch",
	"MUNCHEEAGlobal":"munch",
	"agate_eea_sf_global":"agate",
	"AGATEEEASFGlobal":"agate",
	"marble_demo":"marble",
	"MARBLEDEMO":"marble",
	"vermeer_eea_global":"vermeer",
	"VERMEEREEAGlobal":"vermeer",
	"venus_id_global":"venus",
	"VENUSIDGlobal":"venus",
	"cmi_eea_global":"cmi",
	"CMIEEAGlobal":"cmi",
	"alioth_id_global":"alioth",
	"ALIOTHIDGlobal":"alioth",
	"alioth_in_global":"alioth",
	"ALIOTHINGlobal":"alioth",
	"garnet_demo": "garnet",
	"GARNETDEMO":"garnet",
	"veux_tr_global":"veux",
	"corot_pre_dpp":"corot",
	"corot_pre_dpp_global":"corot",
	"houji_pre_dpp":"houji",
	"houji_pre_dpp_global":"houji",
	"sheng_pre_dpp":"sheng",
	"sheng_pre_dpp_global":"sheng",
	"shennong_pre_dpp":"shennong",
	"VEUXTRGlobal":"veux",
	"veux_tw_global":"veux",
	"VEUXTWGlobal":"veux",
	"spesn_eea_hg_global":"spesn",
	"SPESNEEAHGGlobal":"spesn",
	"vili_in_global":"vili",
	"VILIINGlobal":"vili",
	"vili_global":"vili",
	"VILIGlobal":"vili",
	"vili_ru_global":"vili",
	"VILIRUGlobal":"vili",
	"star_in_global":"star",
	"STARINGlobal":"star",
	"munch_id_global":"munch",
	"MUNCHIDGlobal":"munch",
	"sapphiren_tr_global":"sapphiren",
	"SAPPHIRENTRGlobal":"sapphiren",
	"umi_id_global":"umi",
	"UMIIDGlobal":"umi",
	"umi_global":"umi",
	"UMIGlobal":"umi",
	"umi_tr_global":"umi",
	"UMITRGlobal":"umi",
	"umi_ru_global":"umi",
	"UMIRUGlobal":"umi",
	"umi_in_global":"umi",
	"UMIINGlobal":"umi",
	"spesn_ru_global":"spesn",
	"SPESNRUGlobal":"spesn",
	"vili_tr_global":"vili",
	"VILITRGlobal":"vili",
	"vili_tw_global":"vili",
	"VILITWGlobal":"vili",
	"vili_id_global":"vili",
	"babylon_ep_stdee": "babylon",
	"BABYLONEPSTDEE":"babylon",
	"light_eea_sf_global": "light",
	"LIGHTEEASFGlobal":"light",
	"VILIIDGlobal":"vili",
	"sapphiren_ru_global":"sapphiren",
	"SAPPHIRENRUGlobal":"sapphiren",
	"earth_za_mt_global":"earth",
	"EARTHZAMTGlobal":"earth",
	"lisa_eea_sf_global":"lisa",
	"LISAEEASFGlobal":"lisa",
	"haydn_eea_global":"haydn",
	"HAYDNEEAGlobal":"haydn",
	"haydn_in_global":"haydn",
	"HAYDNINGlobal":"haydn",
	"haydn_global":"haydn",
	"HAYDNGlobal":"haydn",
	"VERMEERRUGlobal":"vermeer",
	"vermeer_ru_global":"vermeer",
	"munch_global":"munch",
	"MUNCHGlobal":"munch",
	"cmi_global":"cmi",
	"CMIGlobal":"cmi",
	"alioth_eea_global":"alioth",
	"ALIOTHEEAGlobal":"alioth",
	"GALEINGlobal":"gale",
	"gale_in_global":"gale",
	"vermeer_global":"vermeer",
	"VERMEERGlobal":"vermeer",
	"vili_eea_global":"vili",
	"VILIEEAGlobal":"vili",
	"gale_eea_global":"gale",
	"GALEEEAGlobal":"gale",
	"sapphiren_id_global":"sapphiren",
	"SAPPHIRENIDGlobal":"sapphiren",
	"VEUXIDGlobal":"veux",
	"veux_id_global":"veux",
	"veux_ru_global":"veux",
	"VEUXRUGlobal":"veux",
	"SHENGIDGlobal":"sheng",
	"sheng_id_global":"sheng",
	"sheng_ep_stdee":"sheng",
	"SHENGEPSTDEE":"sheng",
	"GARNETGlobal": "garnet",
	"fire_in_global":"fire",
	"alioth_global":"alioth",
	"ALIOTHGlobal":"alioth",
	"umi_eea_global":"umi",
	"UMIEEAGlobal":"umi",
	"pissarro_tr_global":"pissarro",
	"PISSARROTRGlobal":"pissarro",
	"pissarro_in_fk_global":"pissarro_in",
	"PISSARROINFKGlobal":"pissarro_in",
	"TANZANITELMCRGlobal":"tanzanite",
	"tanzanite_lm_cr_global":"tanzanite",
	"BERYLLMCRGlobal":"beryl",
	"beryl_lm_cr_global":"beryl",
	"TANZANITEEEAGlobal":"tanzanite",
	"tanzanite_eea_global":"tanzanite",
	"TANZANITETRGlobal":"tanzanite",
	"MALACHITETRGlobal":"malachite",
	"fleur_eea_sf_global":"fleur",
	"beryl_id_global":"beryl",
	"BERYLIDGlobal":"beryl",
	"BERYLTRGlobal":"beryl",
	"beryl_tr_global":"beryl",
	"FLEUREEASFGlobal":"fleur",
	"malachite_tr_global":"malachite",
	"tanzanite_tr_global":"tanzanite",
	"AMETHYSTLMCRGlobal":"amethyst",
	"amethyst_lm_cr_global":"amethyst",
	"spesn_id_global":"spesn",
	"SPESNIDGlobal":"spesn",
	"viva_ru_global":"viva",
	"VIVARUGlobal":"viva",
	"LAKE":"lake",
	"lake":"lake",
	"earth_za_vc_global":"earth",
	"EARTHZAVCGlobal":"earth",
	"lisa_eea_or_global":"lisa",
	"LISAEEAORGlobal":"lisa",
	"lisa_eea_vf_global":"lisa",
	"LISAEEAVFGlobal":"lisa",
	"lisa_eea_by_global":"lisa",
	"LISAEEABYGlobal":"lisa",
	"pissarro_ru_global":"pissarro",
	"PISSARRORUGlobal":"pissarro",
	"veux_in_global":"veux",
	"VEUXINGlobal":"veux",
	"veux_eea_global":"veux",
	"VEUXEEAGlobal":"veux",
	"breeze":"breeze",
	"degas":"degas",
	"rothko":"rothko",
	"tides":"tides",
	"moon":"moon",
	"SHENGGlobal":"sheng",
	"sheng_global":"sheng",
	"SHENGRUGlobal":"sheng",
	"sheng_ru_global":"sheng",
	"GOLDINGlobal":"gold",
	"gold_in_global":"gold",
	"fleur_tw_global":"fleur",
	"FLEURTWGlobal":"fleur",
	"BREEZE":"breeze",
	"DEGAS":"degas",
	"ROTHKO":"rothko",
	"TIDES":"tides",
	"MOON":"moon",
	"venus_eea_global":"venus",
	"VENUSEEAGlobal":"venus",
	"sunstone_ep_stdee": "sunstone",
	"SUNSTONEEPSTDEE":"sunstone",
	"lisa_tr_global":"lisa",
	"LISATRGlobal":"lisa",
	"lisa_in_global":"lisa",
	"LISAINGlobal":"lisa",
	"fleur_id_global":"fleur",
	"FLEURIDGlobal":"fleur",
	"pissarro_tw_global":"pissarro",
	"PISSARROTWGlobal":"pissarro",
	"evergo_in_global":"evergo",
	"EVERGOINGlobal":"evergo",
	"nabu_tr_global":"nabu",
	"NABUTRGlobal":"nabu",
	"nabu_tw_global":"nabu",
	"NABUTWGlobal":"nabu",
	"alioth":"alioth",
	"ALIOTH":"alioth",
	"lisa_ru_global":"lisa",
	"LISARUGlobal":"lisa",
	"lisa_tw_global":"lisa",
	"LISATWGlobal":"lisa",
	"psyche_tw_global":"psyche",
	"PSYCHETWGlobal":"psyche",
	"psyche_eea_global":"psyche",
	"PSYCHEEEAGlobal":"psyche",
	"ziyi_tr_global":"ziyi",
	"ZIYITRGlobal":"ziyi",
	"ziyi_tw_global":"ziyi",
	"ZIYITWGlobal":"ziyi",
	"spes_tr_global":"spes",
	"SPESTRGlobal":"spes",
	"nabu_ru_global":"nabu",
	"NABURUGlobal":"nabu",
	"evergreen_eea_global":"evergreen",
	"EVERGREENEEAGlobal":"evergreen",
	"opal_eea_global":"opal",
	"OPALEEAGlobal":"opal",
	"sapphiren_eea_global":"sapphiren",
	"SAPPHIRENEEAGlobal":"sapphiren",
	"dagu_ep_stdee":"dagu",
	"DAGUEPSTDEE":"dagu",
	"FLAMEINGlobal":"flame",
	"flame_in_global":"flame",
	"BERYLTWGlobal":"beryl",
	"beryl_tw_global":"beryl",
	"onyx_demo":"onyx",
	"BERYLGlobal":"beryl",
	"beryl_global":"beryl",
	"BERYLDCGlobal":"beryl",
	"beryl_dc_global":"beryl",
	"BERYLEEAGlobal":"beryl",
	"beryl_eea_global":"beryl",
	"rodin_global":"rodin",
	"rodin_eea_global":"rodin",
	"RIDONGlobal":"rodin",
	"RIDONEEAGlobal":"rodin",
	"dizi_demo":"dizi",
	"DIZIDEMO":"dizi",
	"ziyi_ru_global":"ziyi",
	"ZIYIRUGlobal":"ziyi",
	"ruan_demo":"ruan",
	"RUANDEMO":"ruan",
	"breeze_demo":"breeze",
	"xaga_global":"xaga",
	"XAGAGlobal":"xaga",
	"EMERALDEEAGlobal":"emerald",
	"EMERALDRUGlobal":"emerald",
	"EMERALDTRGlobal":"emerald",
	"emerald_tr_global":"emerald",
	"emerald_eea_global":"emerald",
	"emerald_ru_global":"emerald",
	"fleur_tr_global":"fleur",
	"FLEURTRGlobal":"fleur",
	"fleur_ru_global":"fleur",
	"FLEURRUGlobal":"fleur",
	"emerald_id_global":"emerald",
	"EMERALDIDGlobal":"emerald",
	"nabu_in_global":"nabu",
	"NABUINGlobal":"nabu",
	"nabu_eea_global":"nabu",
	"NABUEEAGlobal":"nabu",
	"opal_eea_tf_global":"opal",
	"OPALEEATFGlobal":"opal",
	"agate_tr_global":"agate",
	"AGATETRGlobal":"agate",
	"agate_tw_global":"agate",
	"AGATETWGlobal":"agate",
	"agate_id_global":"agate",
	"AGATEIDGlobal":"agate",
	"pearl":"pearl",
	"PEARL":"pearl",
	"peridot_demo":"peridot",
	"PERIDOTDEMO":"peridot",
	"evergreen_tr_global":"evergreen",
	"EVERGREENTRGlobal":"evergreen",
	"evergreen_ru_global":"evergreen",
	"EVERGREENRUGlobal":"evergreen",
	"gold_id_global":"gold",
	"GOLDIDGlobal":"gold",
	"ZIRCONTRGlobal":"zircon",
	"zircon_tr_global":"zircon",
	"ziyi_global":"ziyi",
	"ZIYIGlobal":"ziyi",
	"munch":"munch",
	"haydn":"haydn",
	"xaga":"xaga",
	"thyme":"thyme",
	"cas":"cas",
	"umi":"umi",
	"cmi":"cmi",
	"air":"air",
	"AIR":"air",
	"MUNCH":"munch",
	"HAYDN":"haydn",
	"XAGA":"xaga",
	"THYME":"thyme",
	"CAS":"cas",
	"UMI":"umi",
	"CMI":"cmi",
	"star":"star",
	"venus":"venus",
	"STAR":"star",
	"VENUS":"venus",
	"pissarro_in_global":"pissarro",
	"PISSARROINGlobal":"pissarro",
	"ares_in_global":"ares",
	"ARESINGlobal":"ares",
	"SAPPHIRENGlobal":"sapphiren",
	"sapphiren_global":"sapphiren",
	"opal_ru_global":"opal",
	"OPALRUGlobal":"opal",
	"psyche_ru_global":"psyche",
	"PSYCHERUGlobal":"psyche",
	"zeus_tr_global":"zeus",
	"ZEUSTRGlobal":"zeus",
	"zeus_ru_global":"zeus",
	"ZEUSRUGlobal":"zeus",
	"rembrandt":"rembrandt",
	"REMBRANDT":"rembrandt",
	"zircon_tw_global":"zircon",
	"ZIRCONTWGlobal":"zircon",
	"earth_eea_hg_global":"earth",
	"EARTHEEAHGGlobal":"earth",
	"AURORAINGlobal":"aurora",
	"aurora_in_global":"aurora",
	"earth_gt_tg_global":"earth",
	"EARTHGTTGGlobal":"earth",
	"sweet_k6a_id_global":"sweet_k6a",
	"SWEETK6AIDGlobal":"sweet_k6a",
	"FIREINGlobal":"fire",
	"nabu_global":"nabu",
	"NABUGlobal":"nabu",
	"FLEUREEAGlobal":"fleur",
	"fleur_in_global":"fleur",
	"FLEURINGlobal":"fleur",
	"fleur_eea_global":"fleur",
	"ZIRCONEEAGlobal":"zircon",
	"zircon_eea_global":"zircon",
	"spesn_eea_global":"spesn",
	"SPESNEEAGlobal":"spesn",
	"viva_tr_global":"viva",
	"VIVATRGlobal":"viva",
	"spesn_eea_tf_global":"spesn",
	"SPESNEEATFGlobal":"spesn",
	"lisa_eea_tf_global":"lisa",
	"LISAEEATFGlobal":"lisa",
	"pissarro_global":"pissarro",
	"PISSARROGlobal":"pissarro",
	"ziyi_eea_global":"ziyi",
	"ZIYIEEAGlobal":"ziyi",
	"cupid_tr_global":"cupid",
	"CUPIDTRGlobal":"cupid",
	"zeus_tw_global":"zeus",
	"ZEUSTWGlobal":"zeus",
	"gold_tw_global":"gold",
	"GOLDTWGlobal":"gold",
	"agate_eea_or_global":"agate",
	"AGATEEEAORGlobal":"agate",
	"garnet_tw_global":"garnet",
	"GARNETTWGlobal":"garnet",
	"light_eea_vf_global":"light",
	"LIGHTEEAVFGlobal":"light",
	"agate_eea_tf_global":"agate",
	"earth_eea_vf_global":"earth",
	"EARTHEEAVFGlobal":"earth",
	"AGATEEEATFGlobal":"agate",
	"light_eea_tf_global":"light",
	"LIGHTEEATFGlobal":"light",
	"gale_global":"gale",
	"GALEGlobal":"gale",
	"XUNTWGlobal": "xun",
	"xun_tw_global": "xun",
	"lake_tr_global":"lake",
	"LAKETRGlobal":"lake",
	"dada_ep_stdee":"dada",
	"flame_ep_stdee":"flame",
	"FLAMEEPSTDEE":"flame",
	"sweet_k6a_tr_global":"sweet_k6a",
	"SWEETK6ATRGlobal":"sweet_k6a",
	"cupid_global":"cupid",
	"CUPIDGlobal":"cupid",
	"moonstone_tr_global":"moonstone",
	"MOONSTONETRGlobal":"moonstone",
	"moonstone_id_global":"moonstone",
	"MOONSTONEIDGlobal":"moonstone",
	"yunluo_tw_global":"yunluo",
	"YUNLUOTWGlobal":"yunluo",
	"ruby_tr_global":"ruby",
	"opal_global":"opal",
	"OPALGlobal":"opal",
	"viva_tw_global":"viva",
	"VIVATWGlobal":"viva",
	"SERENITYCLENGlobal": "serenity",
	"evergreen_global":"evergreen",
	"EVERGREENGlobal":"evergreen",
	"pissarro_eea_global":"pissarro",
	"PISSARROEEAGlobal":"pissarro",
	"ingres_tr_global":"ingres",
	"INGRESTRGlobal":"ingres",
	"ingres_ru_global":"ingres",
	"INGRESRUGlobal":"ingres",
	"light_tr_global":"light",
	"LIGHTTRGlobal":"light",
	"light_ru_global":"light",
	"LIGHTRUGlobal":"light",
	"vida_in_global":"vida",
	"VIDAINGlobal":"vida",
	"earth_eea_or_global":"earth",
	"EARTHEEAORGlobal":"earth",
	"yunluo_id_global":"yunluo",
	"YUNLUOIDGlobal":"yunluo",
	"yunluo_tr_global":"yunluo",
	"YUNLUOTRGlobal":"yunluo",
	"manet_ep_stdee":"manet",
	"MANETEPSTDEE":"manet",
	"spes_in_global":"spes",
	"SPESINGlobal":"spes",
	"light_eea_or_global":"light",
	"LIGHTEEAORGlobal":"light",
	"gold_tr_global":"gold",
	"GOLDTRGlobal":"gold",
	"lisa_eea_ti_global":"lisa",
	"LISAEEATIGlobal":"lisa",
	"lisa_eea_hg_global":"lisa",
	"LISAEEAHGGlobal":"lisa",
	"veux_global":"veux",
	"VEUXGlobal":"veux",
	"zircon_ru_global":"zircon",
	"ZIRCONRUGlobal":"zircon",
	"viva_id_global":"viva",
	"VIVAIDGlobal":"viva",
	"garnet_tr_global":"garnet",
	"GARNETTRGlobal":"garnet",
	"garnet_ru_global":"garnet",
	"GARNETRUGlobal":"garnet",
	"garnet_id_global":"garnet",
	"GARNETIDGlobal":"garnet",
	"RUBYTRGlobal":"ruby",
	"opal_tw_global":"opal",
	"OPALTWGlobal":"opal",
	"ruby_ru_global":"ruby",
	"RUBYRUGlobal":"ruby",
	"lisa_global":"lisa",
	"LISAGlobal":"lisa",
	"cupid_tw_global":"cupid",
	"CUPIDTWGlobal":"cupid",
	"cupid_ru_global":"cupid",
	"CUPIDRUGlobal":"cupid",
	"aurora_tr_global":"aurora",
	"AURORATRGlobal":"aurora",
	"sheng_eea_global":"sheng",
	"SHENGEEAGlobal":"sheng",
	"evergreen_tw_global": "evergreen",
	"EVERGREENTWGlobal": "evergreen",
	"agate_eea_vf_global": "agate",
	"AGATEEEAVFGlobal": "agate",
	"agate_eea_by_global":"agate",
	"AGATEEEABYGlobal":"agate",
	"yunluo_ru_global": "yunluo",
	"YUNLUORUGlobal": "yunluo",
	"sky_jp_global": "sky",
	"SKYJPGlobal": "sky",
	"sky_ep_stdee": "sky",
	"zeus_id_global":"zeus",
	"ZEUSIDGlobal":"zeus",
	"SKYEPSTDEE": "sky",
	"ishtar_ep_stdee": "ishtar",
	"ISHTAREPSTDEE": "ishtar",
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
	"SERENITYRUGlobal":"serenity",
	"serenity_ru_global":"serenity",
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
	"koto_dc_global": "koto",
	"onyx_global": "onyx",
	"taiko_id_global": "taiko",
	"taiko_tr_global": "taiko",
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
	"miro_demo":"miro",
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
	"SERENITYEEATFGlobal":"serenity",
	"serenity_eea_tf_global":"serenity",
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
	"onyx":"onyx",
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
	"spring_lm_cr_global": "spring",
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
	"miro_tw_global":"miro",
	"miro_global":"miro",
	"miro_eea_global":"miro",
	"miro_ru_global":"miro",
	"miro_id_global":"miro",
	"miro_tr_global":"miro",
	"zorn_tw_global":"zorn",
	"zorn_global":"zorn",
	"zorn_eea_global":"zorn",
	"zorn_ru_global":"zorn",
	"zorn_id_global":"zorn",
	"zorn_tr_global":"zorn",
	"sunstone_global": "sunstone",
	"SUNSTONEGlobal": "sunstone",
	"evergo": "evergo",
	"EVERGO": "evergo",
	"gale_id_global":"gale",
	"GALEIDGlobal":"gale",
	"gale_ru_global":"gale",
	"GALERUGlobal":"gale",
	"gale_tr_global":"gale",
	"GALETRGlobal":"gale",
	"gale_tw_global":"gale",
	"GALETWGlobal":"gale",
	"GOLDDEMO":"gold",
	"gold_demo":"gold",
	"XUNDEMO":"xun",
	"xun_demo":"xun",
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
	"xun_tr_global":"xun",
	"XUNTRGlobal":"xun",
	"xun_id_global":"xun",
	"XUNIDGlobal":"xun",
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
	"dada_demo":"dada",
	"haotian_demo":"haotian",
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
	"SERENITYMXATGlobal":"serenity",
	"serenity_mx_at_global":"serenity",
	"SERENITYLMMSGlobal":"serenity",
	"serenity_lm_ms_global":"serenity",
	"BERYLRUGlobal":"beryl",
	"beryl_ru_global":"beryl",
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
	"haydn_eea_or_global":"haydn",
	"HAYDNEEAORGlobal":"haydn",
	"haydn_eea_tf_global":"haydn",
	"HAYDNEEATFGlobal":"haydn",
	"vili_eea_vf_global":"vili",
	"VILIEEAVFGlobal":"vili",
	"opal_eea_or_global":"opal",
	"OPALEEAORGlobal":"opal",
	"vili_eea_or_global":"vili",
	"VILIEEAORGlobal":"vili",
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
	"malachite_ep_stdee":"malachite",
	"MALACHITEEPSTDEE":"malachite",
	"DUCHAMPDEMO": "duchamp",
	"duchamp_demo": "duchamp",
	"duchamp": "duchamp",
	"MANET": "manet",
	"CUPID": "cupid",
	"opal_eea_sf_global":"opal",
	"OPALEEASFGlobal":"opal",
	"veux_eea_sf_global":"veux",
	"VEUXEEASFGlobal":"veux",
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
	"SERENITYLMCRGlobal":"serenity",
	"serenity_lm_cr_global": "serenity",
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
	"rodin_tr_global":"rodin",
	"SOCRATES": "socrates",
	"socrates": "socrates",
	"ZIZHAN": "zizhan",
	"BABYLON": "babylon",
	"babylon": "babylon",
	"zizhan": "zizhan",
	"malachite_jp_global":"malachite",
	"NUWA": "nuwa",
	"TANZANITEIDGlobal":"tanzanite",
	"tanzanite_id_global":"tanzanite",
	"NUWADEMO": "nuwa",
	"ISHTAR": "ishtar",
	"ishtar": "ishtar",
	"ISHTARDEMO": "ishtar",
	"ishtar_demo": "ishtar",
	"FLAREIDGlobal":"flare",
	"flare_id_global":"flare",
	"SERENITYEEAORGlobal": "serenity",
	"SERENITYEEAVFGlobal": "serenity",
	"SERENITYEEABYGlobal": "serenity",
	"serenity_eea_or_global": "serenity",
	"serenity_eea_vf_global": "serenity",
	"serenity_eea_by_global": "serenity",
	"SERENITYZAMTGlobal":"serenity",
	"serenity_za_mt_global":"serenity",
	"amethyst_mx_at_global":"amethyst",
	"AMETHYSTMXATGlobal":"amethyst",
	"TANZANITEMXATGlobal":"tanzanite",
	"tanzanite_mx_at_global": "tanzanite",
	"OBSIDIANMXATGlobal":"obsidian",
	"obsidian_mx_at_global": "obsidian",
	"EMERALDRRUGlobal":"emerald_r",
	"serenity_id_global":"serenity",
	"SERENITYIDGlobal":"serenity",
	"emerald_r_ru_global":"emerald_r"
}


def ver_in_order(versions):
	list = versions.split("; ")
	for i in range(len(list)):
		for j in range(i+1, len(list)):
			if list[i] > list[j]:
				list[i], list[j] = list[j], list[i]
	return list
	

def localData(codename):
	if platform == "win32":
		devdata = json.loads(open("public/data/devices/"+codename+".json", 'r', encoding='utf-8').read())
	elif platform == "darwin":
		devdata = json.loads(open("public/data/devices/"+codename+".json", 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open("/sdcard/Codes/HyperOS.fans/public/data/devices/" + codename+".json", 'r', encoding='utf-8').read())
	return devdata

def db_job(sql):
	cnx = None
	try:
		cnx = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True
			)
		cursor = cnx.cursor()
		cursor.execute(sql)
		return cursor.fetchall()
	except Exception as e:
		print(sql,e)
	finally:
		if cnx:
			cnx.close()

def stringify(s):
		return f"'{s}'"
def get_time(url):
	try:
		response = requests.head(url, allow_redirects=True)
		if 'Last-Modified' in response.headers:
			last_modified_str = response.headers['Last-Modified']
			re_date = datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=8)
			return re_date.strftime("%Y-%m-%d")
		else:
			return date.today().strftime("%Y-%m-%d")
	except requests.RequestException as e:
		return date.today().strftime("%Y-%m-%d")

def form_url(filename,version):
	return 'https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/'+version+"/"+filename

def writeData(filename):
	if platform == "win32":
		file = open("public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
	elif platform == "darwin":
		file = open("public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
	else:
		file = open("/sdcard/Codes/HyperOS.fans/public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
	file.write(filename+"\n")
	if ".zip" in filename:
		if "miui" in filename:
		# OS With Android 14 and below uses "miui" as start, and flag is located in spot 1
			rec_seperator = "_"
			rec_spot = 1
		else:
		# OS With Android 15 uses "-ota_full" as a separator, and flag is located in spot 0
			rec_seperator = "-ota_full"
			rec_spot = 0
		flag = filename.split(rec_seperator)[rec_spot]
	elif ".tgz" in filename:
		if "-images" in filename:
			flag = filename.split('-images')[0]
		else:
			flag = filename.split('_images')[0]
	print("发现\t"+flag+"\t分支有未收录的新版本")
	file.close()


def writeFlag(flag, device):
	if platform == "win32":
		file = open("public/data/scripts/Flags.json", "a", encoding='utf-8')
	elif platform == "darwin":
		file = open("public/data/scripts/Flags.json", "a", encoding='utf-8')
	else:
		file = open("/sdcard/Codes/HyperOS.fans/public/data/scripts/Flags.json", "a", encoding='utf-8')
	file.write("\""+flag+"\":\""+device+"\",\n")
	file.close()


def getDeviceCode(filename):
	if ".zip" in filename:
		if "miui" in filename:
			# OS With Android 14 and below uses "miui" as start, and flag is located in spot 1
			rec_seperator = "_"
			rec_spot = 1
		else:
			# OS With Android 15 uses "-ota_full" as a separator, and flag is located in spot 0
			rec_seperator = "-ota_full"
			rec_spot = 0
		flag = filename.split(rec_seperator)[rec_spot]
		if flag in flags:
			codename = flags[flag]
			return codename
		else:
			writeData(filename)
			writeFlag(flag, "")
			return 0
	elif ".tgz" in filename:
		if "-images" in filename:
			flag = filename.split('-images')[0]
		else:
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

def OTAFormer(device, code, region, branch, zone, android, version):
		# print(device, code, region, branch, zone, android, version)
		HyperOSForm['d'] = code
		HyperOSForm["obv"] = version[:5]
		if region == 'cn':
			HyperOSForm['pn'] = code
			HyperOSForm["r"] = 'CN'
		else:
			HyperOSForm["r"] = 'GL'
			if code == device + "_global":
				HyperOSForm['pn'] = code
			else:
				HyperOSForm['pn'] = code.split('_global')[0]
		HyperOSForm['b'] = branch
		HyperOSForm['options']['zone'] = zone
		if android == '':
			print(device,version,"请补充安卓版本")
			HyperOSForm['c'] = '14'
		else:
			HyperOSForm['c'] = android.split('.0')[0]
		HyperOSForm['sdk'] = sdk[android.split('.0')[0]]
		if "OS1"in version:
			HyperOSForm['v'] = 'MIUI-'+ version.replace('OS1','V816')
		else:
			HyperOSForm['v'] = version
		return json.dumps(HyperOSForm)

def db_job_latest(sql):
	cnx = None
	try:
		cnx = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True
			)
		cursor = cnx.cursor()
		cursor.execute(sql)
		return cursor.fetchone()
	except Exception as e:
		print(sql,e)
	finally:
		if cnx:
			cnx.close()

def getBranchcode(filename):
	if filename.endswith(".zip"):
		if filename.startswith("miui"):
			branchCode = filename.split("_")[1]
			get_sql = "SELECT code FROM devices WHERE branchcode = %s" % (stringify(branchCode))
			if len(db_job(get_sql)) > 0:
				return db_job(get_sql)[0][0]
			else:
				return 0
		else:
			return filename.split("-")[0]
	elif filename.endswith(".tgz"):
		return filename.split('_images')[0]

def getData(filename):
	if "miui" in filename:
		filetype = "recovery"
		android = filename.split("_")[4].split(".zip")[0]
		version = filename.split("_")[2]
		get_sql = "SELECT code,device FROM devices WHERE branchcode = %s" % (stringify(filename.split("_")[1]))
		data = db_job_latest(get_sql)
		if data is not None:
			code = data[0]
			device = data[1]
		else:
			if ".EP" in filename:
				devtag = filename.split("_")[1].split("EPS")[0].lower()
			else:
				devtag = version.split(".")[4][1:3]
			ver_code = version[-4:]
			info = db_job_latest("SELECT tag,code,region FROM branches WHERE vercode = %s" % (stringify(ver_code)))
			tag,code,region = [item for item in info]
			device = db_job_latest("SELECT device FROM devices WHERE devtag = %s" % (stringify(devtag)))[0]
			code = device+code
			ins_sql = "INSERT INTO devices(device,devtag,code,tag,region,devcode,branchcode) VALUES (%s,%s,%s,%s,%s,%s,%s)" % (stringify(device),stringify(devtag),stringify(code),stringify(tag),stringify(region),stringify(version[-6:]),stringify(filename.split("_")[1]))
			db_job_latest(ins_sql)
	else:
		if filename.endswith(".tgz"):
			filetype = "fastboot"
			if "-images" in filename:
				android = filename.split("images-")[1].split("-")[3]
				version = filename.split("images-")[1].split("-")[0]
				code = filename.split('-images')[0]
			else:
				android = filename.split("images_")[1].split("_")[2]
				version = filename.split("images_")[1].split("_")[0]
				code = filename.split('_images')[0]
		else:
			filetype = "recovery"
			android = filename.split("ota_full-")[1].split("-")[2]
			version = filename.split("ota_full-")[1].split("-user")[0]
			code = filename.split("-ota_full")[0]
		data = db_job_latest("SELECT device FROM roms where code = %s" % (stringify(code)))
		if data is not None:
			device = data[0]
		else:
			device = db_job_latest("SELECT device FROM devices where code = %s" % (stringify(code)))[0]
	if version.startswith('V'):
		type = "MIUI"
		bigver = "MIUI " + version.split('V')[1].split('.')[0]
	elif version.startswith('OS'):
		type = "HyperOS"
		bigver = "HyperOS " + version.split('OS')[1].split('.')[0]
	elif version.startswith('A'):
		type = "STAN"
		bigver = "STAN " + version.split('.')[0]
	if code == 0:
		return 0
	else:
		if "CNXM" in version:
			if version.split(".")[3] == 0 or version.split(".")[3] == "0":
				tag = "CnOO"
			else:
				tag = "CnOB"
			region = "cn"
			zone = 1
		else:
			info_sql = "SELECT region,tag,zone FROM roms WHERE code = %s" % (stringify(code))
			data = db_job_latest(info_sql)
			if data is not None:
				if len(data) > 0:
					region,tag,zone = [item for item in data]
				else:
					region,tag,zone = db_job_latest(info_sql)
			else:
				data = db_job_latest("SELECT region,tag FROM devices WHERE code = %s" % (stringify(code)))
				region,tag = [item for item in data]
				if region == "cn":
					zone = 1
				else:
					zone = 2
	return device, code, android, version, type, bigver, region,tag,zone, "F", filetype, filename

def checkDatabase(device, code, android, version, type, bigver, region,tag,zone,branch, filetype, filename):
	if filetype == "recovery":
		checkpoint = "recovery"
	else:
		if "chinatelecom" in filename:
			checkpoint = "ctelecom"
		elif "chinaunicom" in filename:
			checkpoint = "cunicom"
		elif "chinamobile" in filename:
			checkpoint = "cmobile"
		else:
			checkpoint = "fastboot"
	get_sql = f"SELECT id,{checkpoint},others FROM roms WHERE code = %s and version = %s" % (stringify(code), stringify(version))
	data = db_job_latest(get_sql)
	if data is not None:
		if len(data) > 0:
			if data[1] == filename:
				pass
			elif data[1] == None:
				if filetype == "recovery":
					beta_date = stringify(get_time(form_url(filename,version)))
					upd_sql = f"UPDATE roms SET {checkpoint} = %s, beta_date = %s WHERE id = %d" % (stringify(filename),beta_date, data[0])
				else:
					public_date = stringify(get_time(form_url(filename,version)))
					upd_sql = f"UPDATE roms SET {checkpoint} = %s, public_date = %s WHERE id = %d" % (stringify(filename),public_date, data[0])
				db_job_latest(upd_sql)
			else:
				if data[2] == None or data[2] == "":
					others = []
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %d" % (data[0])
					db_job_latest(update_sql)
				elif filename in data[2]:
					pass
				else:
					others = list(json.loads(data[2]))
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %d" % (data[0])
					db_job_latest(update_sql)
		else:
			print(filename)
	else:
		insdate = stringify(date.today().strftime("%Y-%m-%d"))
		release_date = stringify(date.today().strftime("%Y-%m-%d"))
		if filetype == "fastboot":
			public_date = stringify(get_time(form_url(filename,version)))
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,insdate, public_date) VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (zone, stringify(device), stringify(code), stringify(android), stringify(version), stringify(type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, insdate, public_date)
		else:
			beta_date = stringify(get_time(form_url(filename,version)))
			public_date = stringify(None)
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,beta_date,insdate) VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (zone, stringify(device), stringify(code), stringify(android), stringify(version), stringify(type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, beta_date, insdate)
		db_job_latest(ins_sql)

def checkExist(filename):
	if platform == "win32":
		newROM = open("public/data/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		UInewROM = open("D:/Projects/HyperOS.fans/Nuxt3MR/public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	elif platform == "darwin":
		newROM = open("public/data/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		UInewROM = open("../NuxtMR/public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	else:
		newROM = open("/sdcard/Codes/HyperOS.fans/public/data/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		newROM = open("/sdcard/Codes/NuxtMR/public/MRdata/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	if "OS" in filename or "A1" in filename:
		if "blockota" in filename:
			return "OTA ROM"
		else:
			if getDeviceCode(filename) == 0:
				writeData(filename)
				return "New ROM"
			elif filename in localData(getDeviceCode(filename)).__str__() or filename in newROM or filename in UInewROM:
				return "Already Exist"
			else:
				device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = [item for item in getData(filename)]
				writeData(filename)
				checkDatabase(device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename)
				# getChangelog2DB()
				return "New ROM"
	else:
		return "UI Maybe"

def versionAdd(version,add):
	parts = [version.split('.')[0],version.split('.')[1],str(int(version.split('.')[2])+add),"0",version.split('.')[4]]
	separator = "."
	return separator.join(parts)

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
	"n": "",
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
	 "av": "8.8.8",
	 "cv": ""
	 }
}


def getFromApi(encrypted_data):
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
	session = requests.Session()
	retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
	session.mount('http://', HTTPAdapter(max_retries=retries))
	session.mount('https://', HTTPAdapter(max_retries=retries))
	try:
		response = session.post(check_url, headers=headers, data=data, timeout=10)
		if "code" in response.text:
			i = 0
		else:
			data = miui_decrypt(response.text.split("q=")[0])
			if "LatestRom" in data:
				package = data["LatestRom"]["filename"].split("?")[0]
				# print(package)
				checkExist(package)
				return 1
			if "CrossRom" in data:
				package = data["CrossRom"]["filename"].split("?")[0]
				# print(package)
				checkExist(package)
				return 1
			else:
				return 0
		response.close()
	except requests.exceptions.RequestException as e:
		print(f"请求失败: {e}")

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
	wrongs = [
		"miui_LIUQIN_OS1.0.7.0.UMYCNXM_d618a5c980_14.0.zipp"
	]
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
					if td.text in wrongs:
						i = 0
					elif ".tgz" in td.text or ".zip" in td.text:
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
	response = requests.post(check_url, headers=headers, data=data)
	if "code" in response.text:
		print(json.loads(response.text)["desc"])
	else:
		data = miui_decrypt(response.text.split("q=")[0])
		if "LatestRom" in data:
			print("最新版本更新日志：")
			print_log(strip_log(data["LatestRom"]["changelog"]))
		if "CurrentRom" in data:
			print("当前版本更新日志：")
			print(device)
			print_log(strip_log(data["CurrentRom"]["changelog"]))
		else:
			print(data)
			return 0
	response.close()

def getChangelog2DB(encrypted_data, device,version):
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
	if "'code'" in response.text:
		print(json.loads(response.text)["desc"])
	else:
		data = miui_decrypt(response.text.split("q=")[0])
		if "LatestRom" in data:
			if "changelog" in data['LatestRom'] and data['LatestRom']['version'] == version:
				log = data["LatestRom"]["changelog"]
			elif "changelog" in data['CurrentRom'] and data['CurrentRom']['version'] == version:
				log = data["CurrentRom"]["changelog"]
			else:
				return False
				i = 0
		else:
			return False
	response.close()
	return json.dumps(strip_log(remove_spaces(log)), ensure_ascii=False)

def remove_spaces(d):
	if isinstance(d, dict):
		return {k: remove_spaces(v) for k, v in d.items() if v and not (isinstance(v, str) and v.isspace())}
	elif isinstance(d, list):
		return [remove_spaces(v) for v in d if v and not (isinstance(v, str) and v.isspace())]
	elif isinstance(d, str):
		# 往后从数据库读取时记得替换回来
		return d.replace('\b','').replace('\t','').replace('%','$$').replace('"','^').replace("'", "^")
	else:
		return d

def parse_version(version):
	try:
		if version.startswith("OS"):
			body = version[2:]
		elif version.startswith("A"):
			body = version[1:]
		else:
			return None
		version_part = body.split(".")
		numeric_parts = tuple(map(int, version_part[:4]))
		return numeric_parts
	except Exception:
		return None

def compare(v1, v2):
	if v1 is None or v2 is None:
		return False
	else:
		return parse_version(v1) > parse_version(v2)

def print_log(log):
	for module in log:
		print(module)
		for entry in log[module]:
			print(entry)
		

def getFastboot(url):
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=3))
	s.mount('https://', HTTPAdapter(max_retries=3))
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
				 'Connection': 'close'}
	try:
		response = s.post(url, headers=headers, json=True)
		if (response.status_code == 200):
			content = response.content.decode('utf8')
			if content == '':
				i = 0
			else:
				data = json.loads(content)['LatestFullRom']
				if len(data) > 0:
					checkExist(data['filename'])
				else:
					i = 0
		else:
			i = 0
	except requests.exceptions.RequestException as e:
		i = 0
	s.close()

def entryChecker(data,device):
	check =[]
	code = data['code']
	if len(data['branches']) == 0:
		i = 0
	else:
		for branch in data['branches']:
			if data['device'] in branch['branchCode']:
				roms = branch['roms']
				bname = branch['name']['zh']
				menu_items = branch['table']
				if len(branch['table']) != len(branch['roms'][next(iter(branch['roms']))]):
					print(device, bname,next(iter(branch['roms'])), "菜单项与ROM实际不符")
					check.append(1)
				else:
					if len(menu_items) != len(set(menu_items)):
						print(device, bname, "菜单项重复")
						check.append(1)
					else:
						for os_version, rom_info in roms.items():
							if os_version[:5] not in data['suppports']:
								if "Developer" in branch['name']['en']:
									i = 0
								else:
									print(device, bname, os_version[:5], os_version, "大版本号没有记录")
									check.append(1)
							if rom_info['android'] not in data['android']:
								print(device, bname, rom_info['android'], os_version, "Android版本号没有记录")
								check.append(1)
							if rom_info['recovery'] != "" and rom_info['recovery'].endswith(".zip") and os_version in rom_info['recovery']:
								if branch['ep'] == "1" or branch['branchtag'] == 'X':
									i = 0
								else:
									if os_version.startswith("OS1") and code+branch['tag'] in rom_info['recovery']:
										i = 0
									elif os_version.startswith("A1") and code+branch['tag'] in rom_info['recovery']:
										i = 0
									elif branch['branchCode'] in rom_info['recovery']:
										i = 0
									else:
										print(device, bname, os_version, "卡刷包的信息不对")
										check.append(1)
							elif rom_info['recovery'] == "":
								i = 0
							else:
								if "Developer" in branch['name']['en']:
									i = 0
								else:
									print(device, bname, os_version, "卡刷包的信息不对")
									check.append(1)
							for i in range(4,len(menu_items)):
								if rom_info[menu_items[i]] != "" and rom_info[menu_items[i]].endswith(".tgz") and os_version in rom_info[menu_items[i]]:
									i = 0
								elif rom_info[menu_items[i]] == "":
									i = 0
								else:
									if "Developer" in branch['name']['en']:
										i = 0
									else:
										print(device, bname, os_version, "线刷包的信息不对")
										check.append(1)
							if os_version != rom_info['os']:
								print(device, bname, os_version, "版本号不匹配")
								check.append(1)
							else:
								if branch['ep'] == "1" or branch['branchtag'] == 'X':
									i = 0
								else:
									if code+branch['tag'] in os_version:
										i = 0
									else:
										print(device, bname, os_version, "版本号不匹配")
										check.append(1)
			else:
				print(device, "机型与分支不配，请核实", branch['branchCode'])
				check.append(1)
	if 1 in list(set(check)):
		return 1
	else:
		return 0

def strip_log(data):
	result = {}
	for key, value in data.items():
		if isinstance(value, dict) and 'txt' in value:
			result[key] = value['txt']
		else:
			result[key] = value
	return result