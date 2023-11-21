import json
from sys import platform
import urllib
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad
import requests


sdk = {
    "14": "34",
    "13": "33"
}

currentBeta = ["houji", "shennong", "cupid", "zeus", "daumier", "mayfly", "unicorn", "thor", "fuxi", "nuwa", "ishtar", "zizhan", "babylon", "dagu",
               "rubens", "matisse", "ingres", "diting", "mondrian", "socrates"]
currentStable = ["houji", "shennong", "fuxi","nuwa", "ishtar", "mondrian", "socrates","zizhan","babylon"]
newDevices = ["houji", "shennong", "duchamp", "manet", "vermeer"]
flags = {
    "HOUJI": "houji",
    "HOUJIDEMO": "houji",
    "houji": "houji",
    "houji_demo": "houji",
    "shennong_demo": "shennong",
    "SHENNONG": "shennong",
    "SHENNONGDEMO": "shennong",
    "shennong": "shennong",
    "FUXIDEMO":"fuxi",
    "FUXI": "fuxi",
    "fuxi": "fuxi",
    "nuwa": "nuwa",
    "NUWA": "nuwa",
    "NUWADEMO": "nuwa",
    "ISHTAR":"ishtar",
    "ishtar":"ishtar",
    "ISHTARDEMO":"ishtar",
    "ishtar_demo":"ishtar",
}
