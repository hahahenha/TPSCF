import argparse
import pickle
from collections import namedtuple
from itertools import count

import os, time
import numpy as np
import matplotlib.pyplot as plt

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal, Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler
from tensorboardX import SummaryWriter

class Actor(nn.Module):
    def __init__(self, num_state, num_action):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(num_state, 100)
        self.action_head = nn.Linear(100, num_action)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        action_prob = F.softmax(self.action_head(x), dim=1)
        return action_prob


class Critic(nn.Module):
    def __init__(self, num_state):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(num_state, 100)
        self.state_value = nn.Linear(100, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        value = self.state_value(x)
        return value


class Model():
    def __init__(self, num_state, num_action, intID, batch_size = 32, buffer_capacity = 1000, ppo_update_time = 10, max_grad_norm = 0.5, clip = 0.2, gamma = 0.99):
        super(Model, self).__init__()
        self.intID = intID
        self.actor_net = Actor(num_state, num_action)
        self.critic_net = Critic(num_state)
        self.buffer = []
        self.counter = 0
        self.training_step = 0
        self.writer = SummaryWriter('./logs/' + self.intID +'/')

        self.actor_optimizer = optim.Adam(self.actor_net.parameters(), 1e-3)
        self.critic_net_optimizer = optim.Adam(self.critic_net.parameters(), 3e-3)
        self.GAMMA = gamma

        self.clip_param = clip
        self.max_grad_norm = max_grad_norm
        self.ppo_update_time = ppo_update_time
        self.buffer_capacity = buffer_capacity
        self.batch_size = batch_size
        if not os.path.exists('./logs/param'):
            os.makedirs('./logs/param/net_param')
            os.makedirs('./logs/param/img')

    def select_action(self, state, a_space):
        state = torch.unsqueeze(torch.FloatTensor(state), 0)  #torch.from_numpy(state).float().unsqueeze(0)
        with torch.no_grad():
            action_prob = self.actor_net(state)
        c = Categorical(action_prob)
        action = c.sample()

        act = action.item()
        if action > len(a_space):
            act = act % len(a_space) + a_space[0]
        else:
            act += a_space[0]

        return act, action_prob[:,action.item()].item()

    def get_value(self, state):
        state = torch.from_numpy(state)
        with torch.no_grad():
            value = self.critic_net(state)
        return value.item()

    def save_param(self):
        torch.save(self.actor_net.state_dict(), './logs/param/net_param/actor_net_'  + self.intID + '_' + str(time.time())[:10], +'.pkl')
        torch.save(self.critic_net.state_dict(), './logs/param/net_param/critic_net_' + self.intID + '_' + str(time.time())[:10], +'.pkl')

    def store_transition(self, transition):
        self.buffer.append(transition)
        self.counter += 1


    def update(self, i_ep):
        state = torch.tensor([t.state for t in self.buffer], dtype=torch.float)
        action = torch.tensor([t.action for t in self.buffer], dtype=torch.long).view(-1, 1)
        reward = [t.reward for t in self.buffer]
        # update: don't need next_state
        #reward = torch.tensor([t.reward for t in self.buffer], dtype=torch.float).view(-1, 1)
        #next_state = torch.tensor([t.next_state for t in self.buffer], dtype=torch.float)
        old_action_log_prob = torch.tensor([t.a_log_prob for t in self.buffer], dtype=torch.float).view(-1, 1)

        R = 0
        Gt = []
        for r in reward[::-1]:
            R = r + self.GAMMA * R
            Gt.insert(0, R)
        Gt = torch.tensor(Gt, dtype=torch.float)
        #print("The agent is updateing....")
        for i in range(self.ppo_update_time):
            for index in BatchSampler(SubsetRandomSampler(range(len(self.buffer))), self.batch_size, False):
                if self.training_step % 5000 ==0:
                    print('I_ep: {}, intersection ID: {}, train {} times'.format(i_ep,self.intID,self.training_step))
                #with torch.no_grad():
                Gt_index = Gt[index].view(-1, 1)
                V = self.critic_net(state[index])
                delta = Gt_index - V
                advantage = delta.detach()
                # epoch iteration, PPO core!!!
                action_prob = self.actor_net(state[index]).gather(1, action[index]) # new policy

                ratio = (action_prob/old_action_log_prob[index])
                surr1 = ratio * advantage
                surr2 = torch.clamp(ratio, 1 - self.clip_param, 1 + self.clip_param) * advantage

                # update actor network
                action_loss = -torch.min(surr1, surr2).mean()  # MAX->MIN desent
                self.writer.add_scalar('action_loss_' + self.intID, action_loss, global_step=self.training_step)
                self.actor_optimizer.zero_grad()
                action_loss.backward()
                nn.utils.clip_grad_norm_(self.actor_net.parameters(), self.max_grad_norm)
                self.actor_optimizer.step()

                #update critic network
                value_loss = F.mse_loss(Gt_index, V)
                self.writer.add_scalar('value_loss_' + self.intID, value_loss, global_step=self.training_step)
                self.critic_net_optimizer.zero_grad()
                value_loss.backward()
                nn.utils.clip_grad_norm_(self.critic_net.parameters(), self.max_grad_norm)
                self.critic_net_optimizer.step()
                self.training_step += 1

        del self.buffer[:] # clear experience

    
def main():
    # Parameters
    render = False
    seed = 1

    env = gym.make('CartPole-v0').unwrapped
    num_state = env.observation_space.shape[0]
    num_action = env.action_space.n
    torch.manual_seed(seed)
    env.seed(seed)
    Transition = namedtuple('Transition', ['state', 'action', 'a_log_prob', 'reward', 'next_state'])

    agent = PPO(num_state, num_action)
    for i_epoch in range(1000):
        state = env.reset()
        if render: env.render()

        for t in count():
            action, action_prob = agent.select_action(state, [0,1,2,3])
            next_state, reward, done, _ = env.step(action)
            trans = Transition(state, action, action_prob, reward, next_state)
            if render: env.render()
            agent.store_transition(trans)
            state = next_state

            if done :
                if len(agent.buffer) >= agent.batch_size:agent.update(i_epoch)
                agent.writer.add_scalar('liveTime/livestep', t, global_step=i_epoch)
                break

if __name__ == '__main__':
    main()
    print("end")
