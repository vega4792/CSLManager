#!/bin/sh
sudo pip install fabric==2.6

sudo rm -rf /home/ubuntu/student
mkdir /home/ubuntu/student

mkdir /home/ubuntu/Desktop/과제제출
mkdir /home/ubuntu/CSLManager

cp fabFunction.py /home/ubuntu/CSLManager/
cp CSLManager.py /home/ubuntu/CSLManager/
cp sitelist.txt /home/ubuntu/CSLManager/
cp CSLManager.desktop /home/ubuntu/Desktop/

sudo chmod +x /home/ubuntu/Desktop/CSLManager.desktop
sudo chmod 777 /home/ubuntu/Desktop/과제제출

echo ""
echo ""
echo "CSL Manager 설치 완료!"
echo ""
echo "바탕화면의 바로가기 아이콘 - 우클릭 - 실행 허용 체크하세요!"
echo ""


