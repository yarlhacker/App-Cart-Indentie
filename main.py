from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets 
from PyQt5.QtCore import * 
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys

from source.text import App




def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()