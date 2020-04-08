# -*- coding: UTF-8 -*-
# Date   : 2020/3/26 17:56
# Editor : gmj
# Desc   : 表中某个字段的特殊字符处理模块


import datetime
import json

from common.database.mysql import MysqlConnect
from common.database.db_config import ALI_MYSQL_CONFIG

clear_cnn = MysqlConnect(ALI_MYSQL_CONFIG)


class ClearBySql(object):
    def __init__(self, connect, theme=None):
        self.connect = connect
        self.day = str(datetime.date.today())
        self.sql_file = open(f'./execute_sql{self.day}{theme if theme else ""}.sql', 'a+', encoding='utf-8')

    # 换行符 \r\n
    def clear_rn(self, table_name, field):
        """
        清除\r\n换行符
        :param table_name:
        :param field:
        :return:
        """
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'\\r\\n','') WHERE `{field}` LIKE '%\\r\\n%';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除换行符\\r\\n')
        self._write_sql(sql)

    # 换行符 \n
    def clear_n(self, table_name, field):
        """
        清除\n换行符
        :param table_name:
        :param field:
        :return:
        """
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'\\n','') WHERE `{field}` LIKE '%\\n%';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除换行符\\n')
        self._write_sql(sql)

    # 空格符
    def clear_space(self, table_name, field):
        """
        清除空格
        :param table_name:
        :param field:
        :return:
        """
        sql = f"update {table_name} set `{field}`=replace(`{field}`,' ','') WHERE `{field}` LIKE '% %';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除空格')
        self._write_sql(sql)
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'&nbsp;','') WHERE `{field}` LIKE '%&nbsp;%';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除空格&nbsp;')
        self._write_sql(sql)

    # tab符号
    def clear_tab(self, table_name, field):
        """
        清除\t符号
        :param table_name:
        :param field:
        :return:
        """
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'\t','') WHERE `{field}` LIKE '%\t%';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除tab符')
        self._write_sql(sql)

    def clear_single(self, table_name, field):
        sql = f'update {table_name} set `{field}`=replace(`{field}`,"\'","") WHERE `{field}` LIKE "%\'%";'
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除单引号')
        self._write_sql(sql)

    def clear_double(self, table_name, field):
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'\"','') WHERE `{field}` LIKE '%\"%';"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 清除单引号')
        self._write_sql(sql)

    # 中文括号
    def clear_chinese_brackets(self, table_name, field):
        """
        把中文括号 换成 英文括号
        :param table_name:
        :param field:
        :return:
        """
        sql = f"update {table_name} set `{field}`=replace(`{field}`,'（','(').replace(`{field}`,'）',')');"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 替换中文括号为英文括号')
        self._write_sql(sql)

    def change_lower_to_upper(self, table_name, field):
        sql = f"update {table_name} set `{field}`=Upper(`{field}`);"
        self.connect.update(sql)
        self._write_explain(f'{table_name} - {field} 将小写字母变为大写')
        self._write_sql(sql)

    def extract_unicode_to_chinese(self, table_name, field):
        """
        根据id来进行更新的   转化unicode编码为中文
        :param table_name: 表名
        :param field: 字段名
        :return:
        """
        datas = self.connect.fetchall(f'select * from {table_name} where {field} like "%u%"')
        i = 0
        for da in datas:
            try:
                id = da['id']
                org = da[field].replace('u', '\\u')
                content = json.loads(f'"{org}"')
                self.connect.execute(f'update {table_name} set {field}="{content}" where id={id}')
                i += 1
            except Exception as e:
                print(e)
            if i % 100 == 0:
                self.connect.commit()
        self.connect.commit()

    def _write_explain(self, txt):
        self.sql_file.write(f'-- {txt}\n')

    def _write_sql(self, txt):
        self.sql_file.write(f'{txt}\n')

    def __del__(self):
        self.sql_file.close()

    def clear_all(self, table_dict: dict):
        items_dict = {
            '\r\n': 'clear_rn',
            '\n': 'clear_n',
            ' ': 'clear_space',
            '\t': 'clear_tab',
            '（': 'clear_chinese_brackets',
            '"': 'clear_single',
            "'": 'clear_double',
        }
        for table_name, fields in table_dict.items():
            for field, items in fields.items():
                for item in items:
                    eval(f'self.{items_dict[item]}(table_name,field)')


CLEAR_BY_SQL = {
    # 表名称  {字段名1：(要替换字符)，字段名2：(要替换的字符)}
    # ('\r\n', '\n', '\t', '（', '"', "'")
    't_major': {'': ('\r\n', '\n', '\t', '（', '"', "'"), }
}



if __name__ == '__main__':
    cl = ClearBySql(clear_cnn)
    cl.clear_double('t_major_art_copy', 'major_id')
