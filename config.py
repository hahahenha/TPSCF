import argparse
import os

from utils.train_utils import add_flags_from_config

config_args = {
    'sql_config': {
        'host':('127.0.0.1', 'mySQL IP Address'),
        'port':(3306, 'mySQL connection port'),
        'usr':('root', 'mySQL user'),
        'passwd':('123456', 'mySQL password'),
        'db': ('regional_traffic_control', 'mySQL database name'),
        'phases_detail_name':('phases_detail', 'table phases_detail name'),
        'road_lanes_name':('road_lanes', 'table road_lanes name'),
        'road_relation_name':('road_relation', 'table road_relation name'),
        'signal_phases_name':('signal_phases', 'table signal_phases name'),
        'sumo_file_name':('txmap', 'sumo file name'),
        'state-len':(82, 'state length: [82, 255]')
    },
    'model_config': {
        'model': ('compare', 'which encoder to use, can be any of [gan, nongan, compare]'),
        'manifold': ('Euclidean', 'which manifold to use, can be any of [Euclidean, Hyperboloid, PoincareBall]'),
        'cuda':(0, 'which device to use, -1 for using CPU'),
        'topk':(100, 'artificially defined parameter'),
        'hid_dim':(128, 'hidden dimension'),
        'log_freq':(500, 'logging frequency')
    },
    'data_config': {
        'val-prop': (0.2, 'proportion of validation samples'),
        'test-prop': (0.2, 'proportion of test samples'),
    }
}

parser = argparse.ArgumentParser()
for _, config_dict in config_args.items():
    parser = add_flags_from_config(parser, config_dict)