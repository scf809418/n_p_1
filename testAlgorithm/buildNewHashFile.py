# coding=utf-8

import getHash
import json, random, os, re, commands
from baseData import basedata
import time

special = basedata.special
S = basedata.S
count = 1
files = basedata.files
filepath = basedata.filepath
list_bit = basedata.list_bit
hid_id = basedata.hid_id
mode = basedata.mode
N = basedata.N
cmd1 = basedata.cmd1
saltAlgorithm = basedata.saltAlgorithm
Dic = {}

'''插入字典的字段'''
def dicts(s=None, line=1, num=1):
    Dic["dictWidth"] = s_len(s)
    Dic["dict"] = filepath + str(s_len(s))
    A = random.randint(0, 3)
    print "A:" + str(A)
    # start和end的区间设置
    if A == 0:
        Dic["startLineNum"] = random.randint(1, line)
        Dic["endLineNum"] = random.randint(line, num + 1)
    elif A == 1:
        Dic["startLineNum"] = -1
        Dic["endLineNum"] = -1
    elif A == 2:
        Dic["startLineNum"] = 1
        Dic["endLineNum"] = random.randint(line, num + 1)
    else:
        Dic["startLineNum"] = random.randint(1, line)
        Dic["endLineNum"] = num + 1

'''判断反斜杠是否在字符串内'''
def judge_fxg(s):
    global count
    if re.search("\\\\", s) is not None:
        return False

'''判断字符串有无特殊字符，并插入密码进入字典'''
def judge_strings(s, line):
    if len(list(set(s).intersection(set(special)))) != 0:  # 判断是否带有特殊字符
        data = ""
        for x in s:  # s为原始字符
            if x in special:
                data = data + ('\\' + x)
            else:
                data = data + x
        cmd2 = "\"" + str(line - 1) + "a" + " " + data + "\"" + " " + filepath + str(s_len(s))
        cmd = cmd1 + cmd2
    else:
        cmd2 = "\"" + str(line - 1) + "a" + " " + s + "\"" + " " + filepath + str(s_len(s))
        cmd = cmd1 + cmd2
    print cmd
    commands.getoutput(cmd)
    # fileSize = int(os.path.getsize(basedata.d1 + str(len(s))))
    # countSize = int(commands.getoutput(basedata.d2 + str(len(s))).split(" ")[0])
    # time.sleep(2)
    # print "fileSize:" + str(fileSize)
    # print "countSize:" + str(countSize*(len(s) + 1))

'''随机该json文件是否应该算出来'''
def random_json():
    return random.randint(0, 1)                                                 # 1表示能算出来

'''读取字典文件，获取总行数，返回插入行'''
def readDictFile(s):
    with open(filepath + str(len(s)), "rb") as f:
        num = 0
        while True:
            buffer = f.read()
            if not buffer:
                break
            num += buffer.count('\n')
    if (N.startswith("office") or N.startswith("rar")) and mode == str(1):
        line = random.randint(1, 1000)
    else:
        line = random.randint(1, num)
    return line, num

'''密码长度'''
def s_len(strings):  # 密码长度
    return len(strings)

