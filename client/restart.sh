#!/bin/sh

pid=`ps -ef | grep "sendIP" | grep -v 'grep' | awk '{print $2}'`

if [ -z $pid ]; then
   sudo python3 /etc/ubuntu/sendIP.py &
fi
