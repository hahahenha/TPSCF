# -*- coding: utf-8 -*-
# @Time : 2022/9/9 16:54
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : sumo_env.py
# @Software: PyCharm

from sumolib import checkBinary
import traci
from utils import plot_metrics
import os
import platform

from utils.sql_query import *

# constant
t_count_down = 10
T_Y_TRANS = 2                                                 # Signal transition time when changing sides
OCC_TH_HIGH = 0.7                                          # Detector occupancy high threshold for jamming
OCC_TH_LOW = 0.3                                           # Detector occupancy low threshold for jamming
NUM_INTN_ROADS = {}  # number of roads in signal controlled intersections
NUM_FULL_ROADS = 0  # number of roads that have detectors
NUM_LANES = {}      # number of lanes for each road in signal controlled intersections
TL_IDS = []         # list of intersectionID with signal controlled

args = parser.parse_args()
# {roadID : lane-num}
full_in_lanes_num = get_full_in_lanes_num(args)
# {intersectionID: total_phase_num}
intersections_phase = get_signal_intersections_phase(args)
# {intersectionID_phase-num : min-green-time},
#                       {intersectionID_phase-num : max-green-time}
MIN_GREEN_TIME, MAX_GREEN_TIME = get_full_minmax_green_time_limit(args)
# df[0] - df[5] -- From-roadID, From-lane-num, To-roadID, Direction, IntersectionID, Control-num
road_relation_df = get_full_road_relation(args)
# dict Format: {intersectionID_phase-num : phase-detail}
phases_detail = get_full_phases_detail(args)

curr_state = {}
prev_state = {}
for key, value in full_in_lanes_num.items():
    iID, in_out, roadNo = key.split('#')
    if key[0] == 'H':
        if iID in NUM_INTN_ROADS.keys():
            NUM_INTN_ROADS[iID] += 1
        else:
            NUM_INTN_ROADS[iID] = 1
        NUM_LANES[key] = value
    curr_state[key] = 0.0
    prev_state[key] = 0.0
    NUM_FULL_ROADS += 1

intn_control_action = {}
intn_cur_action = {}
t = {}
for key, value in intersections_phase.items():
    t[key] = 0
    TL_IDS.append(key)
    intn_control_action[key] = 1
    intn_cur_action[key] = 1

QLEN_FILE = "data/qlengths.xml"
qlenfile = open(QLEN_FILE, 'w')

sumoBinary = checkBinary('sumo-gui')                        # mode of SUMO

first_act_of_run = 0                                        # flag for occurrence of first action of a run
counting_time = 0

# Desc: Starts a new simulation run by generating a random routes file. Also reinitializes the detector counts etc.
# Inputs - run: run number, 0 implies first run
# Outputs - None
def start_new_run(run):

    global curr_state, prev_state, curr_all_state, prev_all_state, intn_control_action, intn_cur_action, first_act_of_run, counting_time, qlenfile, t_count_down

    TL_IDS = []
    intn_control_action = {}
    intn_cur_action = {}
    t = {}
    t_count_down = {}

    curr_state = {}
    curr_all_state = {}
    prev_state = {}
    prev_all_state = {}
    for key, value in intersections_phase.items():
        t_count_down[key] = 10
        t[key] = 0
        TL_IDS.append(key)
        intn_control_action[key] = -1
        intn_cur_action[key] = -1

        curr_all_state[key] = {}
        prev_all_state[key] = {}
        curr_state[key] = {}
        prev_state[key] = {}
        for key2, value2 in full_in_lanes_num.items():
            curr_state[key][key2] = 0.0
            prev_state[key][key2] = 0.0
            for i in range(value2):
                curr_all_state[key][key2+'_'+str(i)] = 0.0
                prev_all_state[key][key2+'_'+str(i)] = 0.0

    first_act_of_run = 0
    counting_time = 0

    # Setup plot_metrics for a new set of runs
    if run == 0:
        plot_metrics.init(100)

    ss = args.sumo_file_name
    if platform.system() == 'Windows':
        # Generate a new random routes file
        os.system(
            "python \"%SUMO_HOME%/tools/randomTrips.py\" -n data/" + ss + ".net.xml --trip-attributes=\"type=\\\"light_norm_heavy\\\"\" "
                                                                          "-a data/" + ss + ".add.xml -r data/" + ss + ".rou.xml -e 10000 -p 0.75 --binomial=5 -L")
        print('Delete useless files...')
        # Delete unwanted alt route file
        os.system("del \"data\\" + ss + ".rou.alt.xml\"")
        # Delete unwanted trips file
        os.system("del trips.trips.xml")
    elif platform.system() == 'Linux':
        # Generate a new random routes file
        os.system(
            "python \"$SUMO_HOME/tools/randomTrips.py\" -n data/" + ss + ".net.xml --trip-attributes=\"type=\\\"light_norm_heavy\\\"\" "
                                                                         "-a data/" + ss + ".add.xml -r data/" + ss + ".rou.xml -e 10000 -p 0.75 --binomial=5 -L")
        print('Delete useless files...')
        # Delete unwanted alt route file
        os.system("rm \"data/" + ss + ".rou.alt.xml\"")
        # Delete unwanted trips file
        os.system("rm trips.trips.xml")

    # Start SUMO and connect traCI to it
    traci.start([sumoBinary, "-c", "data/" + ss + ".sumocfg", "--gui-settings-file", "data/guisettings.xml",
                 "--start", "--quit-on-end", "--no-warnings"])

    qlenfile = open(QLEN_FILE, 'w')
    qlenfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n\n")
    qlenfile.write("<qlengths>" + '\n')
    qlenfile.flush()

    return