'''生成新的json文件，返回原始密码和行数'''
def new_file():
    global count
    print count
    while True:
        a = 0
        str_start = ""
        str_end = ""
        hash_value, ls, rs, nums, strings, saltS, nu = getHash.get_hash()  # nu=getHash.Count(0 or 1)
        try:
            with open(files, "r+") as f:
                f.truncate()
            # if N.startswith("office") or N.startswith("rar") or N.startswith("zip")
            if N.startswith("pdf"):
                Dic["targets"] = [hash_value.split(":")[1].encode("utf-8")]
            else:
                Dic["targets"] = [hash_value.encode("utf-8")]
            Dic["algorithm"] = N
            if N in saltAlgorithm and N != "unix512":
                Dic["hid"] = hid_id[N][nums]
            else:
                Dic["hid"] = hid_id[N][0]
            if N.startswith("office2007") or N.startswith("rar") or N.startswith("zip") or N.startswith("office2010"):
                Dic["mask"] = "00000000ffffffffffffffffffffffff"
            elif N.startswith("office2013"):
                Dic["mask"] = ""
            elif N.startswith("unix512"):
                Dic["mask"] = "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
                              "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            elif N.startswith("pdf"):
                Dic["mask"] = "ffffffffffffffffffffffffffffffff"
            elif N in saltAlgorithm and N != "unix512":
                Dic["mask"] = "f" * len(hash_value.split(":")[0])
            else:
                Dic["mask"] = "f" * len(hash_value)
            if N not in os.listdir(list_bit):
                print "命令行输入算法名不正确，未匹配到对应算法目录"
                break
            else:
                wfpga = os.listdir(list_bit + N)
                for i in wfpga:
                    a += 1
                    if re.search("_" + N.upper() or "_" + N, i) is not None:
                        Dic["bitstream"] = list_bit + N + "/" + i
                        Dic["piplineCount"] = int(i.split("_")[-2])
                        break
                    elif a == len(wfpga):
                         print "无对应位流"
                         time.sleep(100000)
            Dic["mode"] = int(mode)
            '''单字典模式'''
            if int(mode) == 0:
                n1 = 10
                if judge_fxg(strings) == False:
                    continue
                line, num = readDictFile(strings)
                judge_strings(strings, line)                                                          #针对单字典不插入数据进行破解
                dicts(s=strings, line=line, num=num)
            '''双字典模式'''
            if int(mode) == 1:
                n1 = 10
                if judge_fxg(ls) == False or judge_fxg(rs) == False:
                    continue
                line, num = readDictFile(ls)
                judge_strings(ls, line)
                Dic["lDictWidth"] = s_len(ls)
                Dic["lDict"] = filepath + str(s_len(ls))
                Dic["lDictStartLineNum"] = random.randint(1, line)
                Dic["lDictEndLineNum"] = random.randint(line, num + 1)
                line, num = readDictFile(rs)
                judge_strings(rs, line)
                Dic["rDictWidth"] = s_len(rs)
                Dic["rDict"] = filepath + str(s_len(rs))
                Dic["rDictStartLineNum"] = random.randint(1, line)
                Dic["rDictEndLineNum"] = random.randint(line, num + 1)
            '''穷尽模式'''
            if int(mode) == 3:
                n1 = 10
                line = 0
                Dic["passwordLength"] = s_len(strings)
                Dic["charsets"] = []
                for i in strings:
                    n = random.randint(0, 1)                            # 判断start>end or start<end
                    index_s = S.index(i)                                # 判断给出的字符串中每一位在95位字符中的位置index
                    if 1 <= index_s <= len(
                            S) - 2:                                     # S = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !\"#$%&'(# )*+,-./:;<=>?@[\\]^_`{|}~"
                        if 10 <= index_s <= 83:
                            if n == 0:
                                str_start += S[index_s - random.randint(0, 3)]
                                str_end += S[index_s + random.randint(1, 4)]
                            else:
                                str_end += S[index_s - random.randint(0, 3)]
                                str_start += S[index_s + random.randint(1, 4)]
                            Dic["charsets"].append(S[index_s - random.randint(5, 7): index_s + random.randint(5, 7)])
                            # Dic["charsets"].append(S[index_s - 1: index_s + random.randint(2, 3)])      #专为office
                        elif 1 <= index_s <= 9:
                            if n == 0:
                                str_start += S[index_s - random.randint(0, 1)]
                                str_end += S[index_s + random.randint(1, 4)]
                            else:
                                str_end += S[index_s - random.randint(0, 1)]
                                str_start += S[index_s + random.randint(3, 6)]
                            Dic["charsets"].append(S[index_s - 1: index_s + random.randint(9, 11)])
                            # Dic["charsets"].append(S[index_s - 1: index_s + random.randint(3, 4)])      #专为office
                        elif 84 <= index_s <= 93:
                            if n == 0:
                                str_start += S[index_s - random.randint(0, 3)]
                                str_end += S[index_s + random.randint(0, 1)]
                            else:
                                str_end += S[index_s - random.randint(0, 3)]
                                str_start += S[index_s + random.randint(0, 1)]
                            Dic["charsets"].append(S[index_s - random.randint(8, 10): index_s + 1] + S[index_s + 1])
                            # Dic["charsets"].append(S[index_s - random.randint(2, 3): index_s + 1] + S[index_s + 1])            #专为office
                    elif index_s == len(S) - 1:                                                             # 94
                        if strings.index(i) == 0:
                            return 1
                        else:
                            if n == 0:
                                str_start += S[index_s - 1]
                                str_end += S[index_s]
                            else:
                                str_end += S[index_s - 1]
                                str_start += S[index_s]
                            Dic["charsets"].append(S[index_s - random.randint(9, 11): index_s] + "~")             #专为office
                            # Dic["charsets"].append(S[index_s - random.randint(2, 3): index_s] + "~")
                    elif index_s == 0:
                        if strings.index(i) == 0:
                            return 1
                        else:
                            if n == 0:
                                str_start += "0"
                                str_end += S[index_s + 1]
                            else:
                                str_end += "0"
                                str_start += S[index_s + 1]
                            # Dic["charsets"].append(S[index_s: index_s + random.randint(9, 11)])
                            Dic["charsets"].append(S[index_s: index_s + random.randint(2, 3)])
                if Dic["charsets"][0].index(str_start[0]) > Dic["charsets"][0].index(str_end[0]):
                    Dic["passwordStart"] = str_end
                    Dic["passwordEnd"] = str_start
                elif Dic["charsets"][0].index(str_start[0]) == Dic["charsets"][0].index(str_end[0]):
                    continue
                else:
                    n1 = 10#random.randint(0, 1)
                    # print "build:" + str(n1)
                    # print "S.index(strings[0]):" + str(S.index(strings[0]))
                    # if n1 == 0 and basedata.index1 < S.index(strings[0]) < basedata.index2:     # 0代表解不出来
                    #     str_start_new = str_start.replace(str_start[0], S[S.index(strings[0]) + 1])
                    #     str_end_new = str_end.replace(str_end[0], S[S.index(strings[0]) + 2])
                    #     Dic["passwordStart"] = str_start_new
                    #     Dic["passwordEnd"] = str_end_new
                    # else:
                    Dic["passwordStart"] = str_start
                    Dic["passwordEnd"] = str_end
            '''字典+穷尽模式'''
            if int(mode) == 6:
                n1 = 10
                Dic["maskWidth"] = s_len(rs)
                Dic["charsets"] = []
                for i in rs:
                    index_s = S.index(i)                                                    # 判断给出的字符串中每一位在96位字符中的位置index
                    if 1 <= index_s <= len(
                            S) - 2:                                                         # S = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
                        Dic["charsets"].append(S[index_s - random.randint(0, 1): index_s + random.randint(1, 3)])
                    elif index_s == len(S) - 1:  # 94
                        Dic["charsets"].append(S[index_s - random.randint(2, 4): index_s] + "~")
                    elif index_s == 0:
                        Dic["charsets"].append(S[index_s: index_s + random.randint(3, 6)])
                if judge_fxg(ls) == False:
                    continue
                line, num = readDictFile(ls)
                judge_strings(ls, line)
                dicts(s=ls, line=line, num=num)
            '''穷尽+字典模式'''
            if int(mode) == 7:
                n1 = 10
                Dic["maskWidth"] = s_len(ls)
                Dic["charsets"] = []
                for i in ls:
                    index_s = S.index(i)                                                                              # 判断给出的字符串中每一位在95位字符中的位置index
                    if 1 <= index_s <= len(
                            S) - 2:                                                                                   # S = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
                        Dic["charsets"].append(S[index_s - random.randint(0, 1): index_s + random.randint(1, 3)])
                    elif index_s == len(S) - 1:                                                                       # 94
                        Dic["charsets"].append(S[index_s - random.randint(2, 4): index_s] + "~")
                    elif index_s == 0:
                        Dic["charsets"].append(S[index_s: index_s + random.randint(3, 6)])
                if judge_fxg(rs) == False:
                    continue
                line, num = readDictFile(rs)
                judge_strings(rs, line)
                dicts(s=rs, line=line, num=num)
            Dic["jobId"] = 1
            Dic["taskId"] = 1234
            Dic["redisIp"] = "localhost"
            Dic["redisPort"] = 6379
            Dic["redisTaskQueue"] = "ascqueue:task"
            dic = json.dumps(Dic, indent=4)
            with open(files, "w") as f1:
                f1.write(dic)
            return strings, line, nu, n1
        except Exception, e:
            print "build:" + e.message
        finally:
            count += 1
