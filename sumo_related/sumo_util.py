# -*- coding: utf-8 -*-
# @Time : 2022/9/14 9:47
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : sumo_util.py
# @Software: PyCharm

import numpy as np
from sumo_related import sumo_env
from utils.graph_construction import disconnect_edges, input_data_sampling
from utils.rl_utils import OnlineSampling

# Generate a random initial state for the simulation
def initial_state_generate(intIDs):
    for j in range(np.random.choice([12, 16, 20, 24, 28, 32])):
        env_dict = sumo_env.time_pass_after_setting(intIDs)
    return env_dict['state']

# Generate a random initial state for the simulation
def initial_state_generate_with_memory(intIDs, DG, memory, phase_details, lanes_num, relation_df):
    for j in range(np.random.choice([12, 16, 20, 24, 28, 32])):
        env_dict = sumo_env.time_pass_after_setting(intIDs)
        for intID in intIDs:
            DG = disconnect_edges(DG, intID, 0, 0.5, False, phase_details, relation_df, lanes_num)
        state = sumo_env.get_all_lane_state()
        adj, fea = input_data_sampling(DG, state)
        memory.push(adj, fea, list(env_dict['state'].values()))
    return env_dict['state']