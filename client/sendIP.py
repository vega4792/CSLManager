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

myPC = fabric.Connection(host=localIP, user=userName, port=portNum,  connect_kwargs={'password': localPass})
serverPC = fabric.Connection(host=serverIP, user=userName, port=portNum,  connect_kwargs={'password': serverPass})

createDirectory(env_folder)
createDirectory(task_folder)

try:
	myPC.run('rm '+env_folder+'*.ip')
except:
    pass

while True:
	try:
		result=myPC.run('hostname -I')
		localIP = result.stdout.strip()
		myPC.run('echo '+localIP+' > '+env_folder+localIP+'.ip')
		serverPC.put(env_folder+localIP+'.ip', '/home/ubuntu/student')
	except:
		pass

	time.sleep(delayTime)
