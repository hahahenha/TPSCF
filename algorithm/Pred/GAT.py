# -*- coding: utf-8 -*-
# @Time : 2022/9/21 15:30
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: sumo_env.py
# @File : GAT.py
# @Software: PyCharm

import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphAttentionLayer(nn.Module):
    def __init__(self, in_c, out_c):
        super(GraphAttentionLayer, self).__init__()
        self.in_c = in_c
        self.out_c = out_c

        self.F = F.softmax

        self.W = nn.Linear(in_c, out_c, bias=False)  # y = W * x
        self.b = nn.Parameter(torch.Tensor(out_c))

        nn.init.normal_(self.W.weight)
        nn.init.normal_(self.b)

    def forward(self, inputs, graph):
        """
        :param inputs: input features, [B, N, C].
        :param graph: graph structure, [N, N].
        :return:
            output features, [B, N, D].
        """

        h = self.W(inputs)  # [B, N, D]
        outputs = torch.bmm(h, h.transpose(1, 2)) * graph.unsqueeze(0)  # [B, N, N]      x(i)^T * x(j)
        outputs.data.masked_fill_(torch.eq(outputs, 0), -float(1e16))   # x(i)|| x(j)

        attention = self.F(outputs, dim=2)   # [B, N, N]
        return torch.bmm(attention, h) + self.b  # [B, N, N] * [B, N, D]


class GATSubNet(nn.Module):
    def __init__(self, in_c, hid_c, out_c, n_heads):
        super(GATSubNet, self).__init__()

        self.attention_module = nn.ModuleList([GraphAttentionLayer(in_c, hid_c) for _ in range(n_heads)])
        self.out_att = GraphAttentionLayer(hid_c * n_heads, out_c)

        self.act = nn.LeakyReLU()

    def forward(self, inputs, graph):
        """
        :param inputs: [B, N, C]
        :param graph: [N, N]
        :return:
        """
        outputs = torch.cat([attn(inputs, graph) for attn in self.attention_module], dim=-1)  # [B, N, hid_c * h_head]
        outputs = self.act(outputs)

        outputs = self.out_att(outputs, graph)

        return self.act(outputs)



# GAT 网络的定义
class GATNet(nn.Module):
    def __init__(self, in_c, hid_c, out_c, n_heads):
        super(GATNet, self).__init__()
        self.subnet = GATSubNet(in_c, hid_c, out_c, n_heads)

    def forward(self, data, device):
        adj, fea = data
        graph = adj.to(device)  # [N, N]
        flow = fea.to(device)  # [B, N, T, C]

        B, N = flow.size(0), flow.size(1)
        flow = flow.view(B, N, -1)  # [B, N, T * C]

        prediction = self.subnet(flow, graph).unsqueeze(2)  # [B, N, 1, C]

        return prediction
