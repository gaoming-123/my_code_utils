# -*- coding: UTF-8 -*-
# Date   : 2020/1/3 16:10
# Editor : gmj
# Desc   : html文本中的样式去除
import re
from common.database.mysql import MysqlConnect
from common.database.db_config import ALI_MYSQL_CONFIG
from common.database.logger import logger

style_cnn = MysqlConnect(ALI_MYSQL_CONFIG)

STYLE_REPLACE_ITEMS = {
    # 项目名称 ： ('用于筛选数据的字符串', '要被替换的正则表达式', '替换为什么')
    '字体替换': ('font-family', '(font-family.[^>]*?;)|(font-family.*?)"|(font-family.*?)\'', ''),
    '替换img标签': ("<img", "(<p.*?<img.*?</p>)", ''),
    '替换字体大小为28': ("font-size", "(font-size:.*?\d+px)", 'font-size:28px'),
    '去掉style': ("style", '(style=".*?")|(style=\'.*?\')', ''),
    '去除前后的空白': ('前后的空白',)
}


class FontStyleReplace(object):
    def __init__(self, connect, clear_dict: dict, items_dict: dict = STYLE_REPLACE_ITEMS):
        self.clear_dict = clear_dict
        self.cnn = connect
        self.items_dict = items_dict

    def run_all(self):
        for table_name, fields in self.clear_dict.items():
            for field, items in fields.items():
                for item in items:
                    # 自己操作的表后缀
                    work_table_name = table_name + '_operate'
                    self.table_field_item(work_table_name, field, item)

    def table_field_item(self, table_name, field, item):
        print(f"{table_name}--{field}--{item}")
        logger.info(f"{table_name}--{field}--{item}")
        pattern = self.items_dict[item]
        if pattern[0] == '前后的空白':
            data = self.fetchall(f"SELECT id,{field} FROM {table_name}")
            result = self.my_strip(data, field)
        else:
            query_sql = f"SELECT * FROM {table_name} WHERE {field} LIKE '%{pattern[0]}%'"
            data = self.fetchall(query_sql)
            result = self.replace(table_name, data, field, pattern)
        self.save(table_name, field, result)

    def replace(self, table_name, data, field, pattern, unique_key='id'):
        result = []
        for da in data:
            try:
                res = re.sub(pattern[1], pattern[2], da[field], flags=re.I)
                res = re.sub(pattern[1], pattern[2], res, flags=re.S)
                result.append((res, da[unique_key]))
            except Exception as e:
                logger.error(e)
                logger.info(f'处理 表{table_name}--id:{id} 出错请检查错误原因')
        return result

    def my_strip(self, data, field, unique_key='id'):
        result = []
        for da in data:
            try:
                res = da[field].strip()
                result.append([res, da[unique_key]])
            except:
                pass
        return result

    def fetchall(self, query_sql):
        return self.cnn.fetchall(query_sql)

    def save(self, table_name, field, result):
        save_sql = f'update {table_name} set `{field}`=%s where id=%s'
        # print(save_sql)
        self.cnn.save_many(save_sql, result)


CLEAR_CONFIG = {
    # '表名': {'字段名': ['项目名称', ]}  空列表代处理字段前后的空白字符
    't_school': {'intro': ['去除前后的空白', '替换img标签', '去掉style']},
}

if __name__ == '__main__':
    fr = FontStyleReplace(style_cnn, CLEAR_CONFIG)
    fr.run_all()
