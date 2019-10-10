# -*- coding: utf-8 -*-
#  @Time    : 2019/7/25 9:03
#  @Author  : Anonymous
#  @File    : handle_log.py
# python内置的日志模块
import logging
import os
from scripts.handle_config import HandleConfig
from scripts.handle_path_constants import LOGS_DIR


# 封装处理日志的类
class HandleLog:

    def __init__(self, file_path):
        '''
        初始化函数，封装日志相关操作
        '''
        # 创建该类实例对象时传入日志相关的配置文件路径
        self.handle_config = HandleConfig(file_path)
        # 1.定义日志收集器
        self.cases_logger = logging.getLogger(self.handle_config.get_value('handle_log', 'log_name'))  # 会创建一个logger对象
        # 每次调用后清空已存在的handler
        self.cases_logger.handlers.clear()
        # 2.指定日志收集器日志等级，一共有6种等级
        # NOTSET(0)、DEBUG(10)、INFO(20)、WARNING(30)、ERROR(40)、CRITICAL(50)
        # 只能收集当前等级和当前等级以上的日志
        self.cases_logger.setLevel(self.handle_config.get_value('handle_log', 'cases_logger_level'))
        # cases_logger.setLevel('DEBUG')

        # 3.指定日志输出渠道
        # 输出到控制台
        console_handle = logging.StreamHandler()  # handler对象
        # 输出到文件
        file_handle = logging.FileHandler(
            os.path.join(LOGS_DIR, self.handle_config.get_value('handle_log', 'file_path_log')), encoding='utf-8')

        # 4.指定日志输出渠道的日志等级
        console_handle.setLevel(self.handle_config.get_value('handle_log', 'console_handle_level'))
        file_handle.setLevel(self.handle_config.get_value('handle_log', 'file_handle_level'))
        # 5.定义日志显示格式
        simple_formatter = logging.Formatter(self.handle_config.get_value('handle_log', 'simple_format'))
        detail_formatter = logging.Formatter(self.handle_config.get_value('handle_log', 'detail_format'))
        # 控制台显示简洁的日志
        console_handle.setFormatter(simple_formatter)
        # 日志文件显示详细日志
        file_handle.setFormatter(detail_formatter)
        # 6.经日志收集器与输出渠道进行对接
        self.cases_logger.addHandler(console_handle)
        self.cases_logger.addHandler(file_handle)

    def get_logger(self):
        '''
        :return:返回日志收集器对象
        '''
        return self.cases_logger


