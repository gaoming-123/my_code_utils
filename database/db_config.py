# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 9:36
# Editor : gmj
# Desc   : 


# redis配置
REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': 6379,
    # 'PWD': 'root',
    'DB': 1,
    'SET_KEY': 'default_key',
}

# mysql配置
MYSQL_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'root',
    'PWD': 'root',
    'DB': 'school_odb',
}

# 本地mysql配置
LOCAL_MYSQL_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'root',
    'PWD': 'root',
    'DB': 'school_odb',
}

ALI_MYSQL_CONFIG = {
    'HOST': 'rm-bp1mc0587wj5st0g7co.mysql.rds.aliyuncs.com',
    'PORT': 3306,
    'USER': 'qbnqy',
    'PWD': 'qbn@123456',
    'DB': 'qbn_qyzy',
}

ALI_ODB_MYSQL_CONFIG = {
    'HOST': 'rm-bp1mc0587wj5st0g7co.mysql.rds.aliyuncs.com',
    'PORT': 3306,
    'USER': 'qbnqy',
    'PWD': 'qbn@123456',
    'DB': 'da_data_odb',
}
