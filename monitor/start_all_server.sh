#!/bin/bash

echo "启动数据监控总服务"
nohup python data_monitor.py &

sleep 2
echo "启动监控账号服务"
nohup  python user_monitor.py &

sleep 1
echo "启动预警服务"
nohup python warning.py &