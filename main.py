# Main module

# Depends on: static_signalling.py, plot_metrics.py

from algorithm.distributed_PPO import Distr_PPO
from sumo_related import sumo_env
from utils import plot_metrics

# Train the QR-DQN model
sumo_env.endis_sumo_guimode(1)
Nruns = 25
Distr_PPO(Nruns)
print("finish 1")


