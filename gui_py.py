import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton # 설치 : pip3 install PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication # quit 버튼 만들기 위한 import

class MyApp(QWidget):

    def __init__(self): # self는 MyApp 객체
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle('정태이') # setWindowTitle() 메서드는 타이틀바에 나타나는 창의 제목을 설정
        self.setWindowIcon(QIcon('정태이.png')) # QIcon 객체 생성 -> QIcon에 보여질 이미지를 입력// 경로입력가능
        self.setGeometry(300,300,300,200) #앞의 두 매개변수는 창의 x, y 위치를 결정하고, 뒤의 두 매개변수는 각각 창의 너비와 높이를 결정

        #self.move(300, 300) # move() 메서드는 위젯을 스크린의 x=300px, y=300px의 위치로 이동
        #self.resize(400, 200) # 메서드는 위젯의 크기를 너비 400px, 높이 200px로 조절
      #  self.show() # show() 메서드는 위젯을 스크린에

        btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__': # '__name__'은 현재 모듈의 이름이 저장되는 내장 변수

    app = QApplication(sys.argv) # 모든 PyQt5 어플리케이션은 어플리케이션 객체를 생성
    ex = MyApp()
    sys.exit(app.exec_())