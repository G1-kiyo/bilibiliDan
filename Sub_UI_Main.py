#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from qtUI.Dialog_UI import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal,QDate,Qt
from BilibiliDan import BilibiliDan
from GlobalVar import GlobalVar


class Sub_UI_Main(Ui_Dialog,QtWidgets.QDialog):
    send_msg = pyqtSignal(str,str)
    def __init__(self,parent=None):
        super(Sub_UI_Main, self).__init__(parent)
        self.globalVar = GlobalVar()
        self.setupUi(self)
        self.setupFunction()

    def setupFunction(self):
        # 对话窗口
        self.buttonBox.accepted.connect(self.setInfo)
        self.buttonBox.rejected.connect(QtWidgets.QDialog.close)
        self.calendarWidget.clicked['QDate'].connect(self.dateEdit.setDate)
        self.calendarWidget.clicked['QDate'].connect(self.dateEdit_2.setDate)


    def setInfo(self):
        try:
            startDate = self.dateEdit.date()
            endDate = self.dateEdit_2.date()
            now = QDate.currentDate()
            if (startDate.daysTo(now) < endDate.daysTo(now)):
                self.msg("警告", "结束日期不能早于开始日期")
            else:
                self.send_msg.emit(startDate.toString(Qt.ISODate), endDate.toString(Qt.ISODate))
        except Exception as e:
            print(f'Cause:{e}')
    # 调用爬取处理弹幕数据的函数
    def callBilibiliDan(self,url,meta):
        self.bilibiliDan = BilibiliDan(url,meta)
        self.bilibiliDan.getVideoCid()
        self.bilibiliDan.start()


    def msg(self, title, msg):
        QtWidgets.QMessageBox.information(self, title, msg, QtWidgets.QMessageBox.Yes)