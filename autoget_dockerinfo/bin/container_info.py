#!/usr/bin/env python
# -- coding:utf-8 --
# scripts made for get msg to mysql
# by xulin at 2017年3月15日14:11:15

import os, sys, pymysql, json, re, docker_info

host_name = os.popen("hostname").read().strip()
psfile = "../log/docker_ps.log"
infofile = "../log/container_info.log"
container_id = []
container_ip = []
container_port = []

db_msg = {
    "host": "10.10.36.67",
    "port": 3306,
    "user": "root",
    "passwd": "jyall123",
    "db": "docker_msg"
}
# table_name = "container_msg"
table_name = "yufabu"


def get_container_id():
    """
    从数据库中读取容器ID，            根据容器ID 从物理机获取数据，进而将信息入库
    :param container_id:
    :return:
    """
    db = pymysql.connect(**db_msg)
    cursor = db.cursor()
    sql = """ SELECT container_id FROM `%s` WHERE host='%s' AND status='Up'; """ %(table_name, host_name)
    print(sql)
    try:
        ret = cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            container_id.append(row[0])

    except pymysql.Error as err:
       print("ERROR: %s\n%s" %(sql, err))
    # results = cur.fetchall()
    # print(results[1])
    cursor.close()
    db.close()
    return container_id


def insert_mysql(ip_intranet, ip_extrnet, ip_all, port, service, id):
    """
    为数据库 update 数据
    :param ip_intranet: 内网IP
    :param ip_extrnet: 外网IP
    :param service: java服务包名
    :param host: container_id 容器ID
    :return: sql 执行结果
    """
    import pymysql, json
    conn = pymysql.connect(**db_msg)
    cur = conn.cursor()
    sql = "UPDATE %s SET " \
          "`ip intranet`= '%s'," \
          "`ip extrnet`='%s'," \
          "`ip all`='%s'," \
          "`port`='%s'," \
          "service_name='%s' " \
          "WHERE container_id='%s';" %(table_name, ip_intranet, ip_extrnet, ip_all, port, service, id)
    # sql = "INSERT %s " \
    #       "SET host='%s', " \
    #       "container_id='%s'," \
    #       "container_name='%s'," \
    #       "image='%s'," \
    #       "insert_date=now();" %(table_name, host, id, name, img)
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


def input_db_info(id):
    print(id)
    cmd_172 = """ docker exec %s ifconfig 2>/dev/null |grep "172\.16\."|awk -F "[ (addr:)]+" '{print $3}' |xargs -n1 """ %id
    ip172 = os.popen(cmd_172).read().strip()

    cmd_10 = """ docker exec %s ifconfig 2>/dev/null |grep "10\.10\."|awk -F "[ (addr:)]+" '{print $3}' |xargs -n1 """ %id
    ip10 = os.popen(cmd_10).read().strip()

    cmd_all = """ echo `docker exec {0} ip a 2>/dev/null |sed -nr "s#^.*inet ([0-9.]+)/.*#\\1#gp" ;docker exec {0} ifconfig 2>/dev/null |sed -nr "s#^.*inet (.*)  netmask.*#\\1#gp"`|xargs -n1|sort|uniq |grep -v "127.0.0.1" |xargs """.format(id)
    ipall = os.popen(cmd_all).read().strip()

    cmd_port = """ docker exec %s netstat -tnl 2>/dev/null |grep -v "127.0.0.1" |sed -rn 's/tcp.*:([0-9]+) .*:.*/\\1/gp' |sort|uniq|grep -Ev ".....$" |xargs """ %id
    port = os.popen(cmd_port).read().strip()

    cmd_service = """ docker exec %s ls /data/server/libs/  2>/dev/null |grep "ar$" """ %id
    service = os.popen(cmd_service).read().strip()
    service = re.sub(r"-[^-]+.jar", "", service)
    service = re.sub(r"-[0-9\.]+.*", "", service)

    cmd_status = """ docker ps -a|grep %s |egrep "Up|Exited" |wc -l """ %id
    status = os.popen(cmd_status).read().strip()
    if status == '0': docker_info.update_mysql(id, status)

    ret = insert_mysql(ip172, ip10, ipall, port, service, id)
    return ret


if __name__ == '__main__':
    get_container_id()      # 获取容器ID

    for item in container_id:           # 轮询容器ID 获取 该容器ID 并入库
        input_db_info(item)
