# -*- coding: utf-8 -*-
#  @Time    : 2019/8/6 13:29
#  @Author  : Anonymous
#  @File    : path_constants.py
import os
''' 
路径常量:动态获取文件所在的项目路径的模块
'''
# 动态获取项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# print(os.path)

# 获取存放配置文件所在目录configs
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
# 创建config.ini配置文件的路径
# CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'config.ini')
# print(CONFIG_FILE_PATH, type(CONFIG_FILE_PATH))

# 获取存放log日志文件所在目录
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
# LOG_DIR = os.path.join(LOGS_DIR, 'test_cases.log')

# 获取存放查询关键字相关文件所在目录
QUERY_DATAS = os.path.join(BASE_DIR, 'query_datas')

