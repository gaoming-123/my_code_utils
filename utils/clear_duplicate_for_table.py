# -*- coding: UTF-8 -*-
# Date   : 2020/3/25 15:42
# Editor : gmj
# Desc   : 对数据进行去重，只生成sql语句，不进行实际数据库操作
from common.database.mysql import MysqlConnect
from common.database.db_config import ALI_MYSQL_CONFIG
import datetime

# from multiprocessing import Process


duplicate_cnn = MysqlConnect(ALI_MYSQL_CONFIG)


class ClearDuplicateBySql(object):
    def __init__(self, theme=None):
        self.day = str(datetime.date.today())
        self.sql_file = open(f'./sql_{theme if theme else ""}{self.day}.sql', 'a+', encoding='utf-8')

    # 去重
    def clear_duplicate_by_id(self, table_name: str, unique_keys: tuple, table_type=None):
        """
        根据id对重复数据进行删除（不进行操作数据库删除），保存sql文件，用于执行
        :param table_name: 表名
        :param unique_keys: 表示唯一值的字段组合
        :param table_type:  分为'backup'  'operate' None值 (分别代表三种表)
        :return:
        """
        if table_type:
            table_name = table_name + '_' + table_type
        total = duplicate_cnn.fetchall(f'select count(*) from {table_name}')[0]['count(*)']
        unique_str = ','.join([f"`{k}`" for k in unique_keys])
        unique_data = duplicate_cnn.fetchall(f'select DISTINCT {unique_str} from {table_name}')
        unique_num = len(unique_data)
        self._write_explain(f'表{table_name} #重复数据{int(total) - unique_num}条')
        print(f'表{table_name}-重复数据{int(total) - unique_num}条')
        if unique_num == int(total):
            return
        need_clear_id = []
        for data in unique_data:
            sql_part = ' and '.join([f'`{k}`="{v}"' for k, v in data.items()])
            query_data = duplicate_cnn.fetchall(f'select * from {table_name} where {sql_part}')
            num = len(query_data)
            if num == 1:
                continue
            for i in range(1, num):
                need_clear_id.append(query_data[i]['id'])
        self._write_explain(f'{table_name} 根据id删除重复数据')
        sql_ = ''
        for id_ in need_clear_id:
            sql = f'delete from {table_name} where id={id_};\n'
            sql_ += sql
        self._write_sql(sql_)

    def _write_explain(self, txt):
        self.sql_file.write(f'-- {txt}\n')

    def _write_sql(self, txt):
        self.sql_file.write(f'{txt}\n')

    def clear_duplicate_for_all_table(self):
        self.clear_duplicate_for_operate()
        self.clear_duplicate_for_backup()
        self.clear_duplicate_for_test()

    def clear_duplicate_for_test(self):
        # 开发测试test表
        for k, v in tables.items():
            self.clear_duplicate_by_id(k, v)

    def clear_duplicate_for_backup(self):
        # # 线上库的备份表
        for k, v in tables.items():
            self.clear_duplicate_by_id(k, v, table_type='backup')

    def clear_duplicate_for_operate(self):
        # 我操作的表
        for k, v in tables.items():
            self.clear_duplicate_by_id(k, v, table_type='operate')

    def __del__(self):
        self.sql_file.close()


# 需要去重的表 以及 唯一值字段组合
tables = {
    #专业相关表
    't_major_class_type': ('major_class_id', 'name'),S
}

if __name__ == '__main__':
    cs = ClearDuplicateBySql(theme='duplicate')
    # cs.clear_duplicate_for_backup()
    # cs.clear_duplicate_by_id('channel_middle_school', ('school_name', 'school_address'), table_type='operate')
    cs.clear_duplicate_for_all_table()
