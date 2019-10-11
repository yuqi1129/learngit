# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/10/9 10:02

import os
# import sys
# sys.path.append('/home/work/wenbin/qa-system-monitor/qa-system-monitor')
from random import choice
from scripts.handle_path_constants import QUERY_DATAS


class ExtractKeywords:

    def read_search_keywords(self):
        '''
        读取sug.txt文档中所有的搜索关键字query,用列表保存起来data_list
        :return:关键字query列表
        '''
        with open(os.path.join(QUERY_DATAS, 'sug.txt'), mode='r', encoding='GBK') as file:
            data_list = []
            # 一次性读取sug.txt文件中的所有数据,list类型
            data = file.readlines()
            for i in data:
                data_list.append(i.strip('\n'))
            return data_list

    def random_query_value(self):
        '''
        从read_search_keywords()方法的返回值data_list中随机抽取一个元素作为关键字写入到一个新文件中
        :return: 随机抽取到的关键字query
        '''
        query_list = self.read_search_keywords()
        # 随机选择data_list中的一个元素
        query_single = choice(query_list)
        return query_single

    def write_query_single(self):
        '''
        将随机抽取到的某一个查询关键字写入到文件中
        :return:
        '''
        with open(os.path.join(QUERY_DATAS, 'query_single.txt'), mode='w', encoding='utf-8') as file:
            file.write(self.random_query_value())

    # def create_timed_task(self):
        '''
        创建定时器任务，在相应的时间间隔里边去执行对应的方法
        :return:
        '''
        # self.write_query_single()
        # 创建定时器，指定需要定时执行的时间间隔和需要执行的方法名
        # timer = Timer(10, self.create_timed_task)
        # 使用线程方式开始执行
        # timer.start()
        # cancel() ：停止timer，并取消timer动作的执行。这只在timer仍然处于等待阶段时才工作。
        # timer.cancel()
        # return data_dict


if __name__ == '__main__':
    test = ExtractKeywords()
    test.write_query_single()
