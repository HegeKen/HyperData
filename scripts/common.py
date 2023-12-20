import json
from sys import platform
import urllib
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad
import requests
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

currentBeta = ["cupid", "zeus", "mayfly", "unicorn", "thor", "houji", "shennong", "daumier", "fuxi", "nuwa",
               "ishtar", "zizhan", "babylon", "dagu", "rubens", "matisse", "ingres", "diting", "mondrian", "socrates"]
currentStable = ["liuqin", "yudi", "marble", "sea", "plato", "topaz", "dagu", "cupid", "zeus", "mayfly", "unicorn", "thor", "corot",
                 "duchamp", "daumier", "vermeer", "manet", "houji", "shennong", "fuxi", "nuwa",
                 "ishtar", "rubens", "matisse", "ingres", "diting", "mondrian", "socrates", "zizhan", "babylon"]
newDevices = ["aurora", "sheng", "amber", "houji",
              "shennong", "duchamp", "vermeer", "manet"]
flags = {
    "HOUJI": "houji",
    "HOUJIDEMO": "houji",
    "houji": "houji",
    "houji_demo": "houji",
    "DAGU": "dagu",
    "dagu": "dagu",
    "shennong_demo": "shennong",
    "SHENNONG": "shennong",
    "SHENNONGDEMO": "shennong",
    "LIUQIN":"liuqin",
    "liuqin":"liuqin",
    "DAUMIER": "daumier",
    "MARBLEEEAGlobal": "marble",
    "SEAGlobal": "sea",
    "PLATOEEAGlobal": "plato",
    "TOPAZGlobal": "topaz",
    "FUXIEEAGlobal": "fuxi",
    "FUXIGlobal": "fuxi",
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
    "DAUMIER": "daumier",
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
    "vermeer_demo": "vermeer",
    "vermeer": "vermeer",
    "DUCHAMP": "duchamp",
    "DUCHAMPDEMO": "duchamp",
    "duchamp_demo": "duchamp",
    "duchamp": "duchamp",
    "MANET": "manet",
    "CUPID": "cupid",
    "ZEUS": "zeus",
    "MAYFLY": "mayfly",
    "UNICORN": "unicorn",
    "THOR": "thor",
    "COROT": "corot",
    "cupid": "cupid",
    "zeus": "zeus",
    "mayfly": "mayfly",
    "unicorn": "unicorn",
    "thor": "thor",
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
        devdata = json.loads(open(
            "public/data/devices/"+codename+".json", 'r', encoding='utf-8').read())
    else:
        devdata = json.loads(open("/sdcard/Codes/HyperOS.fans/public/data/devices/" +
                             codename+".json", 'r', encoding='utf-8').read())
    return devdata


def writeData(filename):
    print("发现未收录版本")
    if platform == "win32":
        file = open("public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
    else:
        file = open(
            "/sdcard/Codes/HyperOS.fans/public/data/scripts/NewROMs.txt", "a", encoding='utf-8')
    file.write(filename+"\n")
    file.close()


def writeFlag(flag, device):
    if platform == "win32":
        file = open("public/data/scripts/Flags.json", "a", encoding='utf-8')
    else:
        file = open(
            "/sdcard/Codes/HyperOS.fans/public/data/scripts/Flags.json", "a", encoding='utf-8')
    file.write("\""+flag+"\":\""+device+"\",\n")
    file.close()


def getDeviceCode(filename):
    if ".zip" in filename:
        flag = filename.split('_')[1]
        if flag in flags:
            codename = flags[flag]
            return codename
        else:
            writeFlag(flag, "")
            return 0
    elif ".tgz" in filename:
        flag = filename.split('_images')[0]
        codename = flags[flag]
        if flag in flags:
            codename = flags[flag]
            return codename
        else:
            writeFlag(flag, "")
            return 0
    else:
        return 0


def checkExit(filename):
    if "OS" in filename:
        if "blockota" in filename:
            i = 0
        else:
            if getDeviceCode(filename) == 0:
                writeData(filename)
            elif filename in localData(getDeviceCode(filename)).__str__():
                i = 0
            else:
                writeData(filename)
    else:
        i = 0


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
    if platform == "win32":
        devdata = json.loads(
            open("public/data/devices/"+device+".json", 'r', encoding='utf-8').read())
    else:
        devdata = json.loads(open(
            "/sdcard/Codes/HyperOS.fans/public/data/devices/"+device+".json", 'r', encoding='utf-8').read())
    response = requests.post(check_url, headers=headers, data=data)
    print("\r"+"正在抓取"+devdata["name"]["zh"]+"(" +
          devdata["device"]+")                  ", end="")
    if "code" in response.text:
        print(json.loads(response.text))
    else:
        data = miui_decrypt(response.text.split("q=")[0])
        if "LatestRom" in data:
            package = data["LatestRom"]["filename"].split("?")[0]
            print(package)
            checkExit(package)
            return 1
        if "CrossRom" in data:
            package = data["CrossRom"]["filename"].split("?")[0]
            print(package)
            checkExit(package)
            return 1
        else:
            print(data["Code"])
            return 0
    response.close()


def MiFirm(url):
    options = Options()
    driver = webdriver.Edge(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    lists = soup.find_all(
        'a', class_='elementor-button elementor-button-link elementor-size-xs')
    for list in lists:
        link = list.attrs['href']
        if 'mifirmware' in link:
            i = 0
        elif 'telegram' in link:
            i = 0
        else:
            if '.zip' in link:
                checkExit(link.split('/')[4])
            elif '.tgz' in link:
                checkExit(link.split('/')[4])
            else:
                writeData(link)


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
          devdata["codename"]+")                  ", end="")
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
                checkExit(data["filename"])
            else:
                i = 0
    else:
        i = 0
    response.close()
