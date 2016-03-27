#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QMainWindow, QFileDialog,
                             QInputDialog, QLineEdit)
from Project import Project
import pickle


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Voting.ui', self)
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionQuit.triggered.connect(self.close)
        self.actionAdd.triggered.connect(self.addUser)
        self.usersGroup = QActionGroup(self)
        self.show()
        self.project = None
        self.contest = None
        
    def new(self):
        """"""
        dirname = QFileDialog.getExistingDirectory(self, 'Open Directory',
                                                   QDir.currentPath(),
                                                   QFileDialog.ShowDirsOnly
                                                   | QFileDialog.DontResolveSymlinks)
        if dirname:
            print(dirname)
            self.project = Project()
            self.project.set_directory(dirname)
            self.clearUsers()
            self.actionSave.setEnabled(True)            
            self.menuUsers.setEnabled(True)
            self.contest = None
            
        
    def open(self):
        """"""
        fileName = QFileDialog.getOpenFileName(self, 'Open', QDir.currentPath(), "Plk Files (*.plk);;All Files (*)")[0]
        if fileName:
            input = open(fileName, 'rb')
            self.project = pickle.load(input)
            print('load')
            self.actionSave.setEnabled(True)
            self.menuUsers.setEnabled(True)
            self.contest = None
            self.clearUsers()
            for user in self.project.users:
                userAct = QAction(user.name, self, checkable=True, triggered=self.selectUser)
                self.usersGroup.addAction(userAct)
            self.menuSelect.addActions(self.usersGroup.actions())
            
            
    def save(self):
        """"""
        fileName = QFileDialog.getSaveFileName(self, 'Save', QDir.currentPath(), 'Plk Files (*.plk);;All Files (*)')[0]
        if fileName:
            output = open(fileName, 'wb')
            pickle.dump(self.project, output)
            print('save')

    def addUser(self):
        """"""
        text, ok = QInputDialog.getText(self, 'Add user',
                                        'User name:', QLineEdit.Normal)
        if ok and text != '':
            userAct = QAction(text, self, checkable=True, triggered=self.selectUser)
            self.usersGroup.addAction(userAct)
            self.menuSelect.addActions(self.usersGroup.actions())
            self.project.add_user(text)
            print(text)

    def selectUser(self):
        """"""
        user = self.usersGroup.checkedAction()
        if user:
            print('ok ', user.text())
            self.project.select_user(user.text())
            self.setImages()           
            
    def clearUsers(self):
        """"""
        for action in self.usersGroup.actions():
            self.menuSelect.removeAction(action)            
        self.usersGroup = QActionGroup(self)
        pass
    
    def setImages(self):
        """"""
        self.contest = self.project.current_user.get_random_contest()        
        fileName = self.project.images[self.contest[0]]
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(self, "Image Viewer",
                                    "Cannot load %s." % fileName)
            return
        self.img_1.setOriginalPixmap(QPixmap.fromImage(image))
        fileName = self.project.images[self.contest[1]]        
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(self, "Image Viewer",
                                    "Cannot load %s." % fileName)
            return
        self.img_2.setOriginalPixmap(QPixmap.fromImage(image))
        pass

    def selectImage0(self):
        """"""
        print('selected images : ', self.contest)
        self.project.current_user.choice(winner = self.contest[0], looser = self.contest[1])
        self.setImages()

    def selectImage1(self):
        """"""
        print('selected images : ', self.contest)
        self.project.current_user.choice(winner = self.contest[1], looser = self.contest[0])
        self.setImages()
        
    def draw(self):
        """"""
        print('selected images : ', self.contest)
        self.project.current_user.draw(self.contest[0], self.contest[1])
        self.setImages()

    def suppress(self):
        """"""
        eliminate = []
        if self.cbxImg0.isChecked():
            eliminate.append(self.contest[0])
        if self.cbxImg1.isChecked():
            eliminate.append(self.contest[1])
        for img in eliminate:
            self.project.current_user.eliminate(img)
        self.cbxImg0.setChecked(False)
        self.cbxImg1.setChecked(False)
        if eliminate:
            self.setImages()
        
    def passImages(self):
        """"""
        self.setImages()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
