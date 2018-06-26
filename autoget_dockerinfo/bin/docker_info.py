#!/usr/bin/env python
# -- coding:utf-8 --
# scripts made for get msg to mysql
# by xulin at 2017年3月15日14:11:15

import os, sys, pymysql, re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

host_name = os.popen("hostname").read().strip()
psfile = "/usr/local/zabbix/bin/dockerinfo/log/docker_ps.log"
container_id = []
container_name = []
image = []
status = []

db_msg = {
    "host": "10.10.36.67",
    "port": 3306,
    "user": "root",
    "passwd": "jyall123",
    "db": "docker_msg"
}
table_name = "yufabu"
#table_name = "container_msg"


def docker_ps():
    """
    执行 docker ps 更新数据（每次都执行）
    :return:None
    """
    cmd_ps = "docker ps -a|sed 1d > %s" %psfile
    os.popen(cmd_ps)
    with open(psfile, 'r') as f1:
        for line in f1:
            ps_list = line.split()
            container_id.append(ps_list[0])
            container_name.append(ps_list[-1])
            ps_list[1] = re.sub("registry.cloud.jyall.com/", "", ps_list[1])
            image.append(ps_list[1])
            status_t = re.findall('Up|Exited|Created|Dead', line)
            status_t = "".join(status_t)
            status.append(status_t)
        # print(container_id, "\n", container_name, "\n", image)


def select_mysql(args):
    """
    查询 容器ID 是否存在
    :param args: 要查询的容器ID
    :return: ret ,0 为不存在，1 为存在
    """
    import pymysql, json
    conn = pymysql.connect(**db_msg)
    cur = conn.cursor()
    sql = "SELECT container_id FROM %s WHERE container_id='%s';" %(table_name, args)
    # print(sql)
    try:
        ret = cur.execute(sql)
        return ret
    except pymysql.Error as err:
       print("ERROR: %s\n%s" %(sql, err))
    # results = cur.fetchall()
    # print(results[1])
    cur.close()
    conn.close()


def insert_mysql(host, id, name, img, status):
    """
    添加容器信息
    :param host: 所在主机
    :param id: 容器id
    :param name: 容器名
    :param img: 镜像名
    :return: ret,inster 执行结果
    """
    import pymysql, json
    conn = pymysql.connect(**db_msg)
    cur = conn.cursor()
    sql = "INSERT %s " \
          "SET host='%s', " \
          "container_id='%s'," \
          "container_name='%s'," \
          "image='%s'," \
          "status='%s'," \
          "insert_date=now();" %(table_name, host, id, name, img, status)
    # print(sql)
    try:
        ret = cur.execute(sql)
        conn.commit()
        return ret
    except pymysql.Error as err:
       print("ERROR: %s\n%s" %(sql, err))
    # results = cur.fetchall()
    # print(results[1])
    cur.close()
    conn.close()


def update_mysql(id, status):
    """
    添加容器状态信息
    :param host: 所在主机
    :param id: 容器id
    :param status: 容器状态
    :return: ret,inster 执行结果
    """
    import pymysql, json
    conn = pymysql.connect(**db_msg)
    cur = conn.cursor()
    sql = " UPDATE %s " \
          "SET STATUS='%s' " \
          "WHERE container_id='%s'; " %(table_name, status, id)
    # print(sql)
    try:
        ret = cur.execute(sql)
        conn.commit()
        return ret
    except pymysql.Error as err:
       print("ERROR: %s\n%s" %(sql, err))
    # results = cur.fetchall()
    # print(results[1])
    cur.close()
    conn.close()

def create_mysql():
    """
    判断表是否存在，这里本要直接创建的，可是pymysql貌似不支持太长的sql语句
    :return: create 为不存在，exists 为存在
    """
    import pymysql, json
    conn = pymysql.connect(**db_msg)
    cur = conn.cursor()
    show_sql = "show tables like '%s';" %table_name
    create_sql = """CREATE TABLE `%s` (
  `ID` int(255) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) DEFAULT NULL COMMENT '所在主机',
  `container_id` varchar(255) DEFAULT NULL COMMENT '容器ID',
  `container_name` varchar(255) DEFAULT NULL COMMENT '容器名',
  `ip` varchar(255) DEFAULT NULL COMMENT '容器IP',
  `port` int(255) DEFAULT NULL COMMENT '服务tcp端口',
  `service_name` varchar(255) DEFAULT NULL COMMENT '服务包名',
  `image` varchar(255) DEFAULT NULL COMMENT '镜像名',
  `insert_date` datetime DEFAULT NULL COMMENT '记录时间',
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1417 DEFAULT CHARSET=utf8;""" %table_name
    try:
        ret = cur.execute(show_sql)
        cur.close()
        if ret == 0:
            # cur.execute(create_sql)     # 建表语句字符串太长，这里不支持，需在服务端创建该表。
            print("The table is not exists, Please create.\n%s" %create_sql)
            return 'create'
        else:
            return 'exists'
    except pymysql.Error as err:
        print("Mysql Error: %s" %err)
    cur.close()
    conn.close()


def send_msg_lib():
    """
    更新并写信息
    :return: None
    """
    ret = create_mysql()
    if ret == 'create':
        exit()
    for index,item in enumerate(container_id):
        # print(index)
        ret = select_mysql(container_id[index])
        if ret == 0:
            print(host_name, container_id[index], container_name[index], image[index], status[index])
            insert_mysql(host_name, container_id[index], container_name[index], image[index], status[index])
        else:
            update_mysql(container_id[index], status[index])


if __name__ == '__main__':
    docker_ps()             # 更新信息
    send_msg_lib()          # 写信息


