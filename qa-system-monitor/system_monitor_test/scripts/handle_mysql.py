# -*- coding: utf-8 -*-
#  @Time    : 2019/8/5 0:51
#  @Author  : Anonymous
#  @File    : handle_mysql.py

import os
import pymysql
from scripts.handle_config import HandleConfig
from scripts.handle_path_constants import CONFIGS_DIR


class HandleMySQL:
    '''
    mysql封装类
    '''
    # 配置文件config.ini的路径
    config_path = os.path.join(CONFIGS_DIR, 'config.ini')
    do_config = HandleConfig(config_path)

    def __init__(self):
        '''
        host:服务器IP地址
        user:数据库用户名
        password:数据库密码
        database:需要连接的数据库名
        port:端口号
        cursorclass:游标类
        '''
        # 创建连接对象
        self.conn = pymysql.connect(host=self.do_config.get_value('handle_mysql', 'host'),
                                    user=self.do_config.get_value('handle_mysql', 'user'),
                                    password=self.do_config.get_value('handle_mysql', 'password'),
                                    database=self.do_config.get_value('handle_mysql', 'database'),
                                    port=self.do_config.get_int('handle_mysql', 'port'),
                                    cursorclass=pymysql.cursors.DictCursor)  # 指定游标类为字典游标类
        # 创建游标对象
        self.cursor = self.conn.cursor()

    def sql_select_execute(self, sql, args=None, is_more=False):
        '''
        执行查询SQL语句的方法
        :param sql: SQL语句
        :param args: SQL语句中传的元组
        :return:is_more=True->返回多条查询结果, is_more=False->返回单条查询结果
        '''
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        if is_more:
            # 获取多条数据
            return self.cursor.fetchall()
        else:
            # 获取单条数据
            return self.cursor.fetchone()

    def sql_insert_execute(self, sql):
        '''
        插入单条数据的方法
        :param sql: SQL语句
        :return:
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def sql_insert_more_execute(self, sql, args):
        '''
        批量插入多条数据的方法
        :param sql: SQL语句
        :param args: 嵌套tuple的list
        :return:
        '''
        self.cursor.executemany(sql, args=args)
        self.conn.commit()

    def close_mysql(self):
        '''
        关闭游标和数据库连接
        :return:
        '''
        # 关闭游标对象
        self.cursor.close()
        # 关闭数据库连接对象
        self.conn.close()


