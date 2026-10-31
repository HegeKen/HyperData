import json
from sys import platform
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date, timezone
from requests.adapters import HTTPAdapter
import struct
import urllib
import urllib.parse
from urllib3.util.retry import Retry
from urllib.parse import quote
from pymysql import Connection
import config
import os
from collections import OrderedDict
import re

def get_platform_path(relative_path):
	"""获取平台相关的文件路径"""
	if platform == "win32":
		return os.path.join(relative_path)
	elif platform == "darwin":
		return os.path.join(relative_path)
	else:
		return os.path.join("/sdcard/Codes/HyperOS.fans", relative_path)

def detect_json_indent(file_path):
	"""检测JSON文件的缩进格式
	
	Args:
		file_path: JSON文件路径
	
	Returns:
		缩进字符串（'\t' 或 '  '）
	"""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			# 读取第二行（第一行通常是 '{'）
			lines = f.readlines()
			if len(lines) > 1:
				second_line = lines[1]
				# 检查是否以Tab开头
				if second_line.startswith('\t'):
					return '\t'
				# 检查空格数量
				spaces = len(second_line) - len(second_line.lstrip(' '))
				if spaces > 0:
					return ' ' * spaces
		# 默认使用2空格
		return '\t'
	except Exception:
		return '\t'


def extract_flag_from_filename(filename):
	"""从文件名中提取flag"""
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
	else:
		flag = ""
	return flag

