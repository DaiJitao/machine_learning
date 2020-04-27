#!/bin/bash


while true
do
	free -h
	echo "1 正在释放内存..."
	echo 3 > /proc/sys/vm/drop_caches
	sleep 10m
	echo "   "
    echo "   "
	echo "2 内存已释放，结果："
	free -h
done
