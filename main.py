# coding:utf-8
import sys

from ui import *
from enum import Enum

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import *


# 自定义图标
class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    GAME="game"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f'./resource/icons/{self.value}_{c}.svg'

# 窗口


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        # Dark 黑暗;White 浅色; AUTO自动
        setTheme(Theme.AUTO)

        print(dir(FIF))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = QStackedWidget(self)

        self.navigationInterface.setStyleSheet("""
        background-color: transparent;
        """)


        # create sub interface
        self.coreInterface = Widget('core Interface', self)
        self.homeInterface = Widget('home Interface', self)
        self.eventsInterface = Widget('Events Interface', self)
        self.playerInterface = Widget('player Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)

        self.homeInterface.setObjectName("home")  # 替换背景图片只对当前窗口生效 核心代码
        #self.homeInterface.setStyleSheet(
        #    "#home{border-image:url(resource/bg/1.png);}")  # 替换图片路径  核心代码

        self.stackWidget.addWidget(self.coreInterface)
        self.stackWidget.addWidget(self.homeInterface)
        self.stackWidget.addWidget(self.eventsInterface)
        self.stackWidget.addWidget(self.playerInterface)
        self.stackWidget.addWidget(self.folderInterface)
        self.stackWidget.addWidget(self.settingInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)

    def initNavigation(self):
        # icon=MyFluentIcon.HOME,
        self.navigationInterface.addItem(
            routeKey=self.homeInterface.objectName(),
            icon=FIF.HOME,
            text='Home',
            onClick=lambda: self.switchTo(self.homeInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.coreInterface.objectName(),
            icon=MyFluentIcon.GAME,
            text='Versions',
            onClick=lambda: self.switchTo(self.coreInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.eventsInterface.objectName(),
            icon=FIF.INFO,
            text='Events',
            onClick=lambda: self.switchTo(self.eventsInterface)
        )
        self.navigationInterface.addItem(
            routeKey=self.playerInterface.objectName(),
            icon=FIF.MUSIC,
            text='Player',
            onClick=lambda: self.switchTo(self.playerInterface)
        )
        self.navigationInterface.addSeparator()

        # add navigation items to scroll area
        self.navigationInterface.addItem(
            routeKey=self.folderInterface.objectName(),
            icon=FIF.FOLDER,
            text='Folder library',
            onClick=lambda: self.switchTo(self.folderInterface),
            position=NavigationItemPostion.SCROLL
        )
        # for i in range(1, 21):
        #     self.navigationInterface.addItem(
        #         f'folder{i}',
        #         FIF.FOLDER,
        #         f'Folder {i}',
        #         lambda: print('Folder clicked'),
        #         position=NavigationItemPostion.SCROLL
        #     )

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPostion.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text='Settings',
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPostion.BOTTOM
        )

        #!IMPORTANT: don't forget set the default route key
        self.navigationInterface.setDefaultRouteKey(
            self.homeInterface.objectName())

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()

        self.resize(w//2+40, h//2)
        self.setWindowIcon(QIcon('resource/logo/logob.png'))
        self.setWindowTitle('Windy Meta Launcher')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            'This is a help message',
            'You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉',
            self
        )
        w.exec()

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
