#!/usr/bin/env python
# -*- coding: utf-8 -*

import time

import pymongo


def clean_up_mongo():
    conn_link = 'mongodb://127.0.0.1:27017/'
    monclient = pymongo.MongoClient(conn_link)
    mydb = monclient['rain']
    col_list = mydb.list_collection_names()
    for col_name in col_list:
        mycol = mydb[col_name]
        one_data = mycol.find().sort('time', -1).limit(1).next()
        recode_time = one_data['time']
        now_time = int(time.time())
        if (now_time - recode_time) > 0:
            mydb.drop_collection(col_name)


if __name__ == "__main__":
    clean_up_mongo()
