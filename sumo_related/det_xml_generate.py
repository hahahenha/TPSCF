# -*- coding: utf-8 -*-
# @Time : 2022/9/8 13:46
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : det_xml_generate.py
# @Software: PyCharm

import os

from config import parser
from utils.sql_query import get_full_lanes_num

if __name__ == '__main__':
    args = parser.parse_args()

    map_name = args.sumo_file_name
    with open('../data/'+map_name+'.det.xml', 'w') as f:
        f.write('<additional>\n')

        road_lanes = get_full_lanes_num(args)
        for key, value in road_lanes.items():
            if key.split('#')[1] == '1':
                continue
            for i in range(value):
                road_lane = key + '_' + str(i)
                length = 70
                if key[0] != 'H':
                    length = 30
                ss = '<laneAreaDetector id="e2det_' + road_lane + '" lane="' + road_lane + '" endPos="-0.01" length="'+str(length)+'" freq="1" file="e2out.xml" timeThreshold="1.0" speedThreshold="1.39" jamThreshold="10.0"/>\n'
                f.write(ss)

        f.write('</additional>\n')

    os.system('python ../data/randomTrips.py -n ../data/'+ map_name +'.net.xml -r ../data/' + map_name + '.rou.xml -e 10000 -l --validate - flows 500')