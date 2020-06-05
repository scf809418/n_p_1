# coding=utf-8

import redis

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe("ascqueue:task")

def redis_listen():
    for item in p.listen():
        if item["data"] != 1:
            # print item
            if len(item["data"].split("$")) == 4:
                return item["data"].split("$")[3]
            else:
                return 1