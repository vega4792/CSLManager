#!/bin/sh
# crontab -e
# */1 * * * * /etc/ubuntu/restart.sh >> /etc/ubuntu/restart.log
# chmod 755 restart.sh

for i in {1..12}; do
	pid=`ps -ef | grep "sendIP" | grep -v 'grep' | awk '{print $2}'`

	if [ -z $pid ]; then
		sudo python3 /etc/ubuntu/sendIP.py &
	fi
	sleep 5
done
