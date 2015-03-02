#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os.path
import sys
import re
import signal
import hashlib
import re
import urllib2
#import utils
from random import random
from time import sleep, time
from subprocess import Popen, PIPE, check_output
from threading import Thread
from Queue import Queue, Empty
from PySide import QtCore, QtGui


class AmountAdd(QtCore.QObject):
    sig = QtCore.Signal(int)


class KeyPressENG(QtCore.QObject):
    sig = QtCore.Signal(unicode)

class KeyPressRUS(QtCore.QObject):
    sig = QtCore.Signal(unicode)

class KeyBoardENG(QtGui.QPushButton):
    def __init__(self, char, value, sig, *args, **kwargs):
        super(KeyBoardENG, self).__init__(*args, **kwargs)
        self.char = char
        self.value = value
        self.signal = sig
        self.init_ui()
        self.init_style()
        self.init_action()

    def init_ui(self):
        self.setText(self.char)

    def init_style(self):
        self.setStyleSheet('QPushButton {'
            'font-size: 15pt;'
            'background: #318AEF;'
            'color: #ffffff;}')

    def init_action(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.signal.sig.emit(self.value)


class KeyBoardRUS(QtGui.QPushButton):
    def __init__(self, char, value, sig, *args, **kwargs):
        super(KeyBoardRUS, self).__init__(*args, **kwargs)
        self.char = char
        self.value = value
        self.signal = sig
        self.init_ui()
        self.init_style()
        self.init_action()

    def init_ui(self):
        self.setText(self.char)

    def init_style(self):
        self.setStyleSheet('QPushButton {'
            'font-size: 15pt;'
            'background: #318AEF;'
            'color: #ffffff;}')

    def init_action(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.signal.sig.emit(self.value)

class KeyBoardWidgetENG(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(KeyBoardWidgetENG, self).__init__(*args, **kwargs)
        self.signal = KeyPressENG()
        self.init_ui()

    def init_ui(self):
        self._layout = QtGui.QGridLayout()
        self._layout.setHorizontalSpacing(10)
        self._layout.setVerticalSpacing(10)
        self.setLayout(self._layout)

        keys = [
            [['Q', 'q'], ['W', 'w'], ['E', 'e'], ['R','r'], ['T','t'], ['Y','y'], ['U','u'], ['I','i'], ['O','o'], ['P','p']],
            [['A', 'a'], ['S', 's'], ['D', 'd'], ['F','f'], ['G','g'], ['H','h'], ['J','j'], ['K','k'], ['L','l'], ['-','-']],
            [['Z', 'z'], ['X', 'x'], ['C', 'c'], ['V','v'], ['B','b'], ['N','n'], ['M','m'], [',',','], ['!','!'], ['?','?']],
            [['Del', 'del'], ['Space ', ' '], ['Enter', 'enter']]
        ]

        for row, data in enumerate(keys):
            for col, el in enumerate(data):
                widget = KeyBoardENG(char=el[0], value=el[1],
                                      sig=self.signal)
                widget.setFocusPolicy(QtCore.Qt.NoFocus)
                self._layout.addWidget(widget, row, col, 1, 1)


class KeyBoardWidgetRUS(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(KeyBoardWidgetRUS, self).__init__(*args, **kwargs)
        self.signal = KeyPressRUS()
        self.init_ui()

    def init_ui(self):
        self._layout = QtGui.QGridLayout()
        self._layout.setHorizontalSpacing(10)
        self._layout.setVerticalSpacing(10)
        self.setLayout(self._layout)

        keys = [
            [[u'Й',u'й'], [u'Ц',u'ц'], [u'У',u'у'], [u'К',u'к'], [u'Е',u'е'], [u'Н',u'н'], [u'Г',u'г'], [u'Ш',u'ш'], [u'Щ',u'щ'], [u'З',u'з'], [u'Х',u'х'], [u'Ъ',u'ъ']],
            [[u'Ф',u'ф'], [u'Ы',u'ы'], [u'В',u'в'], [u'А',u'а'], [u'П',u'п'], [u'Р',u'р'], [u'О',u'о'], [u'Л',u'л'], [u'Д',u'д'], [u'Ж',u'ж'], [u'Э',u'э'], ['?','?']],
            [[u'Я',u'я'], [u'Ч',u'ч'], [u'С',u'с'], [u'М',u'м'], [u'И',u'и'], [u'Т',u'т'], [u'Ь',u'ь'], [u'Б',u'б'], [u'Ю',u'ю'], [',',','], ['!','!'], ['Del','del']],
            [[u'Пробел',' '], [u'Ввести','enter']]
        ]

        for row, data in enumerate(keys):
            for col, el in enumerate(data):
                widget = KeyBoardRUS(char=el[0], value=el[1],
                                      sig=self.signal)
                widget.setFocusPolicy(QtCore.Qt.NoFocus)
                self._layout.addWidget(widget, row, col, 1, 1)


class Manager(QtGui.QStackedWidget):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.screen = dict()
        self.init_ui()
        self.init_style()
        self.parent().manager = self

    def init_ui(self):
        self.screen.update(
            eng=engPage(main=self.parent(), manager=self),
            rus=rusPage(main=self.parent(), manager=self),
        )
        for key, widget in self.screen.iteritems():
            self.addWidget(widget)

        self.change_widget('rus')

    def change_widget(self, key):
        self.setCurrentWidget(self.screen[key])
        self.screen[key].on_show()

    def init_style(self):
        pass

class engPage(QtGui.QWidget):
    def __init__(self, main, manager, *args, **kwargs):
        super(engPage, self).__init__(*args, **kwargs)
        self.main = main
        self.manager = manager
        self.init_ui()
        self.init_style()
        self.init_action()

    def init_ui(self):
        self._layout = QtGui.QGridLayout()
        self.setLayout(self._layout)

        self.numpad = KeyBoardWidgetENG(parent=self)

        self.continue_label = QtGui.QLabel(parent=self)
        self.continue_label.setText(u'Для смены языка нажмите кнопку:')

        self.continue_button = QtGui.QPushButton(parent=self)
        self.continue_button.setText(u'Смена языка')
        self.continue_button.setFocusPolicy(QtCore.Qt.NoFocus)

        self._layout.addWidget(self.numpad, 2, 1, 5, 2,
                               alignment=QtCore.Qt.AlignCenter)
        self._layout.addWidget(self.continue_label, 7, 1, 1, 1)
        self._layout.addWidget(self.continue_button, 7, 2, 1, 1)

    def init_style(self):
        self.continue_label.setStyleSheet('QLabel {'
            'font-size: 15pt;'
            'color: #318AEF}')

        self.continue_button.setStyleSheet('QPushButton {'
            'font-size: 15pt;'
            'background: #318AEF;'
            'color: #ffffff;}')
    def init_action(self):
        #self.numpad.signal.sig.connect(self.on_keypress)
        self.continue_button.clicked.connect(self.on_continue)

    """def on_keypress(self, value): #Для обработки клавиш Поиска и удаления Анг
        if value == 'del':

        elif value == 'enter':

        self.update_phone()"""

    def on_continue(self):
        self.manager.change_widget('rus')

    def change_widget(self, key):
        self.setCurrentWidget(self.screen[key])
        self.screen[key].on_show()

    def on_show(self):
        pass

class rusPage(QtGui.QWidget):
    def __init__(self, main, manager, *args, **kwargs):
        super(rusPage, self).__init__(*args, **kwargs)
        self.main = main
        self.manager = manager
        self.init_ui()
        self.init_style()
        self.init_action()

    def init_ui(self):
        self._layout = QtGui.QGridLayout()
        self.setLayout(self._layout)

        self.numpad = KeyBoardWidgetRUS(parent=self)

        self.continue_label = QtGui.QLabel(parent=self)
        self.continue_label.setText(u'Для смены языка нажмите кнопку:')

        self.continue_button = QtGui.QPushButton(parent=self)
        self.continue_button.setText(u'Смена языка')
        self.continue_button.setFocusPolicy(QtCore.Qt.NoFocus)

        self._layout.addWidget(self.numpad, 2, 1, 5, 2,
                               alignment=QtCore.Qt.AlignCenter)
        self._layout.addWidget(self.continue_label, 7, 1, 1, 1)
        self._layout.addWidget(self.continue_button, 7, 2, 1, 1)

    def init_style(self):
        self.continue_label.setStyleSheet('QLabel {'
            'font-size: 15pt;'
            'color: #318AEF}')

        self.continue_button.setStyleSheet('QPushButton {'
            'font-size: 15pt;'
            'background: #318AEF;'
            'color: #ffffff;}')

    def init_action(self):
        #self.numpad.signal.sig.connect(self.on_keypress)
        self.continue_button.clicked.connect(self.on_continue)

    """def on_keypress(self, value):#Для обработки клавиш Поиска и удаления Рус
        if value == 'del':

        elif value == 'enter':

        self.update_phone()"""

    def on_continue(self):
        self.manager.change_widget('eng')

    def change_widget(self, key):
        self.setCurrentWidget(self.screen[key])
        self.screen[key].on_show()

    def on_show(self):
        pass


class Main(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        #self.load_ini()
        self.init_ui()
        self.init_style()

    def init_ui(self):
        self._layout = QtGui.QGridLayout()

        self.desktop = QtGui.QApplication.desktop()
        self._layout = QtGui.QGridLayout()
        self.setLayout(self._layout)

        self.manager = Manager(parent=self)
        self._layout.addWidget(self.manager, 0, 0)

        self.setWindowTitle('Keyboard')
        rect = self.desktop.availableGeometry()
        #self.setGeometry(0, 0, self.desktop.width(), self.desktop.height())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 900, 250)
        self.show()

    def init_style(self):
        self.setStyleSheet('QWidget {'
            'background: #ffffff;}')

    def init_action(self):
        self.numpad.signal.sig.connect(self.on_keypress)

    def on_keypress(self, value):
        if value == 'del':
            self.main.phone = self.main.phone[:-1]
        elif len(self.main.phone) < 10:
            self.main.phone += value
        self.update_phone()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Music Box')
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
