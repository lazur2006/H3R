import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.pyqtSignal()

class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(30, 30, 30, 120)
        self.penColor = QtGui.QColor("#333333")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)

        self.SIGNALS = TranslucentWidgetSignals()

    def resizeEvent(self, event):
        s = self.size()
        popup_width = 300
        popup_height = 120
        ow = int(s.width() / 2 - popup_width / 2)
        oh = int(s.height() / 2 - popup_height / 2)

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, s.width(), s.height())

        # drawpopup
        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)
        popup_width = 300
        popup_height = 120
        ow = int(s.width()/2-popup_width/2)
        oh = int(s.height()/2-popup_height/2)
        qp.drawRoundedRect(ow, oh, popup_width, popup_height, 5, 5)

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QtGui.QColor(70, 70, 70))
        tolw, tolh = 80, -5
        qp.drawText(ow + int(popup_width/2) - tolw, oh + int(popup_height/2) - tolh, "Wait ...")

        qp.end()

    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()
