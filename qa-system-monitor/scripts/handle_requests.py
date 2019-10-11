# -*- coding: utf-8 -*-
#  @Time    : 2019/8/1 17:43
#  @Author  : Anonymous
#  @File    : base_requests.py
import json
import requests


class DoRequests:
    '''封装requests的类'''

    def __init__(self):
        # 创建会话管理器,相当于Jemeter中的cookies管理器
        self.req_session = requests.Session()
        self.response = None

    def handle_requests(self, url, method='POST', data=None, is_json=False):
        '''
        :param url: 接口地址
        :param data: 请求数据(params查询字符串格式 或 form表单格式 或 json格式)
        :param method:请求方法
        :param headers:请求头
        :param is_json:判断请求格式是否为json格式
        :return:response响应体
        '''
        # data_dict = "{'name': '哈哈', 'age': '18'}" 字典类型字符串
        # data_json = '{"name": "哈哈", "age": "18"}' json格式字符串
        # if isinstance(data, str):
        #     try:
        #         # 必须是可编码为json格式的字符串才可以，否则会抛出异常
        #         data = json.loads(data)
        #     except Exception as err:
        #         # print(f'str转json报错了,警告信息为:{err}')
        #         # self.handle_log.warning('str转json格式报错了,警告信息为:{}'.format(err))
        #         # 不是可编码为json格式的字符串,通过eval()函数去掉前后""变为dict类型的数据
        #         data = eval(data)
        method = method.upper()
        if method == 'GET':
            # # 如果请求方式是get请求，发起get请求
            self.response = self.req_session.get(url=url, params=data)
        elif method == 'POST':
            if is_json:
                # 如果请求格式是json格式，发起post请求
                self.response = self.req_session.post(url=url, json=data)
            else:
                # 如果请求格式是form表单，发起post请求
                self.response = self.req_session.post(url=url, data=data)
        else:
            print('暂不支持{}请求方法'.format(method))
        # 返回响应体
        return self.response

    def session_close(self):
        '''
        关闭会话管理器方法
        :return:
        '''
        self.req_session.close()
