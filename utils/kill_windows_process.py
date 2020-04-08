# -*- coding: UTF-8 -*-
# Date   : 2020/2/17 15:53
# Editor : gmj
# Desc   : 
#
# import os
# import time
# ret = os.system('tasklist | find "QQ.exe"')
#
# print(ret)

import psutil


def get_count_of_nodejs():
    i = 0
    for pro in psutil.process_iter():
        if pro.name() == 'node.exe':
            i += 1
    return i


def kill_process_with_name(process_name, num):
    """
    根据进程名杀死进程
    """
    if num < 0:
        return
    pid_list = psutil.pids()
    i = 0
    for pid in pid_list:
        try:
            each_pro = psutil.Process(pid)
            if process_name.lower() in each_pro.name().lower():
                each_pro.terminate()
                i += 1
                each_pro.wait(timeout=3)
            if i >= num:
                break
        except psutil.NoSuchProcess:
            pass


def kill_nodejs():
    nodejs_num = get_count_of_nodejs()
    kill_process_with_name('node.exe', nodejs_num - 5)


if __name__ == '__main__':
    kill_nodejs()
