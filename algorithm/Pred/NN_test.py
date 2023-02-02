# -*- coding: utf-8 -*-
# @Time : 2022/9/21 15:39
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: sumo_env.py
# @File : NN_test.py
# @Software: PyCharm
import os
import time

import torch
from torch import optim

from algorithm.Pred.GCN import GCN
from algorithm.Pred.Pred_NET import *


def main():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    N = 100
    Y = 82
    IN_C = 1

    train_adj= torch.rand(size=[N, N])
    train_fea = torch.rand(size=[N, 1])
    train_target = torch.rand(size=[Y])



    # Loading Model

    model = GCN(in_c=IN_C , hid_c=N ,out_c=Y)
    # model = ChebNet(in_c=6, hid_c=32, out_c=1, K=2)      # 2阶切比雪夫模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(params=model.parameters())

    # Train model
    Epoch = 8

    model.train()
    for epoch in range(Epoch):
        epoch_loss = 0.0
        start_time = time.time()
        # ["graph": [B, N, N] , "flow_x": [B, N, H, D], "flow_y": [B, N, 1, D]]
        data = train_adj, train_fea
        model.zero_grad()
        predict_value = model(data, device).to(torch.device("cpu"))  # [0, 1] -> recover
        loss = criterion(predict_value, train_target)
        epoch_loss += loss.item()
        loss.backward()
        optimizer.step()
        end_time = time.time()

        print("Epoch: {:04d}, Loss: {:02.4f}, Time: {:02.2f} mins".format(epoch, 1000 * epoch_loss,
                                                                          (end_time-start_time)/60))


if __name__ == '__main__':
    main()
