#!/bin/sh
sudo pip install fabric==2.6

mkdir /home/ubuntu/Desktop/과제제출
mkdir /home/ubuntu/.stuenv

sudo chmod 777 /home/ubuntu/Desktop/과제제출
sudo chmod 755 /home/ubuntu/restart.sh

sudo mv /home/ubuntu/sendIP.py /etc/ubuntu/
sudo mv /home/ubuntu/clientEnv.py /etc/ubuntu/
sudo mv /home/ubuntu/server.ip /etc/ubuntu/
sudo mv /home/ubuntu/restart.sh /etc/ubuntu/

gio set /home/ubuntu/Desktop/과제제출 metadata::nautilus-icon-position 397,119

cat <(crontab -l) <(echo "*/1 * * * * sudo bash /etc/ubuntu/restart.sh >> /dev/null 2>&1") | sudo crontab -

