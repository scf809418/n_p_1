# coding=utf-8

import commands
from time import time
from manageAndSave import data
from listenRedis import redis_listen
from buildNewHashFile import new_file
from baseData import basedata

crack_file = basedata.crack_file
mode = basedata.mode
start =basedata.start
countName = int(basedata.count_name)
#counts = 1

def run():
    global count
    if int(mode) == 3:
        freq = (13 - start)*countName
    else:
        freq = (33 - start)*countName
    for x in range(1, freq + 1):
        print freq
        try:
            strings, line, nu, n1 = new_file()
            if strings == 1:
                continue
            else:
                time1 = time()
                print "begin Crack"
                print commands.getoutput(crack_file)
                i = redis_listen()
                print i
                time2 = time()
                print time2 - time1
                # fileSize = int(os.path.getsize(basedata.d1 + str(len(string1))))
                # countSize = int(commands.getoutput(basedata.d2 + str(len(string1))).split(" ")[0]) * (len(string1) + 1)
                # if fileSize != countSize:
                #     print "fileSize:" + str(fileSize)
                #     print "countSize:" + str(countSize)
                #     break
                data(i, strings, line, nu, n1)
        except Exception, e:
                print basedata.FAIL + "runjson:" + e.message + basedata.ENDC
        finally:
                print basedata.FAIL + "end" + basedata.ENDC

run()