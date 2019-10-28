from tkinter import *
import os
import cv2
import sys
import PIL.Image, PIL.ImageTk
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton # 설치 : pip3 install PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication # quit 버튼 만들기 위한 import
 
creds = 'DB.temp' # temp파일을 받아옴

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # 비디오 열기 // 디폴트 값은 노트북 웹캠
        self.vid = MyVideoCapture(self.video_source)

        # 캔버스를 만들고, 그걸 비디오 소스 사이즈에 맞춤
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # 스냅샷 기능
        self.btn_snapshot=tkinter.Button(window, text="캡쳐하기", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # 한 번 호출 된 후 update 메소드는 지연 시간 (밀리 초)마다 자동으로 호출
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # 비디오 소스로 부터 프레임 받아옴
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # 비디오 소스로부터 프레임 받아옴
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # 비디오 열기
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # 가로 세로를 비디오로부터 가져옴
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # bool 성공 플래그와 현재 프레임을 BGR로 변환하여 반환
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # 객체 끝나면 비디오소스 해제
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def Signup(): # 회원가입
    global pwordE # 사용할 전역 변수 선언
    global nameE
    global roots
 
    roots = Tk() # 빈 창
    roots.title('회원가입') # 빈 창을 회원가입으로
    intruction = Label(roots, text='어서오세요, 헬창어플입니다. \n') # 인사말 정도
    intruction.grid(row=0, column=0, sticky=E) # grid 만들어서 사용
 
    nameL = Label(roots, text='이름 : ') 
    pwordL = Label(roots, text='비밀번호 : ') 
    nameL.grid(row=1, column=0, sticky=W) # 위치 지정
    pwordL.grid(row=2, column=0, sticky=W) # 그리드로 위치 지정
 
    nameE = Entry(roots) # 텍스트 상자를 입력 대기 상태로
    pwordE = Entry(roots, show='*') # 이것도 입력 대기 상태로 만들고, 비번이니까 별표처리해줌
    nameE.grid(row=1, column=1) 
    pwordE.grid(row=2, column=1)
 
    signupButton = Button(roots, text='회원가입', command=FSSignup) # 회원가입 버튼 만듦, 이거 누르면 FSSignup으로 감
    signupButton.grid(columnspan=2, sticky=W)

    QuitButton = Button(roots, text='나가기', command=close_window) # 회원가입 버튼 만듦, 이거 누르면 FSSignup으로 감
    QuitButton.grid(columnspan=1, column=2, sticky=W)

    roots.mainloop() # 윈도우창이 계속 켜지도록 만듦 
 
def close_window(): # quit버튼
    roots.destroy()

def FSSignup():
    with open(creds, 'w') as f: # 맨 위에 만든 변수를 이용해서 문서 만듦
        f.write(nameE.get()) # nameE는 입력을 저장한 변수, .get은 Tkinter를 사용해서 문자열을 얻는다
        f.write('\n')
        f.write(pwordE.get())
        f.close() # Closes the file
 
    roots.destroy() # 회원가입창 끝낼것
    Login() # 이걸 로그인 def에 옮김
 
def Login():
    global nameEL
    global pwordEL # 하나 더 선언
    global rootA
 
    rootA = Tk() # 새 창
    rootA.title('로그인') # 타이틀
 
    intruction = Label(rootA, text='로그인을 해주세요.\n') # 디테일 설명
    intruction.grid(sticky=E) # Blahdy Blah
 
    nameL = Label(rootA, text='이름 : ') 
    pwordL = Label(rootA, text='비밀번호 : ') 
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)
 
    nameEL = Entry(rootA) # 빈
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)
 
    loginB = Button(rootA, text='Login', command=CheckLogin) # 로그인버튼만들고 CheckLogin으로 이동
    loginB.grid(columnspan=2, sticky=W)
 
    rmuser = Button(rootA, text='회원 삭제', fg='red', command=DelUser) # 빨간색으로 회원삭제 만들고 DelUser로 이동
    rmuser.grid(columnspan=2, sticky=W)
    rootA.mainloop()
 
def CheckLogin():
    with open(creds) as f:
        data = f.readlines() # 정보를 넣은 전체 문서를 가져 와서 데이터 변수에 넣음
        uname = data[0].rstrip() # Data[0], 0은 첫줄
        pword = data[1].rstrip() # rstrip을 쓰는 이유는 뒤에 개행없앨라고
 
    if nameEL.get() == uname and pwordEL.get() == pword: # 올바른 정보인지 확인하는 작업
        r = Tk() # 새 창
        r.title('헬창인생 (로그인성공 버전)')
        r.geometry("400x200")
        intruction = Label(r, text='어서오세요 ,'+uname+'님.\n') # 인사해주고
        intruction.grid(sticky=E)

        loginB = Button(r, text='비디오 test', command=App) # 비디오 test 중
        loginB.grid(columnspan=2, sticky=W)
    
        r.mainloop()
    else:
        r = Tk()
        r.title('D:')
        r.geometry('150x50')
        rlbl = Label(r, text='\n[!] 잘못된 회원 정보입니다.')
        rlbl.pack()
        r.mainloop()
 
def DelUser():
    os.remove(creds) # 파일삭제
    rootA.destroy() # 로그인창 끔
    Signup() # 다시 돌아가게함
 
if os.path.isfile(creds):
    Login()
else: # if else 문은 파일이 존재하는지 확인. 로그인으로 갈지, 가입갈지 정함
    Signup()