# Desc: Enable/Disable GUI mode of SUMO
# Inputs - mode: 1 = GUI mode, 0 = non-GUI mode
# Outputs - None
def endis_sumo_guimode(mode):

    global sumoBinary

    if mode == 1:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    return

# Desc: Returns the detector occupancies at the intersections currently.
# Inputs - None
# Outputs - state: 15-element array containing the detector occupancies at the intersections currently
def get_current_state():
    state = {}

    state_all = {}

    for key, value in full_in_lanes_num.items():
        n = 0.0
        for j in range(value):
            state_all[key + '_' + str(j)] = traci.lanearea.getLastStepOccupancy("e2det_" + key + "_" + str(j)) / 100.0
            n = max(n, traci.lanearea.getLastStepOccupancy("e2det_" + key + "_" + str(j)) / 100.0)
        state[key] = n
        if n > 1:
            print('test state:', n)

    return state, state_all

def get_all_lane_state():
    state = {}

    for key, value in full_in_lanes_num.items():
        for j in range(value):
            state[key + '_' + str(j)] = traci.lanearea.getLastStepOccupancy("e2det_" + key + "_" + str(j)) / 100.0

    return state

def get_current_phase_num(intID):
    global intn_control_action, intn_cur_action
    intn_cur_action[intID] = traci.trafficlight.getPhase(intID)
    # print(traci.trafficlight.getPhaseDuration(intID))
    if getPhaseCountDown(intID) == (traci.trafficlight.getPhaseDuration(intID) / 1000 - 1):
        intn_control_action[intID] = intn_cur_action[intID]
    return intn_cur_action[intID]

def get_next_phase_num(intID, total_phase_num):
    global intn_control_action, intn_cur_action
    if intn_control_action[intID] == intn_cur_action[intID] or intn_control_action[intID] == -1:
        return (intn_control_action[intID] + 1) % total_phase_num
    return intn_control_action[intID]

def getPhaseCountDown(intID):
    return (traci.trafficlight.getNextSwitch(intID) - traci.simulation.getCurrentTime()) / 1000

