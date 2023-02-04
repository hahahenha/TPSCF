# -*- coding: utf-8 -*-
# @Time : 2022/9/21 15:29
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: sumo_env.py
# @File : Pred_NET.py
# @Software: PyCharm

import torch
import torch.nn as nn

class Pred_NET(nn.Module):
    def __init__(self, N, in_c, hid_c, out_c, K=-1):
        super(Pred_NET, self).__init__()
        self.linear_k = nn.Linear(in_c, in_c)
        self.linear_q = nn.Linear(in_c, in_c)
        self.linear_v = nn.Linear(in_c, in_c)
        self.linear_2 = nn.Linear(in_c, hid_c)
        self.act = nn.ReLU()
        if K <= 0 or K > N:
            self.K = N
        else:
            self.K = K
        self.linear_3 = nn.Linear(self.K * hid_c, out_c)

    def forward(self, data, device):
        adj, fea = data
        graph_data = adj.to(device)  # [N, N]
        graph_data = Pred_NET.process_graph(graph_data)
        x = fea.to(device)  # [N, H]

        x = torch.matmul(graph_data, x)  # [N, N], [N, Hid_C]

        K = self.linear_k(x)
        Q = self.linear_q(x)
        V = self.linear_v(x)

        hid1 = torch.matmul(K.transpose(0, 1), V)
        res1 = torch.matmul(Q, hid1)

        q2 = torch.mul(Q, Q)
        k2 = torch.mul(K, K)
        hid2 = torch.matmul(k2.transpose(0, 1), V)
        res2 = torch.matmul(q2, hid2)

        output_1 = res1 - res2

        # output_2 = self.linear_2(output_1)


        # K_T = torch.transpose(K,0,1)
        # ones_q = torch.ones(Q.shape[0], Q.shape[1]).to(device)
        # ones_k_T = torch.ones(K.shape[1], K.shape[0]).to(device)
        #
        # q_plus_one = torch.add(Q, ones_q)
        # k_plus_one = torch.add(K_T, ones_k_T)
        # mul_1 = torch.mm(k_plus_one, V)
        # mul_2 = torch.mm(ones_k_T, V)
        # mul_3 = torch.mm(K_T, V)
        # output_1 = torch.mm(q_plus_one, mul_1) - torch.mm(Q, mul_2) - torch.mm(ones_q, mul_3)
        # # output_2 = self.linear_2(output_1)

        topk, _ = output_1.topk(self.K, dim=0, largest=True, sorted=True)
        output_2 = self.linear_2(topk)
        output_2 = self.act(output_2)  # [k, Out_C]

        output_3 = output_2.view(-1)
        output_3 = self.linear_3(output_3)

        return output_3

    @staticmethod
    def process_graph(graph_data):
        N = graph_data.size(0)
        matrix_i = torch.eye(N, dtype=graph_data.dtype, device=graph_data.device)
        graph_data += matrix_i  # A~ [N, N]

        degree_matrix = torch.sum(graph_data, dim=-1, keepdim=False)  # [N]
        degree_matrix = degree_matrix.pow(-1)
        degree_matrix[degree_matrix == float("inf")] = 0.  # [N]

        degree_matrix = torch.diag(degree_matrix)  # [N, N]

        return torch.mm(degree_matrix, graph_data)  # D^(-1) * A = \hat(A)