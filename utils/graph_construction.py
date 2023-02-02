# -*- coding: utf-8 -*-
# @Time : 2022/9/6 16:13
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: main.py
# @File : graph_construction.py
# @Software: PyCharm
import networkx
import pymysql.cursors
import networkx as nx

import matplotlib.pyplot as plt

from config import parser

from data_verify.data_verify import list_ratio_check

from utils.sql_query import *
import numpy as np

# digraph in networkx: digraph
def full_graph_contruction(args, lanes_num=None,relation_df=None):
    graph = nx.DiGraph()

    if lanes_num == None:
        lanes_num = get_full_lanes_num(args)
    if relation_df == None:
        relation_df = get_full_road_relation(args)

    nodeIDs = []
    for key in lanes_num:
        value = lanes_num[key]
        for i in range(value):
            nodeIDs.append(key+'_'+str(i))

    for row in zip(relation_df[0], relation_df[1], relation_df[2], relation_df[3], relation_df[4], relation_df[5]):
        roadID_from = row[0]
        laneID_from = row[1]
        roadID_to = row[2]

        lane_num_to = lanes_num[roadID_to]
        if laneID_from == -1:
            lane_num_from = lanes_num[roadID_from]
            for i in range(lane_num_from):
                for j in range(lane_num_to):
                    graph.add_weighted_edges_from([(roadID_from+'_'+str(i), roadID_to+'_'+str(j), 1.0)])
        else:
            for j in range(lane_num_to):
                graph.add_weighted_edges_from([(roadID_from+'_'+str(laneID_from), roadID_to+'_'+str(j), 1.0)])

    return graph

