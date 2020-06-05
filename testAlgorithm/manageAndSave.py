# coding=utf-8

import time
from shutil import copy
from baseData import basedata

S = basedata.S
N = basedata.N
files = basedata.files
mode = basedata.mode
f2_path = basedata.f2_path

def recode_time(func):
    def wrapper(i, string1, line, nu, n1):
        time1 = time.time()
        func(i, string1, line, nu, n1)
        time2 = time.time()
        print time2 - time1

    return wrapper

# @recode_time
def data(i, string1, line=None, nu=None, n1=None):
    if i == 1:                                          # nu=1表示正确的json，i=1表示未解出来, n1表示穷尽是否能解出来
        # if (nu == 1): #or (nu == 1 and mode == "3") or (nu == 1 and mode == "3" and n1 == 0):
        #and (S.index(string1[0]) <= basedata.index1 or S.index(string1[0]) >= basedata.index2)):
            copy(files, f2_path[mode] + N + "_" + "none" + "_" + str(string1) + "_" + str(line) + "_" + str(nu) + ".json")
            time.sleep(0.5)
        # else:
        #     print "right"
        #     time.sleep(0.5)
    else:
        with open("/data_dir" + i, "r") as f4:
            if (f4.read().split("\t")[1].strip("\n") != string1) or (
                    n1 == 0 and mode == "3" and basedata.index1 < S.index(string1[0]) < basedata.index2):
                f4.seek(0)
                copy(files,
                     f2_path[mode] + N + "_" + f4.read().split("\t")[1].strip("\n") + "_" + i.split("/")[
                         4] + "_" + string1 + "_" + str(line) + "_" + str(nu) + ".json")
                time.sleep(0.5)
            else:
                f4.seek(0)
                # if f4.read().split("\t")[1].strip("\n") == string1:
                print "right"
                time.sleep(0.5)
                # else:
                #         f4.seek(0)
                #         shutil.copy(files,
                #                 f2_path[mode] + N + "_" + "\"" + f4.read().split("\t")[1].strip("\n") + "\"" + "_" + i.split("/")[4] + "_" + "\"" + string1 + "\"" + "_" + str(line) + str(nu) + ".json")
                #         time.sleep(0.5)
