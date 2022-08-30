#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from qtUI.MainWindow_UI import Ui_MainWindow
from Sub_UI_Main import Sub_UI_Main
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QDate, Qt
from BilibiliDan import BilibiliDan
from GlobalVar import GlobalVar
import os
import sys


class UI_Main(Ui_MainWindow, QtWidgets.QMainWindow):
    send_msg = pyqtSignal(str, dict)
    send_msg2 = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(UI_Main, self).__init__(parent)
        self.globalVar = GlobalVar()
        self.setupUi(self)

    def setupFunction(self):
        # 主窗口
        self.pushButton.clicked.connect(self.sendDirectChoice)
        self.pushButton_2.clicked.connect(self.setQueryDate)
        self.pushButton_3.clicked.connect(self.downloadWordCloud)
        self.pushButton_4.clicked.connect(self.exportAsExcel)

    # 调用爬取处理弹幕数据的函数
    def callBilibiliDan(self, url, meta):
        self.bilibiliDan = BilibiliDan(url, meta)
        self.bilibiliDan.getVideoCid()
        self.bilibiliDan.start()

    # 直接获取
    def sendDirectChoice(self):
        self.globalVar.PATTERN = "direct"
        url = self.lineEdit.text()
        if (url == ""):
            self.msg("警告", "请输入目标地址")
        else:
            try:
                meta = {}
                meta["pattern"] = "direct"
                self.callBilibiliDan(url, meta)
                # self.globalVar.PATTERN = ""
                self.msg("消息", "爬取完成")
            except Exception as e:
                self.msg("消息", "爬取失败")
                print(f'Cause:{e}')

    # 调出设置日期的对话窗口
    def setQueryDate(self):
        self.globalVar.PATTERN = "date"
        # 实例化子窗口
        self.url = self.lineEdit.text()
        self.cookie = self.textEdit.toPlainText()
        if self.url == "":
            self.msg("警告", "请输入目标地址")
        if self.cookie == "":
            self.msg("警告", "请输入cookie")
        else:
            self.dialog = Sub_UI_Main()
            # 将signal与目标方的函数相连接，若无，是发给sys
            self.dialog.send_msg.connect(self.getDanByDate)
            self.dialog.show()

    # 根据日历获取
    def getDanByDate(self,startDate,endDate):
        try:
            meta = {}
            meta["pattern"] = "date"
            meta["startDate"] = startDate
            meta["endDate"] = endDate
            meta["cookie"] = self.cookie
            self.callBilibiliDan(self.url, meta)
            # self.globalVar.PATTERN = ""
            self.msg("消息", "按日期爬取完成")
            self.dialog.close()
        except Exception as e:
            self.msg("消息", "爬取失败")
            print(f'Cause:{e}')


    def downloadWordCloud(self):
        if self.globalVar.PATTERN == "":
            self.msg("警告", "请选择查询模式")
        else:
            try:
                file_path, file_type = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(), "图像文件(*.jpg)")
                if self.globalVar.PATTERN == "direct":
                    dan_list = self.bilibiliDan.DIRECT_DAN_LIST
                    self.bilibiliDan.generateWordCloud(file_path, dan_list)
                elif self.globalVar.PATTERN == "date":
                    dan_date_dict = self.bilibiliDan.DAN_DATE_DICT
                    dan_list = []
                    for key, value in dan_date_dict.items():
                        dan_list = list(map(lambda x:x,value))
                    self.bilibiliDan.generateWordCloud(file_path, dan_list)
                self.msg("消息", "下载成功")
            except Exception as e:
                self.msg("消息", "下载失败")
                print(f'Cause:{e}')

    def exportAsExcel(self):
        if self.globalVar.PATTERN == "":
            self.msg("警告", "请选择查询模式")
        else:
            try:
                if self.globalVar.PATTERN == "direct":
                    file_path, file_type = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", os.getcwd(),
                                                                                 "Excel文件(*.xlsx)")
                    dan_list = self.bilibiliDan.DIRECT_DAN_LIST
                    self.bilibiliDan.exportExcel(file_path, dan_list)
                elif self.globalVar.PATTERN == "date":
                    folder = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
                    dan_date_dict = self.bilibiliDan.DAN_DATE_DICT
                    # print(dan_date_dict)
                    for key, value in dan_date_dict.items():
                        # print()
                        file_path = folder + "\\" + key + ".xlsx"

                        self.bilibiliDan.exportExcel(file_path, value)
                self.msg("消息", "导出成功")
            except Exception as e:
                self.msg("消息", "导出失败")
                print(f'Cause:{e}')

    def msg(self, title, msg):
        QtWidgets.QMessageBox.information(self, title, msg, QtWidgets.QMessageBox.Yes)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_Main()
    ui.setupFunction()
    # ui.handleDisplay("如果你不知道该如何使用本软件，请点击“使用说明”按钮查看帮助")
    ui.show()
    sys.exit(app.exec_())
