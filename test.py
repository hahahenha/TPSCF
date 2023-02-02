# -*- coding: utf-8 -*-
# @Time : 2022/9/8 15:54
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : test.py
# @Software: PyCharm

from algorithm.alg_test import RL_test
from sumo_related import sumo_env
from utils import plot_metrics

# Static signalling
# sumo_env.endis_sumo_guimode(0) # 1 for visualization, 0 for not show
# Nruns = 25
# static_signalling_test.static_signalling(Nruns)
# plot_metrics.plot_all_metrics("Static Signalling")
# print("finish 1")

# RL Pred
# sumo_env.endis_sumo_guimode(1) # 1 for visualization, 0 for not show
# Nruns = 100
# rl_pred_algo.rl_pred_algo(Nruns)
# plot_metrics.plot_all_metrics("RL_Pred_Algo")
# print("finish 1")

# RL test
sumo_env.endis_sumo_guimode(1) # 1 for visualization, 0 for not show
Nruns = 20
RL_test.RL(Nruns)
plot_metrics.plot_all_metrics("RL_test")
print("finish 1")