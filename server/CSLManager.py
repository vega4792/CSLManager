from tkinter import *
from tkinter import filedialog
import fabFunction as ff
import os

root = Tk()
root.title('CSL Manager for Ubuntu Ver.0.8')
root.geometry('550x480')
root.resizable(False, False)

def checkClientFunc():
    ff.checkIP()

    label2 = Label(root,text='총 '+str(len(ff.clientList))+'명 접속 중')
    label2.place(x=350, y=10)

    listbox1.delete(first=0, last=END)
    for idx,client in enumerate(ff.clientList):
        listbox1.insert(idx, client)

btn1 = Button(root,  padx=5, pady=5,text='세션초기화',command=ff.resetClient)
btn1.place(x=10, y=10)

btn2 = Button(root, padx=5, pady=5,text='접속확인',command=checkClientFunc)
btn2.place(x=110, y=10)

btn3 = Button(root, padx=5, pady=5, text='현재 상태를 백업',command=ff.backupAll)
btn3.place(x=10, y=50)

btn4 = Button(root, padx=5, pady=5, text='저장된 상태로 복구',command=ff.restoreAll)
btn4.place(x=140, y=50)

listbox1 = Listbox(root, selectmode='extended', height=0)
listbox1.place(x=370,y=40)


############### remote command
label1 = Label(root,text='원격 명령:')
label1.place(x=10, y=90)

entry1 = Entry(root,width=25)
entry1.place(x=70, y=90)

def btnRunFunc():
    cmd = entry1.get()
    print('run:',cmd)
    ff.runAll(cmd)
    entry1.delete(0,END)

def btnSudoFunc():
    cmd = entry1.get()
    print('sudo:', cmd)
    ff.sudoAll(cmd)
    entry1.delete(0,END)

btnRun = Button(root,text='실행', command=btnRunFunc)
btnRun.place(x=290, y=90)

btnSudo = Button(root,text='sudo', command=btnSudoFunc)
btnSudo.place(x=290, y=60)
############################################ end of area


########### file transfer
label2 = Label(root,text='파일 전송:')
label2.place(x=10, y=140)

entry2 = Entry(root, width=25)
entry2.place(x=70, y=140)

filename=''

def selectFileFunc():
    global filename
    filename = filedialog.askopenfilename(initialdir='/home/ubuntu/', title='파일 선택')
    print(filename)
    entry2.delete(0,END)
    entry2.insert(0,filename)

def transferSelFunc():
    global filename
    for ip in listbox1.curselection():
        idx = ff.clientList.index(listbox1.get(ip))
        ff.transferSel(filename, ff.clientConnection[idx])

def transferAllFunc():
    global filename
    ff.transferAll(filename)

btnFile = Button(root,text='파일 선택', command=selectFileFunc)
btnFile.place(x=290, y=140)

btnSelTrans = Button(root,text='선택 전송', command=transferSelFunc)
btnSelTrans.place(x=100, y=170)

btnAllTrans = Button(root,text='모두 전송', command=transferAllFunc)
btnAllTrans.place(x=200, y=170)
############################################ end of area

############################################ get file
def getFileSelFunc():
    for ip in listbox1.curselection():
        idx = ff.clientList.index(listbox1.get(ip))
        ff.getFileSel(ff.clientList[ip], ff.clientConnection[idx])

label3 = Label(root,text='과제 회수:')
label3.place(x=10, y=220)

btnGetSel = Button(root,text='선택 회수', command=getFileSelFunc)
btnGetSel.place(x=100, y=220)

btnGetAll = Button(root,text='모두 회수', command=ff.getFileAll)
btnGetAll.place(x=200, y=220)
############################################ end of area


############## 사이트 차단 정책 추가
label4 = Label(root,text='사이트 차단:')
label4.place(x=10, y=270)

def siteListFunc():
    os.system('gedit /home/ubuntu/CSLManager/sitelist.txt')

btnSiteList = Button(root,text='목록 열기', command=siteListFunc)
btnSiteList.place(x=100, y=270)

btnSiteRule = Button(root,text='차단 실행', command=ff.runSiteRule)
btnSiteRule.place(x=200, y=270)
############################################ end of area

#ff.createDirectory('/home/ubuntu/student/')
#ff.createDirectory('/home/ubuntu/Desktop/과제제출/')
checkClientFunc()
root.mainloop()
