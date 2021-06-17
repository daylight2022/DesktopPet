from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os


class Pet(object):
    def __init__(self, width=1400, height=800):
        self.image_url = 'images/meizi/meizi_'
        self.image_key = 1
        self.image = self.image_url + str(self.image_key) + '.png'
        self.rect_x = width
        self.rect_y = height

    def gif(self):
        if self.image_key < 61:
            self.image_key += 1
        else:
            self.image_key = 1
        self.image = self.image_url + str(self.image_key) + '.png'


class Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenu)

    def rightMenu(self):
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('images/net.png'), '浏览器', self, triggered=self.net))
        menu.addAction(QAction(QIcon('images/music.ico'), '网易云', self, triggered=self.music))
        menu.addAction(QAction(QIcon('images/eye.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('images/exit.png'), '退出', self, triggered=self.quit))
        menu.exec_(QCursor.pos())

    def quit(self):
        self.close()
        sys.exit()

    def hide(self):
        self.setVisible(False)

    @staticmethod
    def music():
        try:
            os.startfile(r'E:\Software\CloudMusic\cloudmusic.exe')
        except:
            print('路径不正确')

    @staticmethod
    def net():
        try:
            os.startfile(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
        except:
            print('路径不正确')


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.pet = Pet()
        self.is_follow_mouse = False
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet = Label(self)

        self.init_ui()
        self.tray()

        timer = QTimer(self)
        timer.timeout.connect(self.gem)
        timer.start(250)

    def gem(self):
        # 宠物实现gif效果
        self.pet.gif()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet.setPixmap(self.pm_pet)
        pass

    def init_ui(self):
        # 窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # 宠物标签
        self.lb_pet.setPixmap(self.pm_pet)
        self.lb_pet.move(self.pet.rect_x, self.pet.rect_y)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showMaximized()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True

            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.pet.rect_x = QCursor.pos().x() - 77
            self.pet.rect_y = QCursor.pos().y() - 63
            self.lb_pet.move(self.pet.rect_x, self.pet.rect_y)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def tray(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon('images/meizi/meizi_0.png'))

        display = QAction(QIcon('images/eye.png'), '显示', self, triggered=self.display)
        quit = QAction(QIcon('images/exit.png'), '退出', self, triggered=self.quit)
        menu = QMenu(self)
        menu.addAction(quit)
        menu.addAction(display)
        tray.setContextMenu(menu)
        tray.show()

    def quit(self):
        self.close()
        sys.exit()

    def hide(self):
        self.lb_pet.setVisible(False)

    def display(self):
        self.lb_pet.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())
