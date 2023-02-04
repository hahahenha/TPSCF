# -*- coding: utf-8 -*-
# @Time : 2022/9/8 12:41
# @Author : Xiao Han
# @E-mail : hahahenha@gmail.com
# @Site : 
# @project: config.py
# @File : data_verify.py
# @Software: PyCharm

from config import parser

def list_ratio_check(dict):
    dict_checked = {}
    for key,value in dict.items():
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        dict_checked[key] = value
    return dict_checked

if __name__ == '__main__':
    args = parser.parse_args()