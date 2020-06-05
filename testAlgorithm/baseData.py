# coding=utf-8

from sys import argv
from hashlib import *

class basedata:
    # 破解的算法名
    N = argv[1]

    # 特殊字符
    special = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    # 生成文件hash值的工具
    run_officefile = "file2hash/run/office2john.py files/"
    run_pdffile = "file2hash-new/run/pdf2john.pl files/"

    # 破解执行命令
    crack_file = "./Crack 1.json"              #烧位流
    crack_file0 = "./Crack -b 1.json"          #不烧位流

    # 破解模式
    mode = argv[3]

    # 用于判断不同密码长度执行的次数
    lst = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0]

    # 用于随机生成密码的95字符
    S = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    # 单种长度密码执行的次数
    count_name = argv[2]

    # 要破解的文件
    files = "1.json"

    # 获取解析错误或者未解出来的json的存放目录
    f2_path = {"0": "err_json/d_errjson/", "1": "err_json/d2_errjson/", "3": "err_json/ms_errjson/",
               "6": "err_json/dm_errjson/", "7": "err_json/md_errjson/"}

    # 存放不同长度字典的目录
    filepath = "dict/"

    # 位流文件地址
    list_bit = "bitstream/"

    # 算法的id
    hid_id = {"md4": (900, 43200), "ntlm": (1000, 43200), "md5": (0, md5), "sha1": (100, sha1), "smd5": (10, 20, md5),
              "sha256": (1400, sha256), "sha512": (1700, sha512), "office2007": (9400, 0.288), "office2010": (9500, 0.144),
              "ssha1": (110, 120, sha1), "rar5": (13000, 0.0944), "office2013": (9600, 0.0216),
              "unix512": (1800, 0.01), "ssha256": (1410, 1420, sha256), "ssha512": (1710, 1720, sha512), "pdf2": (10400, 100),
              "pdf3": (10500, 100), "pdf5": (10600, 100), "pdf6": (10700, 100)}

    # 字典插入命令
    cmd1 = "sed -i "

    # 字典其他命令
    d1 = "dict/"
    d2 = "wc -l dict/"

    # 破解的算法开始长度
    start = 1                                                   #mode为1,6,7时需要输入大于等于2的数字

    # 穷尽模式区分index之内解不出来
    index1 = 20
    index2 = 60

    # 加盐的算法名称
    saltAlgorithm = ("ssha1", "ssha256", "ssha512", "smd5", "unix512")

    # 颜色
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
