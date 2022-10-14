# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore, QtWidgets


from ui_mainWindow import Ui_MainWindow
from ui_add import Ui_Form_Add
from ui_about import Ui_Dialog_About
from ui_help import Ui_Form_Help
from ui_modify import Ui_Form_Modify
from ui_deleteByName import Ui_Form_DeleteByName
from ui_deleteByNumber import Ui_Form_DeleteByNumber
from ui_deleteSelection import Ui_Form_DeleteSelection
from ui_quiry import Ui_Form_Quiry
from ui_quiryShow import Ui_Form_QuiryShow

import os, sys, time




# 信息存储，一个学生的5条信息存储在下面5个list里，下标一致
names=[]
numbers=[]
ages=[]
professions=[]
classes=[]




# 由于其他文件是qt .ui文件自动转换来的，编写上层功能需要整合一下
class merge():
    global names, numbers, ages, professions, classes

    #----------------------类内部用到的变量-------------------------------
    openFileName=''         #读取学生信息文件时的路径（可由explorer.exe选择）
    saveFileName=''         #写入学生信息至文件时的路径（可由explorer.exe选择）

    globalIndex=[]          #将类内的index转至类外的index
    multiNamesList=[]       #由同名学生时供选择用
    listModel=None          #Qt listModel

    savedFlag=False         #推出前判断是否保存文件用
    modifiedFlag=False


    #----------------------------Start-----------------------------
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)     #高分屏支持
    app=QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.jpg"))            #设置程序图标

    # 主窗口
    mainWindow=QMainWindow()
    mainWindowUi=Ui_MainWindow()
    mainWindow_StatusBar_Label_Time=QLabel()
    mainWindow_StatusBar_Label_Time.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

    mainWindow_StatusBar_Label_Message=QLabel()
    mainWindow_StatusBar_Label_Message.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
    mainWindow_StatusBar_Label_Message.setText("No local file opened")

    mainWindow_StatusBar_Label_Count=QLabel()
    mainWindow_StatusBar_Label_Count.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

    mainWindowUi.setupUi(mainWindow)

    mainWindowUi.statusbar.addWidget(mainWindow_StatusBar_Label_Time)           #底部时间栏
    mainWindowUi.statusbar.addWidget(mainWindow_StatusBar_Label_Message)        #底部消息栏（显示打开/保存路径）
    mainWindowUi.statusbar.addWidget(mainWindow_StatusBar_Label_Count)          #底部学生信息条数统计

    mainWindowTimer=QTimer()                            #更新mainWindow底部时间信息，一秒一更新
    mainWindowTimer.start(1000)

    # 添加学生信息 窗口
    addWidget=QWidget()
    addWidgetUi=Ui_Form_Add()
    addWidgetUi.setupUi(addWidget)

    # 修改学生信息 窗口
    modifyWidget=QWidget()
    modifyWidgetUi=Ui_Form_Modify()
    modifyWidgetUi.setupUi(modifyWidget)

    # 选择删除方式 窗口
    deleteSelectionWidget=QWidget()
    deleteSelectionWidgetUi=Ui_Form_DeleteSelection()
    deleteSelectionWidgetUi.setupUi(deleteSelectionWidget)

    # 选择查询方式 窗口
    quiryWidget=QWidget()
    quiryWidgetUi=Ui_Form_Quiry()
    quiryWidgetUi.setupUi(quiryWidget)

    # 查询结果 窗口
    quiryShowWidget=QWidget()
    quiryShowWidgetUi=Ui_Form_QuiryShow()
    quiryShowWidgetUi.setupUi(quiryShowWidget)

    # 以名字删除 窗口
    deleteByNameWidget=QWidget()
    deleteByNameWidgetUi=Ui_Form_DeleteByName()
    deleteByNameWidgetUi.setupUi(deleteByNameWidget)

    # 以学号删除 窗口
    deleteByNumberWidget=QWidget()
    deleteByNumberWidgetUi=Ui_Form_DeleteByNumber()
    deleteByNumberWidgetUi.setupUi(deleteByNumberWidget)
    
    # 关于 窗口
    aboutDialog=QDialog()
    aboutDialogUi=Ui_Dialog_About()
    aboutDialogUi.setupUi(aboutDialog)

    # 帮助信息 窗口
    helpWidget=QWidget()
    helpWidgetUi=Ui_Form_Help()
    helpWidgetUi.setupUi(helpWidget)

    # 文件选择 窗口
    fileExplorer=QFileDialog()


    def saveToFile(self, path:str):
        try:
            fp=open(path, 'w')
        except:
            QMessageBox.information(self.mainWindow, "错误", "打开文件失败", QMessageBox.Yes)
            return
        else:
            for i in range(len(names)):
                fp.write(f'{names[i]},{numbers[i]},{classes[i]},{professions[i]},{ages[i]},\n')
            fp.close()
            self.savedFlag=True

    def readFromFile(self, path:str):
        if not os.path.exists(path):
            QMessageBox.information(self.mainWindow, "文件不存在", "输入文件不存在", QMessageBox.Yes)
            return

        try:
            fp=open(path, 'r')
        except:
            QMessageBox.information(self.mainWindow, "错误", "打开文件失败", QMessageBox.Yes)
            return
        else:
            # 输入文件解析
            while True:
                data=fp.readline()
                if data=='':
                    break
                elif data=='\n':
                    continue
                data=data[:-1]          #去除末尾的\n

                p=0
                last_p=0
                while data[p]!=',':
                    p+=1
                tmp_name=data[last_p:p]
                
                p+=1
                last_p=p
                while data[p]!=',':
                    p+=1
                tmp_number=data[last_p:p]

                p+=1
                last_p=p
                while data[p]!=',':
                    p+=1
                tmp_class=data[last_p:p]

                p+=1
                last_p=p
                while data[p]!=',':
                    p+=1
                tmp_profession=data[last_p:p]

                p+=1
                last_p=p
                while data[p]!=',':
                    p+=1
                tmp_age=data[last_p:p]

                if (tmp_number not in numbers) and (tmp_name not in names) and \
                    (tmp_class not in classes) and (tmp_profession not in professions)\
                     and (tmp_age not in ages):
                    numbers.append(tmp_number)
                    names.append(tmp_name)
                    classes.append(tmp_class)
                    professions.append(tmp_profession)
                    ages.append(tmp_age)
                else:
                    QMessageBox.information(self.mainWindow, "错误", "数据文件疑似损坏", QMessageBox.Yes)
                    fp.close()
                    names.clear()
                    numbers.clear()
                    classes.clear()
                    professions.clear()
                    ages.clear()
                    self.callback_mainWindowStatusBarCounterUpdate()
                    return
            self.callback_mainWindowStatusBarCounterUpdate()
            fp.close()


    # 获得一个名字在数据库中出现了多少次
    def getNameCount(self, _name:str):
        tmp_cnt=0
        for i in names:
            if i==_name:
                tmp_cnt+=1
        return tmp_cnt


    # 返回一条学生信息字符串（一行）
    def generatePieceOfInformation_List(self, index:int):
        return f'学号:{numbers[index]} 姓名:{names[index]} 班级:{classes[index]} 专业:{professions[index]} 年龄:{ages[index]}'

    # 返回一条学生信息字符串（多行）
    def generatePieceOfInformation_Dialog(self, index:int):
        tmp=f'\
姓名：{names[index]}\n\
学号：{numbers[index]}\n\
年龄：{ages[index]}\n\
专业：{professions[index]}\n\
班级：{classes[index]}\n'
        return tmp


    def addStudentInfo(self, _name:str, _number:str, _age:str, _profession:str, _class:str):
        names.append(_name)
        numbers.append(_number)
        ages.append(_age)
        professions.append(_profession)
        classes.append(_class)
        self.modifiedFlag=True
        self.callback_mainWindowStatusBarCounterUpdate()


    def deleteStudentInfoByName(self, name:str):
        if name in names:
            tmp_index=names.index(name)
            del names[tmp_index]
            del numbers[tmp_index]
            del ages[tmp_index]
            del professions[tmp_index]
            del classes[tmp_index]
            self.modifiedFlag=True
            self.callback_mainWindowStatusBarCounterUpdate()
    

    def deleteStudentInfoByNumber(self, number:str):
        if number in numbers:
            tmp_index=numbers.index(number)
            del names[tmp_index]
            del numbers[tmp_index]
            del ages[tmp_index]
            del professions[tmp_index]
            del classes[tmp_index]
            self.modifiedFlag=True
            self.callback_mainWindowStatusBarCounterUpdate()


    # callback_xxx系列函数说明：某事件触发后的回调函数
    # mainWindow定时器时间到
    def callback_mainWindowTimer(self):
        self.mainWindow_StatusBar_Label_Time.setText(time.strftime("%Y-%m-%d %H:%M:%S %A", time.localtime()))


    # 更新mainWindow状态栏统计信息
    def callback_mainWindowStatusBarCounterUpdate(self):
        self.mainWindow_StatusBar_Label_Count.setText(f'当前有{len(names)}条信息')


    # 添加学生窗口 添加按钮被点击
    def callback_addStudentInfo(self):
        rejectToInputTitle="拒绝录入"
        allowed_age_min=17
        allowed_age_max=25

        # Qt文本框html内容转纯文本
        tmp_name=self.addWidgetUi.textEdit_Add_Name.toPlainText()
        tmp_number=self.addWidgetUi.textEdit_Add_Number.toPlainText()
        tmp_age=self.addWidgetUi.textEdit_Add_Age.toPlainText()
        tmp_profession=self.addWidgetUi.textEdit_Add_Profession.toPlainText()
        tmp_class=self.addWidgetUi.textEdit_Add_Class.toPlainText()

        # 正确性检验
        if tmp_name=='' or tmp_number=='' or tmp_age=='' or tmp_profession=='' or tmp_class=='':
            QMessageBox.information(self.addWidget, rejectToInputTitle, "输入信息不能为空", QMessageBox.Yes)
            return

        if not(tmp_number.isdigit() and len(tmp_number)==6):
            QMessageBox.information(self.addWidget, rejectToInputTitle, "学号必须为6位数字", QMessageBox.Yes)
            return
            
        if tmp_number in numbers:
            QMessageBox.information(self.addWidget, rejectToInputTitle, "该学号已存在", QMessageBox.Yes)
            return
        
        if not(tmp_age.isdigit()):
            QMessageBox.information(self.addWidget, rejectToInputTitle, "年龄必须为纯数字", QMessageBox.Yes)
            return
        
        tmp_age_int=int(tmp_age)
        if tmp_age_int<allowed_age_min or tmp_age_int>allowed_age_max:
            QMessageBox.information(self.addWidget, rejectToInputTitle, "年龄必须在17至25岁之间", QMessageBox.Yes)
            return

        self.addStudentInfo(tmp_name, tmp_number, tmp_age, tmp_profession, tmp_class)


    # 根据名字删除学生信息（如果没有同名学生），或弹出提示要求从多个同名学生中选择并删除
    def callback_deleteByNameRequest(self):
        rejectToInputTitle="拒绝删除"
        tmp_name=self.deleteByNameWidgetUi.textEdit.toPlainText()

        if tmp_name=='':
            QMessageBox.information(self.deleteByNameWidget, rejectToInputTitle, "姓名不能为空", QMessageBox.Yes)
            return

        if tmp_name not in names:
            QMessageBox.information(self.deleteByNameWidget, rejectToInputTitle, "姓名不存在", QMessageBox.Yes)
            return
        
        tmp_cnt=self.getNameCount(tmp_name)

        if tmp_cnt==1:
            tmp_index=names.index(tmp_name)
            tmp_info=self.generatePieceOfInformation_Dialog(tmp_index)

            if QMessageBox.question(self.deleteByNameWidget, "确认删除", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
                self.deleteStudentInfoByName(tmp_name)
        else:
            QMessageBox.information(self.deleteByNameWidget, "有同名学生存在", "有同名学生存在，请在下方双击选择要删除的学生")

            self.globalIndex=[]
            self.multiNamesList=[]
            for i in range(len(names)):
                if names[i]==tmp_name:
                    self.globalIndex.append(i)
                    self.multiNamesList.append(f'{names[i]}\t{numbers[i]}\t{ages[i]}')

            self.listModel=QStringListModel()
            self.listModel.setStringList(self.multiNamesList)
            self.deleteByNameWidgetUi.listView.setModel(self.listModel)
            self.deleteByNameWidgetUi.listView.setEditTrigers(QAbstractItemView.EditTrigger.NoEditTriggers)


    # 从多条学生信息中选择并删除
    def callback_deleteByMultipleNameRequest(self, modelIndex:QModelIndex):
        tmp_index=self.globalIndex[modelIndex.row()]
        tmp_info=self.generatePieceOfInformation_Dialog(tmp_index)

        if QMessageBox.question(self.deleteByNameWidget, "确认删除", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
            self.listModel.removeRow(modelIndex.row())
            self.deleteStudentInfoByNumber(numbers[tmp_index])


    # 根据学号删除学生信息
    def callback_deleteByNumberRequest(self):
        rejectToInputTitle="拒绝删除"
        tmp_number=self.deleteByNumberWidgetUi.textEdit.toPlainText()
        
        if not(tmp_number.isdigit() and len(tmp_number)==6):
            QMessageBox.information(self.deleteByNumberWidget, rejectToInputTitle, "学号必须为6位数字", QMessageBox.Yes)
            return

        if tmp_number not in numbers:
            QMessageBox.information(self.deleteByNumberWidget, rejectToInputTitle, "学号不存在", QMessageBox.Yes)
            return

        tmp_index=numbers.index(tmp_number)
        tmp_info=self.generatePieceOfInformation_List(tmp_index)

        if QMessageBox.question(self.deleteByNameWidget, "确认删除", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
            self.deleteStudentInfoByNumber(tmp_number)

    
    def callback_modifyByNameRequest(self):
        rejectToInputTitle="拒绝修改"
        tmp_name=self.modifyWidgetUi.textEdit_Modify_Name.toPlainText()

        if tmp_name not in names:
            QMessageBox.information(self.modifyWidget, rejectToInputTitle, "姓名不存在", QMessageBox.Yes)
            return

        tmp_cnt=self.getNameCount(tmp_name)
        if tmp_cnt==1:
            tmp_index=names.index(tmp_name)
            tmp_info=self.generatePieceOfInformation_Dialog(tmp_index)
            tmp_info+='点击确认后，当前学生信息会被删除，需要重新录入！'
            if QMessageBox.question(self.modifyWidget, "确认查找并修改", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
                self.addWidgetUi.textEdit_Add_Number.setText(numbers[tmp_index])
                self.addWidgetUi.textEdit_Add_Number.setDisabled(True)
                self.addWidgetUi.textEdit_Add_Name.setText(names[tmp_index])
                self.addWidgetUi.textEdit_Add_Age.setText(ages[tmp_index])
                self.addWidgetUi.textEdit_Add_Class.setText(classes[tmp_index])
                self.addWidgetUi.textEdit_Add_Profession.setText(professions[tmp_index])
                self.deleteStudentInfoByName(tmp_name)
                self.addWidget.show()
        else:
            QMessageBox.information(self.modifyWidget, "有同名学生存在", "有同名学生存在，请在下方双击选择要修改的学生")

            self.globalIndex=[]
            self.multiNamesList=[]
            for i in range(len(names)):
                if names[i]==tmp_name:
                    self.globalIndex.append(i)
                    self.multiNamesList.append(f'{names[i]}\t{numbers[i]}\t{ages[i]}')

            self.listModel=QStringListModel()
            self.listModel.setStringList(self.multiNamesList)
            self.modifyWidgetUi.listView.setModel(self.listModel)
            self.modifyWidgetUi.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


    def callback_modifyByMultipleNameRequest(self, modelIndex:QModelIndex):
        tmp_index=self.globalIndex[modelIndex.row()]
        tmp_number=numbers[tmp_index]
        tmp_info=self.generatePieceOfInformation_Dialog(tmp_index)
        tmp_info+='点击确认后，当前学生信息会被删除，需要重新录入！'

        if QMessageBox.question(self.modifyWidget, "确认查找并修改", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
            self.listModel.removeRow(modelIndex.row())

            self.addWidgetUi.textEdit_Add_Number.setText(numbers[tmp_index])
            self.addWidgetUi.textEdit_Add_Number.setDisabled(True)
            self.addWidgetUi.textEdit_Add_Name.setText(names[tmp_index])
            self.addWidgetUi.textEdit_Add_Age.setText(ages[tmp_index])
            self.addWidgetUi.textEdit_Add_Class.setText(classes[tmp_index])
            self.addWidgetUi.textEdit_Add_Profession.setText(professions[tmp_index])
            self.deleteStudentInfoByNumber(tmp_number)
            self.addWidget.show()
    
    def callback_modifyByNumberRequest(self):
        rejectToInputTitle="拒绝修改"
        tmp_number=self.modifyWidgetUi.textEdit_Modify_Number.toPlainText()

        if not(tmp_number.isdigit() and len(tmp_number)==6):
            QMessageBox.information(self.modifyWidget, rejectToInputTitle, "学号必须为6位数字", QMessageBox.Yes)
            return

        if tmp_number not in numbers:
            QMessageBox.information(self.modifyWidget, rejectToInputTitle, "学号不存在", QMessageBox.Yes)
            return

        tmp_index=numbers.index(tmp_number)
        tmp_info=self.generatePieceOfInformation_Dialog(tmp_index)
        tmp_info+='点击确认后，当前学生信息会被删除，需要重新录入！'
        if QMessageBox.question(self.modifyWidget, "确认查找并修改", tmp_info, QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
            self.addWidgetUi.textEdit_Add_Number.setText(numbers[tmp_index])
            self.addWidgetUi.textEdit_Add_Number.setDisabled(True)
            self.addWidgetUi.textEdit_Add_Name.setText(names[tmp_index])
            self.addWidgetUi.textEdit_Add_Age.setText(ages[tmp_index])
            self.addWidgetUi.textEdit_Add_Class.setText(classes[tmp_index])
            self.addWidgetUi.textEdit_Add_Profession.setText(professions[tmp_index])
            self.deleteStudentInfoByNumber(tmp_number)
            self.addWidget.show()


    def callback_quiryByNumber(self):
        tmp_number=self.quiryWidgetUi.textEdit_Number.toPlainText()
        rejectToInputTitle="拒绝查询"

        if not(tmp_number.isdigit() and len(tmp_number)==6):
            QMessageBox.information(self.quiryWidget, rejectToInputTitle, "学号必须为6位数字", QMessageBox.Yes)
            return

        if tmp_number not in numbers:
            QMessageBox.information(self.quiryWidget, rejectToInputTitle, "学号不存在", QMessageBox.Yes)
            return
        
        tmp_index=numbers.index(tmp_number)
        tmp_listModel=QStringListModel()
        tmp_listModel.setStringList([self.generatePieceOfInformation_List(tmp_index)])
        self.quiryShowWidgetUi.listView.setModel(tmp_listModel)
        self.quiryShowWidgetUi.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.quiryShowWidget.show()


    def callback_quiryByName(self):
        tmp_name=self.quiryWidgetUi.textEdit_Name.toPlainText()
        rejectToInputTitle="拒绝查询"

        if tmp_name not in names:
            QMessageBox.information(self.quiryWidget, rejectToInputTitle, "姓名不存在", QMessageBox.Yes)
            return
        
        tmp_cnt=0
        tmp_list=[]
        tmp_listModel=QStringListModel()
        for i in range(len(names)):
            if tmp_name==names[i]:
                tmp_cnt+=1
                tmp_list.append(self.generatePieceOfInformation_List(i))
        tmp_listModel.setStringList(tmp_list)
        self.quiryShowWidgetUi.listView.setModel(tmp_listModel)
        self.quiryShowWidgetUi.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.quiryShowWidget.show()

    
    def callback_quiryByClass(self):
        tmp_class=self.quiryWidgetUi.textEdit_Class.toPlainText()
        rejectToInputTitle="拒绝查询"

        if tmp_class not in classes:
            QMessageBox.information(self.quiryWidget, rejectToInputTitle, "班级不存在", QMessageBox.Yes)
            return

        tmp_cnt=0
        tmp_list=[]
        tmp_listModel=QStringListModel()
        for i in range(len(classes)):
            if tmp_class==classes[i]:
                tmp_cnt+=1
                tmp_list.append(self.generatePieceOfInformation_List(i))
        tmp_listModel.setStringList(tmp_list)
        self.quiryShowWidgetUi.listView.setModel(tmp_listModel)
        self.quiryShowWidgetUi.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.quiryShowWidget.show()


    # hook_xxx函数说明：清空文本框、添加信号和槽回调函数
    def hook_addWidgetShow(self):
        self.addWidgetUi.textEdit_Add_Age.setText("")
        self.addWidgetUi.textEdit_Add_Class.setText("")
        self.addWidgetUi.textEdit_Add_Name.setText("")
        self.addWidgetUi.textEdit_Add_Number.setText("")
        self.addWidgetUi.textEdit_Add_Profession.setText("")
        self.addWidgetUi.textEdit_Add_Number.setDisabled(False)
        self.addWidgetUi.textEdit_Add_Name.setFocus()
        self.addWidget.show()


    def hook_modifyWidgetShow(self):
        self.modifyWidgetUi.textEdit_Modify_Name.setText("")
        self.modifyWidgetUi.textEdit_Modify_Number.setText("")
        self.modifyWidgetUi.textEdit_Modify_Number.setFocus()
        self.modifyWidget.show()


    def hook_deleteByNameWidgetShow(self):
        self.deleteSelectionWidget.close()
        self.deleteByNameWidgetUi.textEdit.setText("")
        self.deleteByNameWidgetUi.textEdit.setFocus()
        tmp_emptyModel=QStringListModel()
        tmp_emptyModel.setStringList([])
        self.deleteByNameWidgetUi.listView.setModel(tmp_emptyModel)
        self.deleteByNameWidget.show()


    def hook_deleteByNumberWidgetShow(self):
        self.deleteSelectionWidget.close()
        self.deleteByNumberWidgetUi.textEdit.setText("")
        self.deleteByNumberWidgetUi.textEdit.setFocus()
        self.deleteByNumberWidget.show()


    def hook_quiryWidgetShow(self):
        self.quiryWidgetUi.textEdit_Class.setText("")
        self.quiryWidgetUi.textEdit_Name.setText("")
        self.quiryWidgetUi.textEdit_Number.setText("")
        self.quiryWidgetUi.textEdit_Number.setFocus()
        self.quiryWidget.show()


    def hook_quiryShowWidgetClose(self):
        tmp_emptyModel=QStringListModel()
        tmp_emptyModel.setStringList([])
        self.quiryShowWidgetUi.listView.setModel(tmp_emptyModel)


    def hook_openFileExplorerWidgetShow(self):
        self.openFileName=self.fileExplorer.getOpenFileName(self.mainWindow, caption="Choose a file to open...")[0]
        self.mainWindow_StatusBar_Label_Message.setText(f'OpenFile:{self.openFileName}')
        self.readFromFile(self.openFileName)


    def hook_saveFileExplorerWidgetShow(self):
        self.saveFileName=self.fileExplorer.getSaveFileName(self.mainWindow, caption="Choose a file to save...")[0]
        # print(f'Output file: {self.saveFileName}')
        self.saveToFile(self.saveFileName)



    def hook_appExit(self):
        if self.savedFlag==False and self.modifiedFlag==True:
            if QMessageBox.question(self.mainWindow, "是否保存", "学生信息尚未保存到磁盘，是否保存？", QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.No)==QMessageBox.Yes:
                self.hook_saveFileExplorerWidgetShow()
            else:
                self.app.quit()
        else:
            self.app.quit()


    # 配置信号和槽函数
    def connect(self):
        self.mainWindowTimer.timeout\
            .connect(self.callback_mainWindowTimer)         #mainWindow 定时器时间到，更新statusbar显示的信息

        self.mainWindowUi.action_About.triggered\
            .connect(self.aboutDialog.show)                 #mainWindow About选项被触发
        self.mainWindowUi.action_Help.triggered\
            .connect(self.helpWidget.show)                  #mainWindow Help选项被触发
        self.mainWindowUi.action_Exit.triggered\
            .connect(self.hook_appExit)                     #mainWindow Exit选项被触发
        self.mainWindowUi.action_Open.triggered\
            .connect(self.hook_openFileExplorerWidgetShow)  #mainWindow Open选项被触发
        self.mainWindowUi.action_Save.triggered\
            .connect(self.hook_saveFileExplorerWidgetShow)  #mainWindow Save选项被触发

        self.mainWindowUi.pushButton_Add.clicked\
            .connect(self.hook_addWidgetShow)               #mainWindow “添加学生信息”按钮被点击
        self.mainWindowUi.pushButton_Modify.clicked\
            .connect(self.hook_modifyWidgetShow)            #mainWindow “修改学生信息”按钮被点击
        self.mainWindowUi.pushButton_Delete.clicked\
            .connect(self.deleteSelectionWidget.show)       #mainWindow “删除学生信息”按钮被点击
        self.mainWindowUi.pushButton_Quiry.clicked\
            .connect(self.hook_quiryWidgetShow)             #mainWindow “查询学生信息”按钮被点击
        self.mainWindowUi.pushButton_Exit.clicked\
            .connect(self.hook_appExit)                     #mainWindow ”退出“按钮被点击

        self.addWidgetUi.pushButton_Add_Add.clicked\
            .connect(self.callback_addStudentInfo)          #addWidget “添加”按钮被点击


        self.deleteSelectionWidgetUi.pushButton_DeleteByName.clicked\
            .connect(self.hook_deleteByNameWidgetShow)          #deleteSelection “按照名字删除”按钮被点击
        self.deleteSelectionWidgetUi.pushButton_DeleteByNumber.clicked\
            .connect(self.hook_deleteByNumberWidgetShow)        #deleteSelection “按照学号删除”按钮被点击
        

        self.modifyWidgetUi.pushButton_Modify_Number.clicked\
            .connect(self.callback_modifyByNumberRequest)       #modifyWidget ”按学号查找并修改”按钮被点击
        self.modifyWidgetUi.pushButton_Modify_Name.clicked\
            .connect(self.callback_modifyByNameRequest)         #modifyWidget “按姓名查找并修改”按钮被点击
        self.modifyWidgetUi.listView.doubleClicked\
            .connect(self.callback_modifyByMultipleNameRequest) #modifyWidget 多条学生信息之一被双击


        self.quiryWidgetUi.pushButton_Number.clicked\
            .connect(self.callback_quiryByNumber)               #quiryWidget ”按学号查询“按钮被点击
        self.quiryWidgetUi.pushButton_Name.clicked\
            .connect(self.callback_quiryByName)                 #quiryWidget ”按姓名查询“按钮被点击
        self.quiryWidgetUi.pushButton_Class.clicked\
            .connect(self.callback_quiryByClass)                #quiryWidget ”按班级查询“按钮被点击
        self.quiryShowWidgetUi.pushButton_Exit.clicked\
            .connect(self.hook_quiryShowWidgetClose)            #quiryShowWidget ”退出“按钮被点击
        

        self.deleteByNameWidgetUi.pushButton_DeleteByName.clicked\
            .connect(self.callback_deleteByNameRequest)             #deleteByNameWidget “查找姓名并删除”按钮被点击
        self.deleteByNameWidgetUi.listView.doubleClicked\
            .connect(self.callback_deleteByMultipleNameRequest)     #deleteByNameWidget 多条学生信息之一被双击
        self.deleteByNumberWidgetUi.pushButton_Delete.clicked\
            .connect(self.callback_deleteByNumberRequest)           #deleteByNumberWidget “删除”按钮被点击
        


    def init(self):
        self.callback_mainWindowStatusBarCounterUpdate()            #立即更新一次statuaBar计数器
        self.callback_mainWindowTimer()                             #立即更新一次statusBar时间
        self.connect()                                              #槽函数、其他event connect
        self.mainWindow.show()
        sys.exit(self.app.exec())




a=merge()
a.init()















# class UI(object):
#     def initButtons(self):
#         mainWindow=self.mainWindow

#         # <About> button
#         self.pushButton_About=QPushButton(mainWindow)
#         self.pushButton_About.setText("This is a magical button")
#         self.pushButton_About.clicked.connect(self.showHelpInformation)
#         self.pushButton_About.setGeometry(100,100, 300,150)


#     def initMenus(self):
#         mainWindow=self.mainWindow

#         self.menuBar=mainWindow.menuBar()

#         # <File> menu
#         self.menuBar_File=self.menuBar.addMenu("File")

#         self.menuBar_File_Open=QAction(parent=self.menuBar_File, text="Open")
#         self.menuBar_File_Open.setShortcut("ctrl+o")
#         self.menuBar_File.addAction(self.menuBar_File_Open)

#         self.menuBar_File_Close=QAction(parent=self.menuBar_File, text="Close")
#         self.menuBar_File.addAction(self.menuBar_File_Close)

#         self.menuBar_File.addSeparator()

#         self.menuBar_File_Exit=QAction(parent=self.menuBar_File, text="Exit")
#         self.menuBar_File_Exit.triggered.connect(self.appExit)
#         self.menuBar_File_Exit.setShortcut("ctrl+q")
#         self.menuBar_File.addAction(self.menuBar_File_Exit)


#         # <About> menu
#         self.menuBar_About=self.menuBar.addMenu("About")

#         self.menuBar_About_Help=QAction(self.menuBar_About, text="Help")
#         self.menuBar_About_Help.setShortcut("ctrl+h")
#         self.menuBar_About_Help.triggered.connect(self.showHelpInformation)
#         self.menuBar_About.addAction(self.menuBar_About_Help)

#         self.menuBar_About.addSeparator()

#         self.menuBar_About_About=QAction(self.menuBar_About, text="About")
#         self.menuBar_About_About.triggered.connect(self.showAboutMessageBox)
#         self.menuBar_About.addAction(self.menuBar_About_About)


#     def initWidgets(self):
#         mainWindow=self.mainWindow

#         mainWindow.setFont(QFont("Segoe UI"))
#         mainWindow.setWindowTitle("Icelake PyQt5 Test Program")
#         mainWindow.setFixedSize(800, 600)

#         self.widget_HelpInformation=QWidget()
#         self.widget_HelpInformation.setFont(QFont("Segoe UI"))
#         self.widget_HelpInformation.setFixedSize(800, 600)
#         self.widget_HelpInformation.setWindowTitle("114514")
        

#     def initLabels(self):
#         MainWindow=self.mainWindow

#         self.label_HelpInformation=QLabel(self.widget_HelpInformation)
#         txt=\
# '学生管理系统使用说明\n\
# \n\
# 1. 添加学生信息\n\
# 2. 删除学生信息\n\
# 3. 修改学生信息\n\
# 4. 查找学生信息\n\
# '
#         self.label_HelpInformation.setText(txt)
#         self.label_HelpInformation.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
#         self.label_HelpInformation.setFont(QFont("宋体", pointSize=13))
#         self.label_HelpInformation.setGeometry(0,0, 800,600)


#     def initUi(self, mainWindow:QMainWindow):
#         self.mainWindow=mainWindow

#         self.initButtons()
#         self.initMenus()
#         self.initWidgets()
#         self.initLabels()




#     def appExit(self):
#         app=QApplication.instance()
#         if QMessageBox.question(self.mainWindow, "Exit", "Confirm to exit", QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.Yes)==QMessageBox.Yes:
#             app.quit()
        

#     def showAboutMessageBox(self):
#         txt=\
# '学生信息管理系统，基于：\n\
# --------------------------\n\
# Python 3.7.2\n\
# PyQt5\n\
# --------------------------\n\
# Icelake works\n\
# \n\
# '
#         # a=QMessageBox(self.mainWindow)
#         # a.setFont(QFont("微软雅黑"))
#         # a.setWindowTitle("About us")
#         # a.setText(txt)
#         # a.setStandardButtons(QMessageBox.Yes)
#         # a.setDefaultButton(QMessageBox.Yes)
#         # a.exec()
#         QMessageBox.information(self.mainWindow, "About us", txt, QMessageBox.Yes)


#     def showHelpInformation(self):
#         self.widget_HelpInformation.show()



# if ___name_=='__main__':
#     app=QApplication(sys.argv)
#     app.setWindowIcon(QIcon("icon.jpg"))
#     MainWindow=QMainWindow()
#     ui=UI()
#     ui.initUi(MainWindow)
#     MainWindow.show()
#     qDebug("app in exec!")
#     sys.exit(app.exec())