# Desc: Calculates the reward when transitioning states.
# Inputs - curr_state: Current state of congestion
#          prev_state: Previous state of congestion
#          a: Action taken for going from prev to curr state
# Outputs - Reward: Reward
def calculate_reward(current_state, previous_state, intID, phase_num, current_all_state, previous_all_state):
    assert type(intID) == str # intersectionID
    assert type(phase_num) == int # phase_num

    # print('test intID:', intID)

    Reward = 0

    # static signalling; reward doesn't matter
    if phase_num == -1:
        return 0

    total_phase_num = intersections_phase[intID]
    if phase_num % 2 != 0:
        print('Action error!!!')
        phase_num = (phase_num + 1) % total_phase_num

    cur_state = 0
    pre_state = 0
    # phase detail
    # print('test phase num:', phase_num)
    phasedet = phases_detail[str(intID)+'_'+str(phase_num)]
    # print('test phase detail:', phasedet)
    for i in range(len(phasedet)):
        if phasedet[i] == '1':
            ind = i + 1
            relation_res = road_relation_df[(road_relation_df[5]==ind) & (road_relation_df[4] == intID)]
            for index, row in relation_res.iterrows():
                roadID_from = row[0]
                lane_ID = row[1]
                roadID_to = row[2]
                # print('test row[4]:', row[4])
                assert intID == row[4]
                lane_str = str(roadID_from) + '_' + str(lane_ID)
                # print('test lane string:', lane_str)

                cur_state = current_all_state[lane_str]
                pre_state = previous_all_state[lane_str]
                # cur_state = current_state[roadID_from]
                # pre_state = previous_state[roadID_from]

                if cur_state < OCC_TH_LOW and pre_state < OCC_TH_LOW:
                    Reward = -40
                elif cur_state >= OCC_TH_LOW and pre_state < OCC_TH_LOW:
                    Reward = -20
                elif cur_state < OCC_TH_LOW and (OCC_TH_LOW <= pre_state < OCC_TH_HIGH):
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)

                        # tmp_lane_num = full_in_lanes_num[tmp_road_key]
                        # for i in range(tmp_lane_num):
                        #     tmp_lane_str = tmp_road_key + '_' + str(i)
                        #     prev_state_arr.append(previous_all_state[tmp_lane_str])
                        prev_state_arr.append(previous_state[tmp_road_key])

                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = 10
                    else:
                        Reward = 5
                elif cur_state >= OCC_TH_LOW and (OCC_TH_LOW <= pre_state < OCC_TH_HIGH):
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)

                        # tmp_lane_num = full_in_lanes_num[tmp_road_key]
                        # for i in range(tmp_lane_num):
                        #     tmp_lane_str = tmp_road_key + '_' + str(i)
                        #     prev_state_arr.append(previous_all_state[tmp_lane_str])
                        prev_state_arr.append(previous_state[tmp_road_key])

                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = 20
                    else:
                        Reward = 15
                elif cur_state < OCC_TH_LOW and pre_state >= OCC_TH_HIGH:
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)
                        prev_state_arr.append(previous_state[tmp_road_key])
                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = 30
                    else:
                        Reward = 25
                elif cur_state >= OCC_TH_LOW and pre_state >= OCC_TH_HIGH:
                    Reward = 40

                dep_rwd_penality = 5

                if roadID_to.find('#0#') >= 0:
                    if cur_state >= OCC_TH_HIGH and current_state[roadID_to] >= OCC_TH_HIGH:
                        Reward -= dep_rwd_penality
                        break
                else:
                    relation_res2 = road_relation_df[road_relation_df[0] == roadID_to]
                    flag = False
                    for index2, row2 in relation_res2.iterrows():
                        roadID_to2 = row2[2]
                        if roadID_to2.find('#0#') >= 0:
                            if cur_state >= OCC_TH_HIGH and current_state[roadID_to2] >= OCC_TH_HIGH:
                                Reward -= dep_rwd_penality
                                flag = True
                                break
                    if flag:
                        break
    Reward_total = Reward

    phasedet = phases_detail[str(intID) + '_' + str( (phase_num + 2) % total_phase_num )]
    # print('test phase detail:', phasedet)
    for i in range(len(phasedet)):
        if phasedet[i] == '1':
            ind = i + 1
            relation_res = road_relation_df[(road_relation_df[5]==ind) & (road_relation_df[4] == intID)]
            for index, row in relation_res.iterrows():
                roadID_from = row[0]
                lane_ID = row[1]
                roadID_to = row[2]
                assert intID == row[4]
                lane_str = str(roadID_from) + '_' + str(lane_ID)
                # print('test lane string:', lane_str)

                cur_state = current_all_state[lane_str]
                pre_state = previous_all_state[lane_str]
                # cur_state = current_state[roadID_from]
                # pre_state = previous_state[roadID_from]

                if cur_state < OCC_TH_LOW and pre_state < OCC_TH_LOW:
                    Reward = 40
                elif cur_state >= OCC_TH_LOW and pre_state < OCC_TH_LOW:
                    Reward = 20
                elif cur_state < OCC_TH_LOW and (OCC_TH_LOW <= pre_state < OCC_TH_HIGH):
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)

                        # tmp_lane_num = full_in_lanes_num[tmp_road_key]
                        # for i in range(tmp_lane_num):
                        #     tmp_lane_str = tmp_road_key + '_' + str(i)
                        #     prev_state_arr.append(previous_all_state[tmp_lane_str])
                        prev_state_arr.append(previous_state[tmp_road_key])

                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = -10
                    else:
                        Reward = -5
                elif cur_state >= OCC_TH_LOW and (OCC_TH_LOW <= pre_state < OCC_TH_HIGH):
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)

                        # tmp_lane_num = full_in_lanes_num[tmp_road_key]
                        # for i in range(tmp_lane_num):
                        #     tmp_lane_str = tmp_road_key + '_' + str(i)
                        #     prev_state_arr.append(previous_all_state[tmp_lane_str])
                        prev_state_arr.append(previous_state[tmp_road_key])

                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = -20
                    else:
                        Reward = -15
                elif cur_state < OCC_TH_LOW and pre_state >= OCC_TH_HIGH:
                    prev_state_arr = []
                    for i in range(NUM_INTN_ROADS[intID]):
                        tmp_road_key = intID + '#0#' + str(i + 1).zfill(3)
                        prev_state_arr.append(previous_state[tmp_road_key])
                    prev_state_max = max(prev_state_arr)
                    if prev_state_max == pre_state:
                        Reward = -30
                    else:
                        Reward = -25
                elif cur_state >= OCC_TH_LOW and pre_state >= OCC_TH_HIGH:
                    Reward = -40

                dep_rwd_penality = -5

                if roadID_to.find('#0#') >= 0:
                    if cur_state >= OCC_TH_HIGH and current_state[roadID_to] >= OCC_TH_HIGH:
                        Reward -= dep_rwd_penality
                        break
                else:
                    relation_res2 = road_relation_df[road_relation_df[0] == roadID_to]
                    flag = False
                    for index2, row2 in relation_res2.iterrows():
                        roadID_to2 = row2[2]
                        if roadID_to2.find('#0#') >= 0:
                            if cur_state >= OCC_TH_HIGH and current_state[roadID_to2] >= OCC_TH_HIGH:
                                Reward -= dep_rwd_penality
                                flag = True
                                break
                    if flag:
                        break

    Reward_total += Reward




    # road_key = intID + '#0#' + str(int(phase_num / 2) % NUM_INTN_ROADS[intID] + 1).zfill(3)
    #
    # if current_state[road_key] < OCC_TH_LOW and previous_state[road_key] < OCC_TH_LOW:
    #     Reward = -40
    # elif current_state[road_key] >= OCC_TH_LOW and previous_state[road_key] < OCC_TH_LOW:
    #     Reward = -20
    # elif current_state[road_key] < OCC_TH_LOW and (OCC_TH_LOW <= previous_state[road_key] < OCC_TH_HIGH):
    #     prev_state_arr = []
    #     for i in range(NUM_INTN_ROADS[intID]):
    #         tmp_road_key = intID + '#0#' + str(i+1).zfill(3)
    #         prev_state_arr.append(previous_state[tmp_road_key])
    #     prev_state_max = max(prev_state_arr)
    #     if prev_state_max == previous_state[road_key]:
    #         Reward = 10
    #     else:
    #         Reward = 5
    # elif current_state[road_key] >= OCC_TH_LOW and (OCC_TH_LOW <= previous_state[road_key] < OCC_TH_HIGH):
    #     prev_state_arr = []
    #     for i in range(NUM_INTN_ROADS[intID]):
    #         tmp_road_key = intID + '#0#' + str(i+1).zfill(3)
    #         prev_state_arr.append(previous_state[tmp_road_key])
    #     prev_state_max = max(prev_state_arr)
    #     if prev_state_max == previous_state[road_key]:
    #         Reward = 20
    #     else:
    #         Reward = 15
    # elif current_state[road_key] < OCC_TH_LOW and previous_state[road_key] >= OCC_TH_HIGH:
    #     prev_state_arr = []
    #     for i in range(NUM_INTN_ROADS[intID]):
    #         tmp_road_key = intID + '#0#' + str(i+1).zfill(3)
    #         prev_state_arr.append(previous_state[tmp_road_key])
    #     prev_state_max = max(prev_state_arr)
    #     if prev_state_max == previous_state[road_key]:
    #         Reward = 30
    #     else:
    #         Reward = 25
    # elif current_state[road_key] >= OCC_TH_LOW and previous_state[road_key] >= OCC_TH_HIGH:
    #     Reward = 40
    #
    # # road relation
    # dep_rwd_penality = 5
    #
    # relation_res = road_relation_df[road_relation_df[4] == intID]
    # phase_detail = phases_detail[intID+'_'+str(phase_num)]
    # for index, row in relation_res.iterrows():
    #     roadID_from = row[0]
    #     roadID_to = row[2]
    #     control_order = row[5]
    #     if phase_detail[control_order-1] == '1':
    #         if roadID_to.find('#0#') >= 0:
    #             if current_state[roadID_from] >= OCC_TH_HIGH and current_state[roadID_to] >= OCC_TH_HIGH:
    #                 Reward -= dep_rwd_penality
    #                 break
    #         else:
    #             relation_res2 = road_relation_df[road_relation_df[0] == roadID_to]
    #             flag = False
    #             for index2, row2 in relation_res2.iterrows():
    #                 roadID_to2 = row2[2]
    #                 if roadID_to2.find('#0#') >= 0:
    #                     if current_state[roadID_from] >= OCC_TH_HIGH and current_state[roadID_to2] >= OCC_TH_HIGH:
    #                         Reward -= dep_rwd_penality
    #                         flag = True
    #                         break
    #             if flag:
    #                 break

    return Reward_total