sdk = {
	"17.0": "37",
	"17": "37",
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
	if ver == "17.0":
		return "X"
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


unreleased = ['yanan', 'warsaw_y', 'moscow', 'brussels', 'chicago', 'pond', 'suiren', 'zephyr', 'coral']
currentStable = ['darwin', 'yanan', 'warsaw_y', 'hongkong', 'madrid', 'yupei_d', 'donghai', 'shuntian',
                 'lhasa', 'yingtian', 'brussels', 'chicago', 'athens', 'songyuan', 'steppe', 'leedsa', 'mist', 'iolite', 'moscow',  'pond',
								 'warsaw', 'chagall','warhol', 'erhu', 'byron', 'guitar', 'yili', 'prague', 'somalia', 'zephyr', 'suiren', 'coral', 'arctic', 'dew',
								 'klee', 'dash', 'piano', 'yupei', 'pudding', 'nezha', 'flute', 'organ', 'spinel','charoite','annibale', 'myron',
								 'pandora', 'popsicle', 'tornado','goya', 'klimt', 'konghou',  'spring', 'lapis', 'kunzite',
								 'flourite', 'creek', 'taiko', 'bixi', 'dali', 'turner', 'violin', 'koto', 'dijun', 'jinghu', 'luming', 
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

only_os = ['dali', 'turner', 'violin', 'koto', 'taiko', 'jinghu', 'luming', 'serenity', 'emerald_r', 'xuanyuan', 'dijun', 'tanzanite', 'rodin', 'warm', 'onyx', 'miro', 'zorn', 
					 'uke', 'muyu',	'dada', 'haotian', 'obsidian', 'beryl', 'amethyst', 'malachite', 'rothko', 'degas',
					 'flame', 'lake','spring', 'flare', 'spark', 'goku', 'ruyi', 'moon', 'breeze', 'vermeer', 'ruan',
					 'dizi', 'peridot', 'aurora', 'chenfeng', 'duchamp', 'houji', 'manet', 'sheng', 'shennong', 'shennong_t']

cn_devices = ['sheng', 'ziyi', 'cetus', 'lisa', 'pissarro', 'ruyi', 'babylon', 'dagu', 'daumier', 'garnet', 'gold', 'houji', 'lightcm', 'liuqin', 'manet', 'matisse', 'mayfly', 'psyche', 'rubens', 'shennong', 'socrates', 'thor', 'unicorn', 'vermeer', 'xun', 'yudi', 'yuechu', 'zircon', 'zizhan']
gb_devices = ['agate', 'aristotle', 'fire', 'moonstone', 'plato', 'rock', 'sea', 'sunstone', 'sweet_k6a', 'taoyao', 'tapas', 'topaz']
both_regions = ['aurora', 'corot', 'cupid', 'diting', 'duchamp', 'earth', 'fuxi', 'ingres', 'ishtar', 'light', 'marble', 'mondrian', 'nuwa', 'pipa', 'redwood', 'ruby', 'sky', 'yunluo', 'zeus']

order = ['umi', 'cmi', 'cas', 'thyme', 'venus', 'star', 'lisa', 'pissarro_in', 'agate', 'vili', 'cupid', 'zeus', 'psyche',
				 'daumier', 'taoyao', 'mayfly', 'unicorn', 'thor', 'plato', 'fuxi', 'nuwa', 'ishtar', 'aristotle',
				 'houji', 'shennong', 'shennong_t', 'aurora', 'degas', 'dada', 'haotian', 'xuanyuan', 'dijun', 'goya', 'klimt', 'pudding', 'pandora',
				 'byron', 'popsicle', 'nezha', 'chagall','warhol', 'hongkong', 'madrid', 'lhasa',
				 'nabu', 'enuma', 'elish', 'dagu', 'pipa',
				 'liuqin', 'yudi', 'sheng', 'uke', 'muyu', 'jinghu', 'violin', 'piano', 'yupei',  'shuntian', 'yingtian',
				 'odin', 'cetus', 'zizhan', 'babylon', 'goku', 'ruyi', 'bixi', 'mona',
				 'zijin', 'ziyi', 'yuechu', 'chenfeng', 'luming', 'konghou',
				 'fire', 'earth', 'sky', 'gale', 'moon', 'air', 'lake', 'flame', 'creek', 'dew', 'tornado', 'spring', 'evergo', 'light', 'lightcm', 'veux', 'xaga', 'pissarro',
				 'spes', 'spesn', 'viva', 'vida', 'fleur', 'opal', 'sunstone', 'ruby', 'redwood', 'pearl', 'marble', 'tapas', 'topaz',
				 'sweet_k6a', 'sea', 'gold', 'breeze', 'garnet', 'emerald', 'zircon', 'tanzanite', 'obsidian', 'beryl', 'malachite', 'amethyst', 'sapphire', 'sapphiren', 'emerald_r', 'spinel',
				 'kunzite', 'lapis', 'coral', 'flourite', 'mist', 'iolite', 'zephyr', 'brussels', 'peridot', 'rodin', 'onyx', 'klee', 'dash', 'alioth',
				 'charoite', 'haydn', 'ares', 'munch', 'rubens', 'matisse', 'ingres', 'diting', 'rembrandt', 'mondrian', 'socrates', 'corot', 'duchamp',
				 'vermeer', 'manet', 'rothko', 'zorn', 'miro', 'dali', 'annibale', 'prague', 'warsaw', 'myron',
				 'yunluo', 'xun', 'erhu', 'guitar', 'flare', 'spark', 'koto', 'taiko', 'flute', 'organ', 'dizi', 'ruan', 'turner', 'yili', 'warm', 'serenity', 'arctic', 'somalia', 'evergreen', 'rock', 'moonstone']

branches = [
	{
		"code": "",
		"idtag": "CnOO",
		"tag": "CNXM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "CnOB",
		"tag": "CNXM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "Beta",
		"tag": "CNXM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "Dev",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_alpha",
		"idtag": "CNAL",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "CNST",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "CNTT",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "CNUT",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "CNLT",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "",
		"idtag": "GOST",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "2"
	},
	{
		"code": "_demo",
		"idtag": "CnOD",
		"tag": "CNDM",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_stdee",
		"idtag": "EPSTD",
		"tag": "",
		"region": "cn",
		"carrier": [""],
		"zone": "1"
	},
	{
		"code": "_ep_stdce",
		"idtag": "EPSCE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_yunke",
		"idtag": "EPYKE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_xy",
		"idtag": "EPXYE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_yy",
		"idtag": "EPYYE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_sdlybjcg",
		"idtag": "EPSDL",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_tbkj",
		"idtag": "EPTBK",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_tl",
		"idtag": "EPTLE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_tly",
		"idtag": "EPTLY",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_xdja",
		"idtag": "EPXDJ",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_yx",
		"idtag": "EPYXE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_kywl",
		"idtag": "EPKYW",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_cqrcb",
		"idtag": "EPCQR",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_ec",
		"idtag": "EPECE",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_sxht",
		"idtag": "EPSXH",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_yfan",
		"idtag": "EPYFA",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_tkgwdl",
		"idtag": "EPTKG",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_ep_cjcc",
		"idtag": "EPCJC",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_pre_dpp",
		"idtag": "ADPC",
		"tag": "",
		"region": "cn",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_hk_global",
		"idtag": "CNHK",
		"tag": "",
		"region": "hk",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_tw_global",
		"idtag": "CNTP",
		"tag": "TWXM",
		"region": "tw",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_global",
		"idtag": "GDev",
		"tag": "",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_global",
		"idtag": "GBOO",
		"tag": "MIXM",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_global",
		"idtag": "GBOO",
		"tag": "MIDM",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_dc_global",
		"idtag": "GBDC",
		"tag": "MIDC",
		"region": "global",
		"carrier": ["dc"],
		"zone": "2"
	},
	{
		"code": "_h3g_global",
		"idtag": "GBHG",
		"tag": "MIHG",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_pre_dpp_global",
		"idtag": "ADPG",
		"tag": "",
		"region": "global",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_eea_global",
		"idtag": "EEAO",
		"tag": "EUXM",
		"region": "eea",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_eea_global",
		"idtag": "EEAD",
		"tag": "EUDM",
		"region": "eea",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_eea_or_global",
		"idtag": "EUOR",
		"tag": "EUOR",
		"region": "eea",
		"carrier": ["orange"],
		"zone": "2"
	},
	{
		"code": "_eea_vf_global",
		"idtag": "EUVF",
		"tag": "EUVF",
		"region": "eea",
		"carrier": ["vodafone"],
		"zone": "2"
	},
	{
		"code": "_eea_hg_global",
		"idtag": "EUHG",
		"tag": "EUHG",
		"region": "eea",
		"carrier": ["h3g"],
		"zone": "2"
	},
	{
		"code": "_eea_tf_global",
		"idtag": "EUTF",
		"tag": "EUTF",
		"region": "eea",
		"carrier": ["tf"],
		"zone": "2"
	},
	{
		"code": "_eea_sf_global",
		"idtag": "EUSF",
		"tag": "EUSF",
		"region": "eea",
		"carrier": ["sfr"],
		"zone": "2"
	},
	{
		"code": "_eea_ti_global",
		"idtag": "EUTI",
		"tag": "EUTI",
		"region": "eea",
		"carrier": ["tim"],
		"zone": "2"
	},
	{
		"code": "_eea_by_global",
		"idtag": "EUBY",
		"tag": "EUBY",
		"region": "eea",
		"carrier": ["by"],
		"zone": "2"
	},
	{
		"code": "_ru_global",
		"idtag": "RUSO",
		"tag": "RUXM",
		"region": "ru",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_in_global",
		"idtag": "INSO",
		"tag": "INXM",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_in_rf_global",
		"idtag": "INRF",
		"tag": "INRF",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_in_fk_global",
		"idtag": "INSO",
		"tag": "INFK",
		"region": "in",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_id_global",
		"idtag": "IDSO",
		"tag": "IDXM",
		"region": "id",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "",
		"idtag": "MYGS",
		"tag": "",
		"region": "my",
		"carrier": ["", "chinatelecom", "chinamobile", "chinaunicom"],
		"zone": "2"
	},
	{
		"code": "_sg_global",
		"idtag": "SGGS",
		"tag": "",
		"region": "sg",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_sg_global",
		"idtag": "SGGD",
		"tag": "",
		"region": "sg",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_th_as_global",
		"idtag": "THAS",
		"tag": "THAS",
		"region": "th",
		"carrier": ["as"],
		"zone": "2"
	},
	{
		"code": "_tr_global",
		"idtag": "TRSO",
		"tag": "TRXM",
		"region": "tr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_jp_kd_global",
		"idtag": "JPKD",
		"tag": "JPKD",
		"region": "jp",
		"carrier": ["kd"],
		"zone": "2"
	},
	{
		"code": "_jp_global",
		"idtag": "JAPS",
		"tag": "JPXM",
		"region": "jp",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_jp_sb_global",
		"idtag": "JPSB",
		"tag": "JPSB",
		"region": "jp",
		"carrier": ["sb"],
		"zone": "2"
	},
	{
		"code": "_kr_global",
		"idtag": "SKSO",
		"tag": "KRXM",
		"region": "kr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_kr_gu_global",
		"idtag": "SKLG",
		"tag": "KRGU",
		"region": "kr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_kr_kt_global",
		"idtag": "SKKT",
		"tag": "KRKT",
		"region": "kr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_kr_sk_global",
		"idtag": "SKSK",
		"tag": "KRSK",
		"region": "kr",
		"carrier": [""],
		"zone": "2"
	},
	{
		"code": "_lm_cr_global",
		"idtag": "LMCR",
		"tag": "LMCR",
		"region": "lm",
		"carrier": ["cr"],
		"zone": "2"
	},
	{
		"code": "_mx_tc_global",
		"idtag": "MXTC",
		"tag": "MXTC",
		"region": "mx",
		"carrier": ["tc"],
		"zone": "2"
	},
	{
		"code": "_cl_en_global",
		"idtag": "CLEN",
		"tag": "CLEN",
		"region": "cl",
		"carrier": ["en"],
		"zone": "2"
	},
	{
		"code": "_mx_at_global",
		"idtag": "MXAT",
		"tag": "MXAT",
		"region": "mx",
		"carrier": ["at"],
		"zone": "2"
	},
	{
		"code": "_za_mt_global",
		"idtag": "ZAMT",
		"tag": "ZAMT",
		"region": "za",
		"carrier": ["mt"],
		"zone": "2"
	},
	{
		"code": "_za_vc_global",
		"idtag": "ZAVC",
		"tag": "ZAVC",
		"region": "za",
		"carrier": ["vc"],
		"zone": "2"
	},
	{
		"code": "_lm_ms_global",
		"idtag": "LMMS",
		"tag": "LMMS",
		"region": "lm",
		"carrier": ["movistar"],
		"zone": "2"
	},
	{
		"code": "_gt_tg_global",
		"idtag": "GTTG",
		"tag": "GTTG",
		"region": "gt",
		"carrier": ["tg"],
		"zone": "2"
	},
	{
		"code": "_id_global",
		"idtag": "IDDM",
		"tag": "IDDM",
		"region": "id",
		"carrier": [""],
		"zone": "2"
	}
]

flags = {
	"mist": "mist",
	"mist_demo": "mist",
	"iolite": "iolite",
	"iolite_demo": "iolite",
	"HOUJI": "houji",
	"HOUJIDEMO": "houji",
	"houji": "houji",
	"SERENITYZAVCGlobal": "serenity",
	"serenity_za_vc_global": "serenity",
	"flourite_demo": "flourite",
	"flourite": "flourite",
	"houji_demo": "houji",
	"houji_global": "houji",
	"HOUJIGlobal": "houji",
	"zephyr_tw_global": "zephyr",
	"zephyr_eea_global": "zephyr",
	"myron": "myron",
	"koto_id_global": "koto",
	"mist_eea_global": "mist",
	"arctic_in_global": "arctic",
	"somalia": "somalia",
	"spring_tr_global": "spring",
	"charoite_global": "charoite",
	"charoite_eea_global": "charoite",
	"charoite_ru_global": "charoite",
	"charoite_tr_global": "charoite",
	"charoite_dc_global": "charoite",
	"iolite_global": "iolite",
	"brussels_tw_global": "brussels",
	"brussels_global": "brussels",
	"brussels_dc_global": "brussels",
	"brussels_jp_global": "brussels",
	"iolite_tw_global": "iolite",
	"iolite_dc_global": "iolite",
	"iolite_eea_global": "iolite",
	"zephyr_global": "zephyr",
	"kunzite_in_global": "kunzite",
	"flourite_eea_global": "flourite",
	"warhol_ru_global": "warhol",
	"warhol_tr_global": "warhol",
	"klee": "klee",
	"dash": "dash",
	"klee_demo": "klee",
	"dash_demo": "dash",
	"chagall": "chagall",
	"chagall_demo": "chagall",
	"warhol": "warhol",
	"warhol_demo": "warhol",
	"pudding_eea_global": "pudding",
	"pudding_global": "pudding",
	"pudding_id_global": "pudding",
	"pudding_in_global": "pudding",
	"pudding_tw_global": "pudding",
	"pudding_ru_global": "pudding",
	"pudding_tr_global": "pudding",
	"pudding_dc_global":"pudding",
	"nezha_dc_global":"nezha",
	"pudding_lm_cr_global": "pudding",
	"nezha_lm_cr_global": "nezha",
	"nezha_id_global": "nezha",
	"nezha_global": "nezha",
	"nezha_tw_global": "nezha",
	"nezha_eea_global": "nezha",
	"nezha_in_global": "nezha",
	"nezha_ru_global": "nezha",
	"nezha_tr_global": "nezha",
	"somalia_demo": "somalia",
	"byron": "byron",
	"nezha_dpp": "nezha",
	"pudding_dpp": "pudding",
	"pudding_dpp_global": "pudding",
	"nezha_dpp_global": "nezha",
	"klimt_dpp_global": "klimt",
	"byron_demo": "byron",
	"flourite_lm_cr_global": "flourite",
	"kunzite_global": "kunzite",
	"arctic_id_global": "arctic",
	"kunzite_tw_global": "kunzite",
	"kunzite_eea_global": "kunzite",
	"kunzite_ru_global": "kunzite",
	"kunzite_lm_cr_global": "kunzite",
	"spring_jp_global": "spring",
	"kunzite_id_global": "kunzite",
	"flourite_tw_global": "flourite",
	"flourite_global": "flourite",
	"flourite_ru_global": "flourite",
	"flourite_tr_global": "flourite",
	"spinel_tw_global": "spinel",
	"spinel_global": "spinel",
	"spinel_dc_global": "spinel",
	"mist_in_global": "mist",
	"spinel_eea_global": "spinel",
	"lapis_lm_cr_global": "lapis",
	"spinel_lm_cr_global": "spinel",
	"charoite_lm_cr_global": "charoite",
	"leedsa_id_global": "leedsa",
	"leedsa_tw_global": "leedsa",
	"spinel_ru_global": "spinel",
	"spinel_id_global": "spinel",
	"spinel_tr_global": "spinel",
	"songyuan_global": "songyuan",
	"songyuan_eea_global": "songyuan",
	"songyuan_ru_global": "songyuan",
	"songyuan_tr_global": "songyuan",
	"songyuan_jp_global": "songyuan",
	"leedsa_dc_global": "leedsa",
	"athens_tw_global": "athens",
	"athens_tr_global": "athens",
	"athens_global": "athens",
	"athens_id_global": "athens",
	"athens_ru_global": "athens",
	"athens_eea_global": "athens",
	"mist_tw_global": "mist",
	"mist_global": "mist",
	"steppe_tw_global": "steppe",
	"songyuan_tw_global": "songyuan",
	"steppe_in_global": "steppe",
	"steppe_id_global": "steppe",
	"steppe_tr_global": "steppe",
	"leedsa_jp_global": "leedsa",
	"lapis_global": "lapis",
	"steppe_eea_global": "steppe",
	"lapis_id_global": "lapis",
	"lapis_tw_global": "lapis",
	"lapis_eea_global": "lapis",
	"lapis_ru_global": "lapis",
	"lapis_jp_global": "lapis",
	"lapis_in_global": "lapis",
	"lapis_tr_global": "lapis",
	"lapis_dc_global": "lapis",
	"kunzite_dc_global": "kunzite",
	"flourite_dc_global": "flourite",
	"flourite_id_global": "flourite",
	"myron_demo": "myron",
	"annibale": "annibale",
	"guitar": "guitar",
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
	"nezha":"nezha",
	"flute": "flute",
	"flute_demo": "flute",
	"flourite_in_global": "flourite",
	"myron_id_global": "myron",
	"nezha_demo":"nezha",
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
	"leedsa_tr_global": "leedsa",
	"iolite_in_global": "iolite",
	"pudding_ep_stdee": "pudding",
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
	"steppe": "steppe",
	"amethyst_ep_stdee":"amethyst",
	"annibale_ep_stdee":"annibale",
	"flourite_ep_stdee":"flourite",
	"haotian_ep_stdee": "haotian",
	"somalia_ep_stdee": "somalia",
	"tornado_ep_stdee": "tornado",
	"spring_ep_stdee": "spring",
	"taiko_ep_stdee": "taiko",
	"zorn_ep_stdee": "zorn",
	"xuanyuan_ep_stdee": "xuanyuan",
	"rodin_ep_stdee": "rodin",
	"uke_ep_stdee": "uke",
	"muyu_ep_stdee": "muyu",
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
	"erhu": "erhu",
	"erhu_tw_global": "erhu",
	"erhu_global": "erhu",
	"erhu_ru_global": "erhu",
	"erhu_id_global": "erhu",
	"chagall_tw_global": "chagall",
	"chagall_global": "chagall",
	"chagall_dc_global": "chagall",
	"chagall_eea_global": "chagall",
	"chagall_ru_global": "chagall",
	"chagall_id_global": "chagall",
	"chagall_tr_global": "chagall",
	"chagall_in_global": "chagall",
	"chagall_lm_cr_global": "chagall",
	"warhol_tw_global": "warhol",
	"warhol_global": "warhol",
	"warhol_dc_global": "warhol",
	"warhol_eea_global": "warhol",
	"warhol_id_global": "warhol",
	"warhol_jp_global": "warhol",
	"warhol_lm_cr_global": "warhol",
	"arctic_lm_cr_global": "arctic",
	"guitar_tw_global": "guitar",
	"guitar_eea_global": "guitar",
	"guitar_ru_global": "guitar",
	"guitar_id_global": "guitar",
	"guitar_tr_global": "guitar",
	"arctic_dc_global": "arctic",
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
	"pond":"pond",
	"athens": "athens",
	"athens_demo": "athens",
	"songyuan": "songyuan",
	"songyuan_demo": "songyuan",
	"steppe_global": "steppe",
	"leedsa_global": "leedsa",
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
	"lhasa": "lhasa",
	"lhasa_demo": "lhasa",
	"yingtian": "yingtian",
	"yingtian_demo": "yingtian",
	"steppe_dc_global": "steppe",
	"uke_id_global":"uke",
	"uke_ru_global":"uke",
	"uke_tw_global":"uke",
	"uke_eea_global":"uke",
	"uke_global":"uke",
	"arctic_tr_global": "arctic",
	"xuanyuan_tw_global":"xuanyuan",
	"xuanyuan_global":"xuanyuan",
	"xuanyuan_dc_global":"xuanyuan",
	"xuanyuan_eea_global":"xuanyuan",
	"xuanyuan_ru_global":"xuanyuan",
	"xuanyuan_id_global":"xuanyuan",
	"xuanyuan_tr_global":"xuanyuan",
	"dada_tw_global":"dada",
	"dada_global":"dada",
	"organ":"organ",
	"organ_in_global": "organ",
	"dada_dc_global":"dada",
	"annibale_eea_global":"annibale",
	"annibale_global": "annibale",
	"annibale_id_global": "annibale",
	"annibale_tr_global": "annibale",
	"annibale_tw_global": "annibale",
	"annibale_ru_global": "annibale",
	"flute_in_global": "flute",
	"myron_tw_global": "myron",
	"myron_global": "myron",
	"myron_eea_global": "myron",
	"dada_eea_global":"dada",
	"dada_ru_global":"dada",
	"dada_in_global":"dada",
	"dada_id_global":"dada",
	"dada_lm_cr_global":"dada",
	"uke_tr_global":"uke",
	"muyu_demo":"muyu",
	"prague": "prague",
	"prague_demo": "prague",
	"yili": "yili",
	"yili_demo":"yili",
	"beryl_ep_stdee":"beryl",
	"BERYLEPSTDEE":"beryl",
	"dada":"dada",
	"warsaw": "warsaw",
	"warsaw_demo": "warsaw",
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
	"piano_id_global": "piano",
	"piano_tw_global": "piano",
	"piano_eea_global": "piano",
	"piano_ru_global": "piano",
	"piano_tr_global": "piano",
	"piano_global": "piano",
	"yupei_global": "yupei",
	"arctic_global": "arctic",
	"yupei_eea_global": "yupei",
	"yupei_ru_global": "yupei",
	"yupei_id_global": "yupei",
	"yupei_in_global": "yupei",
	"yupei_tw_global": "yupei",
	"yupei_tr_global": "yupei",
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
	"spring_dc_global": "spring",
	"aristotle_lm_cr_global":"aristotle",
	"ARISTOTLELMCRGlobal":"aristotle",
	"aristotle_dc_global":"aristotle",
	"ARISTOTLEDCGlobal":"aristotle",
	"aristotle_cl_en_global":"aristotle",
	"ARISTOTLECLENGlobal":"aristotle",
	"uke_in_global":"uke",
	"guitar_global": "guitar",
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
	"dash_global": "dash",
	"dash_eea_global": "dash",
	"dash_ru_global": "dash",
	"dash_tw_global": "dash",
	"dash_in_global": "dash",
	"dash_id_global": "dash",
	"dash_tr_global": "dash",
	"klee_tw_global": "klee",
	"klee_global": "klee",
	"klee_eea_global": "klee",
	"klee_ru_global": "klee",
	"klee_id_global": "klee",
	"klee_tr_global": "klee",
	"klee_in_global": "klee",
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
	"spring_tw_global": "spring",
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
	"iolite_ru_global": "iolite",
	"iolite_id_global": "iolite",
	"iolite_tr_global": "iolite",
	"mist_dc_global": "mist",
	"zephyr_dc_global": "zephyr",
	"zephyr_ru_global": "zephyr",
	"zephyr_id_global": "zephyr",
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
	"leedsa_eea_global": "leedsa",
	"leedsa_ru_global": "leedsa",
	"SHENGGlobal":"sheng",
	"sheng_global":"sheng",
	"SHENGRUGlobal":"sheng",
	"sheng_ru_global":"sheng",
	"GOLDINGlobal":"gold",
	"gold_in_global":"gold",
	"gold_th_as_global":"gold",
	"GOLDTHASGlobal":"gold",
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
	"darwin_global": "darwin",
	"mist_tr_global": "mist",
	"mist_id_global": "mist",
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
	"charoite_mx_tc_global": "charoite",
	"COROTJPSBGlobal": "corot",
	"corot_jp_sb_global": "corot",
	"creek_mx_tc_global": "creek",
	"CUPIDMXTCGlobal": "cupid",
	"dada_mx_tc_global": "dada",
	"DEGASJPKDGlobal": "degas",
	"degas_jp_kd_global": "degas",
	"DEGASMXTCGlobal": "degas",
	"degas_mx_tc_global": "degas",
	"dew_mx_tc_global": "dew",
	"DITINGJPSBGlobal": "diting",
	"DITINGMXTCGlobal": "diting",
	"EARTHMXTCGlobal": "eatrh",
	"EMERALDMXTCGlobal": "emerald",
	"emerald_mx_tc_global": "emerald",
	"FIREMXTCGlobal": "fire",
	"fire_mx_tc_global": "fire",
	"GALEMXTCGlobal": "gale",
	"gale_mx_tc_global": "gale",
	"GARNETJPKDGlobal": "garnet",
	"garnet_jp_kd_global": "garnet",
	"GARNETMXTCGlobal": "garnet",
	"garnet_mx_tc_global": "garnet",
	"goya_mx_tc_global": "goya",
	"klimt_mx_tc_global": "klimt",
	"LAKEMXTCGlobal": "lake",
	"lake_mx_tc_global": "lake",
	"lapis_mx_tc_global": "lapis",
	"MALACHITEMXTCGlobal": "malachite",
	"malachite_mx_tc_global": "malachite",
	"MOONMXTCGlobal": "moon",
	"moon_mx_tc_global": "moon",
	"nezha_mx_tc_global": "nezha",
	"obsidian_mx_tc_global": "obsidian",
	"emerald_mx_tc_global" : "emerald",
	"OPALMXTCGlobal" : "opal",
	"pudding_mx_tc_global" : "pudding",
	"ROTHKOJPSBGlobal" : "rothko",
	"ROTHKOMXTCGlobal" : "rothko",
	"rothko_mx_tc_global" : "rothko",
	"SAPPHIREMXTCGlobal" : "sapphire",
	"sapphire_mx_tc_global" : "sapphire",
	"SEAMXTCGlobal" : "sea",
	"sea_mx_tc_global" : "sea",
	"SERENITYMXTCGlobal" : "serenity",
	"SKYJPKDGlobal" : "sky",
	"sky_jp_kd_global" : "sky",
	"SKYJPSBGlobal" : "sky",
	"sky_jp_sb_global" : "sky",
	"spinel_mx_tc_global" : "spinel",
	"spring_jp_sb_global" : "spring",
	"TANZANITEMXTCGlobal" : "tanzanite",
	"tanzanite_mx_tc_global" : "tanzanite",
	"TAPASMXTCGlobal" : "tapas",
	"tapas_mx_tc_global" : "tapas",
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
	"arctic_ru_global": "arctic",
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
	"amethyst_mx_tc_global": "amethyst",
	"AMETHYSTMXTCGlobal": "amethyst",
	"ARISTOTLEJPKDGlobal": "aristotle",
	"aristotle_jp_kd_global": "aristotle",
	"ARISTOTLEMXTCGlobal": "aristotle",
	"aristotle_mx_tc_global": "aristotle",
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
	"brussels_eea_global": "brussels",
	"earth_eea_global": "earth",
	"FIRERUGlobal": "fire",
	"fire_id_global": "fire",
	"songyuan_id_global": "songyuan",
	"brussels_id_global": "brussels",
	"brussels_ru_global": "brussels",
	"brussels_tr_global": "brussels",
	"FIREIDGlobal": "fire",
	"brussels_in_global": "brussels",
	"shuntian": "shuntian",
	"hongkong": "hongkong",
	"madrid": "madrid",
	"shuntian_demo": "shuntian",
	"hongkong_demo": "hongkong",
	"zephyr_lm_cr_global": "zephyr",
	"mist_lm_cr_global": "mist",
	"iolite_lm_cr_global": "iolite",
	"brussels_lm_cr_global": "brussels",
	"steppe_lm_cr_global": "steppe",
	"leedsa_lm_cr_global": "leedsa",
	"madrid_demo": "madrid",
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
	"zephyr_tr_global": "zephyr",
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
	"organ_ru_global": "organ",
	"organ_dc_global": "organ",
	"YUDIDEMO": "yudi",
	"dew_mx_at_global": "dew",
	"somalia_in_global": "somalia",
	"tornado_in_global": "tornado",
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
	"ZEUSMXTCGlobal": "zeus",
	"rothko_jp_sb_global": "rothko",
	"darwin_eea_global": "darwin",
	"darwin_ru_global": "darwin",
	"darwin_tr_global": "darwin",
	"arctic_mx_tc_global": "arctic",
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
	"arctic_eea_global": "arctic",
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
	

# 设备数据缓存
_device_cache = {}

def localData(codename):
	"""获取设备数据，使用缓存机制提高效率"""
	global _device_cache
	
	# 检查缓存中是否存在数据
	if codename in _device_cache:
		return _device_cache[codename]
	
	# 读取文件
	device_file = get_platform_path(f"public/data/devices/{codename}.json")
	try:
		with open(device_file, 'r', encoding='utf-8') as f:
			devdata = json.load(f)
		
		# 存入缓存
		_device_cache[codename] = devdata
		return devdata
	except FileNotFoundError:
		print(f"设备文件不存在: {device_file}")
		return {}
	except json.JSONDecodeError:
		print(f"设备文件格式错误: {device_file}")
		return {}
	except Exception as e:
		print(f"读取设备文件时出错: {e}")
		return {}

def db_job(sql):
	"""执行SQL查询并返回所有结果"""
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
		result = cursor.fetchall()
		return result if result is not None else []  # 确保返回列表
	except Exception as e:
		print(sql, e)
		return []  # 异常时返回空列表而不是None
	finally:
		if cnx:
			cnx.close()


def db_job_params(sql, params):
	"""参数化执行SQL（防注入），返回所有结果"""
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
		cursor.execute(sql, params)
		result = cursor.fetchall()
		return result if result is not None else []
	except Exception as e:
		print(sql, e)
		return []
	finally:
		if cnx:
			cnx.close()


# ==================== 更新日志多语言分组存储（logs 表） ====================
# 同一句日志的各语言版本共存于 logs 表的一行（logs_zh / logs_zh_tw / logs_en ...），
# content 为主内容（中文优先 → 英文 → 最早原文），content_hash 为其 MD5。
# roms.logs 单列存 ID 引用结构：
#   [[模块ID, [条目ID, ...], 语言掩码], ...]   如 [[3, [6, 8], 5], [32, [45, 48], 8]]
# 语言掩码是 21 位整数，第 i 位对应 CHANGELOG_LOCALES 第 i 项，只追加、不插队。
# 结构与约定与 hub.miuier.com 的 data/scripts/miroms/logs_store.py 一致。

import hashlib
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple, cast

_logger = logging.getLogger(__name__)

# 语种登记表：column=logs 表列名（同时是前端读取的键名）、api=请求接口的 l 参数
# （无译文的语种会回落英文）、site=站点 i18n locale、zh=中文说明、name=语言自称、
# region=覆盖区域（仅日志输出用）。只追加、不插队：语言掩码按本表顺序取位。
CHANGELOG_LOCALES = [
	{"column": "logs_zh",    "zh": "简体中文", "api": "zh_CN", "site": "zh-Hans", "name": "简体中文",       "region": "cn"},
	{"column": "logs_zh_tw", "zh": "繁体中文", "api": "zh_TW", "site": "zh-Hant", "name": "繁體中文",       "region": "tw/hk/mo"},
	{"column": "logs_en",    "zh": "英文",     "api": "en_US", "site": "en",      "name": "English",        "region": "global"},
	{"column": "logs_ja",    "zh": "日文",     "api": "ja_JP", "site": "ja",      "name": "日本語",          "region": "jp"},
	{"column": "logs_ko",    "zh": "韩文",     "api": "ko_KR", "site": "ko",      "name": "한국어",          "region": "kr"},
	{"column": "logs_ru",    "zh": "俄文",     "api": "ru_RU", "site": "ru",      "name": "Русский",        "region": "ru"},
	{"column": "logs_uk",    "zh": "乌克兰文", "api": "uk_UA", "site": "uk",      "name": "Українська",     "region": "eea"},
	{"column": "logs_pl",    "zh": "波兰文",   "api": "pl_PL", "site": "pl",      "name": "Polski",         "region": "eea"},
	{"column": "logs_de",    "zh": "德文",     "api": "de_DE", "site": "de",      "name": "Deutsch",        "region": "eea"},
	{"column": "logs_fr",    "zh": "法文",     "api": "fr_FR", "site": "fr",      "name": "Français",       "region": "eea"},
	{"column": "logs_it",    "zh": "意大利文", "api": "it_IT", "site": "it",      "name": "Italiano",       "region": "eea"},
	{"column": "logs_es",    "zh": "西班牙文", "api": "es_ES", "site": "es",      "name": "Español",        "region": "mx/lm/cl/gt"},
	{"column": "logs_pt",    "zh": "葡萄牙文", "api": "pt_BR", "site": "pt",      "name": "Português",      "region": "pt/br"},
	{"column": "logs_tr",    "zh": "土耳其文", "api": "tr_TR", "site": "tr",      "name": "Türkçe",         "region": "tr"},
	{"column": "logs_id",    "zh": "印尼文",   "api": "id_ID", "site": "id",      "name": "Bahasa Indonesia", "region": "id"},
	{"column": "logs_vi",    "zh": "越南文",   "api": "vi_VN", "site": "vi",      "name": "Tiếng Việt",     "region": "vn"},
	{"column": "logs_th",    "zh": "泰文",     "api": "th_TH", "site": "th",      "name": "ไทย",            "region": "th"},
	{"column": "logs_ar",    "zh": "阿拉伯文", "api": "ar_EG", "site": "ar",      "name": "العربية",        "region": "eg/sa/ma"},
	{"column": "logs_in",    "zh": "印地文",   "api": "hi_IN", "site": "hi",      "name": "हिन्दी",          "region": "in"},
	{"column": "logs_ug",    "zh": "维吾尔文", "api": "ug_CN", "site": "ug",      "name": "ئۇيغۇرچە",        "region": "cn"},
	{"column": "logs_bo",    "zh": "藏文",     "api": "bo_CN", "site": "bo",      "name": "བོད་ཡིག",          "region": "cn"},
]

# 全部语言列名（顺序即 roms.logs 语言掩码的位序）
CHANGELOG_COLUMNS = [item["column"] for item in CHANGELOG_LOCALES]

# 除简体中文与英文外的其他语言列（保留给按语种批处理的脚本使用）
CHANGELOG_EXTRA_COLUMNS = [c for c in CHANGELOG_COLUMNS if c not in ("logs_zh", "logs_en")]

# 判断「接口没有该语种译文」的基准列：与英文完全相同即视为回落
CHANGELOG_BASE_COLUMN = "logs_en"


def find_changelog_locale(value):
	"""按列名 / api locale / 站点 locale / 语言名查找语种配置（大小写不敏感）"""
	key = str(value or "").strip().lower()
	for item in CHANGELOG_LOCALES:
		if key in (item["column"].lower(), item["api"].lower(), str(item["site"]).lower(), item["name"].lower()):
			return item
	return {}


class DatabaseManager:
	"""数据库操作：参数化 SQL + 共享连接复用

	写入类调用传 raise_on_error=True，避免写失败被静默忽略
	（db_job / db_job_params 仍保持历史行为，返回 [] / None）。
	"""

	_shared_connection = None

	@classmethod
	def _get_connection(cls):
		"""获取数据库连接（复用共享连接，掉线自动重连）"""
		if cls._shared_connection is not None:
			try:
				cls._shared_connection.ping(reconnect=True)
				return cls._shared_connection
			except Exception:
				cls._shared_connection = None
		cls._shared_connection = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True,
			connect_timeout=10,
			read_timeout=30,
			write_timeout=30
		)
		return cls._shared_connection

	@classmethod
	def _close_shared(cls):
		"""关闭共享连接"""
		if cls._shared_connection is not None:
			try:
				cls._shared_connection.close()
			except Exception:
				pass
			cls._shared_connection = None

	@classmethod
	def execute(cls, sql, params=None, fetch_one=False, raise_on_error=False):
		"""执行参数化 SQL；出错时按 raise_on_error 决定抛出或返回 None"""
		cursor = None
		try:
			cursor = cls._get_connection().cursor()
			cursor.execute(sql, params or ())
			return cursor.fetchone() if fetch_one else cursor.fetchall()
		except Exception as e:
			_logger.error(f"SQL执行错误: {sql[:100]}..., 错误: {type(e).__name__}: {e}")
			if raise_on_error:
				raise
			return None
		finally:
			if cursor:
				cursor.close()

	@classmethod
	def query_one(cls, sql, params=None) -> Optional[Tuple[Any, ...]]:
		"""查询单条记录（参数化安全版）：返回单行元组，无结果时返回 None"""
		row = cls.execute(sql, params=params, fetch_one=True)
		# execute 的返回类型同时覆盖 fetchone/fetchall 两种形态，
		# 这里 fetch_one=True 已确定为单行，显式收窄以便调用方按元组取值
		return None if row is None else cast(Tuple[Any, ...], row)

	@classmethod
	def query_all(cls, sql, params=None):
		"""查询所有记录（参数化安全版）"""
		result = cls.execute(sql, params=params, fetch_one=False)
		return result if result else []


class _RowIndex:
	"""内存中的 logs 行池：按语言文本做兼容性去重，冲突则拆成新行

	- `buckets[(type, 语言列, 文本hash)]` -> 行下标列表，用于快速找到「已有该语言文本」的行；
	- 只有在**所有语言都不冲突**（该行对应语言为空或文本相同）时才复用同一行。
	"""

	__slots__ = ('rows', 'buckets', 'by_content', 'splits', 'conflicts')

	def __init__(self):
		self.rows = []
		self.buckets = {}
		self.by_content = {}
		self.splits = 0
		self.conflicts = []

	def seed(self, rows):
		"""把数据库中已有的行灌进行池（保留 id），使写入侧与导出侧共用同一套匹配逻辑"""
		for row in rows:
			self.rows.append({
				'id': int(row['id']),
				'type': row['type'],
				'content': row['content'],
				'texts': dict(row['texts']),
				'dirty': False,
			})
			self._register(len(self.rows) - 1)

	def flush(self):
		"""把行池的变更落库：新行 INSERT，补齐语言的行 UPDATE（COALESCE）

		落库前会校验行池里已有的 id 是否仍然存在：长时间运行的进程（如定时抓取）可能持有
		已被其它进程合并 / 删除的行，若不校验就会往 roms.logs 写死引用。失效的行会针对
		最新数据重新解析（复用幸存的分组，或改为新插入一行）。
		"""
		existing_ids = [int(row['id']) for row in self.rows if row.get('id') is not None]
		stale = LogStore._missing_ids(existing_ids)
		if stale:
			fresh = LogStore.load_index(force=True)
			for row in self.rows:
				if row.get('id') is None or int(row['id']) not in stale:
					continue
				found = fresh.resolve(row['type'], row['texts'])
				if found is not None and fresh.rows[found].get('id') is not None:
					row['id'] = int(fresh.rows[found]['id'])
				else:
					row['id'] = None   # 没有可复用的分组，按新行插入
				row['dirty'] = False
			_logger.warning(f"行池中有 {len(stale)} 个分组已被其它进程删除，已重新解析")

		fills = []
		for row in self.rows:
			if row.get('id') is None:
				row['id'] = LogStore._insert_row(row)
				row['dirty'] = False
			elif row.get('dirty'):
				fills.append((int(row['id']), row['texts']))
				row['dirty'] = False
		for group_id, texts in fills:
			LogStore._fill_row(group_id, texts)
		if fills or any(r.get('id') for r in self.rows):
			LogStore._groups = None

	def _register(self, index):
		row = self.rows[index]
		for column, value in row['texts'].items():
			key = (row['type'], column, LogStore._hash(value))
			bucket = self.buckets.setdefault(key, [])
			if index not in bucket:
				bucket.append(index)
		key = (row['type'], LogStore._hash(row['content']))
		bucket = self.by_content.setdefault(key, [])
		if index not in bucket:
			bucket.append(index)

	def lookup(self, log_type, texts):
		"""只读查找：返回**已包含**这些语言文本的行下标（不复用、不新建）

		用于「行池已建好后」的第二遍遍历（如批量迁移回写 roms.logs），
		保证写出的 id 一定落在已入库的行上。
		"""
		texts = {column: LogStore.normalize(value) for column, value in (texts or {}).items()
				 if column in LogStore.LANG_COLUMNS and LogStore.normalize(value)}
		if not texts:
			return None
		primary = LogStore._primary(texts)
		candidates = []
		seen = set()
		for index in self.by_content.get((log_type, LogStore._hash(primary)), ()):
			seen.add(index)
			candidates.append(index)
		for column, value in texts.items():
			for index in self.buckets.get((log_type, column, LogStore._hash(value)), ()):
				if index not in seen:
					seen.add(index)
					candidates.append(index)
		for index in candidates:
			row = self.rows[index]
			if all(row['texts'].get(column) == value for column, value in texts.items()):
				return index
		return None

	def resolve(self, log_type, texts):
		texts = {column: LogStore.normalize(value) for column, value in (texts or {}).items()
				 if column in LogStore.LANG_COLUMNS and LogStore.normalize(value)}
		if not texts:
			return None
		primary = LogStore._primary(texts)

		candidates = []
		seen = set()
		for index in self.by_content.get((log_type, LogStore._hash(primary)), ()):
			seen.add(index)
			candidates.append(index)
		for column, value in texts.items():
			for index in self.buckets.get((log_type, column, LogStore._hash(value)), ()):
				if index not in seen:
					seen.add(index)
					candidates.append(index)

		for index in candidates:
			row = self.rows[index]
			if all(row['texts'].get(column) in (None, value) for column, value in texts.items()):
				for column, value in texts.items():
					if not row['texts'].get(column):
						row['texts'][column] = value
						row['dirty'] = True
				# 补上中文后主内容以中文为准（保证 content 始终是中文优先）
				zh_text = row['texts'].get(LogStore.ZH_COLUMN)
				if zh_text and row['content'] != zh_text:
					row['content'] = zh_text
					row['dirty'] = True
				self._register(index)
				return index

		if candidates:
			# 主内容相同但译文冲突：另起一行（保证两个 ROM 的日志都能原样还原）
			self.splits += 1
		row = {'id': None, 'type': log_type, 'content': primary, 'texts': dict(texts), 'dirty': False}
		self.rows.append(row)
		index = len(self.rows) - 1
		self._register(index)
		return index


class LogStore:
	"""更新日志的分组存储：写入 logs 表 / 导出各语言原文

	写入：LogStore.write_logs({'logs_zh': zh_obj, 'logs_en': en_obj})  # -> roms.logs 的值
	导出：LogStore.build_localized(parsed)                             # -> {'logs_zh': {...}, ...}
	"""

	TYPE_MODULE = 'module'
	TYPE_LOG = 'log'

	# 语言列（logs_zh 在最前，其余顺序与 CHANGELOG_LOCALES 一致）
	LANG_COLUMNS = tuple(item['column'] for item in CHANGELOG_LOCALES)
	LANG_INDEX = {column: i for i, column in enumerate(LANG_COLUMNS)}
	ZH_COLUMN = 'logs_zh'
	EN_COLUMN = 'logs_en'

	_LANG_COMMENTS = {
		item['column']: f"{item['zh']}（{item['api']}）" for item in CHANGELOG_LOCALES
	}

	_table_ensured = False
	# 整表行池：写入侧用它做「语言不冲突即可复用」的匹配
	_index = None
	# id -> {'type', 'texts'}，导出侧缓存
	_groups = None
	# 最近一次写入的冲突拆行统计
	last_conflicts = []

	# ==================== 基础 ====================

	@classmethod
	def create_sql(cls, table='logs'):
		"""生成 logs 建表语句（列随 CHANGELOG_LOCALES 自动增减）"""
		langs = "\n".join(
			f"  `{column}` longtext COLLATE utf8mb4_bin COMMENT '{cls._LANG_COMMENTS[column]}',"
			for column in cls.LANG_COLUMNS
		)
		return (
			f"CREATE TABLE IF NOT EXISTS `{table}` (\n"
			f"  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键（同一日志的各语言版本共用一行）',\n"
			f"  `type` varchar(8) COLLATE utf8mb4_bin NOT NULL COMMENT '日志类型：module=模块名 / log=日志条目',\n"
			f"  `content` text COLLATE utf8mb4_bin NOT NULL COMMENT '主内容（简体中文；无中文时取英文，再取最早出现的原文）',\n"
			f"  `content_hash` char(32) COLLATE utf8mb4_bin NOT NULL COMMENT 'content 的 MD5（hex），查专用索引（同内容可因译文冲突存在多行）',\n"
			f"{langs}\n"
			f"  PRIMARY KEY (`id`),\n"
			f"  KEY `idx_type_hash` (`type`, `content_hash`)\n"
			f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin"
		)

	@classmethod
	def ensure_table(cls):
		if cls._table_ensured:
			return
		DatabaseManager.execute(cls.create_sql(), raise_on_error=True)
		cls._table_ensured = True

	@staticmethod
	def normalize(content):
		"""主内容归一化：去掉首尾空白（接口原文常带前导空格与尾随空格，归一化后才能正确去重）"""
		return str(content if content is not None else '').strip()

	@staticmethod
	def _hash(content):
		return hashlib.md5(content.encode('utf-8')).hexdigest()

	@classmethod
	def signature(cls, log_type, content, texts):
		"""一行日志的完整签名（类型 + 主内容 + 各语言文本），用于精确匹配已有行"""
		parts = [log_type, content]
		for column in cls.LANG_COLUMNS:
			value = texts.get(column) or ''
			if value:
				parts.append(f'{column}={value}')
		return hashlib.md5('\x1f'.join(parts).encode('utf-8')).hexdigest()

	@staticmethod
	def is_encoded(parsed):
		"""判断解析后的值是否为 ID 引用结构 [[mid, [lids...], mask?], ...]"""
		if not isinstance(parsed, list):
			return False
		for item in parsed:
			if not (isinstance(item, list) and len(item) in (2, 3)
					and isinstance(item[0], int) and isinstance(item[1], list)):
				return False
			if len(item) == 3 and not isinstance(item[2], int):
				return False
		return True

	@staticmethod
	def mask_of(columns):
		"""语言列集合 -> 语言掩码"""
		mask = 0
		for column in columns:
			mask |= 1 << LogStore.LANG_INDEX[column]
		return mask

	@classmethod
	def columns_of(cls, mask):
		"""语言掩码 -> 语言列列表（按 LANG_COLUMNS 顺序）"""
		return [column for i, column in enumerate(cls.LANG_COLUMNS) if (mask >> i) & 1]

	# ==================== 写入侧 ====================

	@staticmethod
	def _primary(texts):
		"""一个分组的「主内容」：优先简体中文，其次英文，最后任一语言"""
		for column in (LogStore.ZH_COLUMN, LogStore.EN_COLUMN):
			value = LogStore.normalize(texts.get(column))
			if value:
				return value
		for value in texts.values():
			value = LogStore.normalize(value)
			if value:
				return value
		return ''

	@classmethod
	def _items(cls, obj):
		"""把一个语言结构规整为 [(模块, [条目, ...]), ...]（去掉空模块）"""
		items = []
		for module, lines in (obj or {}).items():
			if not str(module or '').strip():
				continue
			if not isinstance(lines, list):
				lines = [lines]
			items.append((str(module).strip(), [str(x) for x in lines]))
		return items

	@classmethod
	def shape(cls, obj):
		"""结构指纹：(模块数, 各模块条目数...)，用于判断两门语言能否按序号对齐"""
		items = cls._items(obj)
		return tuple([len(items)] + [len(lines) for _, lines in items])

	@classmethod
	def cluster_languages(cls, langs):
		"""把各语言按结构指纹聚类；只有指纹完全相同的语言才允许按序号对齐

		返回的簇按「含简体中文 → 含英文 → 语言数降序」排序，
		保证总日志以中文结构为主、其余结构作为附加模块追加在后。
		"""
		groups = {}
		for column in cls.LANG_COLUMNS:
			obj = (langs or {}).get(column)
			if not obj:
				continue
			groups.setdefault(cls.shape(obj), []).append(column)

		def rank(item):
			_, cols = item
			if cls.ZH_COLUMN in cols:
				priority = 0
			elif cls.EN_COLUMN in cols:
				priority = 1
			else:
				priority = 2
			return (priority, -len(cols))

		clusters = [cols for _, cols in sorted(groups.items(), key=rank)]
		for cols in clusters:
			cols.sort(key=lambda c: cls.LANG_INDEX[c])
		return clusters

	@classmethod
	def compose(cls, langs):
		"""把多语言结构按「结构指纹聚类 → 簇内按序号对齐」组合成一组分组位置

		返回 [{'texts': {列名: 模块文本}, 'entries': [{'texts': {列名: 条目文本}}, ...],
		       'mask': 语言掩码}, ...]
		"""
		positions = []
		for columns in cls.cluster_languages(langs or {}):
			items = {column: cls._items(langs[column]) for column in columns}
			canonical = columns[0]
			mask = cls.mask_of(columns)
			for index, (_, lines) in enumerate(items[canonical]):
				texts = {}
				for column in columns:
					module = items[column][index][0].strip()
					if module:
						texts[column] = module
				entries = []
				for j in range(len(lines)):
					item = {}
					for column in columns:
						line = items[column][index][1][j]
						if str(line).strip():
							item[column] = str(line).strip()
					entries.append({'texts': item})
				positions.append({'texts': texts, 'entries': entries, 'mask': mask})
		return positions

	@classmethod
	def new_index(cls):
		"""新建一个可跨多次调用共享的内存行池（批量迁移用）"""
		return _RowIndex()

	@classmethod
	def build_rows(cls, positions, index=None, mutate=True):
		"""把分组位置解析成行池与引用关系

		传入 index 可在多次调用间共享行池（如批量迁移时跨 ROM 去重）。
		mutate=False 时只做只读查找（不再补全 / 新建行），用于行池建好后的第二遍遍历。
		返回 (rows, refs)：rows 为待写入行列表；refs 为
		[(模块行下标, [条目行下标, ...], 语言掩码), ...]。
		"""
		index = index if index is not None else _RowIndex()
		resolver = index.resolve if mutate else index.lookup
		refs = []
		for position in positions:
			module_index = resolver(cls.TYPE_MODULE, position['texts'])
			if module_index is None:
				if mutate:
					continue
				raise RuntimeError(f"行池中找不到模块分组: {position['texts']}")
			entry_indices = []
			for entry in position['entries']:
				entry_index = resolver(cls.TYPE_LOG, entry['texts'])
				if entry_index is not None:
					entry_indices.append(entry_index)
			refs.append([module_index, entry_indices, int(position.get('mask', 0))])
		cls.last_conflicts = index.conflicts
		return index.rows, refs

	@classmethod
	def _missing_ids(cls, ids):
		"""返回给定 id 中已不存在的部分（批量查库）"""
		wanted = {int(i) for i in ids}
		if not wanted:
			return set()
		found = set()
		chunk_list = list(wanted)
		for i in range(0, len(chunk_list), 500):
			chunk = chunk_list[i:i + 500]
			rows = DatabaseManager.query_all(
				f"SELECT `id` FROM `logs` WHERE `id` IN ({','.join(['%s'] * len(chunk))})",
				params=tuple(chunk))
			found.update(int(row[0]) for row in rows or [])
		return wanted - found

	@classmethod
	def _fetch_all_rows(cls):
		"""整表载入（id / type / content / texts），作为写入侧的行池来源"""
		columns = ', '.join(f'`{c}`' for c in cls.LANG_COLUMNS)
		rows = DatabaseManager.query_all(
			f"SELECT `id`, `type`, `content`, {columns} FROM `logs`")
		found = []
		for row in rows or []:
			texts = {column: row[3 + i] for i, column in enumerate(cls.LANG_COLUMNS) if row[3 + i]}
			found.append({'id': int(row[0]), 'type': row[1], 'content': row[2], 'texts': texts})
		return found

	@classmethod
	def load_index(cls, force=False):
		"""载入（并缓存）整表行池，供写入侧做「语言不冲突即可复用」的匹配

		只按 content_hash 找候选会让「同一日志、不同主内容」的行永远匹配不上
		（例如 #25 content=相册 与 #27 content=Gallery 其实是同一模块），
		因此写入侧改为在整表行池里按语言文本做兼容匹配，与迁移/导出逻辑完全一致。
		"""
		if cls._index is None or force:
			cls.ensure_table()
			index = _RowIndex()
			index.seed(cls._fetch_all_rows())
			cls._index = index
			_logger.info(f"logs 行池已载入: {len(index.rows)} 条")
		return cls._index

	@classmethod
	def _insert_row(cls, row):
		"""插入一行并返回自增 id"""
		columns = ['`type`', '`content`', '`content_hash`'] + [f'`{c}`' for c in cls.LANG_COLUMNS]
		params = [row['type'], row['content'], cls._hash(row['content'])]
		params.extend([row['texts'].get(c) or None for c in cls.LANG_COLUMNS])
		DatabaseManager.execute(
			f"INSERT INTO `logs` ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
			params=tuple(params), raise_on_error=True,
		)
		found = DatabaseManager.query_one(
			"SELECT `id` FROM `logs` WHERE `type` = %s AND `content_hash` = %s "
			"AND `content` = %s ORDER BY `id` DESC LIMIT 1",
			params=(row['type'], cls._hash(row['content']), row['content']),
		)
		if not found:
			raise RuntimeError(f"logs 表写入后未查到记录: type={row['type']} content={row['content'][:40]!r}")
		return int(found[0])

	@classmethod
	def _fill_row(cls, group_id, texts):
		"""给已有行补齐缺失的语言列（COALESCE，不覆盖已有译文）"""
		sets = [c for c in cls.LANG_COLUMNS if texts.get(c)]
		if not sets:
			return
		DatabaseManager.execute(
			"UPDATE `logs` SET " + ', '.join(f'`{c}` = COALESCE(`{c}`, %s)' for c in sets)
			+ " WHERE `id` = %s",
			params=tuple([texts[c] for c in sets] + [group_id]), raise_on_error=True,
		)

	@classmethod
	def ensure_ids(cls, rows):
		"""把一批内存行落库并返回与 rows 等长的 id 列表

		匹配规则与 load_index 一致：类型相同且各语言不冲突即视为同一行。
		"""
		if not rows:
			return []
		index = cls.load_index()
		result = []
		for row in rows:
			row['sig'] = cls.signature(row['type'], row['content'], row['texts'])
			found = index.resolve(row['type'], row['texts'])
			if found is None:
				raise RuntimeError(f"logs 行解析失败: {row['content'][:40]!r}")
			index.rows[found]['content'] = row['content']
			result.append(found)
		index.flush()
		return [int(index.rows[i]['id']) for i in result]

	@classmethod
	def encode_refs(cls, refs, ids):
		"""refs（行下标引用）+ id 列表 -> roms.logs 的值：[[模块ID,[条目ID,...],掩码],...]"""
		pairs = []
		for module_index, entry_indices, mask in refs:
			pairs.append([ids[module_index], [ids[i] for i in entry_indices], int(mask)])
		return json.dumps(pairs, ensure_ascii=False)

	@classmethod
	def write_logs(cls, langs, dry_run=False, expand_mask=False):
		"""写入一个 ROM 的多语言日志，返回 ID 引用结构 JSON 字符串

		langs = {语言列: 该语言结构}，结构指纹一致的语言会自动合并为一组；
		写入前会把整张 logs 表载入内存行池，按「类型相同 + 各语言不冲突」匹配已有分组
		（同一日志即便主内容不同也能认出来），只补齐缺失语言，不覆盖已有译文。

		expand_mask=True 时语言掩码取「模块分组与全部条目的公共语言」，
		这样复用了库里已有多语言分组时，能顺带拿到中英文之外的其他译文。
		"""
		positions = cls.compose(langs or {})
		index = cls.load_index()
		_, refs = cls.build_rows(positions, index)
		if dry_run:
			ids = [r['id'] if r.get('id') is not None else i + 1 for i, r in enumerate(index.rows)]
			return cls._encode_refs(refs, ids, expand_mask, index.rows)

		index.flush()
		ids = [int(r['id']) for r in index.rows]
		return cls._encode_refs(refs, ids, expand_mask, index.rows)

	@classmethod
	def _encode_refs(cls, refs, ids, expand_mask, rows):
		if not expand_mask:
			return cls.encode_refs(refs, ids)
		pairs = []
		for module_index, entry_indices, mask in refs:
			common = set(rows[module_index]['texts'])
			for entry_index in entry_indices:
				common &= set(rows[entry_index]['texts'])
			new_mask = cls.mask_of([c for c in cls.LANG_COLUMNS if c in common])
			pairs.append([ids[module_index], [ids[i] for i in entry_indices], new_mask or mask])
		return json.dumps(pairs, ensure_ascii=False)

	@classmethod
	def encode_value(cls, value, canonical_column=ZH_COLUMN):
		"""待写入列的值：原文 JSON -> ID 结构 JSON；已是 ID 结构则原样返回（幂等）

		canonical_column 指定原文 JSON 属于哪门语言（默认简体中文）。
		"""
		if not value:
			return value
		try:
			parsed = json.loads(value) if isinstance(value, str) else value
		except (json.JSONDecodeError, TypeError):
			return value
		if cls.is_encoded(parsed):
			return value
		if isinstance(parsed, dict):
			return cls.write_logs({canonical_column: parsed})
		return value

	# ==================== 导出侧 ====================

	@classmethod
	def load_groups(cls, force=False):
		"""全量载入 logs 表（id -> {'type', 'texts'}），导出时纯内存映射"""
		if cls._groups is not None and not force:
			return cls._groups
		cls.ensure_table()
		columns = ', '.join(f'`{c}`' for c in cls.LANG_COLUMNS)
		rows = DatabaseManager.query_all(f"SELECT `id`, `type`, `content`, {columns} FROM `logs`")
		groups = {}
		for row in rows or []:
			texts = {column: row[3 + i] for i, column in enumerate(cls.LANG_COLUMNS) if row[3 + i]}
			if not texts.get(cls.ZH_COLUMN) and row[2]:
				texts[cls.ZH_COLUMN] = row[2]
			groups[int(row[0])] = {'type': row[1], 'texts': texts}
		cls._groups = groups
		_logger.info(f"logs 表已载入内存: {len(groups)} 条")
		return groups

	@classmethod
	def decode_structure(cls, pairs):
		"""ID 引用结构 -> [(模块分组, [条目分组, ...], 语言掩码), ...]（缺失 id 跳过）"""
		if not isinstance(pairs, list):
			return []
		groups = cls.load_groups()
		result = []
		for item in pairs:
			if not (isinstance(item, list) and len(item) in (2, 3)):
				continue
			module = groups.get(int(item[0]))
			if module is None:
				continue
			entries = [groups[int(lid)] for lid in item[1]
					   if isinstance(lid, int) and int(lid) in groups]
			if len(item) == 3 and isinstance(item[2], int):
				mask = int(item[2])
			else:
				mask = cls.mask_of([c for c in cls.LANG_COLUMNS if module['texts'].get(c)])
			result.append((module, entries, mask))
		return result

	@classmethod
	def _entry_text(cls, group, column):
		"""条目文本：该语言缺失时回落英文、再回落中文；简体中文自身不回落"""
		text = group['texts'].get(column)
		if text:
			return text
		if column == cls.ZH_COLUMN:
			return None
		return group['texts'].get(cls.EN_COLUMN) or group['texts'].get(cls.ZH_COLUMN) or None

	@classmethod
	def build_localized(cls, pairs):
		"""ID 引用结构 -> {语言列: {模块: [条目, ...]}}（导出格式）

		只输出语言掩码里包含的语言，避免跨 ROM 复用分组时把别的语言带出来。
		"""
		result = {}
		for module, entries, mask in cls.decode_structure(pairs):
			for index, column in enumerate(cls.LANG_COLUMNS):
				if not (mask >> index) & 1:
					continue
				module_text = module['texts'].get(column)
				if not module_text:
					continue
				lines = []
				for entry in entries:
					text = cls._entry_text(entry, column)
					if text:
						lines.append(text)
				# 空条目的模块也保留（上游日志里确实存在 {"基础体验": []} 这类空模块）
				result.setdefault(column, {}).setdefault(module_text, []).extend(lines)
		# 语言键按 LANG_COLUMNS 顺序输出，保证导出文件稳定、diff 友好
		return {column: result[column] for column in cls.LANG_COLUMNS if column in result}

	@classmethod
	def localized_value(cls, pairs, column):
		"""只要某一门语言的日志（缺失返回 None）"""
		return cls.build_localized(pairs).get(column)

	@classmethod
	def decode(cls, pairs):
		"""ID 引用结构 -> 简体中文原文对象（兼容旧接口）"""
		return cls.build_localized(pairs).get(cls.ZH_COLUMN) or {}

	@classmethod
	def decode_value(cls, parsed):
		"""解析后的列值：ID 结构 -> 多语言对象；其余（旧格式/异常值）原样返回"""
		if cls.is_encoded(parsed):
			return cls.build_localized(parsed)
		return parsed

	@classmethod
	def normalize_json(cls, value):
		"""比较用归一化：ID 结构解码为多语言对象，其余原样返回解析结果"""
		if not value or not isinstance(value, str):
			return value
		try:
			parsed = json.loads(value)
		except (json.JSONDecodeError, TypeError):
			return value
		return cls.decode_value(parsed)

	@classmethod
	def refresh_cache(cls):
		"""全量刷新缓存（导出侧行池 + 写入侧行池）"""
		cls._groups = None
		cls._index = None

	@classmethod
	def count(cls):
		row = DatabaseManager.query_one("SELECT COUNT(*) FROM `logs`")
		return int(row[0]) if row else 0


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
	newroms_file = get_platform_path("public/data/scripts/NewROMs.txt")
	file = open(newroms_file, "a", encoding='utf-8')
	file.write(filename+"\n")
	flag = extract_flag_from_filename(filename)
	print(f"发现\t{flag}\t分支有未收录的新版本")
	file.close()


def writeFlag(flag, device):
	"""写入 flag 到 device 的映射草稿，写入前做归一化与合法性校验"""
	flag = (flag or "").strip().strip('_')
	device = (device or "").strip().strip('_')
	# flag 必须是分支代码，完整的包文件名（含 .zip/.tgz/-images）不是合法 flag
	if not flag or any(mark in flag for mark in (".zip", ".tgz", "-images", "_images")):
		return
	flags_file = get_platform_path("public/data/scripts/Flags.json")
	with open(flags_file, "r+", encoding='utf-8') as file:
		content = file.read()
		if content and not content.endswith("\n"):
			file.write("\n")
		file.write(f"\"{flag}\":\"{device}\",\n")


def getDeviceCode(filename):
	"""从文件名中获取设备代码"""
	flag = extract_flag_from_filename(filename)
	if flag:
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
	"""生成OTA请求表单"""
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
		print(device, version, "请补充安卓版本")
		HyperOSForm['c'] = '14'
	else:
		HyperOSForm['c'] = android.split('.0')[0]
	HyperOSForm['sdk'] = sdk[android.split('.0')[0]]
	if "OS1" in version:
		HyperOSForm['v'] = 'MIUI-' + version.replace('OS1', 'V816')
	else:
		HyperOSForm['v'] = version
	return json.dumps(HyperOSForm)

def db_job_latest(sql):
	"""执行SQL查询并返回第一条结果"""
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
		print(sql, e)
	finally:
		if cnx:
			cnx.close()

def query_device_by_code_or_branchcode(value):
	"""在 devices 表中按 code 或 branchcode 查找（忽略大小写，任一列命中即可）

	devices 表同时存有语义化 code（如 rothko_jp_sb_global）和 MIUI 风格
	branchcode（如 ROTHKOJPSBGlobal），不同调用方传入的格式可能不同，
	因此两列都尝试匹配。
	"""
	if not value:
		return None
	sql = ("SELECT code, device, tag, region, carrier, branchcode FROM devices "
			"WHERE LOWER(code) = LOWER(%s) OR LOWER(branchcode) = LOWER(%s)") % (stringify(value), stringify(value))
	return db_job_latest(sql)

def getBranchcode(filename):
	if filename.endswith(".zip"):
		if filename.startswith("miui"):
			branchCode = filename.split("_")[1]
			record = query_device_by_code_or_branchcode(branchCode)
			return record[0] if record else 0
		else:
			return filename.split("-")[0]
	elif filename.endswith(".tgz"):
		return filename.split('_images')[0]

def getData(filename):
		def parse_miui_recovery(fname):
				"""解析 MIUI 开头卡刷包: miui_BRANCHCODE_VERSION_..._ANDROID.zip"""
				# 例: miui_LIUQIN_OS1.0.7.0.UMYCNXM_d618a5c980_14.0.zip
				pattern = r'^miui_([A-Za-z0-9]+)_([A-Z0-9\.]+)_.*_(\d+\.\d+)\.zip$'
				match = re.match(pattern, fname)
				if match:
						return {
								'branchcode': match.group(1),
								'version': match.group(2),
								'android': match.group(3),
								'filetype': 'recovery'
						}
				return None
		
		def parse_hyperos_recovery(fname):
				"""解析 HyperOS 格式卡刷包: CODE-ota_full-VERSION-user-ANDROID-HASH.zip"""
				# 例1: lapis-ota_full-OS3.0.302.0.WPPCNXM-user-16.0-3ee16184b4.zip
				# 例2: nezha_dpp-ota_full-OS3.3.260422.2.XPACNXM.STABLE-DPP-user-17.0-871d44f4c2.zip
				pattern = r'^([a-z0-9_]+)-ota_full-([A-Z0-9\.]+)-user-(\d+\.\d+)-[a-z0-9]+\.zip$'
				match = re.match(pattern, fname)
				if match:
						return {
								'code': match.group(1),
								'version': match.group(2),
								'android': match.group(3),
								'filetype': 'recovery'
						}
				# 尝试匹配带 STABLE-DPP 等后缀的版本号
				pattern2 = r'^([a-z0-9_]+)-ota_full-([A-Z0-9\.\-]+)-user-(\d+\.\d+)-[a-z0-9]+\.zip$'
				match2 = re.match(pattern2, fname)
				if match2:
						return {
								'code': match2.group(1),
								'version': match2.group(2),
								'android': match2.group(3),
								'filetype': 'recovery'
						}
				return None
		
		def parse_fastboot(fname):
				"""解析线刷包格式"""
				# 新格式: CODE-images-VERSION-TYPE-DATE-ANDROID-REGION-HASH.tgz (带区域标识)
				# 例: arctic_eea_global-images-OS3.0.6.0.WBVEUXM-user-20260409.0000.00-16.0-eea-8581295ba6.tgz
				# 例: arctic_in_global-images-OS3.0.2.0.WBVINXM-user-20260323.0000.00-16.0-in-1fb30dee11.tgz
				if '-images' in fname:
						# 先尝试匹配新格式（带区域标识和运营商）
						pattern_new = r'^([a-z0-9_]+)-images-([A-Z0-9\.]+)-[^-]+-(\d{8}\.\d+\.\d+)-(\d+\.\d+)-([a-z]+)-([a-z0-9]+-[a-z]+)-[a-f0-9]+\.tgz$'
						match = re.match(pattern_new, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(4),
										'filetype': 'fastboot'
								}
						
						# 原来的正则表达式：新格式（带区域标识）
						pattern_new = r'^([a-z0-9_]+)-images-([A-Z0-9\.]+)-[^-]+-(\d{8}\.\d+\.\d+)-(\d+\.\d+)-([a-z_]+)-[a-f0-9]+\.tgz$'
						match = re.match(pattern_new, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(4),
										'filetype': 'fastboot'
								}
						
						# 回退到旧格式: CODE-images-VERSION-TYPE-ANDROID-DATE.tgz
						pattern_old = r'^([a-z0-9_]+)-images-([A-Z0-9\.]+)-[^-]+-(\d+\.\d+)-.*\.tgz$'
						match = re.match(pattern_old, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(3),
										'filetype': 'fastboot'
								}
				
				# 格式2: CODE_images_VERSION_DATE_ANDROID_REGION_CARRIER_HASH.tgz (运营商定制版格式)
				# 例: taiko_images_OS3.0.303.0.WOVCNXM_20260416.0000.00_16.0_cn_chinatelecom_251b6f1689.tgz
				elif '_images_' in fname and ('chinatelecom' in fname or 'chinamobile' in fname or 'chinaunicom' in fname):
						# 匹配运营商定制版格式
						pattern_carrier = r'^([a-z0-9_]+)_images_([A-Z0-9\.]+)_(\d{8}\.\d+\.\d+)_(\d+\.\d+)_[a-z]+_([a-z]+)_([a-f0-9]+)\.tgz$'
						match = re.match(pattern_carrier, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(4),
										'filetype': 'fastboot'
								}
				
				# 格式2: CODE_images_VERSION_DATE_ANDROID_REGION_HASH.tgz (标准格式)
				# 例: taiko_images_OS3.0.303.0.WOVCNXM_20260416.0000.00_16.0_cn_251b6f1689.tgz
				elif '_images' in fname:
						# 先尝试完整格式: CODE_images_VERSION_ANDROID_REGION_HASH.tgz
						pattern_full = r'^([a-z0-9_]+)_images_([A-Z0-9\.]+)_(\d{8}\.\d+\.\d+)_(\d+\.\d+)_([a-z]+)_[a-f0-9]+\.tgz$'
						match = re.match(pattern_full, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(4),
										'filetype': 'fastboot'
								}
						
						# 完整格式: CODE_images_VERSION_TYPE_ANDROID_HASH.tgz
						pattern_full = r'^([a-z0-9_]+)_images_([A-Z0-9\.]+)_[^_]+_(\d+\.\d+)_.*\.tgz$'
						match = re.match(pattern_full, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': match.group(3),
										'filetype': 'fastboot'
								}
						
						# 回退到简化格式: CODE_images_VERSION_HASH.tgz
						pattern_simple = r'^([a-z0-9_]+)_images_([A-Z0-9\.]+)_.+\.tgz$'
						match = re.match(pattern_simple, fname)
						if match:
								return {
										'code': match.group(1),
										'version': match.group(2),
										'android': None,  # 无法从文件名获取，需要后续处理
										'filetype': 'fastboot'
								}
				return None
		
		def determine_version_info(ver):
				"""根据版本号前缀确定 ROM 类型和大版本"""
				if ver.startswith('V'):
						return 'MIUI', f"MIUI {ver[1:].split('.')[0]}"
				elif ver.startswith('OS'):
						return 'HyperOS', f"HyperOS {ver[2:].split('.')[0]}"
				elif ver.startswith('A'):
						return 'STAN', f"STAN {ver.split('.')[0]}"
				return 'Unknown', 'Unknown'
		
		def get_region_info(ver, code):
				"""获取区域信息 (region, tag, zone)"""
				# CNXM 版本特殊处理：根据版本号判断正式版/测试版
				if 'CNXM' in ver:
						try:
								parts = ver.split('.')
								build_num = int(parts[3]) if len(parts) > 3 else 0
								revision_num = int(parts[2]) if len(parts) > 2 else 0
								
								if '.EP.STDEE' in ver or 'EPSTDE' in ver:
										tag = 'EPSTD'  # 政企版
								elif 'STABLE-DPP' in ver:
										tag = 'ADPC'  # 稳定版
								# build为0且revision<300是正式版(CnOO)，否则是测试版(CnOB)
								elif build_num == 0:
										tag = 'CnOO'
								else:
										tag = 'CnOB'
						except (ValueError, IndexError):
								tag = 'CnOB'
						return 'cn', tag, 1
				
				# 非CN版本：先查询 roms 表
				info_sql = "SELECT region, tag, zone FROM roms WHERE code = %s" % stringify(code)
				data = db_job_latest(info_sql)
				
				if data and len(data) == 3:
						# 开发者预览版 (PRE-DPP)
						if 'STABLE-DPP' in ver:
								return data[0], 'ADPG', data[2]
						return data[0], data[1], data[2]
				
				# 回退到 devices 表查询（code 或 branchcode 任一命中）
				device_row = query_device_by_code_or_branchcode(code)
				
				if device_row:
						region, tag = device_row[3], device_row[2]
						if 'STABLE-DPP' in ver:
								tag = 'ADPG'
						zone = 1 if region == 'cn' else 2
						return region, tag, zone
				
				# 最终回退：从 code 推导 region，从版本号推导 tag
				# code 格式: {device}_{region}[_{carrier}]_global
				known_carriers = {'dc', 'at', 'tc', 'cr', 'kd', 'sb', 'cmcc', 'cucc', 'ctcc'}
				segments = code.split('_')
				rest = segments[1:]  # 去掉 device
				if rest and rest[-1] == 'global':
						rest = rest[:-1]
				region = None
				if len(rest) >= 2:
						region = rest[0]
				elif len(rest) == 1:
						if rest[0] in known_carriers:
								region = 'global'
						else:
								region = rest[0]
				
				# 从版本号提取 tag（最后4位），例如 VBNMXTC -> MXTC
				tag = None
				ver_parts = ver.split('.')
				if len(ver_parts) >= 5 and len(ver_parts[4]) >= 4:
						tag = ver_parts[4][-4:]
				
				if region and tag:
						zone = 1 if region == 'cn' else 2
						return region, tag, zone
				
				return None, None, None
		
		def handle_miui_branchcode(branchcode, version):
				"""处理 MIUI branchcode，查询现有记录或创建设备记录"""
				# 查询现有设备：code 或 branchcode 任一命中即可
				result = query_device_by_code_or_branchcode(branchcode)
				
				if result:
						return {'code': result[0], 'device': result[1]}
				
				# 未找到，需要创建新记录
				# 提取 devtag
				if '.EP' in version or 'EPSTDE' in version:
						# EP 版本特殊处理: branchcode 如 LIUQINEPSTDEE -> liuqin
						devtag = branchcode.split('EPS')[0].lower() if 'EPS' in branchcode else branchcode[:2].lower()
				else:
						# 从版本号提取 devtag (如 OS1.0.7.0.UMYCNXM -> MY)
						ver_parts = version.split('.')
						devtag = ver_parts[4][1:3].lower() if len(ver_parts) > 4 and len(ver_parts[4]) >= 3 else ''
				
				ver_code = version[-4:] if len(version) >= 4 else ''
				
				# 查询分支信息获取 tag, code_suffix, region
				branch_sql = "SELECT tag, code, region FROM branches WHERE vercode = %s" % stringify(ver_code)
				branch_info = db_job_latest(branch_sql)
				
				if not branch_info or len(branch_info) != 3:
						return None
				
				tag, code_suffix, region = branch_info
				
				# 查询设备名（devtag 可能不唯一，如 taurus 与 zeus 同为 'LB'）
				device_sql = "SELECT DISTINCT device FROM devices WHERE devtag = %s" % stringify(devtag)
				device_rows = db_job(device_sql)
				
				if not device_rows:
						return None
				
				candidates = [r[0] for r in device_rows]
				device = None
				
				# 优先用 branchcode 前缀匹配：branchcode 形如 {DEVICE_UPPER}{SUFFIX}
				# 如 ZEUSMXTCGlobal -> zeus，取最长匹配以避免 cancro/cancro_lte 前缀冲突
				bc_upper = branchcode.upper()
				best_len = 0
				for cand in candidates:
						cu = cand.upper()
						if bc_upper.startswith(cu) and len(cu) > best_len:
								device = cand
								best_len = len(cu)
				
				# 无前缀匹配时回退到第一个候选（保持原有行为）
				if device is None:
						device = candidates[0]
				
				full_code = device if code_suffix is None else device + code_suffix
				
				# 插入新设备记录
				devcode = version[-6:] if len(version) >= 6 else ''
				insert_sql = (
						"INSERT INTO devices (device, devtag, code, tag, region, devcode, branchcode) "
						"VALUES (%s, %s, %s, %s, %s, %s, %s)" % (
								stringify(device), stringify(devtag), stringify(full_code),
								stringify(tag), stringify(region), stringify(devcode), stringify(branchcode)
						)
				)
				db_job_latest(insert_sql)
				
				return {'code': full_code, 'device': device}
		
		def get_device_by_code(code):
				"""通过 code 查询设备名，优先 roms 表，其次 devices 表；都失败时从 code 推导"""
				# 优先从 roms 表查询
				rom_sql = "SELECT device FROM roms WHERE code = %s" % stringify(code)
				result = db_job_latest(rom_sql)
				
				if result:
						return result[0]
				
				# 从 devices 表查询（code 或 branchcode 任一命中）
				device_row = query_device_by_code_or_branchcode(code)
				if device_row:
						return device_row[1]
				
				# 回退：从 code 推导设备名（取第一段），并在 devices 表中验证该设备存在
				# 例如 dew_mx_tc_global -> dew，若 devices 表中存在 device='dew' 的记录则返回 dew
				guessed_device = code.split('_')[0]
				verify_sql = "SELECT device FROM devices WHERE device = %s LIMIT 1" % stringify(guessed_device)
				result = db_job_latest(verify_sql)
				if result:
						return result[0]
				
				return None
		
		# ========== 主逻辑 ==========
		
		parsed = None
		
		# 根据文件扩展名和格式选择解析器
		if filename.endswith('.zip'):
				if filename.startswith('miui_'):
						# MIUI 格式
						parsed = parse_miui_recovery(filename)
						if parsed:
								device_info = handle_miui_branchcode(parsed['branchcode'], parsed['version'])
								if not device_info:
										return 0
								parsed['code'] = device_info['code']
								parsed['device'] = device_info['device']
				else:
						# HyperOS 格式
						parsed = parse_hyperos_recovery(filename)
						if parsed:
								parsed['device'] = get_device_by_code(parsed['code'])
								if not parsed['device']:
										return 0
		elif filename.endswith('.tgz'):
				# 线刷包格式
				parsed = parse_fastboot(filename)
				if parsed:
						parsed['device'] = get_device_by_code(parsed['code'])
						if not parsed['device']:
								return 0
		
		# 解析失败
		if not parsed:
				return 0
		
		# 提取所有必需字段
		code = parsed.get('code')
		device = parsed.get('device')
		android = parsed.get('android')
		version = parsed.get('version')
		filetype = parsed.get('filetype')
		
		# 检测运营商信息
		if "chinatelecom" in filename:
			carrier = "chinatelecom"
		elif "chinamobile" in filename:
			carrier = "chinamobile"
		elif "chinaunicom" in filename:
			carrier = "chinaunicom"
		else:
			carrier = None
		
		# 如果 android 为空，尝试从版本号推断
		if not android and version:
				if version.startswith('OS'):
						try:
								major_version = int(version.split('.')[0][2:])
								if major_version == 1:
										android = '14.0'
								elif major_version == 2:
										android = '15.0'
								elif major_version >= 3:
										android = '16.0'
						except (ValueError, IndexError):
								pass
				elif version.startswith('V'):
						# MIUI 版本无法准确推断，保持 None
						pass
		
		# 验证必需字段（允许 android 为空，后续可以从数据库获取）
		if not all([code, device, version, filetype]):
				return 0
		
		# 确定版本类型和大版本
		rom_type, bigver = determine_version_info(version)
		
		# 获取区域信息
		region, tag, zone = get_region_info(version, code)
		if region is None:
				return 0
		# 返回完整信息
		return device, code, android, version, rom_type, bigver, region, tag, zone, 'F', filetype

def checkDatabase(device, code, android, version, rom_type, bigver, region,tag,zone,branch, filetype, filename):
	if filetype == "recovery":
		checkpoint = "recovery"
		d_check = checkpoint
	else:
		if "chinatelecom" in filename:
			checkpoint = "ctelecom"
			d_check = checkpoint
		elif "chinaunicom" in filename:
			checkpoint = "cnunicom"
			d_check = "cunicom"
		elif "chinamobile" in filename:
			checkpoint = "cmobile"
			d_check = "cmobile"
		else:
			checkpoint = "fastboot"
			d_check = checkpoint
	get_sql = f"SELECT id,{d_check},others FROM roms WHERE code = %s and version = %s" % (stringify(code), stringify(version))
	data = db_job_latest(get_sql)
	if data is not None:
		if len(data) > 0:
			if data[1] == filename:
				pass
			elif data[1] == None or data[1] == "":
				if filetype == "recovery":
					beta_date = stringify(get_time(form_url(filename,version)))
					# 尝试获取安全补丁日期，失败时不更新 aspatch 字段，保留现有信息
					try:
						url = form_url(filename, version)
						asp = get_security_patch_from_ota_url(url, 'recovery', timeout=30)
					except:
						asp = None
					if asp:
						upd_sql = f"UPDATE roms SET {checkpoint} = %s, beta_date = %s, aspatch = %s WHERE id = %s" % (stringify(filename),beta_date, stringify(asp), stringify(data[0]))
					else:
						upd_sql = f"UPDATE roms SET {checkpoint} = %s, beta_date = %s WHERE id = %s" % (stringify(filename),beta_date, stringify(data[0]))
				else:
					public_date = stringify(get_time(form_url(filename,version)))
					upd_sql = f"UPDATE roms SET {d_check} = %s, public_date = %s WHERE id = %s" % (stringify(filename),public_date, stringify(data[0]))
				db_job_latest(upd_sql)
			else:
				if data[2] == None or data[2] == "":
					others = []
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %s" % (stringify(data[0]))
					db_job_latest(update_sql)
				elif filename in str(data[2]):
					pass
				else:
					others = list(json.loads(str(data[2])))
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %s" % (stringify(data[0]))
					db_job_latest(update_sql)
		else:
			print(filename)
	else:
		insdate = stringify(date.today().strftime("%Y-%m-%d"))
		release_date = stringify(date.today().strftime("%Y-%m-%d"))
		if filetype == "fastboot":
			public_date = stringify(get_time(form_url(filename,version)))
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,insdate, public_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (stringify(zone), stringify(device), stringify(code), stringify(android), stringify(version), stringify(rom_type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, insdate, public_date)
		else:
			beta_date = stringify(get_time(form_url(filename,version)))
			public_date = stringify(None)
			# 尝试获取安全补丁日期，失败时插入 NULL
			aspatch = "NULL"
			try:
				url = form_url(filename, version)
				asp = get_security_patch_from_ota_url(url, 'recovery', timeout=30)
				if asp:
					aspatch = stringify(asp)
			except:
				pass
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,beta_date,insdate, aspatch) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (stringify(zone), stringify(device), stringify(code), stringify(android), stringify(version), stringify(rom_type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, beta_date, insdate, aspatch)
		db_job_latest(ins_sql)



REGION_NAMES = {
	"global": ("国际", "Global"),
	"eea": ("欧洲EEA", "Europe EEA"),
	"ru": ("俄罗斯", "Russia"),
	"id": ("印度尼西亚", "Indonesia"),
	"tr": ("土耳其", "Turkey"),
	"mx": ("墨西哥", "Mexico"),
	"lm": ("拉丁美洲", "Latin America"),
	"jp": ("日本", "Japan"),
	"in": ("印度", "India"),
	"kr": ("韩国", "South Korea"),
	"th": ("泰国", "Thailand"),
	"za": ("南非", "South Africa"),
	"pe": ("秘鲁", "Peru"),
	"cl": ("智利", "Chile"),
	"gt": ("危地马拉", "Guatemala"),
	"tw": ("中国台湾省", "China Taiwan Province"),
	"cn": ("中国大陆", "China Mainland"),
}

CARRIER_NAMES = {
	"at": ("AT&T", "AT&T"),
	"tc": ("Telcel", "Telcel"),
	"cr": ("Claro", "Claro"),
	"dc": ("DC", "DC"),
	"kd": ("KDDI", "KDDI"),
	"sb": ("SoftBank", "SoftBank"),
	"hg": ("ThreeHK", "ThreeHK"),
	"vc": ("Vodacom", "Vodacom"),
	"mt": ("MTN", "MTN"),
	"tg": ("Tigo", "Tigo"),
	"en": ("Entel", "Entel"),
	"as": ("AIS", "AIS"),
}

_branch_templates = None


def load_branch_templates():
	"""读取 device-template.json 的分支模板（用于补建分支时复用正确的名称/区域/运营商）"""
	global _branch_templates
	if _branch_templates is None:
		path = get_platform_path("public/data/device-template.json")
		try:
			with open(path, "r", encoding="utf-8") as f:
				_branch_templates = json.load(f).get("branches", [])
		except (OSError, ValueError):
			_branch_templates = []
	return _branch_templates


def find_branch_spec(code, tag=None, region=None):
	"""在 OScommon.branches（对应数据库 branches 表）中查找分支规格

	数据库 tag -> idtag，数据库 vercode -> tag。
	"""
	code = code or ""
	candidates = [b for b in branches if b.get("code") == code]
	if tag:
		for b in candidates:
			if b.get("idtag") == tag:
				return b
		for b in candidates:
			if b.get("tag") == tag:
				return b
		for b in branches:
			if b.get("idtag") == tag:
				return b
		for b in branches:
			if b.get("tag") == tag:
				return b
	if region:
		matched = [b for b in candidates if b.get("region") == region]
		if len(matched) == 1:
			return matched[0]
	if len(candidates) == 1:
		return candidates[0]
	return None


def create_branch(devdata, device, code, tag=None, region=None, zone=None, branch='F'):
	"""按 branchCode（可选 tag）自动创建分支，追加到 devdata['branches'] 并返回该分支。"""
	# 从 branchCode 解析区域与运营商，格式: {device}_{region?}_{carrier?}_global
	rest = code
	if device and rest.startswith(device + "_"):
		rest = rest[len(device) + 1:]
	if rest.endswith("_global"):
		rest = rest[:-len("_global")]
	parts = rest.split("_") if rest else []
	carrier = ""
	code_region = None
	if len(parts) >= 2:
		code_region, carrier = parts[0], parts[1]
	elif len(parts) == 1:
		if parts[0] in REGION_NAMES:
			code_region = parts[0]
		else:
			carrier = parts[0]

	# 按 OScommon.branches（数据库 branches 表）解析 idtag 与 tag
	# 数据库 tag -> idtag，数据库 vercode -> tag
	spec = find_branch_spec(code, tag, region)
	branch_idtag = spec.get("idtag") if spec else (tag or "")

	# 优先按 idtag 匹配模板，其次按 region + carrier
	tpl = None
	templates = load_branch_templates()
	if branch_idtag:
		for t in templates:
			if t.get("idtag") == branch_idtag:
				tpl = t
				break
	if tpl is None and code_region:
		for t in templates:
			if t.get("region") == code_region and t.get("carrier") == ([carrier] if carrier else [""]):
				tpl = t
				break

	branch_tag = spec.get("tag") if spec else (tpl.get("tag") if tpl else "")

	branch_region = region or (spec.get("region") if spec else None) or (tpl.get("region") if tpl else None) or code_region or "global"
	if zone is not None:
		branch_zone = zone
	elif spec and spec.get("zone"):
		branch_zone = spec["zone"]
	elif tpl and tpl.get("zone"):
		branch_zone = tpl["zone"]
	else:
		branch_zone = "1" if branch_region == "cn" else "2"

	device_name_zh = devdata.get("name", {}).get("zh", device)
	device_name_en = devdata.get("name", {}).get("en", device)
	brand = ""
	for existing_branch in devdata.get("branches", []):
		if existing_branch.get("brand"):
			brand = existing_branch["brand"]
			break

	if tpl:
		name_zh, name_en = tpl["name"]["zh"], tpl["name"]["en"]
		carrier_list = list(tpl.get("carrier", [""]))
		table = list(tpl.get("table", ["os", "android", "release", "aspatch", "recovery", "fastboot"]))
		show, ep = tpl.get("show", "1"), tpl.get("ep", "0")
	else:
		region_zh, region_en = REGION_NAMES.get(branch_region, (branch_region.upper(), branch_region.capitalize()))
		carrier_zh, carrier_en = CARRIER_NAMES.get(carrier, (carrier.upper(), carrier.upper()))
		if carrier == "dc":
			name_zh = f"小米澎湃 OS {region_zh} DC 正式版"
			name_en = f"Xiaomi HyperOS {region_en} DC Stable"
		elif carrier:
			name_zh = f"小米澎湃 OS {region_zh}{carrier_zh}运营商定制版"
			name_en = f"Xiaomi HyperOS {region_en} {carrier_en} Carrier Edition"
		else:
			name_zh = f"小米澎湃 OS {region_zh}正式版"
			name_en = f"Xiaomi HyperOS {region_en} Stable"
		carrier_list = [carrier] if carrier else [""]
		table = ["os", "android", "release", "aspatch", "recovery", "fastboot"]
		show, ep = "1", "0"

	new_branch = {
		"name": {
			"zh": name_zh,
			"en": name_en
		},
		"branchCode": code,
		"brand": brand,
		"device": {
			"zh": device_name_zh,
			"en": device_name_en
		},
		"idtag": branch_idtag,
		"tag": branch_tag,
		"branchtag": branch,
		"table": table,
		"show": show,
		"carrier": carrier_list,
		"region": branch_region,
		"zone": str(branch_zone),
		"ep": ep,
		"roms": {}
	}

	devdata.setdefault("branches", []).append(new_branch)
	print(f"自动创建新分支: {code} (idtag={branch_idtag}, tag={branch_tag}, region={branch_region}, carrier={carrier})")
	return new_branch


def add_rom_to_json(device, code, android, version, filetype, filename, devdata=None, region=None, tag=None, zone=None, branch: str | None = 'F'):
	"""添加 ROM 到 JSON 文件,修复版 - 优化 Git diff - 基于table表新建ROM模板
	当 JSON 中不存在匹配分支时，自动创建对应分支并写入 ROM 信息。"""
	
	branch = branch or 'F'
	
	if devdata is None:
		device_file = get_platform_path(f"public/data/devices/{device}.json")
		try:
			with open(device_file, 'r', encoding='utf-8') as f:
				devdata = json.load(f)
		except Exception as e:
			print(f"读取文件错误: {e}")
			return None
	
	target_branch_idx = None
	target_branch = None
	target_idtag = None
	match_method = None
	
	if "CNXM" in version:
		try:
			version_parts = version.split(".")
			
			# 优先检查特殊版本标识
			if '.EP.STDEE' in version or 'EPSTDE' in version:
				# 政企版：通过 idtag 或 ep 字段匹配
				for idx, branch_info in enumerate(devdata.get("branches", [])):
					if branch_info.get("idtag") in ("EPSTD", "STDEE") or branch_info.get("ep") == "1":
						target_branch_idx = idx
						target_branch = branch_info
						match_method = f"idtag:{branch_info.get('idtag')} (EP.STDEE)"
						break
			elif 'STABLE-DPP' in filename:
				if "global" in filename:
					target_idtag = "ADPG"
				else:
					target_idtag = "ADPC"
			elif len(version_parts) >= 4:
				build_number = int(version_parts[3])
				revision_number = int(version_parts[2])
				
				if build_number == 0:
					target_idtag = "CnOO"  # 正式版
				else:
					target_idtag = "CnOB"  # 测试版/Beta
			else:
				target_idtag = None
		except:
			target_idtag = None
		
		if target_idtag:
			for idx, branch_info in enumerate(devdata.get("branches", [])):
				if branch_info.get("idtag") == target_idtag:
					target_branch_idx = idx
					target_branch = branch_info
					match_method = f"idtag:{target_idtag}"
					break

	# 只有当 idtag 匹配失败时，才尝试 code 匹配
	if target_branch is None:
		# 对于非CNXM版本，检查特殊版本标识
		if 'PRE-DPP' in version or 'PRE_DPP' in version:
			# 国际版开发者预览版，寻找 ADPG 分支
			for idx, branch_info in enumerate(devdata.get("branches", [])):
				if branch_info.get("idtag") == "ADPG":
					target_branch_idx = idx
					target_branch = branch_info
					match_method = f"idtag:ADPG (PRE-DPP)"
					break
		
		# 如果仍未找到，尝试 code 匹配
		if target_branch is None:
			# 如果 idtag 匹配失败，再尝试 code 匹配
			matching_branches_by_code = []
			for idx, branch_info in enumerate(devdata.get("branches", [])):
				if branch_info.get("branchCode") == code:
					matching_branches_by_code.append((idx, branch_info))
			
			# 如果找到多个匹配的分支（branchCode不唯一），则使用版本号中的tag来进一步筛选
			if len(matching_branches_by_code) > 0:
				# 从版本号中提取tag，例如从 OS3.0.302.0.WPSIDDM 提取 "IDDM"
				# 版本号格式通常是 OS主版本.次版本.修订版本.构建号.TAG
				version_parts = version.split(".")
				version_tag = None
				
				if len(version_parts) >= 5:
					# 获取第五部分，如 WPSIDDM
					full_tag = version_parts[4]
					# 提取最后4位，如 IDDM
					if len(full_tag) >= 4:
						version_tag = full_tag[-4:]
				
				# 如果提取到了版本标签，尝试精确匹配
				if version_tag:
					for idx, branch_info in matching_branches_by_code:
						if branch_info.get("tag") == version_tag:
							target_branch_idx = idx
							target_branch = branch_info
							match_method = f"code:{code} + tag:{version_tag}"
							break
				
				# 如果通过版本标签没有找到匹配，但只有一个分支，则使用它
				if target_branch is None and len(matching_branches_by_code) == 1:
					target_branch_idx, target_branch = matching_branches_by_code[0]
					match_method = f"code:{code} (only one)"
	
	# 如果仍然没有找到匹配的分支，尝试单独使用tag匹配（针对海外分支）
	if target_branch is None:
		# 再次尝试从版本号中提取tag
		version_parts = version.split(".")
		version_tag = None
		
		if len(version_parts) >= 5:
			# 获取第五部分，如 WPSIDDM
			full_tag = version_parts[4]
			# 提取最后4位，如 IDDM
			if len(full_tag) >= 4:
				version_tag = full_tag[-4:]
		
		if version_tag:
			for idx, branch_info in enumerate(devdata.get("branches", [])):
				if branch_info.get("tag") == version_tag and code in branch_info.get("branchCode", ""):
					target_branch_idx = idx
					target_branch = branch_info
					match_method = f"tag:{version_tag} + code:{code}"
					break
	
	# 如果仍未找到匹配分支，自动创建新分支
	if target_branch is None:
		# 优先使用传入的 tag，其次从版本号提取（例如 OS3.0.302.0.WNFMXTC -> MXTC）
		branch_tag = tag
		if not branch_tag:
			version_parts_for_tag = version.split(".")
			if len(version_parts_for_tag) >= 5 and len(version_parts_for_tag[4]) >= 4:
				branch_tag = version_parts_for_tag[4][-4:]
		target_branch = create_branch(devdata, device, code, tag=branch_tag,
									  region=region, zone=zone, branch=branch)
		target_branch_idx = len(devdata["branches"]) - 1
		match_method = f"auto-created branch: {code}"

	# 处理 ROM 数据
	if "roms" not in target_branch:
		target_branch["roms"] = {}
	
	roms = target_branch["roms"]
	
	# 版本已存在，更新字段
	if version in roms:
		rom_data = roms[version]
		updated = False
		
		if filetype == "recovery" and rom_data.get("recovery") != filename:
			rom_data["recovery"] = filename
			updated = True
			# 同时更新安全补丁日期
			table_fields = target_branch.get("table", [])
			if "aspatch" in table_fields:
				try:
					url = form_url(filename, version)
					aspatch = get_security_patch_from_ota_url(url, 'recovery', timeout=30)
					if aspatch:
						rom_data["aspatch"] = aspatch
				except Exception as e:
					print(f"更新安全补丁日期失败: {e}")
		elif filetype == "fastboot":
			# 检查是否为运营商定制版
			if "chinatelecom" in filename:
				if rom_data.get("ctelecom") != filename:
					rom_data["ctelecom"] = filename
					updated = True
			elif "chinamobile" in filename:
				if rom_data.get("cnmobile") != filename:
					rom_data["cnmobile"] = filename
					updated = True
			elif "chinaunicom" in filename:
				if rom_data.get("cnunicom") != filename:
					rom_data["cnunicom"] = filename
					updated = True
			else:
				# 普通版 fastboot
				if rom_data.get("fastboot") != filename:
					rom_data["fastboot"] = filename
					updated = True
		
		if not updated:
			print(f"ROM 数据已完整: {version}")
		check_devices_supports(device, android, version, devdata)
		return devdata
	
	# 获取table字段列表
	table_fields = target_branch.get("table", [])
	
	# 根据table表创建新ROM条目，按table顺序构建字典
	new_rom = {}
	
	# 按table顺序初始化所有字段
	for field in table_fields:
		if field == "os":
			new_rom[field] = version
		elif field == "android":
			new_rom[field] = android
		elif field == "release":
			new_rom[field] = get_time(form_url(filename, version))
		elif field == "aspatch":
			# 初始化为空字符串，后续根据文件类型填充
			new_rom[field] = ""
		else:
			# 其他字段初始化为空字符串
			new_rom[field] = ""
	
	# 根据文件类型和运商标识设置相应字段
	if filetype == "recovery":
		new_rom["recovery"] = filename
		# 尝试获取安卓安全补丁日期
		if "aspatch" in table_fields:
			try:
				url = form_url(filename, version)
				aspatch = get_security_patch_from_ota_url(url, 'recovery', timeout=30)
				if aspatch:
					new_rom["aspatch"] = aspatch
			except Exception as e:
				print(f"获取安全补丁日期失败: {e}")
	elif filetype == "fastboot":
		# 检查是否为运营商定制版
		if "chinatelecom" in filename:
			new_rom["ctelecom"] = filename
		elif "chinamobile" in filename:
			new_rom["cnmobile"] = filename
		elif "chinaunicom" in filename:
			new_rom["cnunicom"] = filename
		else:
			# 普通版 fastboot
			new_rom["fastboot"] = filename
	
	ordered_roms = OrderedDict()
	inserted = False
	
	# 按版本号排序插入 - 使用parse_version处理OS/A前缀
	def version_sort_key(v):
		parsed = parse_version(v)
		if parsed is None:
			# 如果解析失败，返回一个默认值让该版本排在最后
			return (999, 999, 999, 999)
		return parsed
	
	sorted_versions = sorted(roms.keys(), key=version_sort_key, reverse=True)
	
	for existing_ver in sorted_versions:
		# 如果当前版本大于要插入的版本，且还未插入
		if not inserted and compare(version, existing_ver):
			ordered_roms[version] = new_rom
			inserted = True
		ordered_roms[existing_ver] = roms[existing_ver]
	
	# 如果还没插入（是最新版本），添加到末尾
	if not inserted:
		ordered_roms[version] = new_rom
	
	# 直接替换 roms，保持有序字典的特性
	devdata["branches"][target_branch_idx]["roms"] = dict(ordered_roms)
	
	# 更新 index.json
	update_index_json(device, devdata, version)
	
	# 核查设备的 supports 和 android 字段（修改 devdata，由调用方写回文件）
	check_devices_supports(device, android, version, devdata)
	
	return devdata


def check_devices_supports(device, android, version, devdata=None):
	"""核查设备的 supports 与 android 字段，缺失则补充
	传入 devdata 时修改内存数据，由调用方统一写回文件；否则直接读写文件"""
	
	# 提取 OS 大版本，如 OS3.0.302.0.WPQCNXM -> OS3.0
	os_major = None
	if version.startswith("OS") and "." in version:
		parts = version.split(".")
		if len(parts) >= 2:
			os_major = parts[0] + "." + parts[1]
	elif version.startswith("V816") and "." in version:
		# V816 对应 HyperOS 1
		os_major = "OS1.0"
	
	# 规范化安卓版本，如 16 -> 16.0
	android_ver = None
	if android:
		android_ver = android.split(".")[0] + ".0"
	
	if not os_major and not android_ver:
		return False
	
	# 在函数开始处定义 device_path
	device_path = get_platform_path(f"public/data/devices/{device}.json")
	
	from_file = False
	if devdata is None:
		try:
			with open(device_path, 'r', encoding='utf-8') as f:
				devdata = json.load(f)
		except Exception as e:
			print(f"读取设备文件错误: {e}")
			return False
		from_file = True
	
	changed = False
	if os_major:
		supports = devdata.setdefault("supports", [])
		if os_major not in supports:
			supports.append(os_major)
			changed = True
	
	if android_ver:
		androids = devdata.setdefault("android", [])
		if android_ver not in androids:
			androids.append(android_ver)
			changed = True
	
	if changed and from_file:
		try:
			with open(device_path, 'w', encoding='utf-8') as f:
				json.dump(devdata, f, ensure_ascii=False, indent='\t', sort_keys=False)
		except Exception as e:
			print(f"写入设备文件错误: {e}")
			return False
	
	if changed:
		print(f"{device} 已更新: supports={os_major} android={android_ver}")
	
	return changed


def update_index_json(device, devdata, version):
	"""更新 index.json 文件，添加新ROM信息"""
	index_path = get_platform_path("public/data/index.json")
	
	# 获取当前东八区日期
	tz = timezone(timedelta(hours=8))
	current_date = datetime.now(tz).strftime("%Y-%m-%d")
	
	# 检查分支是否是需要显示的稳定版
	branchtag = None
	branch_name_en = ""
	for branch in devdata.get("branches", []):
		if "roms" in branch and version in branch["roms"]:
			branchtag = branch.get("branchtag", "")
			branch_name_en = branch.get("name", {}).get("en", "")
			break
	
	# 跳过开发版、每日构建版、政企版和演示机版
	if branchtag == 'X' or branchtag == 'D' or "Enterprise" in branch_name_en or "EP" in branch_name_en or "Demo" in branch_name_en:
		return
	
	try:
		# 读取现有的 index.json
		if os.path.exists(index_path):
			with open(index_path, 'r', encoding='utf-8') as f:
				updates = json.load(f)
		else:
			updates = {
				"recent": {
					"time": "",
					"developing": "no",
					"roms": {}
				}
			}
		
		# 校验 index.json 结构：顶层与 recent 必须为 dict，roms 必须为以设备 code 为键的 dict
		if not isinstance(updates, dict):
			print(f"更新 index.json 失败: 顶层结构应为 dict，实际为 {type(updates).__name__}，请检查 {index_path}")
			return
		recent = updates.get("recent")
		if not isinstance(recent, dict):
			print(f"更新 index.json 失败: recent 字段应为 dict，实际为 {type(recent).__name__}，请检查 {index_path}")
			return
		roms = recent.get("roms")
		if not isinstance(roms, dict):
			print(f"更新 index.json 失败: recent.roms 应为以设备 code 为键的 dict，实际为 {type(roms).__name__}"
				  f"（可能是旧版 list 结构，元素形如 {{\"code\", \"name\", \"rom\"}}），"
				  f"本次跳过更新，请先迁移或修正 {index_path}，对应 rom 为 {version}")
			return

		# 更新时间（东八区）
		updates["recent"]['time'] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
		
		# 获取设备信息
		device_code = devdata.get('device', device)
		name = {
			"zh": devdata.get('name', {}).get('zh', device),
			"en": devdata.get('name', {}).get('en', device)
		}
		
		# 如果设备已存在，添加新版本
		if device_code in updates["recent"]['roms']:
			existing_versions = updates["recent"]['roms'][device_code].get("versions", [])
			# 检查版本是否已存在
			version_exists = any(v.get("version") == version for v in existing_versions)
			if not version_exists:
				existing_versions.append({
					"insert_date": current_date,
					"version": version
				})
		else:
			# 创建新设备条目
			updates["recent"]['roms'][device_code] = {
				"name": name,
				"versions": [{
					"insert_date": current_date,
					"version": version
				}]
			}
		
		# 自动清理：剔除超过6天未更新的条目
		keep_days = 6
		cutoff_date = (datetime.now(tz) - timedelta(days=keep_days)).strftime("%Y-%m-%d")
		devices_to_remove = []
		for dev_code, dev_info in updates["recent"]['roms'].items():
			versions = dev_info.get("versions", [])
			filtered = [v for v in versions if v.get("insert_date", "") >= cutoff_date]
			if filtered:
				updates["recent"]['roms'][dev_code]["versions"] = filtered
			else:
				devices_to_remove.append(dev_code)
		for dev_code in devices_to_remove:
			del updates["recent"]['roms'][dev_code]
		
		# 按 insert_date 降序排列版本（更新日期越近的越靠前）
		for dev_info in updates["recent"]['roms'].values():
			dev_info["versions"].sort(key=lambda v: v.get("insert_date", ""), reverse=True)
		
		# 按设备最新版本日期降序排列机型（更新日期越近的机型越靠前）
		sorted_devices = sorted(
			updates["recent"]['roms'].items(),
			key=lambda item: max(v.get("insert_date", "") for v in item[1].get("versions", [])),
			reverse=True
		)
		updates["recent"]['roms'] = dict(sorted_devices)
		
		# 写入更新后的 index.json
		with open(index_path, 'w', encoding='utf-8') as f:
			json.dump(updates, f, ensure_ascii=False, indent=2)
		
		print(f"✓ 已更新 index.json: {device_code} - {version} (insert_date: {current_date})")
		
	except Exception as e:
		print(f"更新 index.json 失败: {e}")
		import traceback
		traceback.print_exc()


def checkExist(filename):
	newroms_file = get_platform_path("public/data/scripts/NewROMs.txt")
	newROM = open(newroms_file, 'r', encoding='utf-8').read()
	
	# 尝试读取UInewROM，但如果文件不存在则忽略
	UInewROM = ""
	try:
		if platform == "win32":
			UInewROM = open("D:/Projects/HyperOS.fans/Nuxt3MR/public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		elif platform == "darwin":
			UInewROM = open("../NuxtMR/public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		else:
			UInewROM = open("/sdcard/Codes/NuxtMR/public/MRdata/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	except:
		pass
	
	if "OS" in filename or "A1" in filename:
		if "blockota" in filename:
			return "OTA ROM"
		else:
			device_code = getDeviceCode(filename)
			if device_code == 0:
				return "New ROM"
			elif filename in str(localData(device_code)) or filename in newROM or filename in UInewROM:
				return "Already Exist"
			else:
				if "CNXM" in filename:
					writeData(filename)
				else:
					i = 0
				rom_data = getData(filename)
				if type(rom_data) != tuple:
					return "Error"
				else:
					device, code, android, version, rom_type, bigver, region, tag, zone, branch, filetype = [item for item in rom_data]
					checkDatabase(device, code, android, version, rom_type, bigver, region, tag, zone, branch, filetype, filename)
				
				device_file = get_platform_path(f"public/data/devices/{device}.json")
				try:
					with open(device_file, 'r', encoding='utf-8') as f:
						dev_data = json.load(f)
					devdata = add_rom_to_json(device, code, android, version, filetype, filename, dev_data, region=region, tag=tag, zone=zone, branch=branch or 'F')
					
					if devdata is None:
						print(f"错误: add_rom_to_json 返回 None")
						return "Error"
					
					# 检测原始文件的缩进格式
					indent = detect_json_indent(device_file)
					
					with open(device_file, 'w', encoding='utf-8', newline='\n') as f:
						json.dump(devdata, f, ensure_ascii=False, indent=indent, sort_keys=False)
					
				except Exception as e:
					print(f"✗ 处理 JSON 文件时出错: {e}")
					import traceback
					traceback.print_exc()
				return "New ROM"
	else:
		return "UI Maybe"

def versionAdd(version,add):
	parts = [version.split('.')[0],version.split('.')[1],str(int(version.split('.')[2])+add),"0",version.split('.')[4]]
	separator = "."
	return separator.join(parts)

def miui_decrypt(encrypted_response):
	decipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	# 先进行URL解码（因为加密时进行了URL编码）
	encrypted_response = urllib.parse.unquote(encrypted_response)
	decrypted = decipher.decrypt(base64.b64decode(encrypted_response))
	plaintext = decrypted.decode("utf-8").strip()
	# 移除PKCS7填充
	padding_len = ord(plaintext[-1]) if plaintext else 0
	if padding_len > 0 and padding_len <= 16:
		plaintext = plaintext[:-padding_len]
	pos = plaintext.rfind("}")
	if pos != -1:
		return json.loads(plaintext[:pos + 1])
	else:
		return json.loads(plaintext)


def miui_encrypt(json_request):
	cipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	cipher_text = cipher.encrypt(
		pad(bytes(str(json_request), encoding="ascii"), AES.block_size))
	encrypted_request = quote(base64.b64encode(cipher_text).decode("utf-8")).replace("/", "%2F")
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
		response = session.post(check_url, headers=headers, data=data, timeout=(5, 10))
		if "code" in response.text:
			i = 0
		else:
			try:
				data = miui_decrypt(response.text.split("q=")[0])
			except binascii.Error as e:
				print(f"  [解码失败] {e}")
				return 0
			if "LatestRom" in data:
				package = data["LatestRom"]["filename"].split("?")[0]
				# print(package)
				checkExist(package)
				return 1
			if "CurrentRom" in data:
				package = data["CurrentRom"]["filename"].split("?")[0]
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
	response = requests.post(url, timeout=(5, 10))
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
	response = requests.post(check_url, headers=headers, data=data, timeout=(5, 10))
	if "code" in response.text:
		print(json.loads(response.text)["desc"])
	else:
		print("Encrypted Request：",encrypted_data)
		print("Decrypted Response：",response.text.split("q=")[0])
		data = miui_decrypt(response.text.split("q=")[0])
		print("Decrypted Data：",data)
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

def getChangelog2DB(encrypted_data, device, version):
	"""请求更新日志并清洗，返回 {"changelog": <清洗后原文 JSON 字符串 或 None>, "recovery": <卡刷包文件名 或 ''>}

	与参考实现 ChangelogManager.fetch_for_db 对齐：
	- 优先取 CurrentRom，其次 LatestRom（版本号完全匹配时）；recovery 兜底取 LatestRom 的 filename；
	- 剥离原有的 checkExist 副作用（卡刷包检测与日志入库解耦）；
	- 请求失败 / 接口报错 / 解密失败时返回 None。
	调用方拿到 changelog（原文 JSON 字符串）后交给 LogStore.write_logs 分组写入。
	"""
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
	response = requests.post(check_url, headers=headers, data=data, timeout=(5, 10))
	if "'code'" in response.text:
		print(json.loads(response.text)["desc"])
		response.close()
		return None

	result = miui_decrypt(response.text.split("q=")[0])
	response.close()
	if not isinstance(result, dict):
		return None

	log = None
	recovery = ""
	# 优先匹配 CurrentRom，其次 LatestRom
	for key in ("CurrentRom", "LatestRom"):
		rom = result.get(key)
		if isinstance(rom, dict) and rom.get("version") == version:
			log = rom.get("changelog")
			filename = rom.get("filename", "")
			if filename:
				recovery = filename.split("?")[0]
			break

	# 兜底：取 LatestRom 的 recovery（即使版本不完全匹配）
	if not recovery:
		latest = result.get("LatestRom")
		if isinstance(latest, dict) and latest.get("filename"):
			recovery = latest["filename"].split("?")[0]

	cleaned_log = None
	if log:
		cleaned_log = json.dumps(strip_log(remove_spaces(log)), ensure_ascii=False)

	return {"changelog": cleaned_log, "recovery": recovery or ""}


def remove_spaces(d):
	if isinstance(d, dict):
		return {k: remove_spaces(v) for k, v in d.items() if v and not (isinstance(v, str) and v.isspace())}
	elif isinstance(d, list):
		return [remove_spaces(v) for v in d if v and not (isinstance(v, str) and v.isspace())]
	elif isinstance(d, str):
		# 往后从数据库读取时记得替换回来
		return d.replace('\b','').replace('\t','').replace('%','$$').replace('"','^').replace("'", "^").replace('\n','')
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
	version1 = parse_version(v1)
	version2 = parse_version(v2)
	
	if version1 is None or version2 is None:
		return False
	
	return version1 > version2


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
		response = s.post(url, headers=headers, json=True, timeout=(5, 10))
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
				if len(branch['roms']) == 0:
					i = 0
				elif len(branch['table']) != len(branch['roms'][next(iter(branch['roms']))]) :
					# 自动修复：收集所有 ROM 条目的字段并集，补全 table 缺失项
					all_rom_keys = []
					for rom_info in branch['roms'].values():
						for key in rom_info.keys():
							if key not in all_rom_keys:
								all_rom_keys.append(key)
					missing = [k for k in all_rom_keys if k not in branch['table']]
					if missing:
						branch['table'].extend(missing)
						menu_items = branch['table']
						device_file = get_platform_path(f"public/data/devices/{device}.json")
						with open(device_file, 'w', encoding='utf-8') as f:
							json.dump(data, f, ensure_ascii=False, indent='\t')
						print(f"✓ 已修复 {device} {bname} 的 table: 补充了 {missing}")
					else:
						print(device, bname, next(iter(roms)), "菜单项与ROM实际不符（无法自动修复）")
						check.append(1)
				else:
					if len(menu_items) != len(set(menu_items)):
						print(device, bname, "菜单项重复")
						check.append(1)
					else:
						for os_version, rom_info in roms.items():
							# 初始化expected_tag为None
							expected_tag = None
							# 添加对大陆正式版和Beta版的核查逻辑
							if "CNXM" in os_version:
								# 根据版本号前缀和特征进行不同的处理
								if "OS1." in os_version:
									# OS1 没有 Beta 概念，需要特别处理
									# 检查是否为开发者预览版 (PRE-DPP)、体验增强版 Beta (BETA) 等特殊版本
									if "PRE-DPP" in os_version or "PRE_DPP" in os_version:
										expected_tag = "ADPC"  # 开发者预览版
									elif ".BETA" in os_version or "BETA" in os_version:
										expected_tag = "Beta"  # 体验增强版 Beta
									elif ".EP." in os_version or "EPSTD" in os_version:
										expected_tag = "EPSTD"  # 政企版
									else:
										# 对于普通的 OS1 版本，按照 build_number 判断
										try:
											version_parts = os_version.split(".")
											if len(version_parts) >= 4:
												build_number = int(version_parts[3])
												
												# 严格按照build_number判断正式版还是Beta版
												# 只有当build_number == 0时才归类为正式版（CnOO），其余所有情况均属于Beta版（CnOB）
												# 但注意，对于OS1来说，大部分情况下都是正式版
												if build_number == 0:
													expected_tag = "CnOO"  # 正式版
												else:
													# 对于OS1，如果build_number不为0，这可能是一个特殊情况
													# 根据观察，OS1的正式版即使build_number不为0也可能是CnOO
													# 因此，对于OS1，通常应该是CnOO，除非是特殊版本
													expected_tag = "CnOO"  # OS1通常为正式版
											
										except (ValueError, IndexError):
											# 版本号格式不正确，无法解析
											print(device, bname, os_version, "版本号格式不正确，无法解析")
											check.append(1)
								
								elif "OS2." in os_version:
									# 对于OS2版本，按照原始逻辑处理
									if ".EP." in os_version or "EPSTDE" in os_version:
										expected_tag = "EPSTD"  # 政企版
									else:
										try:
											version_parts = os_version.split(".")
											if len(version_parts) >= 4:
												build_number = int(version_parts[3])
												
												# 严格按照build_number判断正式版还是Beta版
												# 只有当build_number == 0时才归类为正式版（CnOO），其余所有情况均属于Beta版（CnOB）
												if build_number == 0:
													expected_tag = "CnOO"  # 正式版
												else:
													expected_tag = "CnOB"  # Beta版
										
										except (ValueError, IndexError):
											# 版本号格式不正确，无法解析
											print(device, bname, os_version, "版本号格式不正确，无法解析")
											check.append(1)
								
								else:
									# 其他情况，尝试通用处理
									try:
										version_parts = os_version.split(".")
										if len(version_parts) >= 4:
											build_number = int(version_parts[3])
											
											# 严格按照build_number判断正式版还是Beta版
											if build_number == 0:
												expected_tag = "CnOO"  # 正式版
											else:
												expected_tag = "CnOB"  # Beta版
									
									except (ValueError, IndexError):
										# 版本号格式不正确，无法解析
										print(device, bname, os_version, "版本号格式不正确，无法解析")
										check.append(1)
								
								# 检查分支的idtag是否与预期相符（仅当expected_tag已设置时）
								actual_idtag = branch.get('idtag')
								if actual_idtag is not None and expected_tag is not None and actual_idtag != expected_tag:
									if actual_idtag in ("ADPC", "ADPG", "STDEE", "EPSTD"):
										i = 0
									else:
										print(device, bname, os_version, f"版本号标识不匹配: 期望 {expected_tag}, 实际 {actual_idtag}")
										# 注意：这里暂时注释掉检查，因为在实际数据中可能存在合理的差异
										check.append(1)
							
							# 如果不是CNXM版本且expected_tag未设置，则跳过idtag检查
							else:
								# 检查分支的idtag是否与预期相符（仅当expected_tag已设置时）
								actual_idtag = branch.get('idtag')
								if actual_idtag is not None and expected_tag is not None and actual_idtag != expected_tag:
									print(device, bname, os_version, f"版本号标识不匹配: 期望 {expected_tag}, 实际 {actual_idtag}")
									# 注意：这里暂时注释掉检查，因为在实际数据中可能存在合理的差异
									check.append(1)
							if os_version[:5] not in data['supports']:
								if "Developer" in branch['name']['en']:
									i = 0
								else:
									print(device, bname, os_version[:5], os_version, "大版本号没有记录")
									check.append(1)
							if rom_info['android'] not in data['android']:
								print(device, bname, rom_info['android'], os_version, "Android版本号没有记录")
								check.append(1)
							if rom_info['recovery'] != "" and rom_info['recovery'].endswith(".zip") and os_version in rom_info['recovery']:
								if "EP." in rom_info['recovery'] or "EPSTDE" in rom_info['recovery'] or ".PRE-" in rom_info['recovery']:
									i = 0
								else:
									if ".zip" in rom_info['recovery']:
										if "miui" in rom_info['recovery']:
											android = rom_info['recovery'].split("_")[4].split(".zip")[0]
										else:
											# 使用正则表达式提取 Android 版本号，支持 STABLE-DPP 等特殊版本
											# 例: CODE-ota_full-VERSION-user-ANDROID-HASH.zip
											recovery_match = re.search(r'-ota_full-[A-Za-z0-9\.\-]+-user-(\d+\.\d+)-[a-z0-9]+\.zip$', rom_info['recovery'])
											if recovery_match:
												android = recovery_match.group(1)
											else:
												android = rom_info['recovery'].split("ota_full-")[1].split("-")[2]
									else:
										android = rom_info['recovery'].split("images_")[1].split("_")[2]
									if rom_info['android'] != android:
										print(device, bname, os_version, android, rom_info['android'], "Android版本号不匹配")
										check.append(1)
									else: i = 0
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
							# 确定线刷包字段的起始索引
							# 如果 table 包含 aspatch，则 recovery 在索引 4，线刷包从索引 5 开始
							# 如果 table 不包含 aspatch，则 recovery 在索引 3，线刷包从索引 4 开始
							fastboot_start_index = 4
							if "aspatch" in menu_items:
								fastboot_start_index = 5
							
							for j in range(fastboot_start_index, len(menu_items)):
								if rom_info[menu_items[j]] != "" and rom_info[menu_items[j]].endswith(".tgz") and os_version in rom_info[menu_items[j]]:
									j = 0
								elif rom_info[menu_items[j]] == "":
									j = 0
								else:
									if "Developer" in branch['name']['en']:
										j = 0
									else:
										print(device, bname, os_version, "线刷包的信息不对")
										check.append(1)
									if os_version != rom_info['os']:
										print(device, bname, os_version, "版本号不匹配")
										check.append(1)
									else:
										if branch['ep'] == "1" or branch['branchtag'] == 'X':
											j = 0
										else:
											if code+branch['tag'] in os_version:
												j = 0
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

def extract_build_date_from_filename(filename):
	"""从ROM包文件名中提取ROM打包日期（注意：这不是安全补丁日期）
	
	Args:
		filename: ROM包文件名
		
	Returns:
		打包日期字符串 (YYYY-MM-DD 格式)，如果无法提取则返回None
	"""
	# 线刷包格式1: CODE-images-VERSION-TYPE-DATE-ANDROID-REGION-HASH.tgz
	# 例: arctic_eea_global-images-OS3.0.6.0.WBVEUXM-user-20260409.0000.00-16.0-eea-8581295ba6.tgz
	pattern1 = r'-(\d{8}\.\d{6})-'
	match = re.search(pattern1, filename)
	if match:
		date_str = match.group(1)[:8]  # 提取 YYYYMMDD 部分
		try:
			date_obj = datetime.strptime(date_str, '%Y%m%d')
			return date_obj.strftime('%Y-%m-%d')
		except ValueError:
			pass
	
	# 线刷包格式2: CODE_images_VERSION_DATE_ANDROID_REGION_HASH.tgz
	# 例: taiko_images_OS3.0.303.0.WOVCNXM_20260416.0000.00_16.0_cn_251b6f1689.tgz
	pattern2 = r'_(\d{8}\.\d{6})_'
	match = re.search(pattern2, filename)
	if match:
		date_str = match.group(1)[:8]  # 提取 YYYYMMDD 部分
		try:
			date_obj = datetime.strptime(date_str, '%Y%m%d')
			return date_obj.strftime('%Y-%m-%d')
		except ValueError:
			pass
	
	# 线刷包格式3: CODE_images_VERSION_DATE_ANDROID_REGION_CARRIER_HASH.tgz (运营商定制版)
	pattern3 = r'_(\d{8})\.(\d{2})(\d{2})(\d{2})_'
	match = re.search(pattern3, filename)
	if match:
		date_str = match.group(1)
		try:
			date_obj = datetime.strptime(date_str, '%Y%m%d')
			return date_obj.strftime('%Y-%m-%d')
		except ValueError:
			pass
	
	# 检测单独的日期字符串 (YYYYMMDD 格式)
	pattern4 = r'(\d{8})'
	match = re.search(pattern4, filename)
	if match:
		date_str = match.group(1)
		# 验证是否是合理的日期范围 (2010-2030)
		if 20100101 <= int(date_str) <= 20301231:
			try:
				date_obj = datetime.strptime(date_str, '%Y%m%d')
				return date_obj.strftime('%Y-%m-%d')
			except ValueError:
				pass
	
	return None

METADATA_PATH = "META-INF/com/android/metadata"
METADATA_PB_PATH = "META-INF/com/android/metadata.pb"
END_BYTES_SIZE = 65536  # 增大到 64KB，应对带较长注释的 ZIP 文件
LOCAL_HEADER_SIZE = 256
TIMEOUT_MS = 20000

# ZIP 签名常量
CENSIG = 0x02014b50  # "PK\001\002" - Central directory file header signature
LOCSIG = 0x04034b50  # "PK\003\004" - Local file header signature
ENDSIG = 0x06054b50  # "PK\005\006" - End of central directory record signature
ENDHDR = 22		  # Minimum size of end of central directory record
ZIP64_ENDSIG = 0x06064b50  # "PK\006\006" - Zip64 end of central directory record signature
ZIP64_LOCSIG = 0x07064b50  # "PK\006\007" - Zip64 end of central directory locator signature
ZIP64_LOCHDR = 20	# Size of Zip64 end of central directory locator
ZIP64_MAGICVAL = 0xFFFFFFFF  # Marker for Zip64 fields


class CdEntry:
	"""ZIP 中央目录条目"""
	def __init__(self, file_name, local_header_offset, compressed_size, uncompressed_size, method):
		self.file_name = file_name
		self.local_header_offset = local_header_offset
		self.compressed_size = compressed_size
		self.uncompressed_size = uncompressed_size
		self.method = method  # 0 = 未压缩, 8 = DEFLATE


def read_int_le(data, offset):
	"""从字节数组中读取小端序整数"""
	return struct.unpack('<I', data[offset:offset+4])[0]


def read_short_le(data, offset):
	"""从字节数组中读取小端序短整数"""
	return struct.unpack('<H', data[offset:offset+2])[0]


def read_long_le(data, offset):
	"""从字节数组中读取小端序长整数"""
	return struct.unpack('<Q', data[offset:offset+8])[0]


def locate_central_directory(bytes_data, file_length, eocd_pos_in_buffer=None):
	"""定位 ZIP 中央目录的位置和大小
	
	Args:
		bytes_data: 从文件末尾读取的字节数据
		file_length: 完整文件长度
		eocd_pos_in_buffer: EOCD 在 buffer 中的位置，如果为 None 则自动搜索
	"""
	# 如果没有指定 EOCD 位置，自动搜索
	if eocd_pos_in_buffer is None:
		search_start_pos = len(bytes_data) - ENDHDR
	else:
		search_start_pos = eocd_pos_in_buffer
	
	cen_size = -1
	cen_offset = -1

	for current_scan_pos in range(search_start_pos, -1, -1):
		if current_scan_pos + 4 > len(bytes_data):
			continue
		
		signature = read_int_le(bytes_data, current_scan_pos)
		if signature == ENDSIG:
			cen_dir_offset_field_pos = current_scan_pos + 16
			cen_dir_size_field_pos = current_scan_pos + 12

			offset_of_central_dir = read_int_le(bytes_data, cen_dir_offset_field_pos) & 0xFFFFFFFF
			size_of_central_dir = read_int_le(bytes_data, cen_dir_size_field_pos) & 0xFFFFFFFF

			if offset_of_central_dir == ZIP64_MAGICVAL or size_of_central_dir == ZIP64_MAGICVAL:
				# 需要处理 ZIP64 格式
				zip64_locator_pos = current_scan_pos - ZIP64_LOCHDR
				if zip64_locator_pos >= 0 and zip64_locator_pos + 4 <= len(bytes_data):
					if read_int_le(bytes_data, zip64_locator_pos) == ZIP64_LOCSIG:
						zip64_eocd_record_offset_in_file = read_long_le(bytes_data, zip64_locator_pos + 8)
						zip64_eocd_record_offset_in_buffer = len(bytes_data) - int(file_length - zip64_eocd_record_offset_in_file)
						
						if (zip64_eocd_record_offset_in_buffer >= 0 and
							zip64_eocd_record_offset_in_buffer + 56 <= len(bytes_data) and
							read_int_le(bytes_data, zip64_eocd_record_offset_in_buffer) == ZIP64_ENDSIG):
							
							cen_size = read_long_le(bytes_data, zip64_eocd_record_offset_in_buffer + 40)
							cen_offset = read_long_le(bytes_data, zip64_eocd_record_offset_in_buffer + 48)
							break
			else:
				cen_size = size_of_central_dir
				cen_offset = offset_of_central_dir
				break

	return cen_offset, cen_size


def locate_entries(central_directory_bytes, file_names):
	"""在中央目录中查找指定的文件条目"""
	results = {}
	pos = 0
	bytes_data = central_directory_bytes
	
	while pos + 46 <= len(bytes_data):
		signature = read_int_le(bytes_data, pos)
		if signature != CENSIG:
			break

		method = read_short_le(bytes_data, pos + 10) & 0xFFFF
		compressed_size = read_int_le(bytes_data, pos + 20) & 0xFFFFFFFF
		uncompressed_size = read_int_le(bytes_data, pos + 24) & 0xFFFFFFFF
		file_name_length = read_short_le(bytes_data, pos + 28) & 0xFFFF
		extra_field_length = read_short_le(bytes_data, pos + 30) & 0xFFFF
		file_comment_length = read_short_le(bytes_data, pos + 32) & 0xFFFF
		local_header_offset = read_int_le(bytes_data, pos + 42) & 0xFFFFFFFF

		file_name_start_pos = pos + 46
		if file_name_start_pos + file_name_length > len(bytes_data):
			break

		current_file_name = bytes_data[file_name_start_pos:file_name_start_pos+file_name_length].decode('utf-8', errors='ignore')
		
		if current_file_name in file_names:
			results[current_file_name] = CdEntry(
				file_name=current_file_name,
				local_header_offset=local_header_offset,
				compressed_size=compressed_size,
				uncompressed_size=uncompressed_size,
				method=method
			)
			if len(results) == len(file_names):
				break

		pos = file_name_start_pos + file_name_length + extra_field_length + file_comment_length

	return results


def locate_local_file_offset(local_header_bytes):
	"""定位本地文件头中的实际数据偏移"""
	if len(local_header_bytes) < 4:
		return -1
	
	signature = read_int_le(local_header_bytes, 0)
	if signature == LOCSIG:
		file_name_length = read_short_le(local_header_bytes, 26) & 0xFFFF
		extra_field_length = read_short_le(local_header_bytes, 28) & 0xFFFF
		return 30 + file_name_length + extra_field_length
	return -1


def read_range(url, start, size, timeout=20):
	"""通过 HTTP Range 请求读取文件的指定字节范围"""
	if size <= 0 or start < 0:
		return None

	try:
		session = requests.Session()
		retry = Retry(connect=3, backoff_factor=1)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('http://', adapter)
		session.mount('https://', adapter)

		headers = {'Range': f'bytes={start}-{start + size - 1}'}
		response = session.get(url, headers=headers, timeout=timeout)
		
		if response.status_code not in (200, 206):
			return None
		
		content = response.content
		
		# 检查返回内容是否为 XML 错误文档（服务器返回的错误信息）
		if content.startswith(b'<?xml') or content.startswith(b'<Error'):
			print("服务器返回 XML 错误文档，资源可能已被删除")
			return None
		
		# 检查内容类型是否为已知的错误类型
		content_type = response.headers.get('Content-Type', '').lower()
		if content_type in ('application/xml', 'text/xml') and b'<Error>' in content:
			print("服务器返回 XML 错误响应，资源不存在或已被删除")
			return None
		
		if len(content) < size:
			print(f"读取字节数不足，期望 {size} 字节，实际 {len(content)} 字节")
			return None
		
		return content[:size] if len(content) > size else content
		
	except Exception as e:
		print(f"读取范围失败: {e}")
		return None


def get_file_length(url, timeout=20):
	"""获取远程文件的大小"""
	try:
		session = requests.Session()
		retry = Retry(connect=3, backoff_factor=1)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('http://', adapter)
		session.mount('https://', adapter)

		# 先尝试 HEAD 请求
		response = session.head(url, headers={'Range': 'bytes=0-0'}, timeout=timeout)
		
		# 检查是否返回错误状态码
		if response.status_code >= 400:
			return None
		
		if 'Content-Range' in response.headers:
			content_range = response.headers['Content-Range']
			parts = content_range.split('/')
			if len(parts) > 1:
				file_len = int(parts[1])
				if file_len > 0:
					return file_len
		
		if 'Content-Length' in response.headers:
			file_len = int(response.headers['Content-Length'])
			if file_len > 0:
				return file_len

		return None
	except Exception as e:
		print(f"获取文件长度失败: {e}")
		return None


def read_entry_bytes(url, entry, file_length, timeout=20):
	"""读取指定条目的数据内容"""
	header_offset = entry.local_header_offset
	
	if header_offset < 0 or header_offset >= file_length:
		return None

	max_local_header_read = min(file_length - header_offset, LOCAL_HEADER_SIZE)
	if max_local_header_read < 30:
		return None

	local_header_bytes = read_range(url, header_offset, int(max_local_header_read), timeout)
	if local_header_bytes is None:
		return None

	internal_offset = locate_local_file_offset(local_header_bytes)
	if internal_offset < 0 or internal_offset > max_local_header_read:
		return None

	data_offset = header_offset + internal_offset
	size = entry.uncompressed_size
	
	if size < 0 or size > file_length or data_offset + size > file_length:
		return None

	return read_range(url, data_offset, int(size), timeout)


def parse_text_metadata(text):
	"""解析文本格式的 metadata"""
	result = {
		'ota_type': 0,
		'pre': {},
		'post': {}
	}
	meta_map = {}
	
	for line in text.split('\n'):
		trimmed = line.strip()
		if not trimmed or trimmed.startswith('#'):
			continue
		idx = trimmed.find('=')
		if idx > 0:
			meta_map[trimmed[:idx]] = trimmed[idx+1:]

	# 解析 OTA 类型
	ota_type = meta_map.get('ota-type', '').upper()
	if ota_type == 'AB':
		result['ota_type'] = 1
	elif ota_type == 'BLOCK':
		result['ota_type'] = 2
	elif ota_type == 'BRICK':
		result['ota_type'] = 3
	else:
		result['ota_type'] = 0

	# 解析 pre 条件
	has_pre = any(k.startswith('pre-') for k in meta_map.keys())
	if has_pre:
		result['pre'] = {
			'device': meta_map.get('pre-device', '').split(','),
			'build': meta_map.get('pre-build', '').split(','),
			'build_incremental': meta_map.get('pre-build-incremental', '')
		}

	# 解析 post 条件（安全补丁信息）
	result['post'] = {
		'device': meta_map.get('post-device', '').split(','),
		'build': meta_map.get('post-build', '').split(','),
		'build_incremental': meta_map.get('post-build-incremental', ''),
		'timestamp': int(meta_map.get('post-timestamp', '0')),
		'sdk_level': meta_map.get('post-sdk-level', ''),
		'security_patch_level': meta_map.get('post-security-patch-level', '')
	}

	return result


def extract_ota_metadata(url,filetype, timeout=20):
		if filetype == 'recovery':
			try:
					# 1. 获取文件大小
					file_length = get_file_length(url, timeout)
					if file_length is None or file_length <= 0:
							print("无法获取文件长度")
							return None

					# 2. 使用阶梯策略读取文件末尾字节查找中央目录
					# 从小到大逐步增加读取大小，直到找到 EOCD 签名并成功定位中央目录
					step_sizes = [4*1024, 16*1024, 64*1024, 256*1024, 512*1024, 1*1024*1024, 5*1024*1024]  # 4KB, 16KB, 64KB, 256KB, 512KB, 1MB, 5MB
					cen_offset = -1
					cen_size = -1
					actual_end_size = 0
					
					for step_size in step_sizes:
							actual_end_size = min(file_length, step_size)
							if actual_end_size <= 0:
									continue
							
							end_bytes = read_range(url, file_length - actual_end_size, int(actual_end_size), timeout)
							if end_bytes is None:
									continue
							
							# 检查是否包含 EOCD 签名
							ENDSIG = 0x06054b50  # "PK\005\006"
							pos = len(end_bytes) - ENDHDR
							eocd_pos_in_buffer = -1
							while pos >= 0:
									if pos + 4 <= len(end_bytes):
											sig = int.from_bytes(end_bytes[pos:pos+4], 'little')
											if sig == ENDSIG:
													eocd_pos_in_buffer = pos
													break
									pos -= 1
							
							if eocd_pos_in_buffer < 0:
									# 未找到 EOCD 签名，继续尝试更大的读取大小
									continue
							
							# 3. 定位中央目录（使用完整 buffer，不截断，以便 ZIP64 定位器在 EOCD 之前）
							cen_offset, cen_size = locate_central_directory(end_bytes, file_length, eocd_pos_in_buffer)
							if cen_offset >= 0 and cen_size > 0 and cen_offset + cen_size <= file_length:
									# 成功定位中央目录，退出循环
									break
							else:
									# 找到 EOCD 但无法定位中央目录，继续尝试更大的读取大小
									print(f"找到 EOCD 但无法定位中央目录，尝试读取更多字节")
									continue
					
					if cen_offset < 0 or cen_size <= 0 or cen_offset + cen_size > file_length:
							print("无法定位中央目录")
							return None

					# 4. 读取中央目录内容
					central_directory = read_range(url, cen_offset, int(cen_size), timeout)
					if central_directory is None:
							print("无法读取中央目录")
							return None

					# 5. 在中央目录中查找 metadata 文件
					entries = locate_entries(central_directory, {METADATA_PB_PATH, METADATA_PATH})

					# 6. 优先尝试读取 protobuf 格式的 metadata
					if METADATA_PB_PATH in entries:
							entry = entries[METADATA_PB_PATH]
							if entry.method == 0:  # 仅处理未压缩的文件
									pb_bytes = read_entry_bytes(url, entry, file_length, timeout)
									if pb_bytes is not None:
											# 这里可以添加 Protobuf 解析逻辑
											# 由于缺少 protobuf schema，暂时跳过
											pass

					# 7. 读取文本格式的 metadata
					if METADATA_PATH in entries:
							entry = entries[METADATA_PATH]
							if entry.method == 0:  # 仅处理未压缩的文件
									text_bytes = read_entry_bytes(url, entry, file_length, timeout)
									if text_bytes is not None:
											text = text_bytes.decode('utf-8', errors='ignore')
											if text:
													return parse_text_metadata(text)

					print("未找到 metadata 文件")
					return None

			except Exception as e:
					print(f"提取 metadata 失败: {e}")
					return None
		else:
			return None


def get_security_patch_from_ota_url(url,filetype, timeout=20):
		if filetype == 'recovery':
			metadata = extract_ota_metadata(url, filetype, timeout)
			if metadata and metadata.get('post'):
				asp = metadata['post'].get('security_patch_level')
				print(asp)
				return asp
			return None
		elif filetype == 'fastboot':
			# 从 tgz 线刷包中获取安全补丁日期
			return get_security_patch_from_tgz(url, timeout)
		else:
			return None


def get_security_patch_from_tgz(url, timeout=20):
	"""从 tgz 线刷包中获取安全补丁日期"""
	import gzip
	import tarfile
	import io
	
	try:
		# 1. 获取文件大小
		file_length = get_file_length(url, timeout)
		if file_length is None or file_length <= 0:
			print("无法获取 tgz 文件长度")
			return None
		
		# 2. 逐步增加读取大小（优化带宽使用）
		# gzip 需要完整数据才能解压，但我们可以逐步尝试
		max_read_size = min(file_length, 100 * 1024 * 1024)  # 最多读取 100MB
		
		# 定义逐步读取的大小序列（从小到大）
		read_sizes = [1*1024*1024, 5*1024*1024, 10*1024*1024, 20*1024*1024, max_read_size]
		
		for read_size in read_sizes:
			if read_size > file_length:
				read_size = file_length
				
			print(f"尝试读取 {read_size//1024//1024}MB 数据...")
			
			file_bytes = read_range(url, 0, read_size, timeout)
			if file_bytes is None:
				print("无法读取 tgz 文件内容")
				continue
			
			# 3. 尝试解压 gzip
			try:
				gzip_file = gzip.GzipFile(fileobj=io.BytesIO(file_bytes))
				tar_content = gzip_file.read()
				tar_buffer = io.BytesIO(tar_content)
			except EOFError:
				print(f"gzip 文件未完整，需要读取更多数据...")
				continue
			except Exception as e:
				print(f"解压 gzip 失败: {e}")
				continue
			
			# 4. 解析 tar 文件
			try:
				with tarfile.open(fileobj=tar_buffer, mode='r') as tar:
					members = tar.getmembers()
					
					# 首先查找目标文件
					for member in members:
						if 'images/platform_security_patch.txt' in member.name:
							f = tar.extractfile(member)
							if f:
								content = f.read().decode('utf-8').strip()
								print(f"从 tgz 获取安全补丁日期: {content}")
								return content
					
					# 如果没找到，检查是否有嵌套的 tar 文件
					for member in members:
						if member.name.endswith('.tar'):
							print(f"发现嵌套 tar 文件: {member.name}")
							f = tar.extractfile(member)
							if f:
								nested_tar_buffer = io.BytesIO(f.read())
								with tarfile.open(fileobj=nested_tar_buffer, mode='r') as nested_tar:
									for nested_member in nested_tar.getmembers():
										if 'images/platform_security_patch.txt' in nested_member.name:
											nested_f = nested_tar.extractfile(nested_member)
											if nested_f:
												content = nested_f.read().decode('utf-8').strip()
												print(f"从嵌套 tar 获取安全补丁日期: {content}")
												return content
				
				print(f"读取 {read_size//1024//1024}MB 未找到目标文件，继续尝试...")
				
			except Exception as e:
				print(f"解析 tar 文件失败: {e}")
				continue
		
		print("tgz 中未找到 images/platform_security_patch.txt")
		return None
			
	except Exception as e:
		print(f"获取 tgz 安全补丁日期失败: {e}")
		return None
