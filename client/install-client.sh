#!/bin/sh
sudo pip install fabric==2.6

mkdir /home/ubuntu/Desktop/과제제출
mkdir /home/ubuntu/.stuenv

sudo chmod 777 /home/ubuntu/Desktop/과제제출

sudo cp sendIP.py /etc/ubuntu/
sudo cp clientEnv.py /etc/ubuntu/

if grep "sendIP.py" /etc/rc.local ; then
  echo "done!"
else
  sed -i "s/exit 0//g" /etc/rc.local
  sed -i "s/EOF//g" /etc/rc.local
  
  echo "sudo python3 /etc/ubuntu/sendIP.py & " >> /etc/rc.local
  echo "exit 0" >> /etc/rc.local
  echo "EOF" >> /etc/rc.local
  echo "done!"
fi
