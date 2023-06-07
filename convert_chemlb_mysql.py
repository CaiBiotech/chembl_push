#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import numpy as np

# -*- coding: utf-8 -*-
# encoding=utf-8

import pymysql
import pandas as pd
import numpy as np

def execute(c, command):
    c.execute(command)
    return c.fetchall()

cnx = pymysql.connect(host='localhost', port=3306, user='root',
                      password='***passwd***', db='chembl_31')

cursor = cnx.cursor()

for table in execute(cursor, "show tables;"):
    table = table[0]
    cols = []
    for item in execute(cursor, "show columns from " + table + ";"):
        cols.append(item[0])
    data = execute(cursor, "select * from " + table + ";")
    with open(table + ".csv", "w", encoding="utf-8") as out:
        out.write("\t".join(cols) + "\n")
        for row in data:
            out.write("\t".join(str(el) for el in row) + "\n")
    print(table + ".csv written")

