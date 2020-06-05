# coding=utf-8

import random
from baseData import basedata

N = basedata.N
count_name = basedata.count_name                            #单位密码循环的次数
S = basedata.S
lst = basedata.lst
mode = basedata.mode
saltAlgorithm = basedata.saltAlgorithm

'''随机该json文件是否应该算出来'''
def random_json():
    return 1                                                                                #random.randint(0, 1)

'''返回算法是否加盐'''
def algo(N):
    if N not in saltAlgorithm:
        return True
    return False

'''验证加盐和不加盐算法的位数'''
def maskLength(ls, rs):
    if N in saltAlgorithm:
        if int(mode) == 7:
            if len(ls) > 10:
                return False
        if int(mode) == 6:
            if len(rs) > 10:
                return False
        if int(mode) == 3:
            if len(ls+rs) > 11:
                return False
    else:
        if int(mode) == 7:
            if len(ls) > 11:
                return False
        if int(mode) == 6:
            if len(rs) > 11:
                return False
        if int(mode) == 3:
            if len(ls+rs) > 12:
                return False
    return True

'''双字典，字典+穷尽， 穷尽+字典 进行切割'''
def qiege(s):
    if int(mode) in (1, 6, 7):
        n = random.randint(1, len(s)-1)
        s1 = s[0: n]
        s2 = s[n: -1] + s[-1]
        return s1, s2
    return s[0: -1], s[-1]

'''计算密码长度'''
def stringLength(s):
    return len(s)

'''给密码加盐'''
def get_saltString(s):
        while 1:
            salt = ""
            if N == "unix512":
                for i in range(8):
                    salt = salt + chr(random.randint(32, 126))
                print salt
                print len(salt)
            else:
                for i in range(random.randint(1, 8)):
                    salt = salt + chr(random.randint(0, 127))
            num = random.randint(0, 1)
            if num == 0:                                                # 盐在后
                saltString = s + salt
            else:
                saltString = salt + s
            # print len(saltString)
            if len(saltString) > 32:
                continue
            return num, s, salt, saltString

'''生成新的原始密码'''
def new_string(S, n):                                               #S为95字符，n为循环次数（需要生成的密码长度）
    string1 = ""
    if n == 1 and (mode == 0 or mode == 3):
        char = random.choice(S)
        string1 = string1 + char
    else:
        for y in range(n - 1):
            char = random.choice(S)
            string1 = string1 + char
    return string1

'''对原始密码进行判断'''
def get_string():
    A = algo(N)
    for j in range(basedata.start, 33):
        if lst[j] < int(count_name):                                                #count_name为不同长度的密码循环次数
            while 1:
                string1 = new_string(S, 1 + j)
                print string1
                '''不加盐'''
                if A == True:
                    if stringLength(string1) <= 32:
                        s1, s2 = qiege(string1)
                        if maskLength(s1, s2) == False:
                            continue
                        lst[j] += 1
                        return s1, s2, random_json()
                    '''加盐'''
                else:
                    s1, s2 = qiege(string1)
                    num, s, salt, saltString = get_saltString(string1)
                    if maskLength(s1, s2) == False:
                        continue
                    lst[j] += 1
                    return s1, s2, num, s, salt, saltString, random_json()