# -*- coding: utf-8 -*-
# @Time : 2022/11/9 22:55
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: main.py
# @File : distributed_PPO.py
# @Software: PyCharm

# A full version is not made public, due to several restrictions

import copy
import time
from collections import namedtuple

import torch.optim as optim

from algorithm.Pred.Pred_NET import Pred_NET
from algorithm.RL.PPO import PPO
from sumo_related import sumo_env, sumo_util
from utils.logger import Logger

from matplotlib import rcParams

from utils.graph_construction import *
from utils.rl_utils import OnlineSampling
from utils.sql_query import *
from utils.train_utils import *

rcParams['figure.figsize'] = 8, 3
rcParams['figure.dpi'] = 300

# Environment and algorithm parameters
GAMMA = 0.6
EPS_START, EPS_END, EPS_DECAY = 0.9, 0.1, 1000
BATCH_SIZE = 32
REPLAY_MEM_SIZE = 500
PMODELPARA = './logs/param/Pmodel.pth'

# Training
# Inputs - Nruns: No. of runs of training
# Outputs - None
def Distr_PPO(Nruns):
    agents = {}
    logger = {}
    running_reward = {}
    reward_list = []
    intIDs = []
    a_spaces = {}
    steps_done = {}

    args = parser.parse_args()
    phase_details = get_full_phases_detail(args)
    lanes_num = get_full_lanes_num(args)
    relation_df = get_full_road_relation(args)
    intersections_phase = get_signal_intersections_phase(args)
    STATE_LEN = args.state_len

    Transition = namedtuple('Transition', ['state', 'action', 'a_log_prob', 'reward', 'next_state'])

    NUM_INTERSECTIONS = 0
    for key, value in intersections_phase.items():
        intIDs.append(key)
        NUM_INTERSECTIONS += 1
        a_spaces[key] = []
        for i in range(int(value/2)):
            a_spaces[key].append(i)
        # network
        agents[key] = PPO(STATE_LEN, int(value/2), key)

    print('Construct graph...')
    G = full_graph_contruction(args)

    print('Build prediction neural network...')
    Log_printing_freq = args.log_freq
    IN_C = 1
    model = Pred_NET(N=514, in_c=IN_C, hid_c=args.hid_dim, out_c=STATE_LEN, K=args.topk)
    device = torch.device("cuda:{}".format(args.cuda) if (args.cuda >= 0 and torch.cuda.is_available()) else "cpu")
    model_p = model.to(device)
    criterion_p = nn.MSELoss()
    optimizer_p = optim.Adam(params=model.parameters())

    # set logger
    logger = Logger('rl-net', fmt={'loss': '.5f'})

    steps_done = 0
    running_reward = 100

    for run in range(Nruns):
        t = 0
        sum_reward = 0.0
        sumo_env.start_new_run(run)

        m_sampling = OnlineSampling(10)
        state = list(
            sumo_util.initial_state_generate_with_memory(intIDs, G.copy(), m_sampling, phase_details,
                                                         lanes_num, relation_df).values())

        # state = list(sumo_util.initial_state_generate(intIDs).values())

        action = {}
        action_prob = {}

        # P model related
        loss_p_total = 0.0
        sub_time_p = 0.0
        p_loss_avg = 0.0

        while True:
            for intID in intIDs:
                a_space = a_spaces[intID]

                action[intID], action_prob[intID] = agents[intID].select_action(state, a_space)

                sumo_env.set_action(intID, action[intID])

            observ = sumo_env.time_pass_after_setting(intIDs)

            next_state = list(observ['state'].values())
            reward = observ['rwd']

            done = 1 if reward == -100 else 0
            steps_done += 1
            t += 1

            if not done:
                for intID in intIDs:
                    trans= Transition(state, action[intID], action_prob[intID], reward, next_state)
                    agents[intID].store_transition(trans)
                    # if len(agents[intID].buffer) >= agents[intID].batch_size: agents[intID].update(run)

            running_reward = running_reward * 0.9999 + t * 0.0001
            sum_reward += reward

            if done:
                print("episode: {}, the episode reward is {}".format(run, round(sum_reward, 3)))
                for intID in intIDs:
                    if len(agents[intID].buffer) >= agents[intID].batch_size: agents[intID].update(run)
                running_reward = sum_reward if not running_reward else 0.2 * sum_reward + 0.8 * running_reward
                logger.add(run + 1, steps=t, running_reward=running_reward)
                logger.iter_info()
                break

            ########## Prediction part ##########
            DG = G.copy()

            for intID in intIDs:
                curr_phase_num = sumo_env.get_current_phase_num(intID)
                # print('curr_light:', intIDs[0], '-', curr_phase_num)
                time_cd = sumo_env.getPhaseCountDown(intID)
                # print('curr_count_down:', time_cd)
                ratio = 1.0
                ratio2 = 0.0
                if time_cd < 10:
                    ratio = time_cd / 10.0
                    ratio2 = (10 - time_cd) / 10.0
                next_phase_num = sumo_env.get_next_phase_num(intID, intersections_phase[intID])

                DG = disconnect_edges(DG, intID, curr_phase_num, ratio, False, phase_details, relation_df,
                                      lanes_num)
                DG = disconnect_edges(DG, intID, next_phase_num, ratio2, True, phase_details, relation_df,
                                      lanes_num)

            state_p = sumo_env.get_all_lane_state()
            adj, fea = input_data_sampling(DG, state_p)

            m_sampling.push(adj, fea, next_state)

            Adj, Fea, Target = m_sampling.sample()

            start_time = time.time()
            data = Adj, Fea
            model_p.train()
            model_p.zero_grad()
            predict_value = model_p(data, device).to(torch.device("cpu"))  # [0, 1] -> recover
            # print(predict_value)
            # print(Target)
            loss_p = torch.sqrt(criterion_p(predict_value, Target)) + l1_regularization(model,0.01) + l2_regularization(model, 0.01)
            loss_p_total += loss_p.item()
            loss_p.backward()
            optimizer_p.step()
            end_time = time.time()
            sub_time_p += end_time - start_time

            if t % Log_printing_freq == 0:
                loss_avg_tmp = loss_p_total / Log_printing_freq
                print("P_model Counting_num: {}, Loss: {:02.4f}, Time: {:02.4f} secs".format(
                    int(t / Log_printing_freq), loss_avg_tmp,
                    sub_time_p / Log_printing_freq))
                p_loss_avg = (p_loss_avg + loss_avg_tmp) / 2
            ########## Prediction end ##########

            if loss_p.item() >= 2 * p_loss_avg:
                state = next_state
            else:
                model_p.eval()
                state = model_p(m_sampling.real_time_sample(), device).to(torch.device("cpu")).tolist()

        r = copy.copy(reward)
        reward_list.append(r)
    return

