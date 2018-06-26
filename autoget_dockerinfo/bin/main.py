#!/usr/bin/env python
# -- coding:utf-8 --
# scripts made for get msg to mysql
# by xulin at 2017年3月15日14:11:15

import container_info, docker_info
import os

cmd = """ps -ef|grep "[/]usr/local/zabbix/bin/dockerinfo/bin/main.py"|wc -l"""
ret = os.popen(cmd).read().strip()
if __name__ == '__main__' and ret == "1":
    docker_info.docker_ps()             # 更新信息
    docker_info.send_msg_lib()          # 写信息

    container_id = container_info.get_container_id()      # 获取容器ID

    for item in container_id:           # 轮询容器ID 获取 该容器ID 并入库
        ret = container_info.input_db_info(item)
        # print(ret)
