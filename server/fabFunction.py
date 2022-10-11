from pydoc import cli
import fabric
from invoke import Responder
import os
import threading
import time

sudopass = Responder(pattern = r'\[sudo\] password:', response = 'wjdqh\n')
#clientConfig = fabric.Config(overrides={'sudo': {'password': 'wjdqh', 'user':'ubuntu'}})
clientConfig = fabric.Config(overrides={'sudo': {'password': 'wjdqh'}})

clientList=[]
clientConnection = []
clientGroup=[]

def createDirectory(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder,0o777)
    except OSError:
        print('[Error] 디렉토리 생성에 실패하였습니다! - ',folder)


# 클라이언트 목록 지움
def resetClient():
    global sudopass,clientList,clientConnection,clientGroup
    clientList=[]
    clientConnection=[]
    clientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    print('===== 클라이언트 연결 리셋 시작 =====')
    print(allIP)
    for ip in allIP:
        os.remove(folder+ip)
    print('===== 클라이언트 연결 리셋 완료 =====')
    print('5초 뒤에 PC확인 버튼을 눌러보세요!')


# 클라이언트 체크 (/home/ubuntu/student 에 목록 생성: 클라이언트에서 자기 ip 보내줌)
def checkIP():
    global sudopass,clientList,clientConnection,clientGroup,clientConfig
    clientList=[]
    clientConnection=[]
    clientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    print('===== 클라이언트 확인 시작 =====')
    for ip in allIP:
        clientList.append(ip[:-3])

    for conIP in clientList:
        try:
            clientConnection.append(fabric.Connection(host=conIP, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
#            clientConnection.append(fabric.Connection(host=conIP, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}))
        except:
            print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -',conIP)

    clientGroup = fabric.ThreadingGroup.from_connections(clientConnection)
    print('===== 클라이언트 확인 완료 =====')
    print(*clientConnection)


## 쓰레드 타이머 - ip 확인 - 테스트 아직..
def threadCheckIP():
    global sudopass,clientList,clientConnection,clientGroup,clientConfig
    tclientList=[]
    tclientConnection=[]
    tclientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    print('===== 클라이언트 확인 시작(threading) =====')
    for ip in allIP:
        tclientList.append(ip[:-3])

    for conIP in tclientList:
        try:
            tclientConnection.append(fabric.Connection(host=conIP, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
        except:
            print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -',conIP)

    tclientGroup = fabric.ThreadingGroup.from_connections(tclientConnection)
    
    clientList,clientConnection,clientGroup = tclientList,tclientConnection,tclientGroup

    print('===== 클라이언트 확인 완료(threading) =====')
    print(*clientConnection)
    
    T=threading.Timer(5, threadCheckIP)
    T.start()


def backupAll():
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 모든 클라이언트 백업 시작 =====')
    try:
#        clientGroup.sudo('rm /etc/ubuntu/reset.tar.gz', in_stream=False, watchers=[sudopass])
#        clientGroup.sudo('tar cvzpf /etc/ubuntu/reset.tar.gz /home/ubuntu/', in_stream=False, watchers=[sudopass])
        clientGroup.sudo('mv /etc/ubuntu/reset.tar.gz /etc/ubuntu/reset_old.tar.gz', in_stream=False)
        clientGroup.sudo('tar cvzpf /etc/ubuntu/reset.tar.gz /home/ubuntu/', in_stream=False)
    except:
        print('[Error] 백업 중 문제가 발생하였습니다!')
    print('===== 모든 클라이언트 백업 완료 =====')


def restoreAll():  # 필요성 검토, 미구현
    return


def runAll(cmd):
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 원격 명령어 전송 시작 =====')
    try:
#        clientGroup.run(cmd, pty=True, in_stream=False, watchers=[sudopass])
        clientGroup.run(cmd, in_stream=False)
    except:
        print('[Error] 명령어 전송 중 문제가 발생하였습니다!')
    print('===== 원격 명령어 전송 완료 =====')


def sudoAll(cmd):
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 원격 명령어(sudo) 전송 시작 =====')
    try:
#        clientGroup.sudo(cmd, pty=True, in_stream=False, watchers=[sudopass])
        clientGroup.sudo(cmd, in_stream=False)
    except:
        print('[Error] 명령어(sudo) 전송 중 문제가 발생하였습니다!')
    print('===== 원격 명령어(sudo) 전송 완료 =====')


def transferAll(filename):
    global sudopass,clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/Desktop/과제제출/'
    print('===== 모든 클라이언트 파일 전송 시작 =====')
    try:
        clientGroup.put(filename, foldername)
    except:
        print('[Error] 파일 전송 중 오류가 발생하였습니다. -', filename)
    print('===== 모든 클라이언트 파일 전송 완료 =====')


def transferSel(filename, client):
    global sudopass,clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/Desktop/과제제출/'

    print('===== 선택된 클라이언트 파일 전송 시작 =====')
    print(filename,'-->', client)
    try:
        client.put(filename, foldername)
    except:
        print('[Error] 파일 전송 중 문제가 발생하였습니다!')
    print('===== 선택된 클라이언트 파일 전송 완료 =====')


def getFileSel(ip, client):
    print('===== 선택된 클라이언트 파일 회수 시작 =====')
    print(ip,'--> Server')
    foldername = '/home/ubuntu/Desktop/과제제출/'
    try:
        output = client.run('ls -1 '+foldername, in_stream=False)
        files = output.stdout.strip().split('\n')
        for file in files:
            print(file,'전송 중')
            try:
                if file!='':
                    client.get(foldername+file, foldername+ip+'_'+file)
                else:
                    client.get(foldername+file, foldername+ip+'_파일없음')
            except:
                print('[Error] 파일 회수 중 문제가 발생하였습니다! -', ip)
    except:
        print('[Error] 폴더를 찾을 수 없습니다!')

    print('===== 선택된 클라이언트 파일 회수 완료 =====')


def getFileAll():
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 모든 클라이언트 파일 회수 시작 =====')
    foldername = '/home/ubuntu/Desktop/과제제출/'

    for idx,client in enumerate(clientConnection):
        print(clientList[idx],'--> Server')
        try:
            result = client.run('ls -1 '+foldername, in_stream=False)
            allfiles = result.stdout.strip().split('\n')
            for file in allfiles:
                try:
                    if file!='':
                        client.get(foldername+file, foldername+clientList[idx]+'_'+file)
                    else:
                        client.get(foldername+file, foldername+clientList[idx]+'_파일없음(미제출)')                    
                except:
                    print('[Error] 파일 회수 중 문제가 발생하였습니다!')
        except:
            print('[Error] 폴더를 찾을 수 없습니다!')

    print('===== 모든 클라이언트 파일 회수 완료 =====')


def runSiteRule():
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 사이트 정책 초기화 =====')
#    clientGroup.sudo('iptables -F', in_stream=False, watchers=[sudopass])
    clientGroup.sudo('iptables -F && iptables -P OUTPUT ACCEPT', in_stream=False)

    print('===== 사이트 차단 정책 적용 시작 =====')
    f=open('/home/ubuntu/CSLManager/sitelist.txt')
    sites = f.readlines()
    f.close()
#    print(sites)

    for site in sites:
        site = site.strip()
        print(site)
        if site=='' or site=='\n' or site[0]=='#':
            pass
        else:
            cmd = f'iptables -A OUTPUT -d {site} -j DROP'
            print('차단 정책 적용 중... ', cmd)
            try:
#                clientGroup.sudo(cmd, in_stream=False, watchers=[sudopass])
                clientGroup.sudo(cmd, in_stream=False)
            except:
                print('[Error] iptables 명령어(sudo) 실행 중 문제가 발생하였습니다!')

    print('===== 사이트 차단 정책 적용 완료 =====')

