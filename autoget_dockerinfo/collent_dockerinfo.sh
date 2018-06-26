#!/bin/bash
# This scripts is made for hand out dir /server/scripts/dockerinfo and execute scripts /usr/local/zabbix/bin/dockerinfo/bin/main.py at host in yufabu
# made by xulin at 2017年3月31日15:13:30
source /etc/profile

echo $(date) >>/root/cron.log

for IP in 192.168.20.{1..100}
do
    echo $IP
    sshpass -p'root' scp -o StrictHostKeyChecking=no -r /server/scripts/dockerinfo root@${IP}:/usr/local/zabbix/bin/
    sshpass -p'root' ssh -o StrictHostKeyChecking=no root@${IP} python /usr/local/zabbix/bin/dockerinfo/bin/main.py  & >>/root/cron.log
done
