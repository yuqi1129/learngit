# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/9/29 15:40

import os
import re
from scripts.handle_path_constants import QUERY_DATAS


class DoParameterize:
    # 定义re匹配模式
    parametric_mode = r"\${query}"

    def read_query_single(self):
        '''
        读取随机选中的查询关键字query
        :return:
        '''
        with open(os.path.join(QUERY_DATAS, 'query_single.txt'), mode='r',
                  encoding='utf-8') as file:
            query_single = file.read()
        return query_single

    def query_parametric(self, data):
        '''
        对查询关键字query进行参数化的方法
        :param data: 需要进行参数化的原始数据data
        :return:
        '''
        if re.search(self.parametric_mode, data):
            data = re.sub(self.parametric_mode, self.read_query_single(), data)
            return data


if __name__ == '__main__':
    # data = """{"q": "${query}", "f": 0, "sd": "xhdpi", "hl": "zh_CN", "p": 0, "nt": "wifi", "lo": 21.8, "la": 51.8, "se": None,"sp": "china mobile", "imei": None, "dm": "MIX 2S", "di": None, "sv": "MIUI 10.3.5", "vr": "4.4.4","vs": "19", "sid": 5, "s": 1, "n": 50, "_sl": True, "addr": "北京市海淀区清河朱房路", "cv": 0, "cc": None, "ti": None,"from": None, "h_t": None, "cd": True}"""
    # test = DoParameterize()
    # print(test.query_parametric(data=data))
    # print(type(eval(test.query_parametric(data=data))), eval(test.query_parametric(data=data)))
    # print(data)
    pass
