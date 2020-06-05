# coding=utf-8

import binascii
import commands
import hashlib
import random
import os
import randomString
from baseData import basedata
import crypt

special = basedata.special
N = basedata.N
run_office = basedata.run_officefile
run_pdf = basedata.run_pdffile
saltAlgorithm = basedata.saltAlgorithm

if N.startswith("office") or N.startswith("rar") or N.startswith("zip") or N.startswith("pdf"):
    next_files = os.listdir("files/" + N)

def cpty(hash_obj, s0, s1, num=None, strings=None, salt=None, saltS=None, Count=None):          # s0:密码的前一段，s1:密码的后一段
    hash_value = hash_obj.hexdigest()                                                           # hash_obg = 加盐的原始密码字符串对象
    if N in saltAlgorithm:
            return hash_value + ":" + binascii.hexlify(salt), s0, s1, num, strings, saltS, Count
    return hash_value, s0, s1, num, s0+s1, saltS, Count

def deal_sring(string1, data):
    for x in string1:
        if x in special:
            data = data + ('\\' + x)
        else:
            data = data + x
    return data

def creat_hashobj(S):
    Count = 1#S[2]                                                                       # 判断能否解出hash，1表示能解得出来，0表示解不出来
    print "getHash:" + str(Count)
    if N in saltAlgorithm and N != "unix512":
        Count = 1#S[6]                                                                    # 判断能否解出hash，1表示能解得出来，0表示解不出来
        print "getHash_salt:" + str(Count)
        if Count == 1:
            hash_obj = basedata.hid_id[N][2](S[5])
        else:
            hash_obj = basedata.hid_id[N][2](S[5] + "b")
        return cpty(hash_obj, S[0], S[1], S[2], S[3], S[4], S[5], Count)
    elif N =="md4":
        if Count == 1:
            hash_obj = hashlib.new("md4", S[0] + S[1])
        else:
            hash_obj = hashlib.new("md4", S[0] + S[1] + "a")
    elif N =="ntlm":
        if Count == 1:
            hash_obj = hashlib.new("md4", (S[0] + S[1]).encode('utf-16le'))
        else:
            hash_obj = hashlib.new("md4", (S[0] + S[1] + "a").encode('utf-16le'))
    elif N == "unix512":
        Count = 1                           #S[6]
        print "getHash_salt:" + str(Count)
        if Count == 1:
            hash_value = crypt.crypt(S[3], "$6$" + S[4] + "$")
        else:
            hash_value = crypt.crypt(S[3] + "c", "$6$" + S[4] + "$")
        print hash_value, S[4], len(S[4])
        return hash_value, S[0], S[1], S[2], S[3], S[5], Count
    else:
        if Count == 1:
            hash_obj = basedata.hid_id[N][1](S[0] + S[1])
        else:
            hash_obj = basedata.hid_id[N][1](S[0] + S[1] + "a")
    return cpty(hash_obj, s0=S[0], s1=S[1], Count=Count)

def get_hash():
    data = ""
    if N.startswith("office"):
        new_file = random.choice(next_files)
        try:
            string1 = new_file[0:-5]                                                #原始密码（文件名）
            s0 = string1[0:random.randint(1, len(string1) - 1)]
            s1 = string1[len(s0) - len(string1):-1] + string1[-1]
            string2 = new_file[-5:]                                                 #文件后缀名
            if len(list(set(string1).intersection(set(special)))) != 0:             #判断是否带有特殊字符
                data = deal_sring(string1, data)
                hash_value = commands.getoutput(
                    "python" + " " + run_office + N + "/" + data + string2)
            else:
                hash_value = commands.getoutput(
                    "python" + " " + run_office + N + "/" + new_file)
            print hash_value, s0, s1, string1
            return hash_value, s0, s1, None, string1, None, 1
        except Exception, e:
            print e.message
        finally:
            next_files.remove(new_file)
    elif N.startswith("pdf"):
        new_file = random.choice(next_files)
        try:
            string1 = new_file[0:-4]                                            # 原始密码（文件名）
            s0 = string1[0:random.randint(1, len(string1) - 1)]
            s1 = string1[len(s0) - len(string1):-1] + string1[-1]
            string2 = new_file[-4:]  # 文件后缀名
            if len(list(set(string1).intersection(set(special)))) != 0:         # 判断是否带有特殊字符
                data = deal_sring(string1, data)
                hash_value = commands.getoutput(run_pdf + N + "/" + data + string2)
            else:
                hash_value = commands.getoutput(run_pdf + N + "/" + new_file)
            print hash_value, s0, s1, string1
            return hash_value, s0, s1, None, string1, None, 1
        except Exception, e:
            print e.message
        finally:
            next_files.remove(new_file)
    elif N.startswith("rar"):
        rar5 = random.choice(next_files)
        try:
            string1 = rar5.split("_$rar5$")[0]
            s0 = string1[0:random.randint(1, len(string1) - 1)]
            s1 = string1[len(s0) - len(string1):-1] + string1[-1]
            hash_value = "$rar5$" + rar5.split("_$rar5$")[1]
            print hash_value, s0, s1, string1
            return hash_value, s0, s1, None, string1, None, 1
        except Exception, e:
            print e.message
        finally:
            next_files.remove(rar5)
    else:
        S = randomString.get_string()                                                                    #S[012345]s1, s2, num, s, salt, saltString
        return creat_hashobj(S)
