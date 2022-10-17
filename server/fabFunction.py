import fabric
from invoke import Responder
import os
import threading

sudopass = Responder(pattern = r'\[sudo\] password:', response = 'wjdqh\n')
clientConfig = fabric.Config(overrides = { 'run': {'in_stream': False }, 'sudo': {'password': 'wjdqh'} } )

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
    for ip in allIP:
        os.remove(folder+ip)
    print('===== 클라이언트 연결 리셋 완료 =====')
    print('>>>>> 5초 마다 갱신 됩니다.접속 확인 버튼을 눌러보세요! <<<<<')


# 클라이언트 체크 (/home/ubuntu/student 에 목록 생성: 클라이언트에서 자기 ip 보내줌)
def checkIP():
    global sudopass,clientList,clientConnection,clientGroup,clientConfig
    tclientList=[]
    tclientConnection=[]
    tclientGroup=[]

    folder = '/home/ubuntu/student/'
    createDirectory(folder)
    allIP = os.listdir(folder)
    
    # 파일 생성 시간(작업 중...)
    fileinfo = []
    for filename in os.listdir(folder):
        # getctime: 입력받은 경로에 대한 생성 시간을 리턴
        fileGenTime = os.path.getctime(folder + filename)
        fileinfo.append( (filename, int(fileGenTime)) )

    print(fileinfo)
        
    # 가장 생성시각이 큰(가장 최근인) 파일을 리턴 
    #most_recent_file = max(each_file_path_and_gen_time, key=lambda x: x[1])[0]
    
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
    
    
def backupAll():
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 모든 클라이언트 백업 시작 =====')
    try:
        clientGroup.sudo('mv /etc/ubuntu/reset.tar.gz /etc/ubuntu/reset_old.tar.gz')
        clientGroup.sudo('tar cvzpf /etc/ubuntu/reset.tar.gz /home/ubuntu/')
    except:
        print('[Error] 백업 중 문제가 발생하였습니다!')
    print('===== 모든 클라이언트 백업 완료 =====')


def restoreAll():  # 필요성 검토, 미구현
    return


def runAll(cmd):
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 원격 명령어 전송 시작 =====')
    try:
        clientGroup.run(cmd)
    except:
        print('[Error] 명령어 전송 중 문제가 발생하였습니다!')
    print('===== 원격 명령어 전송 완료 =====')


def sudoAll(cmd):
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 원격 명령어(sudo) 전송 시작 =====')
    try:
        clientGroup.sudo(cmd)
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
        output = client.run('ls -1 '+foldername)
        files = output.stdout.strip().split('\n')
        for file in files:
            try:
                if file!='':
                    client.get(foldername+file, foldername+ip+'_'+file)
                else:
                    client.get(foldername+file, foldername+ip+'_파일없음')
            except:
                pass
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

    print('===== 모든 클라이언트 파일 회수 완료 =====')


def runSiteRule():
    global sudopass,clientList,clientConnection,clientGroup
    print('===== 사이트 정책 초기화 =====')
    clientGroup.sudo('iptables -F && iptables -P OUTPUT ACCEPT')

    print('===== 사이트 차단 정책 적용 시작 =====')
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
            print('차단 정책 적용 중... ', cmd)
            try:
                clientGroup.sudo(cmd)
            except:
                print('[Error] iptables 명령어(sudo) 실행 중 문제가 발생하였습니다!')

    print('===== 사이트 차단 정책 적용 완료 =====')
