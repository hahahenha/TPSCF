# -*- coding: utf-8 -*-
# @Time : 2022/9/23 13:48
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: test.py
# @File : GCN.py
# @Software: PyCharm

import torch
import torch.nn as nn

class GCN(nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        super(GCN, self).__init__()
        self.linear_1 = nn.Linear(in_c, hid_c)
        self.linear_2 = nn.Linear(hid_c, out_c)
        self.linear_3 = nn.Linear(hid_c*out_c, out_c)
        self.act = nn.ReLU()

    def forward(self, data, device):
        adj, fea = data
        graph_data = adj.to(device)  # [N, N]
        graph_data = GCN.process_graph(graph_data)
        x = fea.to(device)  # [N, H]

        output_1 = self.linear_1(x)  # [N, hid_C]
        output_1 = self.act(torch.matmul(graph_data, output_1))  # [N, N], [N, Hid_C]

        output_2 = self.linear_2(output_1)
        output_2 = self.act(torch.matmul(graph_data, output_2))  # [N, Out_C]

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