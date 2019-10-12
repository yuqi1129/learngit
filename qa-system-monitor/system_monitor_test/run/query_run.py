# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/10/10 14:20
import datetime
# import sys
# sys.path.append('/home/work/wenbin/system_monitor_test/system_monitor_test')
from scripts.handle_requests import DoRequests
from scripts.handle_mysql import HandleMySQL


class QueryInterface:
    '''
    监控系统Query数据查询接口
    '''
    # 创建requests封装类的实例对象
    do_requests = DoRequests()
    # 创建pymysql封装类的实例对象
    do_mysql = HandleMySQL()

    def query_last_result(self):
        '''
        最新数据查询
        通过http.post来发起最新数据查询请求。
        一次请求，返回被查询采集项 最新上报的一个数据点。
        查询多个采集项，会同时返回多个采集项的最新数据点
        :return:响应结果list类型
        '''
        # 请求体
        data = [
            {
                "endpoint": "c4-midata-dp-web01.bj",
                "counter": "dp.pt.xiaomi.com_200__status_code/counter=nginx,pdl=cloudteg",
            },
            {
                "endpoint": "c4-midata-dp-web02.bj",
                "counter": "dp.pt.xiaomi.com_200__status_code/counter=nginx,pdl=cloudteg",
            }
        ]
        # headers = {"Content_Type": "application/json"}
        # 请求url
        url = "http://api.falcon.srv/v1.0/pub/graph/last"
        # 响应结果
        result_list = self.do_requests.handle_requests(url=url, data=data, is_json=True).json()
        return result_list

    def insert_data_to_mysql(self):
        '''
        对响应体数据进行解析，将endpoint、counter、timestamp、value写入到mysql里
        :return:
        '''
        # 响应结果list类型
        data_list = self.query_last_result()
        # print(data_list)
        # sql_list用于存放多条sql数据
        sql_list = []
        for item in data_list:
            # datetime.datetime.fromtimestamp(item['value']['timestamp'])：将timestamp类型时间戳转化成datetime类型时间戳
            sql = (
                'host=' + item['endpoint'], item['value']['value'],
                datetime.datetime.fromtimestamp(item['value']['timestamp']))
            # sql_list用于存放多条sql数据
            sql_list.append(sql)
        # print(sql_list)
        # sql语句
        sql = "insert into dpqadb.metrics(app,metric,tag,`value`,`time`) " \
              "values ('falcon', 'dp.pt.xiaomi.com_200__status_code/counter=nginx,pdl=cloudteg', %s, %s, %s);"
        # "insert into dpqadb.query_data_metrics(endpoint,counter,`time`,`value`) values (%s, %s, %s, %s);"
        # 执行同时插入多条sql语句操作
        self.do_mysql.sql_insert_more_execute(sql=sql, args=sql_list)


if __name__ == '__main__':
    test = QueryInterface()
    test.insert_data_to_mysql()
