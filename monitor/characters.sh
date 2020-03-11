#!/bin/bash

free -h
echo "释放内存"
echo 3 > /proc/sys/vm/drop_caches
sleep 5s

echo "内存已释放"
free -h