# digraph in networkx: digraph
def subgraph_construction(args, max_hop, roadID, lane_num, intersection_phases, future_intersection_phases, intersection_phases_ratio, lanes_num=None, relation_df=None, phases_detail=None):
    if lanes_num == None:
        lanes_num = get_full_lanes_num(args)
    if relation_df is None:
        relation_df = get_full_road_relation(args)
    if phases_detail == None:
        phases_detail = get_full_phases_detail(args)
    intersection_phases_ratio = list_ratio_check(intersection_phases_ratio)


    roadID_list = []
    root_lane_num_list = []
    road_lane_added = {}
    tmp_roadID_list = [roadID]
    tmp_root_lane_num_list = [lane_num]
    downstream_graph = nx.DiGraph()
    downstream_graph.add_node(roadID + '_' + str(lane_num))
    # downstream_graph: 0 to max hop
    for i in range(max_hop):
        roadID_list = tmp_roadID_list.copy()
        root_lane_num_list = tmp_root_lane_num_list.copy()
        tmp_roadID_list.clear()
        tmp_root_lane_num_list.clear()
        for node_num in range(len(roadID_list)):
            # in each hop, search 'from_road_lane' list
            root_roadID = roadID_list[node_num]
            root_lane_num = root_lane_num_list[node_num]
            root_road_lane = root_roadID+'_'+str(root_lane_num)
            if root_road_lane in road_lane_added.keys():
                continue
            road_lane_added[root_road_lane] = 1
            one_hop_df = relation_df[(relation_df[0] == root_roadID) & (relation_df[1] == root_lane_num)]
            # for each from_road_lane, search 'to_road' list
            for row in zip(one_hop_df[2], one_hop_df[4], one_hop_df[5]):
                roadID_to = row[0]
                intersectionID = row[1]
                controlID = row[2]
                # whether if controled by signal
                control_flag = True
                weight = 1.0
                if intersectionID[0] == 'H':
                    weight = 0.0
                    if intersectionID == root_roadID.split('#')[0]:
                        root_phase_detail = phases_detail[intersectionID + '_' + str(intersection_phases[intersectionID])]
                        if root_phase_detail[controlID] == '1':
                            weight = intersection_phases_ratio[intersectionID]
                        else:
                            control_flag = False
                    if intersectionID == root_roadID.split('#')[0]:
                        root_phase_detail = phases_detail[intersectionID + '_' + str(future_intersection_phases[intersectionID])]
                        if root_phase_detail[controlID] == '1':
                            control_flag = True
                            weight += intersection_phases_ratio[intersectionID]
                # for each 'to_road', traverse all lanes
                for j in range(lanes_num[roadID_to]):
                    if control_flag:
                        to_road_lane = roadID_to+'_'+str(j)
                        downstream_graph.add_weighted_edges_from([(root_road_lane, to_road_lane, weight)])
                        tmp_roadID_list.append(roadID_to)
                        tmp_root_lane_num_list.append(j)
                        print(root_road_lane, to_road_lane, weight)


    roadID_list = []
    root_lane_num_list = []
    road_lane_added = {}
    tmp_roadID_list = [roadID]
    tmp_root_lane_num_list = [lane_num]
    upstream_graph = nx.DiGraph()
    upstream_graph.add_node(roadID + '_' + str(lane_num))
    # upstream_graph: 0 to max hop
    for i in range(max_hop):
        roadID_list = tmp_roadID_list.copy()
        root_lane_num_list = tmp_root_lane_num_list.copy()
        tmp_roadID_list.clear()
        tmp_root_lane_num_list.clear()
        for node_num in range(len(roadID_list)):
            # in each hop, search 'from_road_lane' list
            root_roadID = roadID_list[node_num]
            root_lane_num = root_lane_num_list[node_num]
            root_road_lane = root_roadID + '_' + str(root_lane_num)
            if root_road_lane in road_lane_added.keys():
                continue
            road_lane_added[root_road_lane] = 1
            one_hop_df = relation_df[(relation_df[2] == root_roadID)]
            # for each to_road, search 'from_road' list
            for row in zip(one_hop_df[0], one_hop_df[1], one_hop_df[4], one_hop_df[5]):
                roadID_from = row[0]
                road_lane_from = row[1]
                intersectionID = row[2]
                # whether if controled by signal
                control_flag = True
                weight = 1.0
                if intersectionID[0] == 'H':
                    if intersectionID == roadID_from.split('#')[0]:
                        root_phase_detail = phases_detail[intersectionID + '_' + str(intersection_phases[intersectionID])]
                        if root_phase_detail[controlID] == '1':
                            weight += intersection_phases_ratio[intersectionID]
                        else:
                            control_flag = False
                    if intersectionID == roadID_from.split('#')[0]:
                        root_phase_detail = phases_detail[
                            intersectionID + '_' + str(future_intersection_phases[intersectionID])]
                        if root_phase_detail[controlID] == '1':
                            control_flag = True
                            weight += intersection_phases_ratio[intersectionID]
                if control_flag:
                    road_lane_from_num = 1
                    if road_lane_from == -1:
                        road_lane_from_num = lanes_num[roadID_from]
                    for i in range(road_lane_from_num):
                        from_road_lane = roadID_from + '_' + str(i)
                        upstream_graph.add_weighted_edges_from([(from_road_lane, root_road_lane, weight)])
                        tmp_roadID_list.append(roadID_from)
                        tmp_root_lane_num_list.append(i)
                        print(from_road_lane, root_road_lane, weight)

    return upstream_graph, downstream_graph