# Desc: Set the control action for a intersection
# Inputs - intID: intersection ID
#          action: a number of action
# Outputs - flag: True or False, whether the action is correctly setted
def set_action(intID, action):
    global intn_control_action, intn_cur_action, t_count_down

    act = 2 * action

    if action == -1:
        get_current_phase_num(intID)
        return True
    elif t_count_down[intID] == 10:
        if intn_control_action[intID] == intn_cur_action[intID]:
            if intn_control_action[intID] != act:
                intn_control_action[intID] = act
                return True
            elif intn_control_action[intID] == act:
                return True
    return False

# Desc: One Step Time pass after setted actions
# Inputs - None
# Outputs - A dictionary containing 2 elements
#               'rwd': Reward; Returns -100 if the current simulation is over
#               'next_state': 15-element array containing the no. of vehicles waiting at the intersections in new state
def time_pass_after_setting(intIDs, step_num = 1):
    assert type(intIDs) == list

    global curr_state, curr_all_state, prev_state, prev_all_state, intn_control_action, intn_cur_action, first_act_of_run, counting_time, t, t_count_down

    avg_reward = 0.0
    for ts in range(step_num):
        flag = {}
        for intID in intIDs:
            flag[intID] = False
            if intn_control_action[intID] == -1:
                t_count_down[intID] = 10
                get_current_phase_num(intID)
            elif t[intID] == 3:
                get_current_phase_num(intID)
                act = intn_control_action[intID]
                traci.trafficlight.setPhase(intID, act)  # Give Green during transition
                traci.trafficlight.setPhaseDuration(intID, MAX_GREEN_TIME[intID + '_' + str(act)] * 1000)
                intn_cur_action[intID] = act
                t_count_down[intID] = 10
            elif t_count_down[intID] < 10:
                t_count_down[intID] -= 1
                if t_count_down[intID] <= 0:
                    act = intn_control_action[intID]
                    if act == 0:
                        act = intersections_phase[intID]
                    traci.trafficlight.setPhase(intID, act - 1)  # Give Green during transition
                    traci.trafficlight.setPhaseDuration(intID, T_Y_TRANS * 1000)
                    intn_cur_action[intID] = act - 1
                    t[intID] = 0
                    t_count_down[intID] = 10
                    flag[intID] = True
            elif intn_control_action[intID] != intn_cur_action[intID]:
                if t[intID] <= MIN_GREEN_TIME[intID + '_' + str(intn_cur_action[intID])] + T_Y_TRANS:
                    t_count_down[intID] = 10
                else:
                    t_count_down[intID] = 9
            elif t[intID] == MAX_GREEN_TIME[intID + '_' + str(intn_cur_action[intID])] + T_Y_TRANS - 9:
                intn_control_action[intID] = (intn_cur_action[intID] + 2) % intersections_phase[intID]
                t_count_down[intID] = 9
            t[intID] += 1

        traci.simulationStep()
        counting_time += 1

        current_state, current_all_state = get_current_state()

        qlenfile.write(
            '\t' + "<qlength vals=\"" + str(list(curr_state[intIDs[0]].values())) + "\" t=\"" + str(counting_time) + "\"/>" + '\n')
        qlenfile.flush()

        # all vehicles left simulation; current run over
        if traci.simulation.getMinExpectedNumber() == 0:
            traci.close()
            qlenfile.write("</qlengths>")
            qlenfile.close()
            plot_metrics.record_metrics_of_run(10 + T_Y_TRANS)
            return {'rwd': -100, 'state': curr_state}

        R = 0.0
        cnt = 0
        for intID in intIDs:
            curr_state[intID] = current_state
            curr_all_state[intID] = current_all_state
            if flag[intID]:
                cnt += 1
                R += calculate_reward(curr_state[intID], prev_state[intID], intID, intn_control_action[intID], curr_all_state[intID], prev_all_state[intID])
                prev_state[intID] = curr_state[intID]
                prev_all_state[intID] = curr_all_state[intID]
        if cnt > 0:
            avg_reward += R / cnt

    avg_reward = avg_reward / step_num

    return {'rwd': avg_reward, 'state': current_state}