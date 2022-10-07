# CSL Manager for Ubuntu 22.04

## 1. 설치 방법
### 1) 교사용 PC(서버)
```
bash install-server.sh
```
* [x] 설치 후 바탕화면의 아이콘 **마우스 우클릭 - [실행 허용] 체크** 후 실행
<br>

### 2) 학생용 PC(클라이언트)
```
bash install-client.sh
```
* [x] 설치 후 **재부팅 필수**
<br>

<br>

## 2. 파일 설명
### 1) 서버 파일
```
파일 위치 : /home/ubuntu/CSLManager/
```
#### CSLManager.py - tkinter를 이용한 GUI
#### fabFunction.py - fabric을 이용한 ssh 원격 명령 함수
#### CSLManager.desktop - 바탕화면 바로가기 파일
#### siteList.txt - 차단 목록 리스트 파일
<br>

### 2) 클라이언트 파일
```
파일 위치 : /etc/ubuntu/
```
#### sendIP.py - 서버로 자신의 IP를 주기적으로 보냄(백그라운드 실행)
#### clientEnv.py - 환경 변수 파일
<br>