def disconnect_edges(DG: networkx.DiGraph, intID: str, phase_num: int, ratio: float, mode: bool, phase_details = None, relation_df = None, lanes_num=None):
    if lanes_num == None:
        lanes_num = get_full_lanes_num(args)
    if type(relation_df) == type(None):
        relation_df = get_full_road_relation(args)
    if phase_details == None:
        phase_details = get_full_phases_detail(args)

    phase_detail_str = phase_details[intID+'_'+str(phase_num)]
    for i in range(len(phase_detail_str)):
        control_letter = phase_detail_str[i]
        res_df = relation_df[(relation_df[5] == i+1) & (relation_df[4] == intID)]
        for row in res_df.itertuples():
            # print(row)
            roadID_from = row[1]
            laneID_from = row[2]
            roadID_to = row[3]
            lane_num_to = lanes_num[roadID_to]
            for j in range(lane_num_to):
                if control_letter == 'Y' or control_letter == 'y':
                    ratio = ratio / 2.0
                if (control_letter == 'R' or control_letter == 'r'):
                    if not mode:
                        DG[roadID_from + '_' + str(laneID_from)][roadID_to + '_' + str(j)]['weight'] = 0.0
                else:
                    if mode:
                        DG[roadID_from + '_' + str(laneID_from)][roadID_to + '_' + str(j)]['weight'] += ratio
                    else:
                        DG[roadID_from+'_'+str(laneID_from)][roadID_to+'_'+str(j)]['weight'] = ratio
                    if DG[roadID_from + '_' + str(laneID_from)][roadID_to + '_' + str(j)]['weight'] > 1.0:
                        DG[roadID_from + '_' + str(laneID_from)][roadID_to + '_' + str(j)]['weight'] = 1.0

    return DG

def input_data_sampling(DG: networkx.DiGraph, state_dict: dict):
    # print(state_dict)
    nodes = DG.nodes()
    adj_matrix = np.asarray(nx.adj_matrix(DG).todense())
    feature_matrix = []
    for node in nodes:
        ll = node.split('#')
        if ll[1] == '1':
            feature_matrix.append([0.0])
        else:
            aa = state_dict[node]
            feature_matrix.append([aa])
    # print(feature_matrix)
    return adj_matrix, feature_matrix

if __name__ == '__main__':

    args = parser.parse_args()

    conn = pymysql.Connect(host=args.host, port=args.port, user=args.usr, password=args.passwd, db=args.db)
    cursor = conn.cursor()
    signal_machines = []
    phases = []
    flag = True
    count_down = 5
    sql = "SELECT DISTINCT INTERSECTION_ID FROM signal_phases"
    while (flag and count_down):
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
    conn.close()

    intersection_phases = {}
    future_intersection_phases = {}
    intersection_phases_ratio = {}
    for signal_machine in signal_machines:
        if signal_machine[0] == 'N':
            intersection_phases[signal_machine] = 0
            future_intersection_phases[signal_machine] = 0
            intersection_phases_ratio[signal_machine] = 1.0
        elif signal_machine[0] == 'H':
            intersection_phases[signal_machine] = 1
            future_intersection_phases[signal_machine] = 2
            intersection_phases_ratio[signal_machine] = 0.5
        else:
            print('Add phase number error!!!')

    G = full_graph_contruction(args)
    nx.draw(G, node_size=30, with_labels=False)
    # plt.savefig("graph.png")
    plt.show()

    DG = G.copy()

    lanes_num = get_full_lanes_num(args)
    relation_df = get_full_road_relation(args)
    phases_detail = get_full_phases_detail(args)
    DG = disconnect_edges(DG, 'HS001', 1, 0.5, False, phases_detail, relation_df, lanes_num)
    DG = disconnect_edges(DG, 'HS002', 1, 0.5, False, phases_detail, relation_df, lanes_num)
    DG = disconnect_edges(DG, 'HS003', 1, 0.5, False, phases_detail, relation_df, lanes_num)
    DG = disconnect_edges(DG, 'HS004', 1, 0.5, False, phases_detail, relation_df, lanes_num)

    # adj, fea = input_data_sampling(DG, )

    # max_hop = 3
    # root_roadID = 'HS001#0#03'
    # root_lane_num = 0
    # upG, downG = subgraph_construction(args, max_hop, root_roadID, root_lane_num, intersection_phases, future_intersection_phases, intersection_phases_ratio, lanes_num, relation_df, phases_detail)
    # nx.draw(upG, node_size=30, with_labels=True)
    # plt.show()
    # nx.draw(downG, node_size=30, with_labels=True)
    # plt.show()
    #
    # up_nodes = upG.nodes
    # print(len(up_nodes), up_nodes)
    # up_adj = nx.to_scipy_sparse_matrix(upG)
    # print(up_adj)