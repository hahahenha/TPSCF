import argparse
import gym
import numpy as np
from itertools import count

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

class Policy(nn.Module):
    def __init__(self, STATE_LEN, NUM_ACTIONS, GAMMA = 0.99):
        super(Policy, self).__init__()
        self.affine1 = nn.Linear(STATE_LEN, 128)
        self.affine2 = nn.Linear(128, NUM_ACTIONS)

        self.saved_log_probs = []
        self.rewards = []

        self.optimizer = optim.Adam(self.parameters(), lr=1e-2)
        self.eps = np.finfo(np.float32).eps.item()
        self.GAMMA = GAMMA

    def forward(self, x):
        x = F.relu(self.affine1(x))
        action_scores = self.affine2(x)
        return F.softmax(action_scores, dim=1)

    def select_action(self, state, a_space):
        state = torch.unsqueeze(torch.FloatTensor(state), 0)
        probs = self.forward(state)
        m = Categorical(probs)
        action = m.sample()
        self.saved_log_probs.append(m.log_prob(action))

        act = action.item()
        if action > len(a_space):
            act = act % len(a_space) + a_space[0]
        else:
            act += a_space[0]

        return act

    def finish_episode(self):
        R = 0
        policy_loss = []
        rewards = []
        for r in self.rewards[::-1]:
            R = r + self.GAMMA * R
            rewards.insert(0, R)
        rewards = torch.tensor(rewards)
        rewards = (rewards - rewards.mean()) / (rewards.std() + self.eps)
        for log_prob, reward in zip(self.saved_log_probs, rewards):
            policy_loss.append(-log_prob * reward)
        self.optimizer.zero_grad()
        policy_loss = torch.cat(policy_loss).sum()
        policy_loss.backward()
        self.optimizer.step()
        del self.rewards[:]
        del self.saved_log_probs[:]

def main():
    parser = argparse.ArgumentParser(description='PyTorch REINFORCE example')
    parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                        help='discount factor (default: 0.99)')
    parser.add_argument('--seed', type=int, default=543, metavar='N',
                        help='random seed (default: 543)')
    parser.add_argument('--render', action='store_true',
                        help='render the environment')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='interval between training status logs (default: 10)')
    args = parser.parse_args()

    env = gym.make('CartPole-v0')
    env.seed(args.seed)
    torch.manual_seed(args.seed)

    STATE_LEN = 4
    NUM_ACTIONS = 2
    policy = Policy(STATE_LEN, NUM_ACTIONS)

    running_reward = 10
    for i_episode in count(1):
        state = env.reset()
        for t in range(10000):  # Don't infinite loop while learning
            action = policy.select_action(state, [0])
            state, reward, done, _ = env.step(action)
            if args.render:
                env.render()
            policy.rewards.append(reward)
            if done:
                break

        running_reward = running_reward * 0.99 + t * 0.01
        policy.finish_episode()
        if i_episode % args.log_interval == 0:
            print('Episode {}\tLast length: {:5d}\tAverage length: {:.2f}'.format(
                i_episode, t, running_reward))
        if running_reward > env.spec.reward_threshold:
            print("Solved! Running reward is now {} and "
                  "the last episode runs to {} time steps!".format(running_reward, t))
            break


if __name__ == '__main__':
    main()
