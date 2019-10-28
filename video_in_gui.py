import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

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

# 윈도운창 만들고 앱 객체로 전달
App(tkinter.Tk(), "헬창인생")