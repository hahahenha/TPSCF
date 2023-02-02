# -*- coding: utf-8 -*-
# @Time : 2022/9/8 13:31
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : sql_query.py
# @Software: PyCharm

import pymysql
import pandas as pd

from config import parser

# dict Format: {roadID : lane-num}
def get_full_lanes_num(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    lanes_num = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.road_lanes_name
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                lanes_num[row[0]] = row[1]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return lanes_num

# dict Format: {roadID : lane-num}
def get_full_in_lanes_num(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    lanes_num = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.road_lanes_name + " WHERE ROAD_ID LIKE '%#0#%'"
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                lanes_num[row[0]] = row[1]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return lanes_num

# dataframe Format:  df[0] - df[5] -- From-roadID, From-lane-num, To-roadID, Direction, IntersectionID, Control-num
def get_full_road_relation(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.road_relation_name
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            relation_data = cursor.fetchall()
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    relation_df = pd.DataFrame(list(relation_data))
    return relation_df

# dict Format: {intersectionID_phase-num : phase-detail}
def get_full_phases_detail(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    phases_detail = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.phases_detail_name
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                phases_detail[row[0]+'_'+str(row[1]-1)] = row[2]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return phases_detail

# 2 dict Format: {intersectionID_phase-num : min-green-time},
#                       {intersectionID_phase-num : max-green-time}
def get_full_minmax_green_time_limit(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    min_green_time = {}
    max_green_time = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.phases_detail_name
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                min_green_time[row[0]+'_'+str(row[1]-1)] = row[3]
                max_green_time[row[0]+'_'+str(row[1]-1)] = row[4]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return min_green_time, max_green_time

# string: phase-detail
def get_phase_detail(args, intersectionID, intersection_phase):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    phase_detail = ""
    flag = True
    count_down = 5
    sql = "SELECT PHASE_DETAIL FROM " + args.phases_detail_name + " WHERE INTERSECTION_ID = \"" + intersectionID + "\" AND PHASE_NUM = " + str(
        intersection_phase)
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                phase_detail = row[0]
        except Exception as e:
            print(e)
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return phase_detail

# int, int: MIN_GREEN_TIME, MAX_GREEN_TIME
def get_minmax_green_time_limit(args, intersectionID, intersection_phase):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    MIN_GREEN_TIME = 0
    MAX_GREEN_TIME = 255
    flag = True
    count_down = 5
    sql = "SELECT MIN_GREEN_TIME, MAX_GREEN_TIME FROM " + args.phases_detail_name + " WHERE INTERSECTION_ID = \"" + intersectionID + "\" AND PHASE_NUM = " + str(
        intersection_phase)
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                MIN_GREEN_TIME = row[0]
                MAX_GREEN_TIME = row[1]
        except Exception as e:
            print(e)
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return MIN_GREEN_TIME, MAX_GREEN_TIME

# dict {roadID: lane-num}
def get_signal_intersection_lanes_num(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    lanes_num = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.road_lanes_name + " WHERE ROAD_ID LIKE \'HS%#0#%\' ORDER BY ROAD_ID"
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                lanes_num[row[0]] = row[1]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return lanes_num

# dict of signal controlled intersections: {intersectionID: total_phase_num}
def get_signal_intersections_phase(args):
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    intersections = {}
    flag = True
    count_down = 5
    sql = "SELECT * FROM " + args.signal_phases_name + " WHERE INTERSECTION_ID LIKE \'HS%\' ORDER BY INTERSECTION_ID"
    while (flag and count_down):
        flag = False
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                intersections[row[0]] = row[1]
        except Exception as e:
            print(e)
            # reconnect to the database
            conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
            cursor = conn.cursor()
            flag = True
            count_down -= 1
    conn.close()
    return intersections


if __name__ == '__main__':
    args = parser.parse_args()

    print(get_signal_intersection_lanes_num(args))

    print(get_signal_intersections_phase(args))