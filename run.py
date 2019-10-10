# -*- coding:utf-8 -*-
# author:wenbin
# datetime:2019/9/27 13:32

import os
import datetime
from scripts.handle_requests import DoRequests
from scripts.handle_mysql import HandleMySQL
from scripts.handle_config import HandleConfig
from scripts.handle_path_constants import CONFIGS_DIR
from scripts.handle_log import HandleLog
from scripts.handle_parameterize import DoParameterize


class Id_Account:
    '''
    统计IDcount类
    '''
    # 创建封装requests请求类实例对象
    do_requests = DoRequests()
    # 创建封装pymysql类实例对象
    do_mysql = HandleMySQL()
    # 创建DoParameterize参数化类实例对象
    do_parameterize = DoParameterize()
    # 配置文件config.ini的路径
    config_path = os.path.join(CONFIGS_DIR, 'config.ini')
    # 创建DoParameterize参数化类实例对象
    do_config = HandleConfig(config_path)
    # 创建DoParameterize参数化类实例对象
    do_log = HandleLog(config_path).get_logger()
    # 请求参数data
    data = """{"q": "${query}", "f": 0, "sd": "xhdpi", "hl": "zh_CN", "p": 0, "nt": "wifi", "lo": 21.8, "la": 51.8, "se": None,"sp": "china mobile", "imei": None, "dm": "MIX 2S", "di": None, "sv": "MIUI 10.3.5", "vr": "4.4.4","vs": "19", "sid": 5, "s": 1, "n": 50, "_sl": True, "addr": "北京市海淀区清河朱房路", "cv": 0, "cc": None, "ti": None,"from": None, "h_t": None, "cd": True}"""

    # data = {"q": "中秋节", "f": 0, "sd": "xhdpi", "hl": "zh_CN", "p": 0, "nt": "wifi", "lo": 21.8, "la": 51.8, "se": None,
    #         "sp": "china mobile", "imei": None, "dm": "MIX 2S", "di": None, "sv": "MIUI 10.3.5", "vr": "4.4.4",
    #         "vs": "19", "sid": 5, "s": 1, "n": 50, "_sl": True, "addr": "北京市海淀区清河朱房路", "cv": 0, "cc": None, "ti": None,
    #         "from": None, "h_t": None, "cd": True}
    # 请求url
    url = do_config.get_value('handle_interface', 'base_url') + '/sug'
    # 请求方式
    method = 'POST'

    def __init__(self):
        '''
        初始化函数
        '''
        # 创建requests的session会话管理器
        self.do_requests.__init__()
        # 创建数据库连接
        self.do_mysql.__init__()

    def generate_timestamp_long(self):
        '''
        获取当前时间戳long类型
        :return:当前时间戳long类型
        '''
        current_time = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
        return current_time

    def generate_timestamp(self):
        '''
        获取当前时间戳
        :return:当前时间戳
        '''
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def execute_requests(self):
        '''
        请求sug接口方法
        :return:
        '''
        # 替换请求数据data中的查询关键字query
        data_new = self.do_parameterize.query_parametric(data=self.data)
        # print(data_new)
        data_dict = eval(data_new)
        # 将请求字段中的sid重新赋值为当前时间戳long类型
        data_dict['sid'] = self.generate_timestamp_long()
        # print(type(data_dict), data_dict)
        # print(self.create_timed_task())
        try:
            # 接口请求
            response = self.do_requests.handle_requests(url=self.url, method=self.method, data=data_dict)
            # 获取响应体dict类型
            response_dict = response.json()
            if response_dict['message'] == 'success' and response_dict['status'] == 0:
                id_list = []
                # 循环追加到id_list列表中
                for result in response_dict['result']:
                    for data in result['data']:
                        id_list.append(data['type'])
                        id_list.append(data['id'])
                # print(id_list)

                # 获取相同type类型的数据的数量，data_type_dict示例：{'news': 3, 'video': 8, 'book': 1, 'weibo': 3, 'web': 3}
                data_type_dict = {}
                for i in range(len(id_list) - 1):
                    if i % 2 == 0:
                        data_type_dict[id_list[i]] = id_list.count(id_list[i])

                # print('data_type_dict', data_type_dict)
                # 插入单条数据sql语句
                # sql = "insert into dpqadb.metrics(app,metric,`value`,`time`) values ('integrity','idcount',{}, '{}');".format(len(id_list_new),self.generate_timestamp())

                # data_sql_list1示例：[('news', 3), ('video', 8), ('book', 1), ('weibo', 3), ('web', 3)]
                data_sql_list1 = []
                data_sql_list2 = []
                for item in data_type_dict.items():
                    data_sql_list1.append(item)

                # print(data_sql_list1)
                # data_sql_list2示例(动态创建需要插入的多条sql数据)：
                # [('idcount_news', 3, '2019-10-08 15:54:41'), ('idcount_video', 8, '2019-10-08 15:54:41'),
                #  ('idcount_book', 1, '2019-10-08 15:54:41'), ('idcount_weibo', 3, '2019-10-08 15:54:41'),
                #  ('idcount_web', 3, '2019-10-08 15:54:41')]
                for i in data_sql_list1:
                    sql = ('idcount_'+i[0], i[-1], self.generate_timestamp())
                    data_sql_list2.append(sql)

                # 插入的多条数据，var为一个嵌套tuple的list
                var = data_sql_list2
                # print(data_sql_list2)
                # 插入多条数据sql语句
                sql = "insert into dpqadb.metrics(app,metric,`value`,`time`) values ('integrity', %s, %s, %s);"

                # print(sql)
                # print(response_dict)
                # 执行一次性插入多条数据的sql语句
                self.do_mysql.sql_insert_more_execute(sql=sql, args=var)
                # 打印出本次请求的日志保存到sug_requests.log日志文件中
                self.do_log.info(
                    '本次请求Query:{},Search_Result:{},Response_ID_Details(TYPE-ID):{}'.format(
                        response.json()['query'], response.json()['count'], id_list))
        except Exception as err:
            self.do_log.error('程序执行时报错了,具体异常为:{}'.format(err))
            # 关闭session
            self.do_requests.session_close()
            # 关闭mysql连接
            self.do_mysql.close_mysql()


if __name__ == '__main__':
    # 程序的入口
    test = Id_Account()
    test.execute_requests()
    # print(test.replace_data())
