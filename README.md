# CSL Manager for Ubuntu 22.04

## 1. 설치 방법
### 0) 다운로드
```
git clone https://github.com/vega4792/CSLManager install_Manager
```

### 1) 교사용 PC(서버)
```
cd install_Manager/server
bash install-server.sh
```
* [x] 설치 후 바탕화면의 아이콘 **마우스 우클릭 - [실행 허용] 체크** 후 실행
<br>

### 2) 학생용 PC(클라이언트) 원격 설치 방법
* 이 방법을 사용하면 교사용에서 한 번에 클라이언트를 설치할 수 있다.
* 3)의 방법은 일일이 설치하는 방법이므로 이 방법을 추천한다. 설치 방법은 <a href='https://github.com/vega4792/CSLManager/blob/main/remoteInstall/README.md'>remoteInstall 페이지</a>에 따로 작성했으니, 참고 바란다.


### 3) 학생용 PC(클라이언트) - 넘어가세요.
* 2)의 방법으로 설치한 경우 넘어가세요. 이 방법은 일일이 수동 설치 하는 방법임.

```
cd install_Manager/client
sudo bash install-client.sh
```
- 클라이언트의 서버 IP와 Password를 변경한다.
```
sudo nano /etc/ubuntu/server.ip
```
- 서버 주소와 비번을 수정한다.
```
192.168.0.10      # 서버 IP
wjdqh             # 서버 Password
```

* [x] 설치 후 **재부팅 필수**
```
reboot
```

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
#### sitelist.txt - 차단 목록 리스트 파일
<br>

### 2) 클라이언트 파일
```
파일 위치 : /etc/ubuntu/
```
#### sendIP.py - 서버로 자신의 IP를 주기적으로 보냄(백그라운드 실행)
#### clientEnv.py - 클라이언트 환경 변수 파일
#### server.ip - 서버 환경 변수 파일
<br>
