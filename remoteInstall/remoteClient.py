import fabric
import os

clientConfig = fabric.Config(overrides={'sudo': {'password': 'wjdqh'}})

clientList=[]
clientConnection = []
clientGroup=''

def genRangeIP():
    global clientList,clientConnection,clientGroup,clientConfig
    f = open('clientRange.txt','r', encoding='utf8')
    lines = f.readlines()
    f.close()
    
    for line in lines:
        line = line.strip()
        if line=='' or line=='\n' or line[0]=='#':
            pass
        else:
            ips = line.split('-')
            startIP = ips[0]
            prefix = startIP[:startIP.rfind('.')+1]
            start = int(startIP[startIP.rfind('.')+1:])
            end = int(ips[1])
            for x in range(start,end+1):
                ip = prefix+str(x)
                clientList.append(ip)
                try:
                    clientConnection.append(fabric.Connection(host=ip, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
                except:
                    print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -', ip)
            break

    clientGroup = fabric.ThreadingGroup.from_connections(clientConnection)
    print(clientList)
    
    
def genManualIP():
    global clientList,clientConnection,clientGroup,clientConfig
    f = open('clientList.txt','r', encoding='utf8')
    ips = f.readlines()
    f.close()

    for ip in ips:
        ip = ip.strip()
        if ip=='' or ip=='\n' or ip[0]=='#':
            pass
        else:
            clientList.append(ip)
            try:
                clientConnection.append(fabric.Connection(host=ip, user='ubuntu', port=22, connect_kwargs={'password': 'wjdqh'}, config=clientConfig))
            except:
                print('[Error] 클라이언트 연결중 오류가 발생하였습니다! -', ip)

    clientGroup = fabric.ThreadingGroup.from_connections(clientConnection)
    print(clientList)

def sudoAll(cmd):
    global clientList,clientConnection,clientGroup
    try:
        clientGroup.sudo(cmd, in_stream=False)
    except:
        print('[Error] 명령어 전송 중 문제가 발생하였습니다!')


def transferAll(filename):
    global clientList,clientConnection,clientGroup
    foldername = '/home/ubuntu/'
    try:
        clientGroup.put(filename, foldername)
    except:
        print('[Error] 파일 전송 중 오류가 발생하였습니다. -', filename)

######################################################################################################

print('########## CSL 우분투 클라이언트 설치 프로그램 ##########\n\n')
print('[중요] 교사용 CSL 매니저를 반드시 먼저 설치한 후 클라이언트를 설치하시기 바랍니다.')

while True:
    print('설치하기 전 학생용 PC의 IP를 셋팅해야 합니다.')
    print('실습실 IP가 연속적인 경우 clientRange.txt 파일을 열어 수정해야 하고,')
    print('실습실 IP가 연속적이지 않은 경우 clientList.txt 파일을 열어 수정해야 합니다.\n')
    q1 = input('이 두 파일 중 하나를 실습실 환경에 맞게 수정하셨나요? (y/n) ')
    if q1=='y' or q1=='Y':
        break
    else:
        print('해당 파일을 열어 수정하고 다시 시도하기 바랍니다.')
        exit()

while True:
    q2 = input('어떤 파일을 수정하셨나요?\n1. clientRange.txt\t2. clientList.txt\n1 또는 2를 입력하세요: ')
    if q2=='1':
        genRangeIP()
        break
    elif q2=='2':
        genManualIP()
        break
        

serverIP = input('\n서버 PC의 IP를 정확하게 입력해주세요: ')
serverPass = input('서버 PC의 Password를 정확하게 입력해주세요: ')

os.system('echo '+serverIP+'> server.ip')
os.system('echo '+serverPass+'>> server.ip')


print('##### 설치를 시작합니다. #####')

print('클라이언트로 파일 전송 중...')
transferAll('clientEnv.py')
transferAll('sendIP.py')
transferAll('server.ip')
transferAll('restart.sh')
transferAll('install-remote.sh')

print('클라이언트 설치 진행 중...')
sudoAll('bash install-remote.sh')

while True:
    q3=input('설치가 완료되었습니다.\n클라이언트를 모두 재부팅해야 정상 작동합니다.\n\n전원 재부팅 시킬까요? [y/n] ')
    if q3=='y' or q3=='Y':
        sudoAll('reboot')
        print('설치 프로그램을 종료합니다.\n교사용 바탕화면에서 CSL Manager를 실행하세요.')
        break

