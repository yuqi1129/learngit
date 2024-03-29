# -*- coding: utf-8 -*-
#  @Time    : 2019/7/25 9:49
#  @Author  : Anonymous
#  @File    : handle_config.py
from configparser import ConfigParser


class HandleConfig:
    def __init__(self, file_name):
        '''
        初始化方法,用作创建HandleConfig类的实例时创建配置文件路径实例变量,并创建配置解析器对象去指定读取的配置文件路径
        :param file_name:
        '''
        # 创建HandleConfig类的实例时需要传入配置文件的文件路径然后赋值给实例变量self.file_name
        self.file_name = file_name
        # 创建配置解析器对象
        self.config = ConfigParser()
        # 去指定读取的配置文件路径
        self.config.read(self.file_name, encoding='utf-8')

    def get_value(self, section, option):
        '''
        根据区域名和选项名返回str类型配置数据值
        :param section:区域名
        :param option: 选项名
        :return:
        '''
        return self.config.get(section, option)

    def get_int(self, section, option):
        '''
        根据区域名和选项名返回int类型配置数据值
        :param section:区域名
        :param option: 选项名
        :return:
        '''
        return self.config.getint(section, option)

    def get_float(self, section, option):
        '''
        根据区域名和选项名返回float类型配置数据值
        :param section:区域名
        :param option:选项名
        :return:
        '''
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):
        '''
        根据区域名和选项名返回bool类型配置数据值
        :param section: 区域名
        :param option: 选项名
        :return:
        '''
        return self.config.getboolean(section, option)

    def get_eval_data(self, section, option):
        '''
        根据区域名和选项名返回序列(list,tuple,dict)类型配置数据值
        :param section:区域名
        :param option:选项名
        :return:
        '''
        return eval(self.get_value(section, option))

    @staticmethod
    def write_config(datas, filename):
        '''
        将嵌套字典的字典的配置文件数据写入到配置文件中，调用该方法时需要传入datas
        datas示例：
        datas = {
                'handle_excel':{
                'file_path':'H:\test_case_data\data.xlsx',
                'sheet_name_sub':'sub',
                'sheet_name_div':'divide'
                },
                {
                'test_result':{
                'success_result':'PASS',
                'fail_result':'FAIL'
                }
                }
        }
        :param datas:嵌套字典的字典
        :param filename:需要写入的配置文件路径
        :return:
        '''
        if isinstance(datas, dict):
            for value in datas.values():
                if not isinstance(value, dict):
                    return '数据不合法,应为嵌套字典的字典'
            config = ConfigParser()
            for key in datas:
                config[key] = datas[key]
            with open(filename, mode='w', encoding='utf-8') as file:
                config.write(file)
