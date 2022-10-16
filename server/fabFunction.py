import fabric
from invoke import Responder
import os
import threading

sudopass = Responder(pattern = r'\[sudo\] password:', response = 'wjdqh\n')
clientConfig = fabric.Config(overrides = { 'run': {'in_stream': False }, 'sudo': {'password': 'wjdqh'} } )

clientList=[]
clientConnection = []
clientGroup=[]

def work(f):
    def status():
        print('=====', f.__doc__, '시작 =====')
        f()
        print('=====', f.__doc__, '완료 =====')
    return status


def createDirectory(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder,0o777)
    except OSError:
        print('[Error] 디렉토리 생성에 실패하였습니다! - ',folder)


@work
def resetClient():
    '''클라이언트 연결 리셋'''
    global sudopass,clientList,clientConnection,clientGroup
    clientList=[]
    clientConnection=[]
    clientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    #print(allIP)
    for ip in allIP:
        os.remove(folder+ip)
    print('>>>>> 5초 마다 연결을 확인합니다. 접속 확인 버튼을 눌러보세요! <<<<<')


# 클라이언트 체크 (/home/ubuntu/student 에 목록 생성: 클라이언트에서 자기 ip 보내줌)
@work
def checkIP():
    '''클라이언트 접속 확인'''
    global sudopass,clientList,clientConnection,clientGroup,clientConfig
    clientList=[]
    clientConnection=[]
    clientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    for ip in allIP:
        clientList.append(ip[:-3])

    for conIP in clientList:
        try:
            clientConnection.append(fabric.Connection(host=conIP, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
        except:
            print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -', conIP)

    clientGroup = fabric.ThreadingGroup.from_connections(clientConnection)


@work
## 쓰레드 타이머 - ip 확인 - 테스트 아직..
def threadCheckIP():
    '''클라이언트 접속 확인(threading)'''
    global sudopass,clientList,clientConnection,clientGroup,clientConfig
    tclientList=[]
    tclientConnection=[]
    tclientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    for ip in allIP:
        tclientList.append(ip[:-3])

    for conIP in tclientList:
        try:
            tclientConnection.append(fabric.Connection(host=conIP, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
        except:
            print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -',conIP)

    tclientGroup = fabric.ThreadingGroup.from_connections(tclientConnection)
    
    clientList,clientConnection,clientGroup = tclientList,tclientConnection,tclientGroup

    T=threading.Timer(5, threadCheckIP) #5초마다 실행
    T.start()


@work
def backupAll():
    '''모든 클라이언트 백업'''
    global sudopass,clientList,clientConnection,clientGroup
    try:
        clientGroup.sudo('mv /etc/ubuntu/reset.tar.gz /etc/ubuntu/reset_old.tar.gz')
        clientGroup.sudo('tar cvzpf /etc/ubuntu/reset.tar.gz /home/ubuntu/')
    except:
        print('[Error] 백업 중 문제가 발생하였습니다!')
        
@work
def restoreAll():  # 필요성 검토, 미구현
    return

@work
def runAll(cmd):
    '''원격 명령어 전송'''
    global sudopass,clientList,clientConnection,clientGroup
    try:
        clientGroup.run(cmd)
    except:
        print('[Error] 명령어 전송 중 문제가 발생하였습니다!')

@work
def sudoAll(cmd):
    '''원격 명령어(sudo) 전송'''
    global sudopass,clientList,clientConnection,clientGroup
    try:
        clientGroup.sudo(cmd)
    except:
        print('[Error] 명령어(sudo) 전송 중 문제가 발생하였습니다!')

@work
def transferAll(filename):
    '''모든 클라이언트에 파일 전송'''
    global sudopass,clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/Desktop/과제제출/'
    try:
        clientGroup.put(filename, foldername)
    except:
        print('[Error] 파일 전송 중 오류가 발생하였습니다. -', filename)

@work
def transferSel(filename, client):
    '''선택된 클라이언트에 파일 전송'''
    global sudopass,clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/Desktop/과제제출/'

    print(filename,'-->', client)
    try:
        client.put(filename, foldername)
    except:
        print('[Error] 파일 전송 중 문제가 발생하였습니다!')

@work
def getFileSel(ip, client):
    '''선택된 클라이언트의 과제 파일 회수'''
    print(ip,'--> Server')
    foldername = '/home/ubuntu/Desktop/과제제출/'
    try:
        output = client.run('ls -1 '+foldername)
        files = output.stdout.strip().split('\n')
        for file in files:
            print(file,'전송 중')
            try:
                if file!='':
                    client.get(foldername+file, foldername+ip+'_'+file)
                else:
                    client.get(foldername+file, foldername+ip+'_파일없음')
            except:
                pass
    except:
        print('[Error] 폴더를 찾을 수 없습니다!')

@work
def getFileAll():
    '''모든 클라이언트의 과제 파일 회수'''
    global sudopass,clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/Desktop/과제제출/'

    for idx,client in enumerate(clientConnection):
        print(clientList[idx],'--> Server')
        try:
            result = client.run('ls -1 '+foldername)
            allfiles = result.stdout.strip().split('\n')
            for file in allfiles:
                try:
                    if file!='':
                        client.get(foldername+file, foldername+clientList[idx]+'_'+file)
                    else:
                        client.get(foldername+file, foldername+clientList[idx]+'_파일없음(미제출)')                    
                except:
                    pass
        except:
            print('[Error] 폴더를 찾을 수 없습니다!')

@work
def runSiteRule():
    '''사이트 차단 정책 적용'''
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 사이트 정책 초기화 =====')
    clientGroup.sudo('iptables -F')

    f=open('/home/ubuntu/CSLManager/sitelist.txt')
    sites = f.readlines()
    f.close()

    for site in sites:
        site = site.strip()
        print(site)
        if site=='' or site=='\n' or site[0]=='#':
            pass
        else:
            cmd = f'iptables -A OUTPUT -d {site} -j DROP'
            print('차단 정책 :', cmd, '적용 중..')
            try:
                clientGroup.sudo(cmd)
            except:
                print('[Error] iptables 명령어(sudo) 실행 중 문제가 발생하였습니다!')
