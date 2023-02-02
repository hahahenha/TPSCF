# -*- coding: utf-8 -*-
# @Time : 2022/9/21 15:25
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: sumo_env.py
# @File : simple_layer.py
# @Software: PyCharm
import random

import torch
import torch.nn as nn

class Network(nn.Module):
    def __init__(self, len_state, num_quant, num_actions):
        nn.Module.__init__(self)

        self.num_quant = num_quant
        self.num_actions = num_actions

        self.layer1 = nn.Linear(len_state, 256)
        self.layer2 = nn.Linear(256, num_actions * num_quant)

    def forward(self, x):
        x = self.layer1(x)
        x = torch.relu(x)
        x = self.layer2(x)
        return x.view(-1, self.num_actions, self.num_quant)

    def select_action(self, state, a_space, epsilon):
        if not isinstance(state, torch.Tensor):
            state = torch.Tensor([state])
        action = torch.randint(a_space[0], a_space[-1] + 1, (1,))
        if random.random() > epsilon:
            action = (self.forward(state).mean(2)[0, [a_space]]).max(1)[1] + a_space[0]
        return int(action)