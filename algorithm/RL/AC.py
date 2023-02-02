import gym, os
import numpy as np
import matplotlib.pyplot as plt
from itertools import count
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

class Policy(nn.Module):
    def __init__(self, state_space, action_space, gamma = 0.99, lr = 0.01):
        super(Policy, self).__init__()
        self.fc1 = nn.Linear(state_space, 32)

        self.action_head = nn.Linear(32, action_space)
        self.value_head = nn.Linear(32, 1) # Scalar Value

        self.save_actions = []
        self.rewards = []

        self.GAMMA = gamma
        self.eps = np.finfo(np.float32).eps.item()

        self.SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])

        self.optimizer = optim.Adam(self.parameters(), lr=lr)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        action_score = self.action_head(x)
        state_value = self.value_head(x)

        return F.softmax(action_score, dim=-1), state_value

    def select_action(self, state, a_space):
        state = torch.unsqueeze(torch.FloatTensor(state), 0)
        probs, state_value = self.forward(state)
        m = Categorical(probs)
        action = m.sample()
        self.save_actions.append(self.SavedAction(m.log_prob(action), state_value))

        act = action.item()
        if action > len(a_space):
            act = act % len(a_space) + a_space[0]
        else:
            act += a_space[0]

        return act

    def finish_episode(self):
        R = 0
        save_actions = self.save_actions
        policy_loss = []
        value_loss = []
        rewards = []

        for r in self.rewards[::-1]:
            R = r + self.GAMMA * R
            rewards.insert(0, R)

        rewards = torch.tensor(rewards)
        rewards = (rewards - rewards.mean()) / (rewards.std() + self.eps)

        for (log_prob, value), r in zip(save_actions, rewards):
            reward = r - value.item()
            policy_loss.append(-log_prob * reward)
            value_loss.append(F.smooth_l1_loss(value, torch.tensor([r])))

        self.optimizer.zero_grad()
        loss = torch.stack(policy_loss).sum() + torch.stack(value_loss).sum()
        loss.backward()
        self.optimizer.step()

        del self.rewards[:]
        del self.save_actions[:]


def plot(steps):
    ax = plt.subplot(111)
    ax.cla()
    ax.grid()
    ax.set_title('Training')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Run Time')
    ax.plot(steps)
    RunTime = len(steps)

    path = './AC_CartPole-v0/' + 'RunTime' + str(RunTime) + '.jpg'
    if len(steps) % 5000 == 0:
        plt.savefig(path)
    plt.pause(0.0000001)

def main():
    # Parameters
    env = gym.make('CartPole-v0')
    env = env.unwrapped

    env.seed(1)
    torch.manual_seed(1)

    state_space = env.observation_space.shape[0]
    action_space = env.action_space.n

    os.makedirs('./AC_CartPole-v0', exist_ok=True)

    # Hyperparameters
    episodes = 20000
    render = False

    model = Policy(state_space, action_space)

    running_reward = 10
    live_time = []
    for i_episode in count(episodes):
        state = env.reset()
        for t in count():
            action = model.select_action(state, [0, 1, 2, 3])
            state, reward, done, info = env.step(action)
            if render: env.render()
            model.rewards.append(reward)

            if done or t > 1000:
                break
        running_reward = running_reward * 0.99 + t * 0.01
        live_time.append(t)
        if t % 1000 == 0:
            plot(live_time)
        # if i_episode % 100 == 0:
        #     modelPath = './AC_CartPole-v0/ModelTraing'+str(i_episode)+'Times.pkl'
        #     torch.save(model, modelPath)
        model.finish_episode()

if __name__ == '__main__':
    main()
