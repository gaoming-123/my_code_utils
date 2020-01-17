# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:38
# Editor : gmj
# Desc   : 

import pymysql
from .db_config import MYSQL_CONFIG
from .logger import logger


class MysqlConnect(object):
    def __init__(self, my_config=MYSQL_CONFIG):
        self.config = my_config
        self.cnn = self.connect()
        self.cursor = self.cnn.cursor()
        self.logger = logger

    def connect(self):
        return pymysql.connect(
            host=self.config['HOST'],
            port=self.config['PORT'],
            user=self.config['USER'],
            password=self.config['PWD'],
            db=self.config['DB'],
            charset='utf8',
        )

    def set_logger(self, my_logger):
        self.logger = my_logger

    def set_cursor(self, cursor):  # pymysql.cursors.DictCursor
        self.cursor = self.cnn.cursor(cursor=cursor)

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.logger.error(e)

    def fetchall(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def query_number_result(self, theme, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()[0]
        self.logger.info(f'{theme} : {res["count(*)"]} 条')

    def save_many(self, save_sql, save_data):
        try:
            self.cursor.executemany(save_sql, save_data)
            self.cnn.commit()
        except Exception as ee:
            self.logger.error(f'保存出错：{save_data}')
            self.logger.error(ee)
            self.cnn.commit()

    def commit(self):
        self.cnn.commit()

    def close(self):
        self.commit()
        self.cursor.close()
        self.cnn.close()


# def get_save_sql(destination_table):
#     des_table = DESTINATION_TABLES[destination_table]
#     save_sql = ' insert into ' + destination_table + f'({",".join(des_table.keys())}) ' + f' values({",".join(["%s"] * len(des_table.keys()))})'
#     return save_sql




# mysql_cnn.set_cursor(cursor=pymysql.cursors.DictCursor)
