import fabric
from clientEnv import *
import time
import os

def createDirectory(folder):
    try:
        if not os.path.exists(folder):
            os.umask(0)
            os.makedirs(folder,0o777)
    except OSError:
        print('[Error] 디렉토리 생성에 실패하였습니다! - ',folder)

createDirectory(env_folder)
createDirectory(task_folder)

f=open('/etc/ubuntu/server.ip','r')
serverIP = f.readline().strip()
serverPass = f.readline().strip()
f.close()

myPC = fabric.Connection(host=localIP, user=userName, port=portNum,  connect_kwargs={'password': localPass})
serverPC = fabric.Connection(host=serverIP, user=userName, port=portNum,  connect_kwargs={'password': serverPass})


try:
	myPC.run('rm '+env_folder+'*.ip')
except:
    pass

while True:
	try:
		result=myPC.run('hostname -I')
		myIP = result.stdout.strip().split(' ')
		myPC.run('echo '+myIP[0]+' > '+env_folder+myIP[0]+'.ip')
		serverPC.put(env_folder+myIP[0]+'.ip', '/home/ubuntu/student')
	except:
		pass

	time.sleep(delayTime)
