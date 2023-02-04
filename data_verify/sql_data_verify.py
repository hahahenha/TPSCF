# -*- coding: utf-8 -*-
# @Time : 2022/9/6 14:56
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: main.py
# @File : sql_data_verify.py
# @Software: PyCharm

import pymysql.cursors

from config import parser

if __name__ == '__main__':
    args = parser.parse_args()

    #连接数据库
    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)

    #创建游标
    cursor = conn.cursor()

    signal_machines = []

    flag = True
    count_down = 5
    sql = "SELECT DISTINCT INTERSECTION_ID FROM signal_phases"
    while(flag and count_down):
           flag = False
           try:
                  cursor.execute(sql)
                  result = cursor.fetchall()
                  for row in result:
                      signal_machines.append(row[0])
           except Exception as e:
                  print(e)
                  # 连接数据库
                  conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                  # 创建游标
                  cursor = conn.cursor()
                  flag = True
                  count_down -= 1

    if count_down == 0:
        print('Error!!!')

    for signal_machine in signal_machines:
        print('Intersection ID: ' + signal_machine)
        # 001. phase number
        phase_num = -1
        flag = True
        count_down = 5
        sql = "SELECT TOTAL_PHASES FROM signal_phases WHERE INTERSECTION_ID = \"" + signal_machine + "\""
        while (flag and count_down):
            flag = False
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    phase_num = row[0]
            except Exception as e:
                print(e)
                # reconnect to the database
                conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                cursor = conn.cursor()
                flag = True
                count_down -= 1
        if phase_num == 0:
            phase_num = 1

        # 002. phase number verify
        flag = True
        count_down = 5
        sql = "SELECT count(*) FROM phases_detail WHERE INTERSECTION_ID = \"" + signal_machine + "\""
        while (flag and count_down):
            flag = False
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    if phase_num != row[0]:
                        print('\tTable: phases_detail, phase num error!!!')
            except Exception as e:
                print(e)
                # reconnect to the database
                conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                cursor = conn.cursor()
                flag = True
                count_down -= 1

        # 003. in_lane number
        road_ids = []
        lanes_num = []
        flag = True
        count_down = 5
        sql = "SELECT * FROM road_lanes WHERE ROAD_ID LIKE \"" + signal_machine + "#0#%\""
        while (flag and count_down):
            flag = False
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    road_ids.append(row[0])
                    lanes_num.append(row[1])
            except Exception as e:
                print(e)
                # reconnect to the database
                conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                cursor = conn.cursor()
                flag = True
                count_down -= 1

        # 004. in_lane number verify
        for i in range(len(road_ids)):
            flag = True
            count_down = 5
            sql = "SELECT count(DISTINCT ROAD_ID_FROM, FROM_LANE_ID) FROM road_relation WHERE ROAD_ID_FROM = \"" + road_ids[i] + "\""
            while (flag and count_down):
                flag = False
                try:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for row in result:
                        if lanes_num[i] != row[0]:
                            print('\tTable: road_relation, Road ID: ' + road_ids[i] + ', lane num error!!!')
                except Exception as e:
                    print(e)
                    # reconnect to the database
                    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                    cursor = conn.cursor()
                    flag = True
                    count_down -= 1

        # 005. control number
        control_num = -1
        flag = True
        count_down = 5
        sql = "SELECT count(*) FROM road_relation WHERE INTERSECTION_ID = \"" + signal_machine + "\""
        while (flag and count_down):
            flag = False
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    control_num = row[0]
            except Exception as e:
                print(e)
                # reconnect to the database
                conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                cursor = conn.cursor()
                flag = True
                count_down -= 1

        # 006. control number verify
        flag = True
        count_down = 5
        sql = "SELECT PHASE_DETAIL FROM phases_detail WHERE INTERSECTION_ID = \"" + signal_machine + "\""
        while (flag and count_down):
            flag = False
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    if control_num != len(row[0]):
                        print('\tTable: phases_detail, control number error!!!')
            except Exception as e:
                print(e)
                # reconnect to the database
                conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
                cursor = conn.cursor()
                flag = True
                count_down -= 1


    print('All data verified!!!')
    conn.close()